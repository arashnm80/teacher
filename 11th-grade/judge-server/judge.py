#!/usr/bin/env python3
"""The judge: runs students' Python programs for the accounts service, in a sealed container.

The accounts service sends one request over a Unix socket: the program, the kind of question and
the inputs of each test. The judge starts one single-use container (see runner.py) and returns
what the program printed or returned for each test. It never sees an expected output: comparing
is done by the accounts service. The judge does not touch the database, the sessions or the website.

The container has no network, a read-only file system holding only Python, one small scratch
folder, a memory limit, a limit on the number of processes, a CPU limit and a time limit. It is
removed when the run ends or when the hard time limit passes.

  python3 judge.py serve       run the service
  python3 judge.py selftest    run a few programs through the sandbox and print the answers
"""
import json
import logging
import os
import secrets
import socket
import socketserver
import subprocess
import sys
import threading
import time
from pathlib import Path

SOCKET = os.environ.get("TJ_SOCKET", "/run/teacher-judge/judge.sock")
IMAGE = os.environ.get("TJ_IMAGE", "teacher-judge:current")
DOCKER = os.environ.get("TJ_DOCKER", "docker")
SLOTS = int(os.environ.get("TJ_SLOTS", "8"))          # containers running at the same time
QUEUE_MAX = int(os.environ.get("TJ_QUEUE", "60"))     # requests allowed to wait for a slot
QUEUE_WAIT = float(os.environ.get("TJ_QUEUE_WAIT", "18"))
HARD_LIMIT = float(os.environ.get("TJ_HARD_LIMIT", "20"))  # seconds for one container, then it is removed
MAX_REQUEST = 1_000_000
MAX_SOURCE = 40_000
MAX_TESTS = 20
MAX_STDIN = 20_000

log = logging.getLogger("judge")
slots = threading.BoundedSemaphore(SLOTS)
waiting = 0
waiting_lock = threading.Lock()


class Refused(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


def container_command(name: str) -> list[str]:
    return [
        DOCKER, "run", "--rm", "-i", "--name", name,
        "--network", "none", "--read-only", "--ipc", "none",
        "--cap-drop", "ALL", "--cap-add", "SETUID", "--cap-add", "SETGID", "--cap-add", "KILL",
        "--security-opt", "no-new-privileges",
        "--pids-limit", "32", "--memory", "128m", "--memory-swap", "128m", "--cpus", "0.5",
        "--ulimit", "core=0", "--ulimit", "nofile=256:256",
        "--tmpfs", "/work:rw,nosuid,nodev,size=24m,mode=0755",
        "--tmpfs", "/tmp:rw,nosuid,nodev,noexec,size=8m",
        "--user", "0:0", "--stop-timeout", "0",
        IMAGE,
    ]


def check_request(request: object) -> dict:
    if not isinstance(request, dict):
        raise Refused("bad_request", "The request is not valid.")
    mode = request.get("mode")
    source = request.get("source")
    tests = request.get("tests")
    if mode not in ("stdio", "function") or not isinstance(source, str) or not isinstance(tests, list):
        raise Refused("bad_request", "The request is not valid.")
    if len(source) > MAX_SOURCE:
        raise Refused("too_big", "The program is too long.")
    if not 1 <= len(tests) <= MAX_TESTS:
        raise Refused("bad_request", "The number of tests is not valid.")
    clean = []
    for test in tests:
        if not isinstance(test, dict):
            raise Refused("bad_request", "The request is not valid.")
        stdin = test.get("stdin", "")
        if not isinstance(stdin, str) or len(stdin) > MAX_STDIN:
            raise Refused("bad_request", "The request is not valid.")
        item = {"stdin": stdin}
        if mode == "function":
            args, kwargs = test.get("args", []), test.get("kwargs", {})
            if not isinstance(args, list) or not isinstance(kwargs, dict):
                raise Refused("bad_request", "The request is not valid.")
            item = {"args": args, "kwargs": kwargs}
        clean.append(item)
    limit = request.get("timeLimit", 2.0)
    limit = float(limit) if isinstance(limit, (int, float)) and not isinstance(limit, bool) else 2.0
    return {"problem": str(request.get("problem") or "")[:40], "mode": mode, "source": source, "functionName": str(request.get("functionName") or "")[:80],
            "timeLimit": min(max(limit, 0.3), 4.0), "tests": clean}


def run_container(job: dict) -> dict:
    name = "tj-" + secrets.token_hex(8)
    payload = json.dumps(job, ensure_ascii=False).encode("utf-8")
    started = time.monotonic()
    proc = subprocess.Popen(container_command(name), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, start_new_session=True)
    try:
        out, err = proc.communicate(payload, timeout=HARD_LIMIT)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.communicate()
        raise Refused("timeout", "The check took too long.")
    except Exception:
        proc.kill()
        raise
    finally:
        # Whatever happened, the container must not stay: the --rm flag does not cover a killed client.
        subprocess.run([DOCKER, "rm", "-f", name], capture_output=True, timeout=30)
    if proc.returncode != 0 or not out:
        log.error("container failed: code=%s err=%s", proc.returncode, err[-500:].decode("utf-8", "replace"))
        raise Refused("sandbox_failed", "The sandbox could not run.")
    try:
        answer = json.loads(out.decode("utf-8", "replace"))
        results = answer["results"]
        if not isinstance(results, list) or len(results) != len(job["tests"]):
            raise ValueError("shape")
    except (ValueError, KeyError):
        log.error("container gave an unreadable answer: %r", out[:300])
        raise Refused("sandbox_failed", "The sandbox could not run.")
    log.info("ran %d tests of %s in %.2fs", len(results), job.get("problem") or "-", time.monotonic() - started)
    return {"results": results}


def judge(request: object) -> dict:
    """Validate, wait for a free slot, run. Raises Refused for anything the caller should be told."""
    global waiting
    job = check_request(request)
    with waiting_lock:
        if waiting >= QUEUE_MAX:
            raise Refused("busy", "The checker is busy.")
        waiting += 1
    try:
        got = slots.acquire(timeout=QUEUE_WAIT)
    finally:
        with waiting_lock:
            waiting -= 1
    if not got:
        raise Refused("busy", "The checker is busy.")
    try:
        return run_container(job)
    finally:
        slots.release()


class Handler(socketserver.StreamRequestHandler):
    timeout = 30

    def handle(self) -> None:
        try:
            line = self.rfile.readline(MAX_REQUEST + 1)
            if len(line) > MAX_REQUEST:
                raise Refused("too_big", "The request is too big.")
            request = json.loads(line.decode("utf-8"))
            if isinstance(request, dict) and request.get("ping"):
                answer = {"ok": True, "slots": SLOTS, "waiting": waiting}
            else:
                answer = {"ok": True, **judge(request)}
        except Refused as err:
            answer = {"ok": False, "error": err.code, "message": err.message}
        except (ValueError, UnicodeDecodeError):
            answer = {"ok": False, "error": "bad_request", "message": "The request is not valid."}
        except Exception:
            log.exception("unexpected failure")
            answer = {"ok": False, "error": "sandbox_failed", "message": "The sandbox could not run."}
        try:
            self.wfile.write(json.dumps(answer, ensure_ascii=False).encode("utf-8") + b"\n")
        except OSError:
            pass


class Server(socketserver.ThreadingMixIn, socketserver.UnixStreamServer):
    daemon_threads = True
    request_queue_size = 64


def clear_old_containers() -> None:
    listed = subprocess.run([DOCKER, "ps", "-aq", "--filter", "name=^tj-"], capture_output=True, text=True)
    ids = listed.stdout.split()
    if ids:
        subprocess.run([DOCKER, "rm", "-f", *ids], capture_output=True)
        log.info("removed %d old containers", len(ids))


def serve() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    clear_old_containers()
    path = Path(SOCKET)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()
    server = Server(SOCKET, Handler)
    group = os.environ.get("TJ_SOCKET_GROUP")
    if group:
        import grp
        os.chown(SOCKET, -1, grp.getgrnam(group).gr_gid)
    os.chmod(SOCKET, 0o660)
    log.info("listening on %s (%d slots, image %s)", SOCKET, SLOTS, IMAGE)
    server.serve_forever()


def selftest() -> int:
    answer = judge({"mode": "stdio", "source": "print(int(input()) * 2)", "tests": [{"stdin": "21\n"}]})
    print(json.dumps(answer, ensure_ascii=False, indent=1))
    return 0 if answer["results"][0]["stdout"] == "42\n" else 1


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else "serve"
    sys.exit(selftest() if command == "selftest" else serve() or 0)

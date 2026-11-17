"""The checker inside the sandbox container (PID 1 of the container).

The host sends one JSON request on standard input and reads one JSON answer from standard output:

  request:  {"mode": "stdio"|"function", "source": str, "functionName": str, "timeLimit": float,
             "tests": [{"stdin": str} | {"args": [...], "kwargs": {...}}, ...]}
  answer:   {"results": [{"status": "ok"|"error"|"timeout"|"memory"|"output"|"crash"|"skipped",
             "stdout": str, "error": str|null, "value": any, "ms": int, "truncated": bool}, ...]}

Every test starts a new Python process as the unprivileged user 65534, with a time limit, a memory
limit, no files outside its own small scratch folder, and no network (the container has none). This
file runs as root with only the three capabilities it needs (SETUID/SETGID to change user, KILL to
stop what it started); it cannot even change file owners. It never executes the student's code itself.
"""
import json
import os
import resource
import select
import shutil
import signal
import subprocess
import sys
import time

PYTHON = "/usr/bin/python3"
CHILD = "/opt/judge/child.py"
WORK = "/work"
UID = GID = 65534

MAX_REQUEST = 4_000_000
MAX_TESTS = 40
MAX_SOURCE = 100_000
MAX_STDIN = 100_000
OUTPUT_CAP = 64_000          # bytes of output kept per test
CHANNEL_CAP = 64_000
TOTAL_BUDGET = 10.0          # seconds for the whole request
MEMORY = 96 * 1024 * 1024    # address space of one test (class programs are under 100 lines)
FILE_SIZE = 2 * 1024 * 1024  # largest file a test may write
OPEN_FILES = 64


def limits():
    """Runs in the new process, before the student's code: drop every right, then set the limits."""
    os.setsid()
    resource.setrlimit(resource.RLIMIT_AS, (MEMORY, MEMORY))
    resource.setrlimit(resource.RLIMIT_FSIZE, (FILE_SIZE, FILE_SIZE))
    resource.setrlimit(resource.RLIMIT_NOFILE, (OPEN_FILES, OPEN_FILES))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    resource.setrlimit(resource.RLIMIT_CPU, (3, 4))
    os.setgroups([])
    os.setgid(GID)
    os.setuid(UID)


def kill_everything():
    """Stop every process the test may have started (it runs as the only other user)."""
    if os.getpid() == 1:
        try:
            os.kill(-1, signal.SIGKILL)
        except OSError:
            pass
    while True:
        try:
            pid, _ = os.waitpid(-1, os.WNOHANG)
        except ChildProcessError:
            break
        if pid == 0:
            time.sleep(0.005)
            try:
                os.waitpid(-1, os.WNOHANG)
            except ChildProcessError:
                pass
            break


def run_one(index, spec, source, test, limit, remaining):
    folder = os.path.join(WORK, f"t{index}")
    os.mkdir(folder)
    os.chmod(folder, 0o1777)  # the test may write here; it cannot remove the two files below
    call = {"args": test.get("args") or [], "kwargs": test.get("kwargs") or {}} if spec["mode"] == "function" else {}
    for name, text in (("main.py", source), ("spec.json", json.dumps({**spec, **call}))):
        path = os.path.join(folder, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        os.chmod(path, 0o444)
    stdin = (test.get("stdin") or "")[:MAX_STDIN].encode("utf-8", "replace")

    read_end, write_end = os.pipe()
    env = {"PATH": "/usr/bin", "HOME": folder, "TMPDIR": folder, "LANG": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1"}

    started = time.monotonic()
    proc = subprocess.Popen(
        [PYTHON, "-I", "-S", "-X", "utf8", CHILD, folder, str(write_end)],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        env=env, cwd=folder, preexec_fn=limits, close_fds=True, pass_fds=(write_end,),
    )
    os.close(write_end)
    try:
        os.write(proc.stdin.fileno(), stdin)
    except OSError:
        pass
    try:
        proc.stdin.close()
    except OSError:
        pass

    out, chan = bytearray(), bytearray()
    watching = {proc.stdout.fileno(): out, read_end: chan}
    deadline = started + min(limit, max(remaining, 0.2))
    status = None
    truncated = False
    while watching:
        left = deadline - time.monotonic()
        if left <= 0:
            status = "timeout"
            break
        ready, _, _ = select.select(list(watching), [], [], left)
        for fd in ready:
            data = os.read(fd, 65536)
            if not data:
                watching.pop(fd)
                continue
            buf = watching[fd]
            cap = OUTPUT_CAP if buf is out else CHANNEL_CAP
            buf.extend(data[: max(cap + 1 - len(buf), 0)])
            if len(buf) > cap:
                truncated = True
                status = "output"
                watching.clear()
                break
    code = None
    if status is None:
        try:
            code = proc.wait(timeout=max(deadline - time.monotonic(), 0.05))
        except subprocess.TimeoutExpired:
            status = "timeout"
    ms = int((time.monotonic() - started) * 1000)
    kill_everything()
    try:
        proc.wait(timeout=1)
    except Exception:
        pass
    code = proc.returncode if code is None else code
    os.close(read_end)
    shutil.rmtree(folder, ignore_errors=True)

    text = bytes(out[:OUTPUT_CAP]).decode("utf-8", "replace")
    answer = {"status": status or "ok", "stdout": text, "error": None, "value": None, "ms": ms,
              "truncated": truncated}
    if status:
        return answer
    try:
        channel = json.loads(bytes(chan).decode("utf-8", "replace")) if chan else None
    except ValueError:
        channel = None
    if isinstance(channel, dict):
        answer["error"] = channel.get("error")
        answer["value"] = channel.get("value")
        if answer["error"]:
            answer["status"] = "error"
    elif code is not None and code < 0:
        # killed by the kernel: the memory limit is the usual reason
        answer["status"] = "memory" if -code == signal.SIGKILL else "crash"
    elif spec["mode"] == "function" or (code not in (0, None)):
        answer["status"] = "crash"
    return answer


def main():
    raw = sys.stdin.buffer.read(MAX_REQUEST + 1)
    if len(raw) > MAX_REQUEST:
        sys.exit(2)
    request = json.loads(raw.decode("utf-8"))
    mode = request.get("mode")
    source = request.get("source")
    tests = request.get("tests")
    if mode not in ("stdio", "function") or not isinstance(source, str) or len(source) > MAX_SOURCE \
            or not isinstance(tests, list) or len(tests) > MAX_TESTS:
        sys.exit(2)
    limit = min(max(float(request.get("timeLimit") or 2.0), 0.3), 4.0)
    spec = {"mode": mode, "functionName": str(request.get("functionName") or "")}
    begin = time.monotonic()
    results = []
    for index, test in enumerate(tests):
        remaining = TOTAL_BUDGET - (time.monotonic() - begin)
        if remaining <= 0.2:
            results.append({"status": "skipped", "stdout": "", "error": None, "value": None, "ms": 0,
                            "truncated": False})
            continue
        results.append(run_one(index, spec, source, test if isinstance(test, dict) else {}, limit, remaining))
    sys.stdout.write(json.dumps({"results": results}, ensure_ascii=False))
    sys.stdout.flush()


if __name__ == "__main__":
    main()

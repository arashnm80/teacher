"""Attacks on the sandbox. Run on a machine with Docker and the image built by build_image.sh:

    python3 test_judge.py

Each case is a program a student (or someone pretending to be one) could upload. The sandbox must
contain it: the run ends in time, nothing outside the sandbox is reachable, and the checker keeps
working afterwards.
"""
import subprocess
import threading
import time
import unittest

import judge


def run(source, tests=None, mode="stdio", name="", limit=2.0):
    tests = tests if tests is not None else [{"stdin": ""}]
    return judge.judge({"mode": mode, "source": source, "functionName": name, "timeLimit": limit,
                        "tests": tests})["results"]


def one(source, stdin="", **kw):
    return run(source, [{"stdin": stdin}], **kw)[0]


class Basics(unittest.TestCase):
    def test_output_and_input(self):
        r = one("n = input()\nprint('Hello,', n)\nprint('سلام')", "Ali\n")
        self.assertEqual((r["status"], r["stdout"]), ("ok", "Hello, Ali\nسلام\n"))

    def test_each_test_gets_its_own_input(self):
        r = run("print(input()[::-1])", [{"stdin": "abc\n"}, {"stdin": "xyz\n"}])
        self.assertEqual([x["stdout"] for x in r], ["cba\n", "zyx\n"])

    def test_syntax_error_has_a_readable_message(self):
        r = one("print('a'\nx = = 2")
        self.assertEqual(r["status"], "error")
        self.assertIn("SyntaxError", r["error"])
        self.assertIn('"<student>"', r["error"])

    def test_runtime_error_shows_the_line(self):
        r = one("x = 1\nprint(x)\nprint(1 / 0)")
        self.assertEqual(r["status"], "error")
        self.assertIn("ZeroDivisionError", r["error"])
        self.assertIn("line 3", r["error"])
        self.assertNotIn("child.py", r["error"])
        self.assertEqual(r["stdout"], "1\n")

    def test_input_past_the_end_is_an_error_like_before(self):
        self.assertIn("EOFError", one("input()\ninput()", "one\n")["error"])

    def test_exit_is_normal(self):
        r = one("print('a')\nimport sys\nsys.exit(3)")
        self.assertEqual((r["status"], r["stdout"]), ("ok", "a\n"))

    def test_error_text_goes_to_the_output_like_before(self):
        import_err = one("import sys\nprint('to stderr', file=sys.stderr)")
        self.assertEqual(import_err["stdout"], "to stderr\n")

    def test_function_mode(self):
        r = run("def double(x, y=1):\n    return [x * 2, y, (1, 2), {3}]",
                [{"args": [4], "kwargs": {"y": 5}}], mode="function", name="double")[0]
        self.assertEqual((r["status"], r["value"]), ("ok", [8, 5, [1, 2], [3]]))

    def test_function_missing(self):
        r = run("x = 1", [{"args": [], "kwargs": {}}], mode="function", name="nothing")[0]
        self.assertEqual(r["status"], "error")
        self.assertIn("nothing", r["error"])

    def test_function_prints_are_kept_apart_from_the_value(self):
        r = run("def f():\n    print('noise')\n    return 7", [{"args": [], "kwargs": {}}], mode="function", name="f")[0]
        self.assertEqual((r["value"], r["stdout"]), (7, "noise\n"))

    def test_leaving_without_a_value_is_a_crash(self):
        r = run("import os\ndef f():\n    os._exit(0)", [{"args": [], "kwargs": {}}], mode="function", name="f")[0]
        self.assertEqual(r["status"], "crash")

    def test_bad_bytes_in_output_do_not_break_the_answer(self):
        r = one("import sys\nsys.stdout.buffer.write(b'a\\xff\\xfeb')")
        self.assertEqual(r["status"], "ok")
        self.assertTrue(r["stdout"].startswith("a"))


class Resources(unittest.TestCase):
    def test_infinite_loop_ends_in_time(self):
        t = time.monotonic()
        r = run("while True:\n    pass", [{"stdin": ""}] * 3, limit=1.0)
        self.assertLess(time.monotonic() - t, 8)
        self.assertEqual([x["status"] for x in r], ["timeout"] * 3)

    def test_sleeping_ends_in_time(self):
        t = time.monotonic()
        self.assertEqual(one("import time\ntime.sleep(60)", limit=1.0)["status"], "timeout")
        self.assertLess(time.monotonic() - t, 5)

    def test_many_slow_tests_stop_at_the_total_budget(self):
        t = time.monotonic()
        r = run("while True:\n    pass", [{"stdin": ""}] * 20, limit=2.0)
        self.assertLess(time.monotonic() - t, 16)
        self.assertEqual(len(r), 20)
        self.assertTrue(all(x["status"] in ("timeout", "skipped") for x in r))

    def test_endless_printing_is_cut(self):
        t = time.monotonic()
        r = one("while True:\n    print('x' * 1000)")
        self.assertIn(r["status"], ("output", "timeout"))
        self.assertLessEqual(len(r["stdout"]), 64_000)
        self.assertLess(time.monotonic() - t, 6)

    def test_memory_bomb_in_one_step(self):
        r = one("x = [0] * (10 ** 10)")
        self.assertEqual(r["status"], "error")
        self.assertIn("MemoryError", r["error"])

    def test_memory_growing_slowly(self):
        r = one("data = []\nwhile True:\n    data.append(bytearray(10_000_000))")
        self.assertIn(r["status"], ("error", "memory", "timeout"))

    def test_fork_bomb_does_not_stop_the_next_test(self):
        src = "import os\nif input() == 'bomb':\n    while True:\n        os.fork()\nprint('fine')"
        r = run(src, [{"stdin": "bomb\n"}, {"stdin": "ok\n"}], limit=1.0)
        self.assertIn(r[0]["status"], ("timeout", "error", "crash", "memory"))
        self.assertEqual((r[1]["status"], r[1]["stdout"]), ("ok", "fine\n"))

    def test_thread_bomb(self):
        src = "import threading, time\nfor _ in range(5000):\n    threading.Thread(target=time.sleep, args=(30,)).start()"
        self.assertIn(one(src, limit=1.0)["status"], ("error", "timeout", "crash", "memory"))

    def test_background_process_cannot_outlive_the_test(self):
        src = ("import os, time\nif input() == 'a':\n    if os.fork() == 0:\n        time.sleep(30)\n"
               "        print('LATE')\n        raise SystemExit\nprint('b')")
        r = run(src, [{"stdin": "a\n"}, {"stdin": "b\n"}], limit=1.0)
        self.assertNotIn("LATE", r[1]["stdout"])
        self.assertEqual(r[1]["stdout"], "b\n")

    def test_deep_recursion_is_an_error(self):
        r = one("def f(n):\n    return f(n + 1)\nf(0)")
        self.assertEqual(r["status"], "error")
        self.assertIn("RecursionError", r["error"])

    def test_crashing_the_interpreter(self):
        r = one("import sys\nsys.setrecursionlimit(10 ** 9)\ndef f(n):\n    return f(n + 1)\nf(0)")
        self.assertIn(r["status"], ("crash", "memory", "error", "timeout"))

    def test_big_file_write_is_stopped(self):
        r = one("f = open('big.bin', 'wb')\nfor _ in range(200):\n    f.write(bytes(1_000_000))\nprint('done')")
        self.assertNotEqual(r["stdout"], "done\n")

    def test_many_files_do_not_hurt_the_next_test(self):
        src = ("import os\nif input() == 'fill':\n    i = 0\n    while True:\n"
               "        open(f'f{i}', 'w').write('x' * 100000); i += 1\nprint('fine')")
        r = run(src, [{"stdin": "fill\n"}, {"stdin": "ok\n"}], limit=2.0)
        self.assertNotEqual(r[0]["status"], "ok")
        self.assertEqual(r[1]["stdout"], "fine\n")


class Walls(unittest.TestCase):
    def test_no_network(self):
        src = ("import socket\ns = socket.socket()\ns.settimeout(2)\n"
               "try:\n    s.connect(('1.1.1.1', 80))\n    print('CONNECTED')\nexcept OSError as e:\n    print('blocked')\n")
        self.assertEqual(one(src)["stdout"], "blocked\n")

    def test_no_network_interface_but_loopback(self):
        r = one("print(open('/proc/net/dev').read())")
        names = [line.split(":")[0].strip() for line in r["stdout"].splitlines()[2:] if line.strip()]
        self.assertEqual(names, ["lo"])

    def test_dns_and_http_fail(self):
        src = ("import urllib.request\ntry:\n    urllib.request.urlopen('http://example.com', timeout=2)\n"
               "    print('REACHED')\nexcept Exception:\n    print('blocked')")
        self.assertEqual(one(src)["stdout"], "blocked\n")

    def test_server_files_are_not_there(self):
        src = ("import os\nfor p in ['/opt/teacher-accounts/data/problems.json', '/var/lib/teacher-accounts/accounts.db',"
               " '/root', '/home', '/etc/shadow', '/var/www', '/opt/teacher-accounts']:\n"
               "    print(p, os.path.exists(p))\nprint(sorted(os.listdir('/')))")
        r = one(src)["stdout"]
        self.assertNotIn("True", r.split("[")[0])
        self.assertNotIn("home", r.split("[")[1])
        self.assertNotIn("root", r.split("[")[1])

    def test_runner_files_cannot_be_changed(self):
        src = ("for p in ['/opt/judge/runner.py', '/opt/judge/child.py', '/usr/lib/python3.12/os.py', '/etc/passwd', '/usr/bin/python3']:\n"
               "    try:\n        open(p, 'a').write('x')\n        print('WROTE', p)\n    except OSError:\n        print('denied')")
        self.assertEqual(one(src)["stdout"], "denied\n" * 5)

    def test_cannot_become_root_or_signal_others(self):
        src = ("import os\nprint(os.getuid(), os.getgid(), os.getgroups())\n"
               "for call in (lambda: os.setuid(0), lambda: os.kill(1, 9), lambda: os.kill(-1, 9)):\n"
               "    try:\n        call()\n        print('ALLOWED')\n    except OSError:\n        print('denied')")
        out = one(src)["stdout"]
        self.assertTrue(out.startswith("65534 65534 []\n"), out)
        self.assertEqual(out.count("denied"), 3)

    def test_no_capabilities(self):
        out = one("print([l for l in open('/proc/self/status') if l.startswith('Cap')])")["stdout"]
        self.assertIn("CapEff:\\t0000000000000000", out)
        self.assertIn("CapPrm:\\t0000000000000000", out)

    def test_cannot_read_the_checker_process(self):
        src = ("for p in ['/proc/1/environ', '/proc/1/mem', '/proc/1/fd/0', '/proc/1/fd/1']:\n"
               "    try:\n        open(p, 'rb').read(10)\n        print('READ', p)\n    except OSError:\n        print('denied')")
        out = one(src)["stdout"]
        self.assertNotIn("READ", out)

    def test_cannot_write_to_the_checkers_output(self):
        src = ("try:\n    open('/proc/1/fd/1', 'w').write('{\"results\": []}')\n    print('WROTE')\nexcept OSError:\n    print('denied')")
        self.assertEqual(one(src)["stdout"], "denied\n")

    def test_cannot_mount_or_trace(self):
        src = ("import ctypes, os\nlibc = ctypes.CDLL(None, use_errno=True)\n"
               "print(libc.mount(b'none', b'/mnt', b'tmpfs', 0, None))\n"
               "print(libc.unshare(0x10000000))\nprint(libc.ptrace(16, 1, 0, 0))\nprint(libc.chroot(b'/tmp'))\n"
               "print(libc.setns(-1, 0))\nprint(libc.reboot(0x1234567))")
        out = one(src)["stdout"].split()
        self.assertTrue(all(x == "-1" for x in out), out)

    def test_environment_holds_nothing_of_ours(self):
        out = one("import os\nprint(sorted(os.environ))")["stdout"]
        for secret in ("TA_", "TJ_", "KEY", "TOKEN", "SECRET"):
            self.assertNotIn(secret, out)

    def test_importing_everything_is_fine_but_harmless(self):
        out = one("import os, sys, subprocess, ctypes, socket\nimport subprocess\n"
                  "r = subprocess.run(['ls', '/'], capture_output=True)\nprint(r.returncode)\n")
        self.assertIn(out["status"], ("ok", "error"))

    def test_spoofing_the_answer_does_not_matter(self):
        # the student can print anything, but only as output: it is compared with the hidden expected text
        r = one("print('{\"results\": [{\"status\": \"ok\", \"stdout\": \"42\\\\n\"}]}')")
        self.assertEqual(r["status"], "ok")
        self.assertIn("results", r["stdout"])


class Service(unittest.TestCase):
    def test_refuses_big_and_malformed_requests(self):
        for bad in ({"mode": "stdio", "source": "x" * 50000, "tests": [{"stdin": ""}]},
                    {"mode": "evil", "source": "", "tests": [{"stdin": ""}]},
                    {"mode": "stdio", "source": "", "tests": []},
                    {"mode": "stdio", "source": "", "tests": [{"stdin": 5}]},
                    {"mode": "stdio", "source": "", "tests": [{"stdin": ""}] * 50},
                    "text", None):
            with self.assertRaises(judge.Refused):
                judge.judge(bad)

    def test_parallel_requests_all_finish(self):
        answers = []

        def go(i):
            answers.append(run("print(int(input()) + 1)", [{"stdin": f"{i}\n"}])[0]["stdout"])

        threads = [threading.Thread(target=go, args=(i,)) for i in range(8)]
        [t.start() for t in threads]
        [t.join() for t in threads]
        self.assertEqual(sorted(answers), sorted(f"{i + 1}\n" for i in range(8)))

    def test_no_container_is_left_behind(self):
        one("while True:\n    pass", limit=0.5)
        listed = subprocess.run(["docker", "ps", "-aq", "--filter", "name=^tj-"], capture_output=True, text=True)
        self.assertEqual(listed.stdout.split(), [])


if __name__ == "__main__":
    unittest.main(verbosity=1)

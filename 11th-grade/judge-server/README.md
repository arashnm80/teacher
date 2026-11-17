# The judge: students' code runs here, not on their devices

The playground used to run Python in the student's browser (Pyodide, a 10 MB download that many
devices could not load). Now the browser only sends the code. The accounts service
(`accounts-server/grading.py`) asks the judge to run it, compares the result with the expected one,
and answers with what to show.

```
browser ──code──▶ accounts service ──Unix socket──▶ judge ──docker run──▶ sealed container
                  (compares with the                (queue, 3 at a time)     runner.py ─▶ one new
                   expected outputs)                                         process per test
```

## What a program can and cannot do

Each submission runs in a new, single-use container made from `teacher-judge:current` (built by
`build_image.sh` from this server's own Python; it holds only Python, its standard library, `runner.py`
and `child.py`). The container has:

- **no network** (`--network none`), no other containers or IPC;
- a **read-only file system** with nothing of the website, the database or the questions; one small scratch
  folder per test (24 MB in total, files up to 2 MB);
- **no capabilities** except three for the checker itself (change user, stop its children); the student's
  program runs as user 65534 with none, and with no-new-privileges and Docker's default seccomp profile;
- limits: 384 MB memory (256 MB per program), 64 processes (fork bombs), 1 CPU, 2 s per test (wall and CPU),
  10 s for all the tests of one run, 64 KB of output, 64 open files; a hard stop of 20 s from outside;
- **a new process for every test**, so nothing carries over, and the checker kills everything the test started
  before the next one.

The judge never receives an expected output: it returns what the program printed or returned, and the
accounts service compares. The tests after the first (the visible one) never leave the server, so a student
cannot read them from the page either.

`test_judge.py` holds the attacks that are checked (infinite loops, endless output, memory bombs, fork and
thread bombs, background processes, network, reading server files, writing to the checker, becoming root,
mount/ptrace/chroot, reading the checker's memory, huge files, parallel runs, no container left behind).

What is not covered: the container shares the server's kernel, as every Docker container does, so a kernel
flaw could in theory be used to get out; keep the server's kernel and Docker updated. The offline copy
still runs Python on the student's device (it has to work without internet) and sends its results to be
recorded as before.

## Install and operate

```
sudo bash judge-server/install.sh      # user, image, unit; prints "the judge answered: 21 * 2 = 42"
systemctl status teacher-judge
journalctl -u teacher-judge -n 50
python3 judge-server/test_judge.py     # the attacks (needs Docker and the image)
```

After changing `runner.py` or `child.py`, run `install.sh` again (it rebuilds the image).
Settings (environment of the unit): `TJ_SLOTS` (containers at once, 3), `TJ_QUEUE` (waiting requests, 30),
`TJ_QUEUE_WAIT` (seconds a request may wait for a slot, 18).

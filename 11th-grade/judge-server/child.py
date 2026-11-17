"""One test run, inside the sandbox, as an unprivileged user (see runner.py).

It runs the student's program as the main program. Standard input and output are the process's own;
the only extra channel is a pipe whose number is the second argument, which carries the error text and, for function
questions, the returned value. The expected outputs are never here: the host compares.
"""
import json
import os
import sys

WORKDIR = sys.argv[1]
THIS_FILE = os.path.abspath(__file__)

with open(os.path.join(WORKDIR, "spec.json"), encoding="utf-8") as f:
    spec = json.load(f)
with open(os.path.join(WORKDIR, "main.py"), encoding="utf-8") as f:
    source = f.read()
os.chdir(WORKDIR)

channel = os.fdopen(int(sys.argv[2]), "w", encoding="utf-8")
# Like the browser version did, error output and print(..., file=sys.stderr) land in the output.
sys.stderr = sys.stdout


def error_text(exc):
    """The traceback without this file's own frames."""
    import linecache
    import traceback
    linecache.cache["<student>"] = (len(source), None, source.splitlines(True), "<student>")
    tb = exc.__traceback__
    while tb is not None and tb.tb_frame.f_code.co_filename == THIS_FILE:
        tb = tb.tb_next
    return "".join(traceback.format_exception(type(exc), exc, tb))


def convert(v):
    if isinstance(v, (str, int, float, bool)) or v is None:
        return v
    if isinstance(v, (list, tuple)):
        return [convert(x) for x in v]
    if isinstance(v, dict):
        return {str(k): convert(val) for k, val in v.items()}
    if isinstance(v, (set, frozenset)):
        return sorted((convert(x) for x in v), key=lambda x: str(x))
    return str(v)


def finish(error, value=None):
    try:
        sys.stdout.flush()
    except Exception:
        pass
    channel.write(json.dumps({"error": error, "value": convert(value)}, ensure_ascii=False))
    channel.flush()


namespace = {"__name__": "__main__", "__builtins__": __builtins__}
error = None
value = None
try:
    exec(compile(source, "<student>", "exec"), namespace, namespace)
    if spec.get("mode") == "function":
        name = spec.get("functionName") or ""
        func = namespace.get(name)
        if not callable(func):
            error = "NameError: function " + name + " was not found"
            raise SystemExit
        value = func(*(spec.get("args") or []), **(spec.get("kwargs") or {}))
except SystemExit:
    pass
except BaseException as exc:  # includes RecursionError, MemoryError, KeyboardInterrupt
    error = error_text(exc)
finish(error, value)

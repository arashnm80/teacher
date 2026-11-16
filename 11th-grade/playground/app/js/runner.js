import { ltrIsolate } from "./bidi.js?v=19";
import { normalizeNewlines } from "./diff.js?v=12";
import { define, t } from "./i18n.js?v=5";

define({
  "run.require": { fa: "در این مسئله باید از «{what}» استفاده کنید.", en: "In this problem you must use “{what}”." },
  "run.forbid": { fa: "در این مسئله نباید از «{what}» استفاده کنید.", en: "In this problem you must not use “{what}”." },
  "run.for": { fa: "حلقه {code}", en: "a {code} loop" },
  "run.while": { fa: "حلقه {code}", en: "a {code} loop" },
  "run.if": { fa: "دستور {code}", en: "the {code} statement" },
  "run.def": { fa: "تابع ({code})", en: "a function ({code})" },
  "run.timeout": { fa: "زمان اجرا بیش از حد مجاز بود.", en: "The run took longer than allowed." },
  "run.nofunction": { fa: "تابع «{name}» پیدا نشد. آن را با def تعریف کنید.", en: "Function “{name}” was not found. Define it with def." },
});

const TIMEOUT_MS = 2500;

/** Strip string/comment literals so keyword checks are less noisy. */
export function stripNoise(source) {
  return String(source || "")
    .replace(/('''[\s\S]*?'''|"""[\s\S]*?"""|'(?:\\.|[^'\\])*'|"(?:\\.|[^"\\])*")/g, '""')
    .replace(/#.*/g, "");
}

/**
 * Keywords: matched as whole words (`for`, `while`, …).
 * Callables (builtins): matched only as calls (`max(`), so a variable named
 * `max` is allowed — forbidding `\bmax\b` would false-positive on that.
 */
const KEYWORD_TOKENS = new Set([
  "for",
  "while",
  "if",
  "elif",
  "else",
  "def",
  "return",
  "import",
  "in",
  "not",
  "and",
  "or",
  "pass",
  "break",
  "continue",
]);

const CALL_TOKENS = new Set([
  "max",
  "min",
  "sum",
  "sorted",
  "reversed",
  "len",
  "abs",
  "round",
  "map",
  "filter",
  "any",
  "all",
  "enumerate",
  "zip",
  "list",
  "set",
  "dict",
  "tuple",
  "int",
  "float",
  "str",
  "input",
  "print",
  "open",
  "eval",
  "exec",
]);

export function checkConstraints(source, constraints = {}) {
  const cleaned = stripNoise(source);
  const require = constraints.require || [];
  const forbid = constraints.forbid || [];
  const issues = [];

  for (const token of require) {
    const re = tokenRe(token);
    if (!re.test(cleaned)) {
      issues.push({
        type: "require",
        token,
        message: t("run.require", { what: labelFor(token) }),
      });
    }
  }
  for (const token of forbid) {
    const re = tokenRe(token);
    if (re.test(cleaned)) {
      issues.push({
        type: "forbid",
        token,
        message: t("run.forbid", { what: labelFor(token) }),
      });
    }
  }
  return issues;
}

/** Exported for local smoke tests. */
export function tokenRe(token) {
  if (token === "import") return /\bimport\b|\bfrom\b/;
  if (KEYWORD_TOKENS.has(token)) {
    return new RegExp(`\\b${escapeReg(token)}\\b`);
  }
  // Builtins / callables: only the call form, not variable names.
  // (?<![\w.]) skips my_max( and obj.max(
  if (CALL_TOKENS.has(token)) {
    return callRe(token);
  }
  // Unknown forbid/require tokens default to call-form (safer than bare word).
  return callRe(token);
}

function callRe(token) {
  return new RegExp(`(?<![\\w.])${escapeReg(token)}\\s*\\(`);
}

function labelFor(token) {
  const map = {
    for: t("run.for", { code: ltrIsolate("for") }),
    while: t("run.while", { code: ltrIsolate("while") }),
    if: t("run.if", { code: ltrIsolate("if") }),
    def: t("run.def", { code: ltrIsolate("def") }),
    import: `${ltrIsolate("import")} / ${ltrIsolate("from")}`,
    max: `${ltrIsolate("max(...)")}`,
    min: `${ltrIsolate("min(...)")}`,
    sum: `${ltrIsolate("sum(...)")}`,
    sorted: `${ltrIsolate("sorted(...)")}`,
    len: `${ltrIsolate("len(...)")}`,
    str: `${ltrIsolate("str(...)")}`,
  };
  return map[token] || ltrIsolate(token);
}

function escapeReg(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

export function outputsEqual(expected, actual) {
  return normalizeNewlines(expected) === normalizeNewlines(actual);
}

/**
 * Run all tests for a problem inside an initialized Pyodide instance.
 */
export async function runProblem(pyodide, problem, source) {
  const constraintIssues = checkConstraints(source, problem.constraints);
  if (constraintIssues.length) {
    return {
      blocked: true,
      constraintIssues,
      results: [],
    };
  }

  const results = [];
  for (let i = 0; i < problem.tests.length; i++) {
    const test = problem.tests[i];
    results.push(await runOneTest(pyodide, problem, source, test, i + 1));
  }
  return { blocked: false, constraintIssues: [], results };
}

async function runOneTest(pyodide, problem, source, test, index) {
  const payload = {
    source,
    mode: problem.mode || "stdio",
    functionName: problem.functionName || "",
    stdin: test.stdin ?? "",
    expected: test.stdout ?? "",
    call: test.call || null,
    noFunction: t("run.nofunction", { name: problem.functionName || "" }),
  };

  try {
    pyodide.globals.set("payload_json", JSON.stringify(payload));
    const raw = await withTimeout(pyodide.runPythonAsync(HARNESS), TIMEOUT_MS);
    const parsed = JSON.parse(raw);
    if (parsed.error) {
      return {
        index,
        ok: false,
        kind: "runtime",
        message: parsed.error,
        expected: displayExpected(problem, test),
        actual: parsed.stdout || "",
        test,
      };
    }

    if ((problem.mode || "stdio") === "function") {
      const ok = deepEqual(parsed.value, test.call.expected);
      return {
        index,
        ok,
        kind: "function",
        expected: formatValue(test.call.expected),
        actual: formatValue(parsed.value),
        stdout: parsed.stdout || "",
        test,
      };
    }

    const expected = test.stdout ?? "";
    const actual = parsed.stdout ?? "";
    return {
      index,
      ok: outputsEqual(expected, actual),
      kind: "stdio",
      expected,
      actual,
      test,
    };
  } catch (err) {
    return {
      index,
      ok: false,
      kind: "runner",
      message: String(err?.message || err),
      expected: displayExpected(problem, test),
      actual: "",
      test,
    };
  }
}

function displayExpected(problem, test) {
  if ((problem.mode || "stdio") === "function") {
    return formatValue(test.call?.expected);
  }
  return test.stdout ?? "";
}

function formatValue(value) {
  try {
    return JSON.stringify(value);
  } catch {
    return String(value);
  }
}

function deepEqual(a, b) {
  if (Object.is(a, b)) return true;
  // Float answers (e.g. math.pi * r * r) may differ by 1 ULP across engines.
  if (typeof a === "number" && typeof b === "number") {
    if (Number.isNaN(a) && Number.isNaN(b)) return true;
    return Math.abs(a - b) <= 1e-9 * Math.max(1, Math.abs(a), Math.abs(b));
  }
  return JSON.stringify(a) === JSON.stringify(b);
}

function withTimeout(promise, ms) {
  return new Promise((resolve, reject) => {
    const timer = setTimeout(() => reject(new Error(t("run.timeout"))), ms);
    promise
      .then((v) => {
        clearTimeout(timer);
        resolve(v);
      })
      .catch((e) => {
        clearTimeout(timer);
        reject(e);
      });
  });
}

const HARNESS = `
import sys, json, io, traceback

payload = json.loads(payload_json)
source = payload["source"]
mode = payload.get("mode") or "stdio"
buf_out = io.StringIO()
old_out, old_err, old_in = sys.stdout, sys.stderr, sys.stdin
sys.stdout = buf_out
sys.stderr = buf_out

result = {"error": None, "stdout": "", "value": None}
ns = {"__name__": "__main__"}

try:
    if mode == "stdio":
        sys.stdin = io.StringIO(payload.get("stdin") or "")
        exec(compile(source, "<student>", "exec"), ns, ns)
        result["stdout"] = buf_out.getvalue()
    else:
        sys.stdin = io.StringIO("")
        exec(compile(source, "<student>", "exec"), ns, ns)
        name = payload.get("functionName") or ""
        if name not in ns or not callable(ns[name]):
            raise NameError(payload.get("noFunction") or f"Function {name} was not found.")  # name is Latin; traceback shown in LTR pre
        call = payload.get("call") or {}
        args = call.get("args") or []
        kwargs = call.get("kwargs") or {}
        # JSON objects become dicts; lists stay lists (OK for our tests).
        value = ns[name](*args, **kwargs)
        result["value"] = value
        result["stdout"] = buf_out.getvalue()
except Exception:
    result["error"] = traceback.format_exc()
    result["stdout"] = buf_out.getvalue()
finally:
    sys.stdout, sys.stderr, sys.stdin = old_out, old_err, old_in

def convert(v):
    if isinstance(v, (str, int, float, bool)) or v is None:
        return v
    if isinstance(v, (list, tuple)):
        return [convert(x) for x in v]
    if isinstance(v, dict):
        return {str(k): convert(val) for k, val in v.items()}
    if isinstance(v, set):
        return sorted((convert(x) for x in v), key=lambda x: str(x))
    return str(v)

result["value"] = convert(result["value"])
json.dumps(result, ensure_ascii=False)
`;

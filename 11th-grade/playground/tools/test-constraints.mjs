/**
 * Smoke-test constraint matching (mirrors app/js/runner.js — keep in sync).
 * Usage: node tools/test-constraints.mjs
 */

function stripNoise(source) {
  return String(source || "")
    .replace(/('''[\s\S]*?'''|"""[\s\S]*?"""|'(?:\\.|[^'\\])*'|"(?:\\.|[^"\\])*")/g, '""')
    .replace(/#.*/g, "");
}

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

function escapeReg(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function callRe(token) {
  return new RegExp(`(?<![\\w.])${escapeReg(token)}\\s*\\(`);
}

function tokenRe(token) {
  if (token === "import") return /\bimport\b|\bfrom\b/;
  if (KEYWORD_TOKENS.has(token)) {
    return new RegExp(`\\b${escapeReg(token)}\\b`);
  }
  if (CALL_TOKENS.has(token)) {
    return callRe(token);
  }
  return callRe(token);
}

function checkConstraints(source, constraints = {}) {
  const cleaned = stripNoise(source);
  const require = constraints.require || [];
  const forbid = constraints.forbid || [];
  const issues = [];
  for (const token of require) {
    if (!tokenRe(token).test(cleaned)) issues.push({ type: "require", token });
  }
  for (const token of forbid) {
    if (tokenRe(token).test(cleaned)) issues.push({ type: "forbid", token });
  }
  return issues;
}

function assert(cond, msg) {
  if (!cond) {
    console.error("FAIL:", msg);
    process.exitCode = 1;
  } else {
    console.log("OK:", msg);
  }
}

// --- p07: max / sorted ---
const p07 = { forbid: ["max", "sorted"] };
assert(
  checkConstraints("print(max(a,b,c))\n", p07).length > 0,
  "p07: max(a,b,c) blocked"
);
assert(
  checkConstraints("print(sorted([a,b,c])[-1])\n", p07).length > 0,
  "p07: sorted(...) blocked"
);
assert(
  checkConstraints("max = a\nif b > max: max = b\nif c > max: max = c\nprint(max)\n", p07)
    .length === 0,
  "p07: variable named max allowed"
);
assert(
  checkConstraints("def second_max(nums):\n return nums[0]\n", p07).length === 0,
  "p07: name second_max does not trip max forbid"
);

// --- p10 / p14: sum ---
const p10 = { require: ["for"], forbid: ["while", "sum"] };
assert(
  checkConstraints("n=int(input())\nprint(sum(int(input()) for _ in range(n)))\n", p10).length > 0,
  "p10: sum(...) blocked"
);
assert(
  checkConstraints(
    "n=int(input())\nsum=0\nfor _ in range(n):\n sum+=int(input())\nprint(sum)\n",
    p10
  ).length === 0,
  "p10: variable sum = 0 in for-loop allowed"
);

const p14 = { require: ["while"], forbid: ["for", "sum"] };
assert(
  checkConstraints("xs=[]\nwhile True:\n x=int(input())\n if x==0: break\n xs.append(x)\nprint(sum(xs))\n", p14)
    .length > 0,
  "p14: sum(xs) blocked"
);
assert(
  checkConstraints(
    "sum=0\nx=int(input())\nwhile x!=0:\n sum+=x\n x=int(input())\nprint(sum)\n",
    p14
  ).length === 0,
  "p14: variable sum under while allowed"
);

// --- p15: str ---
const p15 = { require: ["while"], forbid: ["for", "str"] };
assert(
  checkConstraints("n=int(input())\nprint(len(str(n)))\n", p15).length > 0,
  "p15: str(n) blocked"
);
assert(
  checkConstraints(
    "n=int(input())\nif n==0:\n print(1)\nelse:\n c=0\n while n:\n  n//=10\n  c+=1\n print(c)\n",
    p15
  ).length === 0,
  "p15: digit loop without str allowed"
);

// --- keyword loop constraints ---
const forOnly = { require: ["for"], forbid: ["while"] };
assert(
  checkConstraints("n=int(input())\ni=0\nwhile i<n:\n i+=1\n", forOnly).length >= 2,
  "for-only: while solution fails"
);
assert(
  checkConstraints("for i in range(3):\n print(i)\n", forOnly).length === 0,
  "for-only: plain for passes"
);

const whileOnly = { require: ["while"], forbid: ["for"] };
assert(
  checkConstraints("for i in range(3):\n print(i)\n", whileOnly).length > 0,
  "while-only: for solution fails"
);
assert(
  checkConstraints('print("for")\n# while\nx=1\nwhile x:\n break\n', whileOnly).length === 0,
  "while-only: for in string/comment ignored"
);

assert(
  checkConstraints("print(max (a, b))\n", { forbid: ["max"] }).length > 0,
  "max (a, b) with space blocked"
);
assert(
  checkConstraints("x = my_max(a, b)\n", { forbid: ["max"] }).length === 0,
  "my_max( not treated as max("
);

if (process.exitCode) {
  console.error("\nConstraint tests FAILED");
} else {
  console.log("\nConstraint tests PASSED");
}

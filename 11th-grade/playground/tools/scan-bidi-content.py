"""Report Latin/Python tokens in Persian copy that are not inside markdown code."""
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
problems = json.loads((root / "app/data/problems.json").read_text(encoding="utf-8"))
concepts = json.loads((root / "app/data/concepts.json").read_text(encoding="utf-8"))
pat = re.compile(
    r"\b(for|while|if|else|elif|def|import|from|input|print|math|range|"
    r"True|False|None|int|float|str|list|set|dict|tuple|exit)\b"
)
fence = re.compile(r"```[\s\S]*?```")
tick = re.compile(r"`[^`]+`")
issues = []
for p in problems + concepts:
    for key in ("statement", "title", "hints", "body"):
        v = p.get(key)
        vals = v if isinstance(v, list) else ([v] if isinstance(v, str) else [])
        for text in vals:
            if not isinstance(text, str):
                continue
            cleaned = fence.sub("", text)
            cleaned = tick.sub("", cleaned)
            for m in pat.finditer(cleaned):
                ctx = cleaned[max(0, m.start() - 25) : m.end() + 25].replace("\n", " ")
                issues.append((p.get("id") or p.get("title"), key, m.group(0), ctx))

print(f"unmarked latin tokens outside backticks: {len(issues)}")
print("(titles/topics are also wrapped at runtime by bidiMixHtml)")
for row in issues:
    print(row)

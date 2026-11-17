---
name: progress-follows-question-id
description: "Student progress belongs to a question's id; only a major edit (tests, mode, function name, constraints) or --bump starts a question again"
metadata:
  node_type: memory
  type: project
  modified: 2026-11-15T17:13:28.249Z
---

The owner will keep adding questions in the middle and at the end. Progress must survive that.

Rules as built:
- Progress is keyed by the stable id (p01, p02, ...). Display numbers may change freely.
- A question's revision comes from playground-authoring/revisions.json. The build (build.py,
  reconcile_revisions) bumps it only when the contract changes: mode, functionName, tests or
  constraints (fingerprint). Wording, hints, guides, starter code and difficulty never bump.
- `python3 playground-authoring/build.py --bump ID` forces a new revision (a meaning change the
  build cannot see). Never delete entries from revisions.json; never reuse an id for other content.
- Server (accounts-server/app.py, sync_revisions): a revision change resets only the solved mark and
  hints of that question. Attempts, code and the teacher's flags stay.
- The checker must never mutate published test data (build.py deep-copies before check_problem).

**Why:** the owner said progress must not be lost when questions are added; a reset is only for a
major modification of the question itself.

**How to apply:** when changing questions, first decide whether the contract changed. Use --bump only
for changes the fingerprint cannot see. Keep test_revisions.py passing.

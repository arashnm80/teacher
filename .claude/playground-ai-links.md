# Playground AI helper + lesson links

Requested by the user on 2026-11-15 (mid-turn, while lesson refinement was running).

## Requirements (from the user)

1. A sidebar AI in the playground. When a student's answer is wrong, offer
   "ask AI what is wrong for this question".
2. Each student enters their own OpenRouter API key once; after that they can
   use the AI section.
3. Every OpenRouter request is sent from this machine (the teacher.arashnm80.ir
   server), and only through the WARP proxy. Never from the student's device.
4. The offline downloaded version uses the same server (teacher.arashnm80.ir)
   as the mediator.
5. Each playground question links to the related lesson page.

## Queue (user interrupts, in the order they came)

1. AI sidebar + server (A1–A8 below).            <- next
2. Lesson link per playground question (A5).    <- pending
3. DONE: home landing + book entry (2026-11-15).
4. DONE: playground rendering of mixed Persian/English (2026-11-15, v15).
5. Then lesson refinement (T9 leftover, C1, I1, B1, S1, S2, H1), Poodman 1–2 first.

## Priority rules (from the user)

- A task the user interrupts with is done BEFORE continuing lesson refinement
  (refinement is slow). Then go back to the refinement list in
  `grade11-rebuild-tasks.md`.
- Lesson refinement: Poodman 1 and 2 first (taught now). Poodman 3–5 later.

## Decisions I made (the user can change them)

- Server piece: a small Python service on 127.0.0.1, behind nginx at `/api/ai/`.
  It calls OpenRouter through the WARP SOCKS5 proxy only. It fails closed when
  WARP is down.
- The server never stores or logs keys. The browser keeps the key in
  localStorage (per device, per browser).
- The server builds the prompt from structured fields only (problem, student
  code, failing test). It is not a general relay, so nobody can send arbitrary
  prompts through it.
- The AI answers in Persian, gives hints first, and does not print the full
  solution (the goal is learning).
- CORS `*` on the AI endpoint, because the offline page sends requests with
  origin `null`. No cookies are used, so `*` is safe here.
- Rate limit at nginx (`limit_req`) and in the service.

## Status

| ID | Subtask | Status |
|---|---|---|
| A1 | Check WARP, nginx, python packages, playground layout | in progress |
| A2 | Server service `ai-proxy/` (code, install script, systemd unit) | todo |
| A3 | nginx location `/api/ai/` (CORS, preflight, limits) | todo |
| A4 | Playground UI: sidebar AI (key setup, wrong-answer button, answer) | todo |
| A5 | Lesson link per playground problem (concept → lesson page) | todo |
| A6 | Offline playground zip uses the absolute server URL | todo |
| A7 | Tests: curl (CORS, WARP trace, fake key → 401), Playwright (mocked API) | todo |
| A8 | Docs: REQUIREMENTS.md exception for absolute server URL; this file | todo |

## Resume here

Read the status table, then continue from the first row that is not done.
After each finished row, update the table here and the progress log in
`grade11-rebuild-tasks.md`.

## Update 2026-11-15 (mid-turn request, takes priority over lesson refinement)

- AI panel gets FIXED choices only (no free text):
  1. explain the problem
  2. give a few sample input and output
  3. explain my written answer and tell which part is wrong
- Provider choice: OpenRouter or Groq, each with its own key (stored in the browser).
- Progress and API keys must survive version updates as much as possible:
  stable storage keys, schema version + migrations, never clear on load,
  backup/restore of progress (keys are NOT in the backup), and a stable port for
  the offline launcher (localStorage is per origin).
- Mid-turn (2026-11-15), done first: code comments keep the «#» on the LEFT. The
  rest of the comment (English, Persian or both) sits to its right in its own
  island with correct bidi order. Supersedes the earlier «#-at-the-right» layout.
- Mid-turn (2026-11-15): set a few best FREE models per provider (OpenRouter and
  Groq). The server tries them in order and falls back on model-level errors
  (not on key errors). The service returns which model answered.
- Mid-turn (2026-11-15): the AI agent is ALWAYS visible at the LEFT side of the
  playground (own column, not hidden inside the problem list), so students know
  it exists. Problem list stays on the right (RTL start).
- Pending interrupts after this: site structure (landing without 5 modules,
  sidebars only inside sections, brand link on every page, one cohesive design),
  Persian-fluency weighting for free models (done in config.json, evidence
  limited, see final message).
- Mid-turn (2026-11-15): ONE offline zip for the whole site (lessons + problems,
  and the AI panel, which needs the internet). Students download once. Replaces
  grade11-offline.zip (textbook only) and teacher-playground-offline.zip. The zip
  starts with شروع.bat (local server on a fixed port, so localStorage keeps progress).
  Hints rewritten per problem (2 tips each, hints.json). Run button renamed to تست و آزمون.
- Mid-turn (2026-11-15): when a problem has several solutions, do NOT keep the
  shortest. Keep the ones a beginner can follow (plain loops, if, simple
  variables). Solutions must still pass tests and the checker's banned lists.
- Done before this: progress backup/restore (playground «پیشرفت من» under the
  problem list), lesson links, AI panel on the left with loading and timeout,
  materials page with its own contents sidebar, landing without modules, one zip.


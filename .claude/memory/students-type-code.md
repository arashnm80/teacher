---
name: students-type-code
description: "The owner wants students to type code by hand, not paste it; what the site blocks, and what stays public"
metadata:
  node_type: memory
  type: project
  modified: 2026-11-15T17:20:56.136Z
---

The owner wants students to write every piece of code by hand: "otherwise, they would just copy and paste."

Built so far (guard script web/guard.js, shared asset version 23): copy, cut and drag of text are blocked page-wide except in form fields (search box, API key). The lesson articles and the playground statement, hints, concept, results, AI answer and AI dialog carry the `no-copy` class. Paste and drop are blocked in the CodeMirror editor. Checked in a real browser, locally and live: 18 of 18 checks.

**Why:** a web page cannot make text uncopyable in every case. Online (since the accounts launch): the questions file with the solutions is no longer published; the server releases a solution only after the student passes that question. Still public: the whole book text in /assets/search-index.js (about 1 MB), and the offline zip grade11-offline.zip, which contains all 100 solutions in data/problems.json. View-source, DevTools, screenshots and print-to-PDF also get around page code.

**How to apply:** do not claim the solutions are protected. When asked for more protection, say that the public JSON and search index are the real leak. Options for the owner to choose: obfuscate or encrypt the guide data (a deterrent only, the key is in the page), serve guides through the relay only after a passing attempt (needs a server), or keep the current UI protection.

# Capture verification

## Setup

- Tool: AI assistant using Copilot SDK in VS Code (`vscode-agent-host`)
- Model: `gpt-5.6-luna` (automatic routing); no separate planning model is exposed
- Mechanism: Copilot SDK lifecycle events written automatically to each session's
  `events.jsonl`, plus the repo-local watcher
  [.agent-logs/capture-watcher.ps1](.agent-logs/capture-watcher.ps1), which
  monitors every session-state stream and writes only submitted prompts and
  terminal responses.
- Config changed: `.agent-logs/capture-watcher.ps1` and
  `.agent-logs/README.md`. The watcher was started once for this repository; no
  per-prompt command is required.
- Canary log files:
  - [.agent-logs/2026-09-26_05-44-23_0628a43a-cb4c-4c94-8d89-fbb3db9d74de_0628a43a-cb4c-4c94-8d89-fbb3db9d74de.md](.agent-logs/2026-09-26_05-44-23_0628a43a-cb4c-4c94-8d89-fbb3db9d74de_0628a43a-cb4c-4c94-8d89-fbb3db9d74de.md)
  - [.agent-logs/2026-09-26_05-44-52_9c2bff38-e028-4759-8dda-2c86f2648167_9c2bff38-e028-4759-8dda-2c86f2648167.md](.agent-logs/2026-09-26_05-44-52_9c2bff38-e028-4759-8dda-2c86f2648167_9c2bff38-e028-4759-8dda-2c86f2648167.md)

The first canary was run in a Copilot child chat and the second in an
independent Copilot session. Both prompt and response are present in
`.agent-logs/`.

## Raw canary entry 1

```text
---
session_id: 0628a43a-cb4c-4c94-8d89-fbb3db9d74de
date: 2026-09-26
author: Xeeshan-23
model: unknown
tool: copilot-sdk-vscode
project: tenant_saas
total_exchanges: 0
first_prompt_time: 2026-09-26T05:44:23.8120000Z
last_prompt_time: 2026-09-26T05:44:23.8120000Z
---

# Session Log - 2026-09-26

Session: `0628a43a` | Project: `tenant_saas` | Author: `Xeeshan-23`

---

[LOG_ENTRY type=PROMPT num=1 session=0628a43a]
timestamp: 2026-09-26T05:44:23.8120000Z
model: unknown

CAPTURE TEST - 8x assignment, Xeeshan, second session


[LOG_ENTRY type=RESPONSE num=1 session=0628a43a]
timestamp: 2026-09-26T05:44:31.2650000Z
model: unknown

Capture test acknowledged: 8× assignment, Xeeshan, second session.

---
```

## Raw canary entry 2

```text
---
session_id: 9c2bff38-e028-4759-8dda-2c86f2648167
date: 2026-09-26
author: Xeeshan-23
model: unknown
tool: copilot-sdk-vscode
project: tenant_saas
total_exchanges: 0
first_prompt_time: 2026-09-26T05:44:52.6520000Z
last_prompt_time: 2026-09-26T05:44:52.6520000Z
---

# Session Log - 2026-09-26

Session: `9c2bff38` | Project: `tenant_saas` | Author: `Xeeshan-23`

---

[LOG_ENTRY type=PROMPT num=1 session=9c2bff38]
timestamp: 2026-09-26T05:44:52.6520000Z
model: unknown

CAPTURE TEST - 8x assignment, Xeeshan, independent session


[LOG_ENTRY type=RESPONSE num=1 session=9c2bff38]
timestamp: 2026-09-26T05:45:00.1410000Z
model: unknown

Capture test acknowledged for the 8× assignment, Xeeshan, in an independent session.

---
```

## Initial attempt that did not work

There was no repo-local hook configuration. The first watcher implementation
looked for the model only in `session.auto_mode_resolved`, which can occur before
the submitted-prompt event, so the two canary files correctly preserve the
captured `unknown` model value. The watcher now also reads the model from every
assistant message for subsequent turns. The prompt and response capture itself
worked in both sessions.

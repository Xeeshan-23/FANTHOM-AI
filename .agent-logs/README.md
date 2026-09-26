# Copilot capture

`capture-watcher.ps1` monitors Copilot SDK for VS Code `events.jsonl` lifecycle
streams and writes prompt/terminal-response pairs into this directory. The
runtime emits the stream automatically for every session; the watcher is started
once for this repository and requires no per-prompt action.

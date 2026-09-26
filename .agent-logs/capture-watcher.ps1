param(
    [string]$SessionRoot = "$env:USERPROFILE\.copilot\session-state",
    [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot)
)

$ErrorActionPreference = "Stop"
$logRoot = Join-Path $RepoRoot ".agent-logs"
New-Item -ItemType Directory -Force -Path $logRoot | Out-Null
$state = @{}

function Write-Entry {
    param(
        [string]$Path,
        [hashtable]$Pending,
        [string]$ResponseTimestamp
    )

    $date = [DateTime]::Parse($Pending.promptTimestamp).ToUniversalTime()
    $fileName = "{0}_{1}.md" -f $date.ToString("yyyy-MM-dd_HH-mm-ss"), $Pending.sessionId
    $outputPath = Join-Path $logRoot $fileName
    if (-not (Test-Path $outputPath)) {
        @"
---
session_id: $($Pending.sessionId)
date: $($date.ToString("yyyy-MM-dd"))
author: Xeeshan-23
model: $($Pending.model)
tool: copilot-sdk-vscode
project: $(Split-Path -Leaf $RepoRoot)
total_exchanges: 0
first_prompt_time: $($Pending.promptTimestamp)
last_prompt_time: $($Pending.promptTimestamp)
---

# Session Log - $($date.ToString("yyyy-MM-dd"))

Session: ``$($Pending.sessionId.Substring(0, 8))`` | Project: ``$(Split-Path -Leaf $RepoRoot)`` | Author: ``Xeeshan-23``

---

[LOG_ENTRY type=PROMPT num=1 session=$($Pending.sessionId.Substring(0, 8))]
timestamp: $($Pending.promptTimestamp)
model: $($Pending.model)

$($Pending.prompt)


[LOG_ENTRY type=RESPONSE num=1 session=$($Pending.sessionId.Substring(0, 8))]
timestamp: $ResponseTimestamp
model: $($Pending.model)

$($Pending.response)

---
"@ | Set-Content -Path $outputPath -Encoding utf8
    } else {
        $entryCount = (Select-String -Path $outputPath -Pattern "\[LOG_ENTRY type=PROMPT" -SimpleMatch).Count + 1
        @"

[LOG_ENTRY type=PROMPT num=$entryCount session=$($Pending.sessionId.Substring(0, 8))]
timestamp: $($Pending.promptTimestamp)
model: $($Pending.model)

$($Pending.prompt)


[LOG_ENTRY type=RESPONSE num=$entryCount session=$($Pending.sessionId.Substring(0, 8))]
timestamp: $ResponseTimestamp
model: $($Pending.model)

$($Pending.response)

---
"@ | Add-Content -Path $outputPath -Encoding utf8
    }
}

while ($true) {
    Get-ChildItem -Path $SessionRoot -Filter events.jsonl -Recurse -File -ErrorAction SilentlyContinue | ForEach-Object {
        $path = $_.FullName
        if (-not $state.ContainsKey($path)) {
            $state[$path] = @{ Position = 0; Pending = $null }
        }

        $stream = [System.IO.File]::Open($path, "Open", "Read", "ReadWrite")
        try {
            $stream.Seek($state[$path].Position, [System.IO.SeekOrigin]::Begin) | Out-Null
            $reader = New-Object System.IO.StreamReader($stream)
            while ($null -ne ($line = $reader.ReadLine())) {
                $event = $line | ConvertFrom-Json
                if ($event.type -eq "hook.start" -and $event.data.hookType -eq "userPromptSubmitted") {
                    $input = $event.data.input
                    $state[$path].Pending = @{
                        sessionId = [string]$input.sessionId
                        prompt = [string]$input.prompt
                        promptTimestamp = ([DateTimeOffset]::FromUnixTimeMilliseconds([int64]$input.timestamp)).UtcDateTime.ToString("o")
                        model = "unknown"
                        response = ""
                    }
                } elseif ($event.type -eq "session.auto_mode_resolved" -and $null -ne $state[$path].Pending) {
                    $state[$path].Pending.model = [string]$event.data.chosenModel
                } elseif ($event.type -eq "assistant.message" -and $null -ne $state[$path].Pending) {
                    if (-not [string]::IsNullOrWhiteSpace([string]$event.data.model)) {
                        $state[$path].Pending.model = [string]$event.data.model
                    }
                    $toolRequests = @($event.data.toolRequests)
                    if ($toolRequests.Count -eq 0 -and -not [string]::IsNullOrWhiteSpace([string]$event.data.content)) {
                        $state[$path].Pending.response = [string]$event.data.content
                        $state[$path].Pending.responseTimestamp = [DateTime]::Parse([string]$event.timestamp).ToUniversalTime().ToString("o")
                    }
                } elseif ($event.type -eq "assistant.turn_end" -and $null -ne $state[$path].Pending -and -not [string]::IsNullOrWhiteSpace($state[$path].Pending.response)) {
                    Write-Entry -Path $path -Pending $state[$path].Pending -ResponseTimestamp $state[$path].Pending.responseTimestamp
                    $state[$path].Pending = $null
                }
            }
            $state[$path].Position = $stream.Position
            $reader.Dispose()
        } finally {
            $stream.Dispose()
        }
    }
    Start-Sleep -Milliseconds 500
}

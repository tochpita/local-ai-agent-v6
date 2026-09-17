# Local AI Agent

V6 is a lightweight, local Windows computer-use agent. It runs the decision loop through Ollama using `qwen3:1.7b`; the model chooses tools, reads their results, and continues until it can complete the requested task or reaches the safety step limit.

It is designed for a CPU-only Windows machine and uses `think=False` for every Ollama model call.

## What it can do

- Discover and open safe supported Windows apps: Notepad, Calculator, Edge, File Explorer, Paint, Snipping Tool, Photos, and Media Player, plus installed Chrome, Firefox, VS Code, and Microsoft Office apps.
- Open normal websites or an Edge InPrivate window.
- Type, press keys, use hotkeys, move/click/scroll, and capture screenshots.
- Use a headed Playwright browser session for DOM-based navigation, typing, clicking, waiting, and reading page text.
- Search the web and return a small set of results for the model to compare.
- Read, write, append, target-edit, and create folders strictly inside `workspace/`.
- Initialize a local Git repository for the V6 project and inspect its status, without creating remotes or transmitting code.
- Create an HTML file in `workspace/` and open it locally in a browser.

## Safety boundaries

The agent does not expose arbitrary shell or administrative-command execution. Workspace paths cannot escape `C:\AI-Agent\workspace`. It must not bypass authentication, CAPTCHA, human verification, or other security controls. It should stop and ask the user to take over when a site needs human verification or a consequential external submission is about to occur.

## Requirements

- Windows 10 or 11
- Python 3.10 or newer (make sure Python is available from `PATH`)
- [Ollama for Windows](https://ollama.com/download/windows)
- Microsoft Edge, which is included with Windows 10/11

## First-time setup

Open PowerShell and run the following commands. The Ollama installer can also be downloaded from the link above; if you use `winget`, run:

```powershell
winget install Ollama.Ollama
```

Close and reopen PowerShell after installation, then download the required model:

```powershell
ollama pull qwen3:1.7b
```

Set up the project environment and install its Python packages:

```powershell
cd C:\AI-Agent
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install ollama pyautogui playwright requests beautifulsoup4
python -m playwright install chromium
```

`python -m playwright install chromium` downloads Playwright's fallback browser. It is recommended even though V5 prefers the installed Edge browser.

If PowerShell prevents environment activation, use this process-only setting and activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Launching V5

Make sure the Ollama service is available. The Windows Ollama app normally starts it automatically. If `ollama list` does not work, start it in a separate PowerShell window:

```powershell
ollama serve
```

In the project directory, launch the agent:

```powershell
cd C:\AI-Agent
.\.venv\Scripts\python.exe .\agent.py
```

Example prompts:

```text
Open Notepad and type Hello from my AI agent.
Create an HTML file called game_test.html containing a simple game and open it.
Search the web for the current CEO of Apple and tell me.
Open YouTube and Calculator.
Initialize a local Git repository in my workspace and show its status.
```

Type `exit` to close the agent.

## Project layout

```text
agent.py             Model/tool orchestration loop
config.py            Model, step-limit, and workspace settings
tools/
  schemas.py         Ollama function schemas
  computer.py        Safe desktop controls
  browser.py         Playwright browser controls
  filesystem.py      Workspace-only file controls
  research.py        Web search
  repository.py      Local workspace Git helpers
workspace/           Files the agent is allowed to create and edit
```

## Troubleshooting

- **`Connection refused` or Ollama errors:** run `ollama list`, verify `qwen3:1.7b` appears, then start `ollama serve` if necessary.
- **`ModuleNotFoundError`:** rerun the package-install command using `.venv\\Scripts\\python.exe -m pip`.
- **Playwright launch errors:** rerun `.venv\\Scripts\\python.exe -m playwright install chromium`.
- **A website asks to sign in, solve a CAPTCHA, or complete human verification:** complete it yourself; V5 is intentionally not permitted to bypass it.

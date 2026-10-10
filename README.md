# CapyHarness

CapyHarness is an open-source, developer-focused AI agent harness being built incrementally as both a practical development tool and an educational exploration of agent architecture. The name belongs to the broader SleepyCapybara project.

## Current state

This project is at **Milestone 1**. Its only command is `capyh status`, which finds the Git workspace containing the current directory and shows its root, repository name, branch, and counts of modified, untracked, and staged files. It works from a subdirectory of a repository. The command reads Git information; it does not change files or run an AI agent.

There are no model providers, agent loops, tool calls, sandbox, or filesystem tools yet.

## Requirements and local installation

- Python 3.11 or newer
- Git available on `PATH`

From the project root:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

The `-e` flag installs the package in editable mode, so changes under `src/capyharness` are used without another installation. The application and tests have no third-party Python runtime dependencies; Git is a separate executable.

## Usage

From any local Git repository, including a nested directory:

```bash
capyh status
```

Use `capyh --verbose status` to see debug logs. `capyh` by itself shows help. Outside a Git repository, `capyh status` prints a clear message to standard error and exits with code 1.

## Tests

```bash
python -m unittest discover -s tests -v
```

Tests create and clean up temporary Git repositories. They do not rely on the repository containing this project.

## Architecture

```text
src/capyharness/cli.py       command parsing and result display
src/capyharness/workspace.py  Git workspace discovery
src/capyharness/git.py        Git process execution and branch/status reading
tests/                       checks using temporary repositories
```

The flow is CLI → workspace discovery → Git inspection → terminal output. The code uses Python's `argparse`, `subprocess`, `pathlib`, and `logging`. Git receives a list of arguments without a shell. Status uses Git's stable `--porcelain=v1 -z` format so file names are separated unambiguously.

## Educational purpose

Building CapyHarness is also a way to study Python, software architecture, Git, process execution, security boundaries, AI agents and harnesses, context engineering, tool design, sandboxing, and orchestration. Each milestone should remain small enough to understand fully before the next one begins.

## Vision, not current functionality

Future milestones may explore agent loops, model providers, tool calling, filesystem tools, deeper Git integration, context management, permissions, sandboxing, tracing, MCP, worktrees, and multi-agent orchestration. These are possible directions, **not implemented features**. The next milestone will be chosen after reviewing the current foundation.

## Principles

- Understand before automate.
- Small milestones.
- Explicit code over magic.
- Safety before autonomy.
- Observability from the beginning.
- One agent before multi-agent.
- Tools before orchestration complexity.
- Context matters as much as the model.
- Git is the safety net.

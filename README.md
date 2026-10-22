<div align="center">
  <img src="docs/assets/harnessguard-mark.svg" alt="HarnessGuard mark" width="120" />
  <h1>HarnessGuard</h1>
  <p>
    <strong>Operational guardrails for autonomous agents.</strong>
  </p>
  <p>
    HarnessGuard enforces token budgets, blocks destructive execution patterns, and forces a human approval gate before sensitive agent actions are allowed through.
  </p>
  <p>
    <a href="#quick-start"><img alt="Quick start" src="https://img.shields.io/badge/Quick-Start-5F7FFF?style=flat-square" /></a>
    <a href="#how-it-works"><img alt="How it works" src="https://img.shields.io/badge/How-It-Works-161B22?style=flat-square" /></a>
    <a href="#configuration"><img alt="Configuration" src="https://img.shields.io/badge/Config-CLI-3B82F6?style=flat-square" /></a>
  </p>
  <p>
    <img alt="Python 3.10+" src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" />
    <img alt="MIT License" src="https://img.shields.io/badge/License-MIT-4F46E5" />
  </p>
</div>

HarnessGuard is a lightweight governance layer for agent-driven workflows. It models the important question in real time: is this action still within budget, and is it safe enough to proceed without a human checkpoint?

## Why it exists

Autonomous systems are fast, but they can also overrun limits or execute commands that are operationally dangerous. HarnessGuard is designed for those moments: it introduces a deterministic safety gate before shell execution or other high-impact actions are allowed to continue.

Instead of relying on accidental restraint, the project makes governance explicit:

- token budgets are enforced before action continues
- destructive shell patterns are blocked and escalated
- human approval is required when a shell action crosses a safety threshold
- the decision is small, testable, and easy to integrate into agent harnesses

## At a glance

| Capability | What it does |
| --- | --- |
| Budget enforcement | Stops action once token spend reaches the configured cap. |
| Shell safety checks | Detects destructive commands such as `rm -rf`, `mkfs`, `dd`, and `shutdown`. |
| Human approval gates | Requires explicit authorization for sensitive shell execution. |
| Small API surface | Exposes a simple `HarnessGovernor` and state model that can be embedded in richer orchestration flows. |

## Key capabilities

- `HarnessState` tracks current token spend, the maximum budget, and action counts.
- `AgentActionType` defines the kinds of actions the governor evaluates.
- `HarnessGovernor.evaluate_action()` returns an `ActionVerdict` with approval and escalation details.
- Shell execution is treated as a privileged class of action and can be denied even when the command is otherwise harmless.
- The project is intentionally minimal, making it easy to build into larger harnesses and policy engines.

## How it works

```text
Agent action
      ↓
HarnessGovernor.evaluate_action()
      ↓
Budget check
      ↓
Action type check
      ↓
Risk pattern detection
      ↓
Approve / deny + human gate verdict
```

The default behavior is conservative:

- if the token budget is exhausted, the action is rejected
- if the action is a shell command and the safety gate is enabled, it is reviewed for destructive patterns
- when the command matches a known dangerous pattern, approval is denied and escalation is requested

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Quick start

```bash
harnessguard --action shell_exec --meta "echo safe" --budget 1.0
harnessguard --action shell_exec --meta "rm -rf /tmp/test" --budget 1.0
```

The first command is allowed through the governor with a human approval gate. The second is rejected because the command contains a destructive pattern.

```text
$ harnessguard --action shell_exec --meta "echo safe" --budget 1.0
[*] Verdict: Approved=True, HumanGate=True, Reason=Shell execution requires authorization gate.

$ harnessguard --action shell_exec --meta "rm -rf /tmp/test" --budget 1.0
[*] Verdict: Approved=False, HumanGate=True, Reason=Destructive shell command detected.
```

## CLI usage

```bash
harnessguard --help
```

Available action types:

- `file_write`
- `shell_exec`
- `api_call`

## Configuration

The CLI accepts a compact set of runtime controls:

```bash
harnessguard --action <file_write|shell_exec|api_call> \
  --meta "<action details>" \
  --budget 1.0
```

The underlying state model is defined in `src/harnessguard/governor.py` and includes:

- `token_spend`
- `max_token_budget`
- `actions_executed`
- `requires_approval_for_shell`

This makes the governance policy explicit and easy to extend without adding a large framework.

## Technical details

This repository is intentionally small and focused. The core logic is centered around a single governor pattern:

```python
from harnessguard.governor import HarnessGovernor, HarnessState, AgentActionType

state = HarnessState(token_spend=0.1, max_token_budget=1.0, actions_executed=2)
governor = HarnessGovernor(state)
verdict = governor.evaluate_action(AgentActionType.SHELL_EXEC, {"command": "echo safe"})
```

The enforcement logic checks, in order:

1. token budget exhaustion
2. shell execution safety gate
3. destructive command pattern detection
4. approval verdict and escalation requirement

## Roadmap

Planned work is intentionally modest and practical:

- policy rules as structured configuration rather than hard-coded checks
- allowlist-based file and shell controls
- richer action metadata and structured verdict reporting
- stronger integration hooks for broader agent harnesses

## Contributing

Contributions are welcome if they improve the governance model, clarify the policy logic, or make the project easier to integrate in real agent environments.

Suggested workflow:

```bash
git clone https://github.com/dntaskmehow/harnessguard.git
cd harnessguard
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Then open an issue or pull request with a clear description of the rule change or safety improvement.

## Security and responsible use

HarnessGuard is a safety and governance wrapper, not a substitute for operational discipline. It is designed to reduce the risk of destructive or unbounded automation, but it should be paired with review procedures and environment controls where autonomous actions are trusted with privileged access.

- treat shell access as a sensitive capability
- review human approval flows for production use
- avoid disabling safety checks without explicit operational justification

## License

This project is distributed under the MIT license, as declared in the package metadata for this repository.

---

<p align="center">
  <sub>Built for agent safety, explicit policy checks, and human oversight.</sub>
</p>

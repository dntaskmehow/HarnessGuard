import argparse
import sys
from .governor import HarnessGovernor, HarnessState, AgentActionType

def main():
    parser = argparse.ArgumentParser(description="HarnessGuard: Agent Governance.")
    parser.add_argument("--action", required=True, choices=["file_write", "shell_exec", "api_call"])
    parser.add_argument("--meta", default="")
    parser.add_argument("--budget", type=float, default=1.0)
    args = parser.parse_args()
    state = HarnessState(token_spend=0.1, max_token_budget=args.budget, actions_executed=2)
    governor = HarnessGovernor(state)
    verdict = governor.evaluate_action(AgentActionType(args.action), {"command": args.meta})
    print(f"[*] Verdict: Approved={verdict.approved}, HumanGate={verdict.requires_human_gate}, Reason={verdict.reason}")
    if not verdict.approved: sys.exit(1)

if __name__ == "__main__": main()

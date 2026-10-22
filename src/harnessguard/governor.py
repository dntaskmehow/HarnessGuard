from enum import Enum
from typing import Dict, Any
from pydantic import BaseModel

class AgentActionType(Enum):
    FILE_WRITE = "file_write"
    SHELL_EXEC = "shell_exec"
    API_CALL = "api_call"

class HarnessState(BaseModel):
    token_spend: float
    max_token_budget: float
    actions_executed: int
    requires_approval_for_shell: bool = True

class ActionVerdict(BaseModel):
    approved: bool
    requires_human_gate: bool
    reason: str

class HarnessGovernor:
    def __init__(self, state: HarnessState):
        self.state = state

    def evaluate_action(self, action_type: AgentActionType, metadata: Dict[str, Any]) -> ActionVerdict:
        if self.state.token_spend >= self.state.max_token_budget:
            return ActionVerdict(approved=False, requires_human_gate=False, reason="Token budget exhausted.")
        if action_type == AgentActionType.SHELL_EXEC and self.state.requires_approval_for_shell:
            cmd = metadata.get("command", "")
            if any(p in cmd for p in ["rm -rf", "mkfs", "dd", "shutdown"]):
                return ActionVerdict(approved=False, requires_human_gate=True, reason="Destructive shell command detected.")
            return ActionVerdict(approved=True, requires_human_gate=True, reason="Shell execution requires authorization gate.")
        return ActionVerdict(approved=True, requires_human_gate=False, reason="Action cleared.")

"""Validate tool calls against the allowlist and parameter constraints."""
import yaml
import json
from pathlib import Path
from typing import Any

class ToolValidator:
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    ALLOWLIST_PATH = PROJECT_ROOT / "configs" / "tool_allowlist.yaml"
    def __init__(self, allowlist_path: str = str(ALLOWLIST_PATH)):
        with open(allowlist_path) as f:
            self.config = yaml.safe_load(f)
        self.allowed = {t["name"]: t for t in self.config["allowed_tools"]}

    def validate_call(self, tool_name: str, parameters: dict) -> tuple[bool, str]:
        """Return (success, error_message)."""
        if tool_name not in self.allowed:
            return False, f"Tool '{tool_name}' is not allowed."

        spec = self.allowed[tool_name]
        if "parameters" not in spec or not spec["parameters"]:
            # no parameters expected
            if parameters:
                return False, f"Tool '{tool_name}' does not accept parameters."
            return True, ""

        # Validate each parameter
        for param_name, constraints in spec["parameters"].items():
            if constraints.get("required", True):  # default required
                if param_name not in parameters:
                    return False, f"Missing required parameter '{param_name}'."
            else:
                if param_name not in parameters:
                    continue

            value = parameters.get(param_name)
            if "type" in constraints:
                expected = constraints["type"]
                if expected == "string" and not isinstance(value, str):
                    return False, f"Parameter '{param_name}' must be a string."
                if expected == "number" and not isinstance(value, (int, float)):
                    return False, f"Parameter '{param_name}' must be a number."

            if "min_length" in constraints and isinstance(value, str):
                if len(value) < constraints["min_length"]:
                    return False, f"Parameter '{param_name}' too short."
            if "max_length" in constraints and isinstance(value, str):
                if len(value) > constraints["max_length"]:
                    return False, f"Parameter '{param_name}' too long."

            if "minimum" in constraints and isinstance(value, (int, float)):
                if value < constraints["minimum"]:
                    return False, f"Parameter '{param_name}' below minimum."
            if "maximum" in constraints and isinstance(value, (int, float)):
                if value > constraints["maximum"]:
                    return False, f"Parameter '{param_name}' above maximum."

        return True, ""

    def requires_confirmation(self, tool_name: str) -> bool:
        spec = self.allowed.get(tool_name)
        if spec is None:
            return False
        return spec.get("confirmation_required", False)

# Example usage
if __name__ == "__main__":
    v = ToolValidator()
    ok, msg = v.validate_call("generate_audio", {"prompt": "lofi chill", "duration_seconds": 30})
    print(f"Allowed: {ok} – {msg}")
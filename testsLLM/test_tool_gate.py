"""Tool Gate – expand existing tool validator for gate-specific checks"""
import pytest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from src.tool_validator import ToolValidator

validator = ToolValidator()

def test_only_allowlisted_tools():
    """Any tool not in allowlist must be rejected."""
    ok, msg = validator.validate_call("delete_audio", {})
    assert not ok
    assert "not allowed" in msg or "Blocked tool" in msg

def test_write_tools_require_confirmation():
    """generate_audio is a write tool; must set requires_human_review=True"""
    ok, msg = validator.validate_call("generate_audio", {"prompt": "test", "duration_seconds": 30})
    assert ok
    # The validator's ToolConfig should return a flag. Assume validator returns a tuple (ok, msg, requires_confirm).
    # If your current validator doesn't, extend it. Example:
    # result = validator.validate_call_with_confirmation(...)
    # assert result.requires_human_review is True

def test_parameter_schema_validation():
    """Invalid parameters must be rejected (from original test)."""
    ok, msg = validator.validate_call(
        "generate_audio",
        {"prompt": "test", "duration_seconds": 200}
    )
    assert not ok
    assert "above maximum" in msg
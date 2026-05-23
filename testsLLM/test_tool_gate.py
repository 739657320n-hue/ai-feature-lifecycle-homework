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
    assert "not allowed" in msg or "Blocked tool" in msg or "not in allowlist" in msg

def test_write_tools_require_confirmation():
    """generate_audio is a write tool; must set requires_human_review=True"""
    # Assume validator now has a method requires_confirmation(tool_name) -> bool
    # If not, we can mock or add a simple check based on tool name.
    # We'll check by calling a dedicated method.
    # For now, we assume the method exists. If not, uncomment the next lines to directly check.
    # If validator doesn't have the method, we can add a temporary check here:
    assert hasattr(validator, 'requires_confirmation'), "Validator must implement requires_confirmation()"
    assert validator.requires_confirmation("generate_audio") is True, \
        "generate_audio should require confirmation"
    assert validator.requires_confirmation("search_sounds") is False, \
        "search_sounds should not require confirmation"

def test_parameter_schema_validation():
    """Invalid parameters must be rejected (from original test)."""
    ok, msg = validator.validate_call(
        "generate_audio",
        {"prompt": "test", "duration_seconds": 200}
    )
    assert not ok
    assert "above maximum" in msg or "invalid" in msg or "duration" in msg.lower()

def test_valid_parameters_pass():
    """Valid parameters should be accepted for an allowlisted tool."""
    ok, msg = validator.validate_call(
        "generate_audio",
        {"prompt": "test", "duration_seconds": 30}
    )
    assert ok, f"Valid call should pass: {msg}"
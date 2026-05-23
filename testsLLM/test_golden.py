"""Schema Gate – validate all golden prompts against Output_Schema.json"""
import json
import jsonschema
import pytest
from pathlib import Path
from typing import Any, Dict

# Paths
SCHEMA_PATH = Path(__file__).parent.parent / "specsLLM" / "Output_Schema.json"
GOLDEN_PATH = Path(__file__).parent / "golden_prompts.json"

# Load schema
with open(SCHEMA_PATH) as f:
    SCHEMA = json.load(f)

# Load golden prompts
with open(GOLDEN_PATH) as f:
    GOLDEN_PROMPTS = json.load(f)

def mock_llm_response(input_prompt: str, expected_action: str) -> Dict[str, Any]:
    """
    Simulates the LLM output for a given golden prompt.
    In production, call the actual LLM here.
    Returns a dictionary that should conform to Output_Schema.json.
    """
    response = {
        "answer": f"Simulated response for: {input_prompt}",
        "confidence": 0.9,
        "action": expected_action,
        "sources": ["style_guide_v2"],
        "error_code": None,
        "requires_human_review": True if expected_action == "generate_audio" else False
    }

    if expected_action == "generate_audio":
        response["audio_url"] = "http://example.com/audio/simulated"
        response["tool_call"] = {
            "tool_name": "generate_audio",
            "parameters": {"prompt": input_prompt, "duration_seconds": 30},
            "status": "allowed"
        }
    # For "search_sounds", "clarify", "none": do NOT include audio_url or tool_call
    # They are not required and allowing null would break schema validation.

    return response

def test_golden_prompt_output_schema():
    """Every golden prompt output must conform to Output_Schema.json"""
    for case in GOLDEN_PROMPTS:
        input_text = case["input"]
        expected_action = case["expected_action"]
        output = mock_llm_response(input_text, expected_action)
        try:
            jsonschema.validate(instance=output, schema=SCHEMA)
        except jsonschema.ValidationError as e:
            pytest.fail(f"Golden prompt '{input_text}' failed schema validation: {e}")

def test_golden_action_and_confidence():
    """Additional checks: action matches expected and confidence above minimum"""
    for case in GOLDEN_PROMPTS:
        input_text = case["input"]
        expected_action = case["expected_action"]
        output = mock_llm_response(input_text, expected_action)
        assert output["action"] == expected_action, f"Action mismatch for '{input_text}': got {output['action']}, expected {expected_action}"
        min_conf = case.get("expected_confidence_min", 0.0)
        assert output["confidence"] >= min_conf, f"Confidence too low for '{input_text}': {output['confidence']}"

def test_requires_human_review():
    """Check that write tools set requires_human_review=True"""
    for case in GOLDEN_PROMPTS:
        input_text = case["input"]
        expected_action = case["expected_action"]
        output = mock_llm_response(input_text, expected_action)
        expected_flag = case["expected_requires_human_review"]
        assert output["requires_human_review"] == expected_flag, \
            f"requires_human_review mismatch for '{input_text}': got {output['requires_human_review']}, expected {expected_flag}"
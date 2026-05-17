"""Schema Gate – validate all golden prompts against Output_Schema.json"""
import json
import jsonschema
import pytest
from pathlib import Path

# Load schema
SCHEMA_PATH = Path(__file__).parent.parent / "Output_Schema.json"
with open(SCHEMA_PATH) as f:
    SCHEMA = json.load(f)

# Golden prompts and expected outputs (you should expand to 20)
GOLDEN_PROMPTS = [
    {
        "input": "Generate a 30-second classical piano piece",
        "expected_output": {
            "action": "generate_audio",
            "confidence": 0.5,
            "answer": "Here is your classical piano audio:",
            "audio_url": "http://example.com/audio/1",
            "tool_call": {"tool_name": "generate_audio", "parameters": {"prompt": "classical piano", "duration_seconds": 30}, "status": "allowed"},
            "requires_human_review": True,
            "sources": []
        }
    },
    # Add remaining 19 prompts...
]

def test_golden_prompt_output_schema():
    """Every golden prompt output must conform to Output_Schema.json"""
    for case in GOLDEN_PROMPTS:
        # In production, call the actual LLM here.
        output = case["expected_output"]
        try:
            jsonschema.validate(instance=output, schema=SCHEMA)
        except jsonschema.ValidationError as e:
            pytest.fail(f"Golden prompt '{case['input']}' failed schema validation: {e}")
.PHONY: test data-check eval-gate setup safety-tests schema-gate tool-gate slo-gate

setup:
	pip install -r requirements.txt

test:
	python -m pytest tests/test_preprocessing.py -v

data-check:
	python tests/test_data_checks.py

eval-gate:
	python pipelines/eval_gate.py

safety-tests:
	python -m pytest tests/test_safety.py -v

schema-gate:
	python -m pytest testsLLM/test_golden.py -v

tool-gate:
	python -m pytest testsLLM/test_tool_gate.py -v

slo-gate:
	python pipelines/slo_gate.py
PY=python3
PIP=pip

.PHONY: setup test run fmt clean install help

setup:
	$(PY) -m venv .venv && . .venv/bin/activate && $(PIP) install -r requirements.txt

test:
	pytest -q

run:
	$(PY) main.py "What is 12.5% of 243?"

fmt:
	@echo "Running code formatters (black + isort)..."
	$(PY) -m isort .
	$(PY) -m black .

lint:
	@echo "Running linter (flake8)..."
	$(PY) -m flake8 agent --max-line-length=100

help:
	@echo "Available commands:"
	@echo "  setup       - Create virtual environment and install dependencies"
	@echo "  test        - Run tests quietly"
	@echo "  run         - Run example query"
	@echo "  fmt         - Format code (placeholder)"
	@echo "  install     - Install package in development mode"
	@echo "  test-v      - Run tests with verbose output"
	@echo "  test-cov    - Run tests with coverage report"
	@echo "  clean       - Clean up build artifacts and cache"
	@echo "  examples    - Run example queries"

install:
	$(PIP) install -e .

test-v:
	pytest -v

test-cov:
	pytest --cov=agent --cov-report=html --cov-report=term

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ *.egg-info/ .pytest_cache/ htmlcov/ .coverage

examples:
	@echo "Running example queries..."
	$(PY) main.py "What is 12.5% of 243?"
	$(PY) main.py "What is the weather in Paris?"
	$(PY) main.py "Who is Ada Lovelace?"
	$(PY) main.py "Translate hello to Spanish"
	
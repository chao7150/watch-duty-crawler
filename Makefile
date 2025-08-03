.PHONY: lint typecheck test format check-all install dev-install

install:
	pip install -e .

dev-install:
	pip install -e ".[dev]"

lint:
	ruff check src/watch_duty_crawler

typecheck:
	mypy

test:
	pytest

format:
	ruff format src tests

check-all: lint typecheck test
	@echo "All checks completed!"

clean:
	rm -rf build/ dist/ *.egg-info/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

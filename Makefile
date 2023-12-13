TESTS := tests

.venv:
	poetry install --no-root
	poetry check

# Test
.pytest:
	poetry run pytest $(TESTS)

test: .venv .pytest

# Lint
isort: .venv
	poetry run isort --check $(PROJECT) $(TESTS)

.black:
	poetry run black --check --diff $(PROJECT) $(TESTS)

flake: .venv
	poetry run flake8 $(PROJECT) $(TESTS)

mypy: .venv
	poetry run mypy $(PROJECT) $(TESTS)

pylint: .venv
	poetry run pylint $(PROJECT) $(TESTS)

lint: isort flake

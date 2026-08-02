PYTHON ?= .venv/bin/python
CC ?= cc
CXX ?= c++
BUILD_DIR := .build

CFLAGS := -O3 -std=c11 -Wall -Wextra -pedantic
CXXFLAGS := -O3 -std=c++17 -Wall -Wextra -pedantic

.PHONY: help setup check test syntax checkers clean

help:
	@echo "make setup     Create .venv and install pinned development dependencies"
	@echo "make check     Build native checkers, parse Python, and run the test suite"
	@echo "make checkers  Build all native verification binaries under $(BUILD_DIR)/"
	@echo "make clean     Remove disposable build and test caches"

setup:
	python3 -m venv .venv
	.venv/bin/python -m pip install --upgrade pip
	.venv/bin/python -m pip install -r requirements-dev.txt

check: checkers syntax test

test:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -m pytest -p no:cacheprovider -q

syntax:
	PYTHONDONTWRITEBYTECODE=1 $(PYTHON) -c 'import ast, pathlib; files = sorted(pathlib.Path("verifier").glob("*.py")) + sorted(pathlib.Path("tests").glob("*.py")); [ast.parse(path.read_text(), filename=str(path)) for path in files]; print(f"syntax: {len(files)} Python files")'

checkers: \
	$(BUILD_DIR)/check_g6 \
	$(BUILD_DIR)/check_c8 \
	$(BUILD_DIR)/check_power_masks \
	$(BUILD_DIR)/z3_lift_search

$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

$(BUILD_DIR)/check_g6: verifier/check_g6.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) $< -o $@

$(BUILD_DIR)/check_c8: verifier/check_c8.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) $< -o $@

$(BUILD_DIR)/check_power_masks: verifier/check_power_masks.c | $(BUILD_DIR)
	$(CC) $(CFLAGS) $< -o $@

$(BUILD_DIR)/z3_lift_search: verifier/z3_lift_search.cpp | $(BUILD_DIR)
	$(CXX) $(CXXFLAGS) $< -o $@

clean:
	rm -rf .build .pytest_cache .mypy_cache .ruff_cache htmlcov
	find verifier tests -type d -name __pycache__ -prune -exec rm -rf {} +

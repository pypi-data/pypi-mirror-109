.PHONY: clean lint format help
.DEFAULT_GOAL := help

PYTHON := python

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("\033[36m%-15s\033[0m %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: ## remove all build, test, coverage and Python artifacts
	find modoboa_automua tests \
	  \( -name '*.py[co]' -o -name '__pycache__' \) -exec rm -rf {} +
	rm -rf build dist .eggs *.egg-info

test: ## run tests quickly with the current Python
	$(PYTHON) ./tests/manage.py test tests

coverage: ## check code coverage quickly with the current Python
	$(PYTHON) -m coverage run ./runtests.py
	$(PYTHON) -m coverage report -m
	$(PYTHON) -m coverage html
	@echo open htmlcov/index.html

lint: ## check the Python code syntax and style
	$(PYTHON) -m flake8 modoboa_automua tests

format: ## fix the Python code syntax and imports order
	$(PYTHON) -m isort modoboa_automua tests
	$(PYTHON) -m black modoboa_automua tests

release: dist ## package and upload a release
	twine upload dist/*

dist: clean ## builds source and wheel package
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

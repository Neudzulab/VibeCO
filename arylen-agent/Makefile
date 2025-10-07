.PHONY: lint test ci

lint:
	python -m pyflakes scripts src tests

test:
	pytest

ci: lint test

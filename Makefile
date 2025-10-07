.PHONY: render test clean refactor-test refactor-metrics refactor-ci

render:
	python scripts/render.py

test:
	pytest

clean:
	rm -f PROJECT_SUMMARY.md

refactor-test:
	pytest -q --maxfail=1 --disable-warnings | tee .pytest-out.txt
	# example: produce a coverage summary (customise for the project)
	@echo "TOTAL 85%" > .coverage-summary

refactor-metrics:
	python - <<'PY'
print("metrics: TODO integrate radon/phpmd etc.")
PY

refactor-ci: refactor-test refactor-metrics

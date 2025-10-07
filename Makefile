.PHONY: render test clean

render:
	python scripts/render.py

test:
	pytest

clean:
	rm -f PROJECT_SUMMARY.md

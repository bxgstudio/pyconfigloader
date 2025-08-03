SHELL:=/bin/bash

install-dev:
	mkdir -p ignored && echo '*' > ignored/.gitignore && \
	python3 -m venv ignored/venv && \
	source ignored/venv/bin/activate && \
	cd python && pip install -e . && pip install pytest

unit-tests:
	source ignored/venv/bin/activate && cd python/tests && pytest

PYTHON=python3

all: build test

build: build/limit_checker

build/limit_checker: src/limit_checker.c
	mkdir -p build
	cc -Wall -Wextra -O2 src/limit_checker.c -o build/limit_checker

test:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py'

run:
	$(PYTHON) -m verify.runner --manifest data/manifest.yaml

PYTHON ?= python3
LATEXMK ?= latexmk

.PHONY: all build check test container clean
all: check

build:
	$(LATEXMK) -pdf -interaction=nonstopmode -halt-on-error -file-line-error -no-shell-escape -recorder -outdir=../build -cd manuscript/main.tex

check: test build
	$(PYTHON) scripts/project.py check
	$(PYTHON) scripts/project.py collect

test:
	$(PYTHON) -m unittest discover -s tests -v

container:
	sh scripts/container-build.sh

clean:
	rm -rf build dist

LATEXMK_OPTIONS := -interaction=nonstopmode -file-line-error -pdf -outdir=../build -cd

all: | dist
	latexmk $(LATEXMK_OPTIONS) src/main.tex
	cp build/main.pdf dist/

dist:
	mkdir -p $@

clean:
	rm -rf build dist

.PHONY: all clean

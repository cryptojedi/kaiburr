kaiburr.pdf: *.tex *.bib
	lualatex kaiburr.tex
	lualatex kaiburr.tex
	bibtex kaiburr
	lualatex kaiburr.tex

.PHONY: clean

clean:
	-rm *.aux
	-rm kaiburr.abstract
	-rm kaiburr.bbl
	-rm kaiburr.blg
	-rm kaiburr.brf
	-rm kaiburr.log
	-rm kaiburr.meta
	-rm kaiburr.out
	-rm kaiburr.pdf

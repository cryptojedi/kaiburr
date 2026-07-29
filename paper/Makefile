kaiburr.pdf: *.tex *.bib
	lualatex kaiburr.tex
	bibtex kaiburr
	lualatex kaiburr.tex
	lualatex kaiburr.tex

draft.pdf: draft.tex *.bib
	lualatex draft.tex
	lualatex draft.tex
	-bibtex draft
	lualatex draft.tex

proposal.pdf:
	$(MAKE) -C proposal proposal.pdf

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
	-rm draft.bbl
	-rm draft.blg
	-rm draft.brf
	-rm draft.log
	-rm draft.out
	-rm draft.pdf
	-$(MAKE) -C proposal clean

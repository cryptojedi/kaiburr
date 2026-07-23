kaiburr.pdf: *.tex *.bib
	lualatex kaiburr.tex
	lualatex kaiburr.tex
	bibtex kaiburr
	lualatex kaiburr.tex

draft.pdf: draft.tex *.bib
	lualatex draft.tex
	lualatex draft.tex
	-bibtex draft
	lualatex draft.tex

proposal.pdf: proposal.tex *.bib
	lualatex proposal.tex
	lualatex proposal.tex
	-bibtex proposal
	lualatex proposal.tex

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
	-rm proposal.bbl
	-rm proposal.blg
	-rm proposal.brf
	-rm proposal.log
	-rm proposal.out
	-rm proposal.pdf

BUILDDIR = build

proposal.pdf: proposal.tex *.bib
	latexmk -pdflua -output-directory=$(BUILDDIR) proposal.tex
	cp $(BUILDDIR)/proposal.pdf .

.PHONY: clean

clean:
	latexmk -output-directory=$(BUILDDIR) -C proposal.tex
	-rm -rf $(BUILDDIR)
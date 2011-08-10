
documentation.pdf: documentation.tex
	pdflatex $<
	pdflatex $<

%.tex: %.txt
	./txt2tags -t tex --toc -i $<

.PHONY: clean

clean:
	@rm documentation.tex
	@rm documentation.log
	@rm documentation.aux
	@rm documentation.out
	@rm documentation.toc

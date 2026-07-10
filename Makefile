TECTONIC ?= tectonic
CVDIR    := cv
SITE     := _site

PT_PDF := $(CVDIR)/cv-pt.pdf
EN_PDF := $(CVDIR)/cv-en.pdf

.PHONY: all pdf site serve clean

all: pdf

pdf: $(PT_PDF) $(EN_PDF)

$(CVDIR)/%.pdf: $(CVDIR)/%.tex $(CVDIR)/resume.cls
	$(TECTONIC) -X compile $< --outdir $(CVDIR)

site: pdf
	rm -rf $(SITE)
	mkdir -p $(SITE)
	cp -r site/. $(SITE)/
	cp CNAME $(SITE)/ 2>/dev/null || true
	cp $(PT_PDF) $(SITE)/rodrigo-roque-cv-pt.pdf
	cp $(EN_PDF) $(SITE)/rodrigo-roque-cv-en.pdf
	@echo "Site assembled in $(SITE)/"

serve: site
	@echo "Serving $(SITE)/ at http://localhost:8000 (Ctrl+C to stop)"
	cd $(SITE) && python3 -m http.server 8000

clean:
	rm -rf $(SITE)
	rm -f $(CVDIR)/*.pdf $(CVDIR)/*.log $(CVDIR)/*.aux $(CVDIR)/*.png

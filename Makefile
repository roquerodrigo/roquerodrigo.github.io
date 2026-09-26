TECTONIC ?= tectonic
CVDIR    := cv
SITE     := _site

PT_PDF := $(CVDIR)/cv-pt.pdf
EN_PDF := $(CVDIR)/cv-en.pdf

.PHONY: all pdf site serve projects clean

all: pdf

pdf: $(PT_PDF) $(EN_PDF)

$(CVDIR)/%.pdf: $(CVDIR)/%.tex $(CVDIR)/resume.cls
	$(TECTONIC) -X compile $< --outdir $(CVDIR)

site: pdf
	rm -rf $(SITE)
	mkdir -p $(SITE)
	cp -r site/. $(SITE)/
	sed -e "s|href=\"styles.css\"|href=\"styles.css?v=$$(shasum -a 256 site/styles.css | cut -c1-10)\"|" \
	    -e "s|src=\"app.js\"|src=\"app.js?v=$$(shasum -a 256 site/app.js | cut -c1-10)\"|" \
	    site/index.html > $(SITE)/index.html
	cp CNAME $(SITE)/ 2>/dev/null || true
	cp $(PT_PDF) $(SITE)/rodrigo-roque-cv-pt.pdf
	cp $(EN_PDF) $(SITE)/rodrigo-roque-cv-en.pdf
	@echo "Site assembled in $(SITE)/"

serve: site
	@echo "Serving $(SITE)/ at http://localhost:8000 (Ctrl+C to stop)"
	cd $(SITE) && python3 -m http.server 8000

projects:
	python3 -m scripts.project_stats

clean:
	rm -rf $(SITE)
	rm -f $(CVDIR)/*.pdf $(CVDIR)/*.log $(CVDIR)/*.aux $(CVDIR)/*.png

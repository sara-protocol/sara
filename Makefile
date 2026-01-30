\
SHELL := /usr/bin/env bash

ROOT := $(CURDIR)
LANG ?= zh

MANUSCRIPT := $(ROOT)/manuscript/$(LANG)
BUILD := $(ROOT)/build/$(LANG)

META := $(ROOT)/metadata/book.$(LANG).yml
CSS := $(ROOT)/metadata/style.css
TEX := $(ROOT)/templates/book.tex
DOCX_REF := $(ROOT)/templates/reference.docx

MERGED := $(BUILD)/book_merged.md
PDF := $(BUILD)/book.pdf
EPUB := $(BUILD)/book.epub
DOCX := $(BUILD)/book.docx

.PHONY: all clean merge qa qa-strict pdf epub docx

all: qa-strict pdf epub docx

clean:
	rm -rf $(ROOT)/build

$(BUILD):
	mkdir -p $(BUILD)

merge: $(BUILD)
	@echo "==> Merging chapters (LANG=$(LANG))..."
	@python3 scripts/build.py --lang $(LANG) --merge-only

qa: merge
	@echo "==> QA (L1) (LANG=$(LANG))..."
	@python3 scripts/qa.py --input $(MERGED)

qa-strict: qa pdf epub
	@echo "==> QA_STRICT (L1+L2) (LANG=$(LANG))..."
	@python3 scripts/qa_strict.py --lang $(LANG) --config config/qa_rules.yml --exceptions config/language_exceptions.yml

pdf: merge
	@echo "==> Building PDF (LANG=$(LANG))..."
	@pandoc $(MERGED) \
		--metadata-file $(META) \
		--pdf-engine="/c/Program Files/MiKTeX/miktex/bin/x64/xelatex.exe" \
                  --syntax-highlighting=none \
		--template $(TEX) \
		--output $(PDF)

epub: merge
	@echo "==> Building EPUB (LANG=$(LANG))..."
	@pandoc $(MERGED) \
		--metadata-file $(META) \
		--css $(CSS) \
		--toc --toc-depth=3 \
		--output $(EPUB)

docx: merge
	@echo "==> Building DOCX (LANG=$(LANG))..."
	@pandoc $(MERGED) \
		--metadata-file $(META) \
		--reference-doc $(DOCX_REF) \
		--output $(DOCX)

.PHONY: baseline-init
baseline-init: qa pdf epub
	@echo "==> Baseline init (LANG=$(LANG))..."
	@python3 scripts/qa_strict.py --lang $(LANG) --config config/qa_rules.yml --exceptions config/language_exceptions.yml --baseline-init

.PHONY: dashboard
dashboard:
	@python3 scripts/dashboard.py

.PHONY: release
release: qa-strict dashboard
	@python3 scripts/release.py


.PHONY: apple-books-package apple-books-verify apple-books-upload
apple-books-package: epub
	@python3 scripts/apple_books_package.py

apple-books-verify: apple-books-package
	@ACRE_APPLE_MODE=verify python3 scripts/apple_books_transporter.py

apple-books-upload: apple-books-package
	@ACRE_APPLE_MODE=upload python3 scripts/apple_books_transporter.py

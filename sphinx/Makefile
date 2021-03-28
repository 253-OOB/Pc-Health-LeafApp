# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line, and also
# from the environment for the first two.
SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = rstfiles
BUILDDIR      = ..


REMOVE		  = rd
DOCFILES      = ../docs
REMOVE_DOCS  = IF exist "$(DOCFILES)" ( $(REMOVE) /s /q "$(DOCFILES)"  )

REMOVE_DOCTREES  = IF exist "../doctrees" ( $(REMOVE) /s /q "../doctrees"  )

RENAME        = ren

# Put it first so that "make" without argument is like "make help".
help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@ echo "" > ../dirhtml/.nojekyll
	@ echo "Deleting folders.."
	@$(REMOVE_DOCS)
	@$(REMOVE_DOCTREES)
	@ echo "Finished deleting folders."
	@ echo "Renaming folder.."
	@$(RENAME) "../dirhtml" docs
	@ echo "Finished renaming folder."
	@ echo "END"
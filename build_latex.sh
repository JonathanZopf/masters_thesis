#!/bin/bash

set -e
export PATH="/Library/TeX/texbin:$PATH"

FILE="solution_proposal_presentation/presentation.tex"

latexmk -c

latexmk -pdf -interaction=nonstopmode -halt-on-error "$FILE"

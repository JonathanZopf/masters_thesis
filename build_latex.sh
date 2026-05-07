#!/bin/bash

set -e
export PATH="/Library/TeX/texbin:$PATH"

FILE="main.tex"

latexmk -c

latexmk -pdf -interaction=nonstopmode -halt-on-error "$FILE"

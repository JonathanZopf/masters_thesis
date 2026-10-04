#!/bin/bash

set -e
export PATH="/Library/TeX/texbin:$PATH"

FILE="main.tex"

latexmk -c

latexindent -w *.tex
latexindent -w chapters/*.tex

latexmk -pdf -interaction=nonstopmode -halt-on-error "$FILE"

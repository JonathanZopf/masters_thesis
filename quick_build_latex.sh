#!/bin/bash
set -e
export PATH="/Library/TeX/texbin:$PATH"
latexmk -pdf -interaction=nonstopmode -f main.tex

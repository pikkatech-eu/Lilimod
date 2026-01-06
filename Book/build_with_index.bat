@echo off
rem Batch file to build LaTeX book with index

set nameonly=main

echo Building %nameonly%.tex ...

rem First XeLaTeX pass (output to build folder)
xelatex -synctex=1 -interaction=nonstopmode -output-directory=build "%nameonly%.tex"

rem Run makeindex (build folder)
makeindex -o build\%nameonly%.ind build\%nameonly%.idx

rem Second XeLaTeX pass
xelatex -synctex=1 -interaction=nonstopmode -output-directory=build "%nameonly%.tex"

rem Copy PDF to main folder
copy /Y build\%nameonly%.pdf "%cd%\%nameonly%.pdf"

pause

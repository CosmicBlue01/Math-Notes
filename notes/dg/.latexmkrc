# 锁定 XeLaTeX，禁止回落到 pdfLaTeX
$pdf_mode = 5;
$xelatex  = 'xelatex -interaction=nonstopmode -file-line-error -synctex=1 %O %S';

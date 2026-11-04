# 锁定 XeLaTeX，禁止回落到 pdfLaTeX
$pdf_mode = 5;
$xelatex  = 'xelatex -interaction=nonstopmode -file-line-error -synctex=1 %O %S';
# 不用 out_dir：\include 的子目录 aux 会找不到，就地编译、产物由 .gitignore 排除

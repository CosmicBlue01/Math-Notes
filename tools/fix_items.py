import io, re, sys

B = chr(92)
MARK = re.compile(r'^\((i|ii|iii|iv|v|vi|1|2|3|4|5|6)\)\s')
BEG = re.compile(r'^' + re.escape(B + 'begin') + r'\{(example|remark|proof)\}')
END = re.compile(r'^' + re.escape(B + 'end') + r'\{(example|remark|proof)\}')

def convert(path):
    lines = io.open(path, encoding='utf-8').read().split('\n')
    out = []
    env = None
    in_list = False
    has_enum = False
    changed = 0
    for line in lines:
        s = line.strip()
        m = BEG.match(s)
        if m:
            env = m.group(1); in_list = False; has_enum = False
            out.append(line); continue
        if END.match(s):
            if in_list:
                out.append(B + 'end{enumerate}')
                in_list = False
            env = None
            out.append(line); continue
        if env:
            if B + 'begin{enumerate}' in line:
                has_enum = True
            if MARK.match(s) and not has_enum:
                if not in_list:
                    out.append(B + 'begin{enumerate}')
                    in_list = True
                out.append(B + 'item ' + MARK.sub('', s))
                changed += 1
                continue
        out.append(line)
    if changed:
        io.open(path, 'w', encoding='utf-8').write('\n'.join(out))
    print(path, 'items converted:', changed)

for p in sys.argv[1:]:
    convert(p)

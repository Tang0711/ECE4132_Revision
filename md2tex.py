#!/usr/bin/env python3
import argparse
import re
import sys
import unicodedata
from pathlib import Path

SYM = {
    'α': r'\alpha', 'β': r'\beta', 'γ': r'\gamma', 'δ': r'\delta', 'ε': r'\varepsilon',
    'ζ': r'\zeta', 'η': r'\eta', 'θ': r'\theta', 'ι': r'\iota', 'κ': r'\kappa',
    'λ': r'\lambda', 'μ': r'\mu', 'ν': r'\nu', 'ξ': r'\xi', 'π': r'\pi', 'ρ': r'\rho',
    'σ': r'\sigma', 'ς': r'\varsigma', 'τ': r'\tau', 'υ': r'\upsilon', 'φ': r'\varphi',
    'ϕ': r'\phi', 'χ': r'\chi', 'ψ': r'\psi', 'ω': r'\omega',
    'Γ': r'\Gamma', 'Δ': r'\Delta', 'Θ': r'\Theta', 'Λ': r'\Lambda', 'Ξ': r'\Xi',
    'Π': r'\Pi', 'Σ': r'\Sigma', 'Φ': r'\Phi', 'Ψ': r'\Psi', 'Ω': r'\Omega',
    '→': r'\rightarrow', '←': r'\leftarrow', '⇒': r'\Rightarrow', '⟹': r'\implies',
    '⇔': r'\Leftrightarrow', '≈': r'\approx', '≤': r'\leq', '≥': r'\geq', '≠': r'\neq',
    '±': r'\pm', '×': r'\times', '∞': r'\infty', '∈': r'\in', '∂': r'\partial',
    '·': r'\cdot', '°': r'^{\circ}', '≡': r'\equiv', '∼': r'\sim',
}
ASCII = {'→': '->', '←': '<-', '⇒': '=>', '≤': '<=', '≥': '>=', '≈': '~',
         '±': '+/-', '×': 'x', '°': 'deg', '·': '.'}
ESC = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '#': r'\#', '_': r'\_',
       '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}', '$': r'\$'}
LEVELS = ['section', 'subsection', 'subsubsection', 'paragraph', 'subparagraph', 'subparagraph']

SYM_RE = re.compile('[' + ''.join(SYM) + ']')
FENCE = re.compile(r'^([ \t]*)```[^\n]*\n(.*?)^[ \t]*```[ \t]*$', re.M | re.S)
CODE = re.compile(r'`([^`\n]+)`')
DISPLAY = re.compile(r'\$\$(.+?)\$\$', re.S)
ESC_DOLLAR = re.compile(r'\\\$([^$\n]*?[\\^_{][^$\n]*?)\\\$')
INLINE = re.compile(r'(?<![\\$])\$([^$\n]+?)\$')
LINK = re.compile(r'\[([^\]]+)\]\(([^)\s]+)\)')
BOLD = re.compile(r'\*\*(.+?)\*\*')
ITAL1 = re.compile(r'(?<![*\w])\*(?![\s*])(.+?)(?<![\s*])\*(?![*\w])')
ITAL2 = re.compile(r'(?<!\w)_(?!\s)([^_\n]+?)(?<!\s)_(?!\w)')
LIST = re.compile(r'^(\s*)([-*+]|\d+[.)])\s+(.*)$')
HR = re.compile(r'^\s{0,3}([-*_])(?:\s*\1){2,}\s*$')
HEAD = re.compile(r'^(#{1,6})\s+(.*?)\s*#*\s*$')
BOX = re.compile(r'^\[([ xX])\]\s+(.*)$')

PREAMBLE = r'''\documentclass[11pt,onecolumn]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{lmodern} % <--- ADD THIS LINE TO PROVIDE SCALABLE FONTS
\usepackage{amsmath,amssymb,amsfonts}
\usepackage{booktabs}
\usepackage{siunitx}
\usepackage[american,siunitx]{circuitikz}
\usepackage[margin=2cm]{geometry}
\usepackage{cite}
\usepackage{tabularx,listings,enumitem}
\usepackage[colorlinks=true,allcolors=black]{hyperref}
\usepackage{microtype}
\newcolumntype{Y}{>{\raggedright\arraybackslash}X}
\lstset{basicstyle=\ttfamily\footnotesize,breaklines=true,frame=single,columns=fullflexible}
'''

STASH = []


def hold(s):
    STASH.append(s)
    return f'\ue000{len(STASH) - 1}\ue001'


def restore(s):
    return re.sub('\ue000(\\d+)\ue001', lambda m: STASH[int(m.group(1))], s)


def escape(s):
    return re.sub(r'[\\&%#_{}~^$]', lambda m: ESC[m.group()], s)


def text_sym(s):
    return SYM_RE.sub(lambda m: r'\ensuremath{' + SYM[m.group()] + '}', s)


def math_sym(s):
    return SYM_RE.sub(lambda m: SYM[m.group()] + ' ', s)


MATRIX = re.compile(r'\\begin\{(?P<e>[a-zA-Z]*matrix\*?|array|aligned|align\*?|cases|split|gathered)\}'
                    r'(?P<b>.*?)\\end\{(?P=e)\}', re.S)
LONE_BS = re.compile(r'(?<!\\)\\(?=\s|$)')


def fix_rows(m):
    body = re.sub(r'\s*\\\\\s*$', ' ', LONE_BS.sub(r'\\\\', m['b']))
    return '\\begin{' + m['e'] + '}' + body + '\\end{' + m['e'] + '}'


SET_OPEN = re.compile(r'(\\mathcal\{L\}|\\in|=)\s*(?=\{)')


def brace_end(s, i):
    depth = 0
    for j in range(i, len(s)):
        depth += (s[j] == '{') - (s[j] == '}')
        if depth == 0:
            return j
    return -1


def fix_sets(s):
    out, pos = [], 0
    for m in SET_OPEN.finditer(s):
        a = m.end()
        b = brace_end(s, a) if a >= pos else -1
        if b < 0 or (m[1] == '=' and '\\mid' not in s[a:b]):
            continue
        out += [s[pos:a], r'\{', s[a + 1:b], r'\}']
        pos = b + 1
    return ''.join(out) + s[pos:]


def fix_math(s):
    s = MATRIX.sub(fix_rows, s.strip())
    s = re.sub(r'\s*,\s*;\s*', r',\\; ', s)
    s = fix_sets(s)
    s = re.sub(r'(?<!\\)\\\s*$', '', s)
    s = re.sub(r'(?<!\\)([%#])', r'\\\1', s)
    s = re.sub(r'\^\s*_(?![\w{\\])', '^*', s)
    return re.sub(r'\s,\s*(?=d[a-zA-Z\\])', r'\\, ', s)


def ascii_safe(s):
    def f(c):
        if ord(c) < 128:
            return c
        if c in ASCII:
            return ASCII[c]
        if c in SYM:
            return SYM[c].lstrip('\\')
        return unicodedata.normalize('NFKD', c).encode('ascii', 'ignore').decode() or '?'
    return ''.join(map(f, s))


def link(m):
    url = re.sub(r'([%#])', r'\\\1', m.group(2))
    return hold(r'\href{' + url + '}{') + m.group(1) + hold('}')


def inline(s):
    s = re.sub(r'\\([!-/:-@\[-`{-~])', r'\1', s)
    s = LINK.sub(link, s)
    s = BOLD.sub('\ue002\\1\ue003', s)
    s = ITAL1.sub('\ue004\\1\ue005', s)
    s = ITAL2.sub('\ue004\\1\ue005', s)
    s = escape(s)
    s = (s.replace('\ue002', r'\textbf{').replace('\ue004', r'\textit{')
          .replace('\ue003', '}').replace('\ue005', '}'))
    return text_sym(s)


def heading(level, text, strip):
    if strip:
        text = re.sub(r'^(\d+(\.\d+)*\.?\s+)+', '', text)
    return rf'\{LEVELS[min(level, 6) - 1]}{{{inline(text)}}}'


def table(rows):
    cells = [[c.strip() for c in r.strip().strip('|').split('|')] for r in rows]
    cells = [r for r in cells if not all(re.fullmatch(r':?-+:?', c) for c in r)]
    if not cells:
        return ''
    n = max(len(r) for r in cells)
    out = [rf'\begin{{center}}\small\begin{{tabularx}}{{\textwidth}}{{*{{{n}}}{{Y}}}}', r'\toprule']
    for k, r in enumerate(cells):
        row = [inline(c) for c in r + [''] * (n - len(r))]
        if k == 0:
            row = [rf'\textbf{{{c}}}' for c in row]
        out.append(' & '.join(row) + r' \\')
        if k == 0:
            out.append(r'\midrule')
    out += [r'\bottomrule', r'\end{tabularx}\end{center}']
    return '\n'.join(out)


def blocks(lines, strip):
    out, para, stack = [], [], []

    def flush():
        if para:
            out.append(inline(' '.join(para)))
            para.clear()

    def close(depth=0):
        flush()
        while len(stack) > depth:
            out.append(rf'\end{{{stack.pop()[1]}}}')

    i = 0
    while i < len(lines):
        line = lines[i].expandtabs(4).rstrip()
        i += 1

        if not line.strip():
            flush()
            nxt = next((l for l in lines[i:] if l.strip()), '')
            if stack and not (LIST.match(nxt) or nxt.startswith(' ')):
                close()
            continue

        if line.lstrip().startswith('|'):
            close()
            rows = [line]
            while i < len(lines) and lines[i].lstrip().startswith('|'):
                rows.append(lines[i])
                i += 1
            out.append(table(rows))
            continue

        m = HEAD.match(line)
        if m:
            close()
            out.append(heading(len(m[1]), m[2], strip))
            continue

        if HR.match(line):
            close()
            out.append(r'\medskip\hrule\medskip')
            continue

        if line.startswith('>'):
            close()
            quote = [re.sub(r'^>\s?', '', line)]
            while i < len(lines) and lines[i].startswith('>'):
                quote.append(re.sub(r'^>\s?', '', lines[i]))
                i += 1
            out += [r'\begin{quote}', inline(' '.join(quote)), r'\end{quote}']
            continue

        m = LIST.match(line)
        if m:
            flush()
            indent, text = len(m[1]), m[3]
            env = 'enumerate' if m[2][0].isdigit() else 'itemize'
            while stack and stack[-1][0] > indent:
                out.append(rf'\end{{{stack.pop()[1]}}}')
            if stack and stack[-1][0] == indent and stack[-1][1] != env:
                out.append(rf'\end{{{stack.pop()[1]}}}')
            if not stack or stack[-1][0] < indent:
                stack.append((indent, env))
                out.append(rf'\begin{{{env}}}')
            box = BOX.match(text)
            if box:
                mark = r'$\square$' if box[1] == ' ' else r'$\boxtimes$'
                out.append(rf'\item[{mark}]')
                text = box[2]
            else:
                out.append(r'\item\relax')
            para.append(text)
            continue

        if stack and line.startswith(' '):
            para.append(line.strip())
            continue

        close()
        para.append(line.strip())

    close()
    return out


def convert(md, strip=False):
    md = FENCE.sub(lambda m: m[1] + hold('\\begin{lstlisting}\n' + ascii_safe(m[2].rstrip('\n'))
                                          + '\n\\end{lstlisting}'), md)
    md = CODE.sub(lambda m: hold(r'\texttt{' + text_sym(escape(m[1])) + '}'), md)
    md = ESC_DOLLAR.sub(lambda m: '$' + m[1] + '$', md)
    md = DISPLAY.sub(lambda m: hold('\\[\n' + math_sym(fix_math(m[1])) + '\n\\]'), md)
    md = INLINE.sub(lambda m: hold('$' + math_sym(fix_math(m[1])) + '$'), md)
    return restore('\n'.join(blocks(md.splitlines(), strip)))


def natural(p):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', p.name)]


def main():
    ap = argparse.ArgumentParser(description='Merge all Markdown files in a folder into one LaTeX file.')
    ap.add_argument('folder', nargs='?', default='.')
    ap.add_argument('-o', '--output', default='merged.tex')
    ap.add_argument('-r', '--recursive', action='store_true')
    ap.add_argument('--title')
    ap.add_argument('--author', default='')
    ap.add_argument('--toc', action='store_true')
    ap.add_argument('--strip-numbers', action='store_true', help='drop leading numbers from headings')
    a = ap.parse_args()

    root = Path(a.folder)
    files = sorted(root.rglob('*.md') if a.recursive else root.glob('*.md'), key=natural)
    if not files:
        sys.exit(f'no .md files in {root}')

    parts = []
    for f in files:
        print(f'+ {f}')
        parts.append(convert(f.read_text(encoding='utf-8'), a.strip_numbers))

    head = [PREAMBLE]
    if a.title:
        head.append(rf'\title{{{escape(a.title)}}}' '\n' rf'\author{{{escape(a.author)}}}' '\n' r'\date{\today}')
    head.append(r'\begin{document}')
    if a.title:
        head.append(r'\maketitle')
    if a.toc:
        head.append(r'\tableofcontents' '\n' r'\newpage')

    doc = '\n'.join(head) + '\n' + '\n\\newpage\n'.join(parts) + '\n\\end{document}\n'
    Path(a.output).write_text(doc, encoding='utf-8')
    print(f'-> {a.output} ({len(files)} files)')


if __name__ == '__main__':
    main()
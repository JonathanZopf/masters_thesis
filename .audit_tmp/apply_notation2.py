import sys, os

root = sys.argv[1]

E = {}  # path -> list of (old, new, expected_count)

E['chapters/evaluation.tex'] = [
    # 33 PCC macro, as in modeling.tex
    (r"\operatorname{PCC}\!\left(", r"\mathrm{PCC}\left(", 2),
    # 25 kappa uses the stored partition
    (r"\sum_{s \,\in\, \mathcal{O}(\mathbf{x},\mathbf{C},n_{\max})} \ \sum_{\emptyset \neq T \subseteq s} |T|,",
     r"\sum_{s \,\in\, \mathbf{S}(\mathbf{x})} \ \sum_{\emptyset \neq T \subseteq s} |T|,", 1),
    (r"that is, the total number of concept occurrences across all non-empty treatments evaluated for $\mathbf{x}$, normalized by the number of concepts $|\mathbf{C}|$.",
     r"where $\mathbf{S}(\mathbf{x})=\mathcal{O}(\mathbf{x},\mathbf{C},n_{\max})$ is the partition from a single oracle invocation for $\mathbf{x}$, which is stored and reused instead of querying the oracle again. The value $\kappa(\mathbf{x},n_{\max})$ is the total number of concept occurrences across all non-empty treatments evaluated for $\mathbf{x}$, normalized by the number of concepts $|\mathbf{C}|$.", 1),
    # 29 "at most"
    (r"This requires the one-sided TOST $p$-values to be below $0.05$ for",
     r"This requires the one-sided TOST $p$-values to be at most $0.05$ for", 1),
]

E['results/rq2.tex'] = [
    (r"to be below $0.05$.}", r"to be at most $0.05$.}", 1),
]

E['chapters/modeling.tex'] = [
    # 31 edge not named e
    (r"\For{each edge $e = (C_i, C_j, A_{i,j}) \in \mathcal{L}$}",
     r"\For{each edge $(C_i, C_j, A_{i,j}) \in \mathcal{L}$}", 1),
    # 28 softmax range
    (r"the components are strictly confined to $[0,1]$ and sum to exactly $1$",
     r"the components are strictly confined to $(0,1)$ and sum to exactly $1$", 1),
]

E['appendix/additional_result_visualizations.tex'] = [
    # 30 dangling k
    (r"In the CE plots, marker area increases with the number of concepts contributing to the question-level mean, and $k$ in the caption denotes the range of this number.",
     r"In the CE plots, marker area increases with the number of concepts contributing to the question-level mean.", 1),
]


def sym_line(template, sym, desc):
    # reuse the column widths of an existing row
    amp = template.index('&')
    w1 = amp - 1
    w2 = len(template.rstrip('\n')) - 2 - (amp + 2)
    return '\t' + sym.ljust(w1) + '& ' + desc.ljust(w2) + '\\\\\n'


def edit_symbols(text):
    lines = text.splitlines(keepends=True)
    out = []
    hits = {'E': 0, 'Cm': 0}
    for ln in lines:
        s = ln.strip()
        # 22 expectation entry
        if s.startswith(r'$\mathbb{E}_{\mathcal{E}}[\,\cdot\mid\cdot\,]$') and 'differences between these expectations define the direct and joint causal effects.' in s:
            hits['E'] += 1
            out.append(sym_line(ln, r'$\mathbb{E}_{\mathcal{E}}[\,\cdot\mid\cdot\,]$',
                                r"Expected value of the model's answer variable $Y$ over its stochasticity $\mathcal{E}$, conditional on the stated intervention, used to specify the interventional answer distributions conceptually."))
            continue
        out.append(ln)
        # 26 set of alternative values
        if s.startswith(r'$\mathbb{C}_m$') and 'Domain of plausible values of concept $C_m$.' in s:
            hits['Cm'] += 1
            out.append(sym_line(ln, r"$\mathbb{C}'_m$", r"Set of alternative values of concept $C_m$ for counterfactuals, which excludes the original value $c_m$."))
    assert all(v == 1 for v in hits.values()), hits
    assert sum(1 for l in lines if l.strip().startswith(r"$\mathbb{C}'_m$")) == 0, 'C prime entry exists'
    return ''.join(out)


errors = []
new_texts = {}
for path, reps in E.items():
    p = os.path.join(root, path)
    t = open(p, encoding='utf-8').read()
    for old, new, n in reps:
        c = t.count(old)
        if c != n:
            errors.append(f'{path}: expected {n}, found {c}: {old[:80]}')
            continue
        t = t.replace(old, new)
    new_texts[path] = t

p = os.path.join(root, 'list_of_symbols.tex')
try:
    new_texts['list_of_symbols.tex'] = edit_symbols(open(p, encoding='utf-8').read())
except AssertionError as e:
    errors.append(f'list_of_symbols.tex: {e}')

if errors:
    print('ABORT, nothing written')
    print('\n'.join(errors))
    sys.exit(1)

for path, t in new_texts.items():
    with open(os.path.join(root, path), 'w', encoding='utf-8') as f:
        f.write(t)
print('OK, wrote', len(new_texts), 'files')

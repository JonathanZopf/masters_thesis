import sys, os

root = sys.argv[1]

E = {}  # path -> list of (old, new, expected_count)

E['chapters/modeling.tex'] = [
    # 13 bound brackets
    (r"\sum_{i=1}^{\lceil M/n_{\max} \rceil} 2^{\min(n_{\max},\, M - (i-1)n_{\max})} - 1.",
     r"\sum_{i=1}^{\lceil M/n_{\max} \rceil} \left(2^{\min(n_{\max},\, M - (i-1)n_{\max})} - 1\right).", 1),
    # 3 disjointness
    (r"s_i\cap s_j=\emptyset\ \text{for all }s_i,s_j\in\mathbf{S},",
     r"s_i\cap s_j=\emptyset\ \text{for all }s_i,s_j\in\mathbf{S}\text{ with }s_i\neq s_j,", 1),
    # 18 n -> |Z|
    (r"\left( \sum_{a=1}^{R_i} O_{a,v} \right)}{n},",
     r"\left( \sum_{a=1}^{R_i} O_{a,v} \right)}{|Z|},", 1),
    (r"where $n:=\sum_{u=1}^{R_i}\sum_{v=1}^{R_j}O_{u,v}$ denotes the number of rows represented in the contingency table. Under the completeness assumption stated above, both concept columns contain a value in every row, so $n$ equals the total number of rows in the dataset.",
     r"where $|Z|$ is the number of rows in the dataset. Under the completeness assumption stated above, both concept columns contain a value in every row, so $|Z|$ also equals the total count $\sum_{u=1}^{R_i}\sum_{v=1}^{R_j}O_{u,v}$ of the contingency table.", 1),
    (r"\sqrt{\frac{\chi^2}{n \cdot (\min(R_i, R_j) - 1)}}",
     r"\sqrt{\frac{\chi^2}{|Z| \cdot (\min(R_i, R_j) - 1)}}", 1),
    # 2, 4, 6 helper: new label, f_x, n_max
    ("\t\\label{eq:new_ce_vector}\n\tf_{\\mathbf{C}}(C_m) = s \\in \\mathcal{O}(\\mathbf{x}, \\mathbf{C}, 5) \\quad",
     "\t\\label{eq:group_lookup}\n\tf_{\\mathbf{x}}(C_m) = s \\in \\mathcal{O}(\\mathbf{x}, \\mathbf{C}, n_{\\max}) \\quad", 1),
    (r"Depending on the experimental setting, the value for $n_{\max}$ (currently set to 5) can be hardcoded to another value.",
     r"Keeping $n_{\max}$ fixed per experimental setting, instead of passing it as an argument, leaves the signature $\mathbf{CE}(\mathbf{x},\mathbf{C})$ of the CE vector identical to that of the original metric.", 1),
    ("\t\\mathbf{CE}(\\mathbf{x}, \\mathbf{C}) = \\Big( \\mathrm{CE}\\big(\\mathbf{x}, C_m, f_{\\mathbf{C}}(C_m)\\big) \\Big)",
     "\t\\label{eq:new_ce_vector}\n\t\\mathbf{CE}(\\mathbf{x}, \\mathbf{C}) = \\Big( \\mathrm{CE}\\big(\\mathbf{x}, C_m, f_{\\mathbf{x}}(C_m)\\big) \\Big)", 1),
]

E['chapters/evaluation.tex'] = [
    # 5, 6 partition name and helper reference
    ("For the joint run, let $\\mathbf{S}_{\\mathbf{x}}$ be the fixed oracle partition used for question $\\mathbf{x}$, and define\n"
     "\\begin{equation}\n"
     "\t\\label{eq:evaluation_group_lookup}\n"
     "\tf_{\\mathbf{x}}(C_m) := \\text{the unique }s\\in\\mathbf{S}_{\\mathbf{x}}\\text{ such that }C_m\\in s.\n"
     "\\end{equation}\n"
     "This helper retrieves an existing group; it does not query the oracle again. Using",
     "For the joint run, the oracle partition $\\mathbf{S}(\\mathbf{x})$ of each question $\\mathbf{x}$ is fixed. The helper $f_{\\mathbf{x}}(C_m)$ from Equation~\\ref{eq:group_lookup} returns the group of $C_m$ in this fixed partition and does not query the oracle again. Using", 1),
    (r"uses the oracle partition $\mathbf{S}_{\mathbf{x}}$.",
     r"uses the oracle partition $\mathbf{S}(\mathbf{x})$.", 1),
    # 14 plain r
    (r"\noindent\textbf{Decision criterion.} Denoting the resulting Pearson correlation coefficient by $r_{\Delta}$, the hypothesis is considered supported for a given dataset and model if $r_{\Delta} \ge 0.10$ and $p \le 0.10$.",
     r"\noindent\textbf{Decision criterion.} The hypothesis is considered supported for a given dataset and model if the resulting Pearson correlation coefficient satisfies $r \ge 0.10$ and $p \le 0.10$.", 1),
    # 12 nu
    (r"with $\eta_{\mathrm{tol}} = 10^{-8}$ is", r"with $\nu = 10^{-8}$ is", 1),
    (r"+\eta_{\mathrm{tol}}},", r"+\nu},", 1),
    # 5, 6 in RQ3
    (r"let $s=f_{\mathbf{x}}(C_m)\in\mathbf{S}_{\mathbf{x}}$ be the group assigned to $C_m$ in the fixed partition for question $\mathbf{x}$, using the lookup defined in Equation~\ref{eq:evaluation_group_lookup}.",
     r"let $s=f_{\mathbf{x}}(C_m)\in\mathbf{S}(\mathbf{x})$ be the group assigned to $C_m$ in the fixed partition for question $\mathbf{x}$, using the lookup defined in Equation~\ref{eq:group_lookup}.", 1),
    # 7 CE_raw points to eq:new_ce
    ("\t\\mathrm{CE}_{\\mathrm{raw}}(\\mathbf{x},C_m,s) := \\phi_m(v_{\\mathbf{x}}),\n"
     "\\end{equation}\n"
     "passing the question-specific unadjusted value function $v_{\\mathbf{x}}$ into $\\phi_m$ with player set $s$, which corresponds to the Shapley formulation of Equation~\\ref{eq:shapley}.",
     "\t\\mathrm{CE}_{\\mathrm{raw}}(\\mathbf{x},C_m,s) := \\mathrm{CE}(\\mathbf{x},C_m,s),\n"
     "\\end{equation}\n"
     "the unadjusted Shapley effect of Equation~\\ref{eq:new_ce}, which applies the Shapley formulation of Equation~\\ref{eq:shapley} to the question-specific value function $v_{\\mathbf{x}}$ with player set $s$.", 1),
]

E['results/rq2.tex'] = [
    (r"to be below $\alpha=0.05$.}", r"to be below $0.05$.}", 1),
    (r"At the nominal $\alpha=0.05$ level", r"At the nominal $0.05$ level", 1),
]
E['results/rq4.tex'] = [
    (r"At the nominal $\alpha=0.05$ level", r"At the nominal $0.05$ level", 1),
]

E['results/rq5.tex'] = [
    (r"The shift is defined as $\Delta\mathrm{CE}=\mathrm{CE}_{\mathrm{joint}}-\mathrm{CE}_{\mathrm{atomic}}$.",
     r"The shift is defined as $\mathrm{CE}_{\mathrm{joint}}-\mathrm{CE}_{\mathrm{atomic}}$.", 1),
    (r"column name={\textbf{$\Delta$CE}}", r"column name={\textbf{Shift}}", 2),
    (r"under Mistral Medium 3.5 ($\Delta\mathrm{CE}=0.070$)", r"under Mistral Medium 3.5 ($0.070$)", 1),
    (r"the largest negative shift ($\Delta\mathrm{CE}=-0.148$)", r"the largest negative shift ($-0.148$)", 1),
    (r"The intervals are 90\% credible intervals and $\Delta\mathcal{F}=\mathcal{F}_{\mathrm{joint}}-\mathcal{F}_{\mathrm{atomic}}$.",
     r"The intervals are 90\% credible intervals, and the shift is $\mathcal{F}_{\mathrm{joint}}-\mathcal{F}_{\mathrm{atomic}}$.", 1),
    (r"column name={\textbf{$\Delta\mathcal{F}$}}", r"column name={\textbf{Shift}}", 1),
]

E['results/examples.tex'] = [
    (r"v_{\mathbf{x},\mathrm{adj}}(T)", r"v_{\mathrm{adj},\mathbf{x}}(T)", 1),
    (r"using a payout reference coefficient of $0.904$", r"using a reference coefficient $\bar\gamma$ of $0.904$", 1),
]

E['appendix/oracle_partition_details.tex'] = [
    (r"\textbf{Node 1} & \textbf{Node 2} & \textbf{$V$}\\", r"\textbf{Node 1} & \textbf{Node 2} & \textbf{$A$}\\", 2),
]

E['graphs/results/appendix_rq3_credit_concept_delta.tex'] = [
    (r"xlabel={$\overline{\Delta\mathrm{CE}}=\overline{\mathrm{CE}_{\mathrm{adjusted}}-\mathrm{CE}_{\mathrm{raw}}}$}",
     r"xlabel={$\overline{\mathrm{CE}_{\mathrm{adj}}-\mathrm{CE}_{\mathrm{raw}}}$}", 1),
]
E['graphs/results/appendix_rq3_normalization_identity.tex'] = [
    (r"ylabel={$\mathrm{CE}_{\mathrm{adjusted}}$}", r"ylabel={$\mathrm{CE}_{\mathrm{adj}}$}", 1),
]
E['graphs/results/shared_scatter_plot.tex'] = [
    (r"y label={$\mathcal{F}_{\mathrm{FELICS},\,n_{\max}=1}(\mathbf{x})$}",
     r"y label={$\mathcal{F}_{\mathrm{singleton}}(\mathbf{x})$}", 1),
]
E['graphs/results/appendix_rq2_ce_identity.tex'] = [
    (r"y label={$\overline{\mathrm{CE}}_{\mathrm{FELICS},\,n_{\max}=1}(\mathbf{x})$}",
     r"y label={$\overline{\mathrm{CE}}_{\mathrm{singleton}}(\mathbf{x})$}", 1),
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
    hits = {'r_delta': 0, 't': 0, 'eta_tol': 0, 'Sx': 0, 'Z': 0}
    for ln in lines:
        s = ln.strip()
        if s.startswith(r'$r_{\Delta}$'):
            hits['r_delta'] += 1
            continue
        if s.startswith('$t$') and 'Test statistic of the paired $t$-test' in s:
            hits['t'] += 1
            continue
        if s.startswith(r'$\eta_{\mathrm{tol}}$'):
            hits['eta_tol'] += 1
            out.append(sym_line(ln, r'$\nu$', r'Small constant added to the denominator of $d_{\mathrm{CE}}$ to avoid division by zero.'))
            continue
        if s.startswith('$Z$') and 'Continuous feature vector prior to discretization by the tabular oracle.' in s:
            hits['Z'] += 1
            out.append(sym_line(ln, '$Z$', r'Continuous feature vector prior to discretization by the tabular oracle, whose length $|Z|$ equals the number of dataset rows.'))
            continue
        out.append(ln)
        if s.startswith(r'$\mathbf{S}(\mathbf{x})$'):
            hits['Sx'] += 1
            out.append(sym_line(ln, r'$f_{\mathbf{x}}(C_m)$', r'Candidate interaction group in $\mathbf{S}(\mathbf{x})$ that contains concept $C_m$.'))
    assert all(v == 1 for v in hits.values()), hits
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

"""
Process-noise sweep analysis. Fixed seed, varying q.
Reads sweep_q.csv and plots each metric vs q for the three trackers.
Run:  python analysis_sweep.py
"""
import pandas as pd, numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('sweep_q.csv').sort_values('q').reset_index(drop=True)

# RF-DOA absent -> real completeness = 0 (other RF-DOA metrics stay NaN)
df.loc[df.rfdoa_ntracks == 0, 'T2_compl'] = 0.0

qs = df['q'].values
METRICS = [
    ('ospa2d', 'OSPA 2D [m]',          'lower'),
    ('compl',  'Completeness',         'higher'),
    ('spur',   'Spuriousness',         'lower'),
    ('pa2d',   'Pos. Accuracy 2D [m]', 'lower'),
    ('t2t',    'Track-to-Truth ratio', '~1'),
]
TRACKERS = [('T1', 'Radar', 'tab:blue'),
            ('T2', 'RF-DOA', 'tab:orange'),
            ('Tf', 'Fusion', 'tab:green')]

fig, axes = plt.subplots(2, 3, figsize=(16, 9))
axes = axes.ravel()
for ax, (suf, name, better) in zip(axes, METRICS):
    for pre, lab, col in TRACKERS:
        c = f'{pre}_{suf}'
        if c in df.columns:
            ax.plot(qs, df[c].values, marker='o', color=col, label=lab)
    ax.set_xscale('log')
    ax.set_xlabel('q (process-noise coefficient)')
    ax.set_ylabel(name)
    ax.set_title(f'{name}  (better: {better})', fontsize=10)
    ax.grid(alpha=0.3, which='both')
    ax.legend(fontsize=8)
axes[-1].axis('off')
fig.suptitle(f'Process-noise sweep (seed {int(df.seed.iloc[0])}) - metrics vs q', fontsize=14)
plt.tight_layout()
plt.savefig('sweep_metrics.png', dpi=150, bbox_inches='tight')
plt.close()

print("OSPA 2D vs q:")
print(df[['q','T1_ospa2d','T2_ospa2d','Tf_ospa2d']].round(2).to_string(index=False))
print("\nOptimal q per tracker (minimum OSPA 2D):")
for pre, lab, _ in TRACKERS:
    c = f'{pre}_ospa2d'
    s = df[[ 'q', c]].dropna()
    qopt = s.loc[s[c].idxmin(), 'q']
    print(f"  {lab}: q = {qopt}  (OSPA = {s[c].min():.2f})")
print("\nSaved: sweep_metrics.png")

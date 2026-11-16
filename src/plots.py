import argparse
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .analyze import read
from .config import *

def main():
    p=argparse.ArgumentParser();p.add_argument('--out-dir',default='figures');a=p.parse_args();out=Path(a.out_dir);out.mkdir(parents=True,exist_ok=True)
    rows=read('data/summary/results.csv')
    def plot(series,title,path):
        fig,ax=plt.subplots(figsize=(8,5))
        for label,data in series:
            ax.plot([int(r['n']) for r in data],[float(r['average_ms']) for r in data],'o-',label=label)
        ax.set(xlabel='Input size n',ylabel='Mean time (ms; per search for binary)',title=title)
        ax.grid(alpha=.3);ax.legend();fig.tight_layout();fig.savefig(out/path,dpi=160);plt.close(fig)
    for name,case in zip(NAMES,PRIMARY):
        plot([(case,[r for r in rows if r['algorithm']==name and r['case']==case])],name.replace('_',' ').title(),f'{name}_{case}.png')
        cases=sorted({r['case'] for r in rows if r['algorithm']==name})
        if len(cases)>1:plot([(c,[r for r in rows if r['algorithm']==name and r['case']==c]) for c in cases],name+' case comparison',f'{name}_cases.png')
    plot([(n,[r for r in rows if r['algorithm']==n and r['case']=='random']) for n in NAMES[:3]],'Sorting identical random arrays','sorting_comparison.png')
    print('Figures generated')
if __name__=='__main__':main()

import csv,math,statistics,argparse
from pathlib import Path
from .config import *

def read(path):
    with Path(path).open(newline='') as f:return list(csv.DictReader(f))

def aggregate(rows,full=True):
    groups={}
    for r in rows:
        key=(r['algorithm'],r['case'],int(r['n']))
        assert r['valid']=='True' and int(r['elapsed_total_ns'])>0
        calls=int(r['batch_calls']);assert calls>0 and (calls>1 if r['algorithm']=='binary_search' else calls==1)
        assert math.isclose(float(r['elapsed_per_call_ms']),int(r['elapsed_total_ns'])/1e6/calls,rel_tol=1e-12)
        groups.setdefault(key,[]).append(r)
    if full:
        expected=set()
        for idx,name in enumerate(NAMES):
            cases=['random','sorted','reverse_sorted'] if idx<3 else (['present_mid','present_last','absent'] if idx==3 else ['random_unsorted'])
            for case in cases:
                sizes=(SORT_SIZES if case=='random' else SUPPLEMENTAL_SIZES) if idx<3 else BINARY_SIZES
                expected.update((name,case,n) for n in sizes)
        assert set(groups)==expected,'Missing or unexpected experiment groups'
    result=[];previous={}
    for (name,case,n),runs in sorted(groups.items()):
        runs.sort(key=lambda r:int(r['run_number']));assert [int(r['run_number']) for r in runs]==[1,2,3]
        assert len({r['batch_calls'] for r in runs})==1
        vals=[float(r['elapsed_per_call_ms']) for r in runs];assert all(math.isfinite(x) and x>0 for x in vals)
        avg=statistics.mean(vals);key=(name,case);ratio=''
        if key in previous:
            pn,pt=previous[key];assert n==2*pn;ratio=avg/pt
        previous[key]=(n,avg);r=runs[0]
        complexity='O(n log n)' if name in ['merge_sort','activity_selection'] else ('O(1)' if case=='present_mid' else 'O(log n)' if name=='binary_search' else 'O(n)' if case=='sorted' else 'O(n^2)')
        result.append(dict(algorithm_id=r['algorithm_id'],algorithm=name,group=r['group'],case=case,n=n,run1_ms=vals[0],run2_ms=vals[1],run3_ms=vals[2],average_ms=avg,stddev_ms=statistics.stdev(vals),ratio_to_previous_size=ratio,batch_calls=r['batch_calls'],expected_complexity=complexity))
    return result

def main():
    p=argparse.ArgumentParser();p.add_argument('--input',default='data/raw/measurements.csv');p.add_argument('--out-dir',default='data/summary');a=p.parse_args()
    rows=aggregate(read(a.input));out=Path(a.out_dir);out.mkdir(parents=True,exist_ok=True)
    with (out/'results.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    print(f'Validated {len(rows)} summary groups')
if __name__=='__main__':main()

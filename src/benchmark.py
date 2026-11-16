import argparse,csv,json,platform,subprocess,time
from pathlib import Path
from datetime import datetime,timezone
from . import algorithms as alg
from .config import *
from .cases import numbers,activities,feasible
FIELDS='algorithm_id algorithm group case n run_number seed batch_calls elapsed_total_ns elapsed_per_call_ms valid notes'.split()

def batch(a,target,count):
    checksum=0
    for _ in range(count):checksum+=alg.binary_search(a,target)
    return checksum

def main():
    p=argparse.ArgumentParser(description='Deterministic local algorithm timings')
    g=p.add_mutually_exclusive_group();g.add_argument('--smoke',action='store_true');g.add_argument('--all',action='store_true');g.add_argument('--main-only',action='store_true')
    p.add_argument('--seed',type=int,default=SEED);p.add_argument('--out-dir',type=Path)
    args=p.parse_args();out=args.out_dir or Path('data/smoke' if args.smoke else 'data/raw');out.mkdir(parents=True,exist_ok=True)
    # Calibrate outside recorded trials, using the fastest case so all batches resolve well.
    calls=1024;a=list(range(16000));target=a[7999]
    while True:
        start=time.perf_counter_ns();batch(a,target,calls);elapsed=time.perf_counter_ns()-start
        if elapsed>=100000000 or calls>=4194304:break
        calls*=2
    rows=[]
    for idx,name in enumerate(NAMES):
        cases=['random'] if idx<3 else (['present_mid','present_last','absent'] if idx==3 else ['random_unsorted'])
        if idx<3 and not args.main_only:cases+=['sorted','reverse_sorted']
        for case in cases:
            sizes=(SORT_SIZES if case=='random' else SUPPLEMENTAL_SIZES) if idx<3 else BINARY_SIZES
            if args.smoke:sizes=[8,16,32,64,128]
            for n in sizes:
                for run in range(1,RUNS+1):
                    fn=getattr(alg,name);count=1
                    if idx<3:
                        baseline=numbers(n,run,args.seed)
                        if case!='random':baseline=tuple(sorted(baseline,reverse=case=='reverse_sorted'))
                        expected=sorted(baseline);assert fn(list(baseline))==expected
                        values=list(baseline)
                        start=time.perf_counter_ns();result=fn(values);elapsed=time.perf_counter_ns()-start
                        assert result==expected
                    elif idx==3:
                        values=list(range(n));target=values[(n-1)//2] if case=='present_mid' else (n-1 if case=='present_last' else n)
                        expected=target if target<n else -1;assert fn(values,target)==expected
                        count=calls
                        start=time.perf_counter_ns();result=batch(values,target,count);elapsed=time.perf_counter_ns()-start
                        assert result==expected*count
                    else:
                        values=activities(n,run,args.seed);original=values[:];check=fn(values)
                        assert feasible(check) and all(x in values for x in check) and values==original
                        start=time.perf_counter_ns();result=fn(values);elapsed=time.perf_counter_ns()-start
                        assert result==check and values==original
                    assert elapsed>0
                    rows.append(dict(zip(FIELDS,[f'A{idx+1}',name,GROUPS[idx],case,n,run,args.seed,count,elapsed,elapsed/1e6/count,True,'common binary loop/checksum overhead included' if idx==3 else ''])))
                print(name,case,n,flush=True)
    dest=out/'measurements.csv';tmp=dest.with_suffix('.tmp')
    with tmp.open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(rows)
    tmp.replace(dest)
    import matplotlib,pytest
    try:commit=subprocess.check_output(['git','rev-parse','HEAD'],stderr=subprocess.DEVNULL,text=True).strip()
    except (OSError,subprocess.CalledProcessError):commit=None
    env=dict(python_version=platform.python_version(),matplotlib_version=matplotlib.__version__,pytest_version=pytest.__version__,os=platform.platform(),cpu=platform.processor() or 'Not recorded',architecture=platform.machine(),editor='Not recorded; Python CLI used',seed=args.seed,timestamp_utc=datetime.now(timezone.utc).isoformat(),run_count=RUNS,timer='perf_counter_ns',timer_resolution=time.get_clock_info('perf_counter').resolution,git_commit=commit,source_file='plan.md; original PDF unavailable',batch_calls=calls,data_sizes=dict(sort=SORT_SIZES,supplemental=SUPPLEMENTAL_SIZES,binary=BINARY_SIZES,activity=ACTIVITY_SIZES),notes='Local CLI; power mode and background load not controlled. No overhead subtraction.')
    (out/'environment.json').write_text(json.dumps(env,indent=2))
    if not args.smoke:Path('report/environment.json').write_text(json.dumps(env,indent=2))
    print(f'Validated {len(rows)} measured records -> {dest}')
if __name__=='__main__':main()

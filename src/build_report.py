import argparse,json,re,statistics
from pathlib import Path
from .analyze import read,aggregate
from .config import *

PSEUDO=["for end from n-1 down to 1: swapped=false; compare adjacent pairs up to end; swap inverted pairs and set swapped; break if no swap; return A", "for i from 1 to n-1: save key=A[i]; shift larger prefix entries right; insert key at its position; return A", "if n<=1 return A; recursively sort both halves; merge by taking smaller head (left on ties); copy merged sequence into A; return A", "low=0; high=n-1; while low<=high: mid=low+(high-low)//2; return mid on equality; otherwise discard half by updating low or high; return -1", "sort by (finish,start,id); last=-infinity; for each activity: if start>=last, select it and set last=finish; return selected"]
THEORY=["Best O(n); average/worst O(n^2); O(1) auxiliary space. Early exit detects sorted input. Strict swaps preserve stability. Each pass fixes the largest remaining item.", "Best O(n); average/worst O(n^2); O(1) auxiliary space. Strict shifts preserve stability. The sorted prefix grows by one each pass.", "Best/average/worst O(n log n); O(n) auxiliary space plus O(log n) recursion depth. Balanced splitting and linear stable merging preserve order.", "Sorted input is required. Best O(1), average/worst O(log n); O(1) space. Each unsuccessful iteration discards half the candidate interval without discarding a possible match.", "Unsorted input has O(n log n) worst-case total time, including sorting, then O(n) scan; O(n) space. Python's adaptive sort can be linear on ordered input; random unsorted inputs have expected O(n log n) sorting work. Replacing the first activity of an optimum with an earliest-finishing activity leaves at least as much room for the rest, proving the greedy choice by induction."]
CORRECT=["Boundary, negative, duplicate, ascending, descending and seeded random arrays match the independent sorted oracle; identity and stability are tested."]*3+["All targets across seeded sorted arrays, duplicates, empty inputs and out-of-range misses are checked; input preservation is tested.","Empty/singleton, ties, touching boundaries, overlapping and disjoint sets pass. Exhaustive subset enumeration independently checks optimal counts for small seeded cases; membership, non-overlap, unique IDs and input preservation are checked."]

def table(rows):
    s='| Input size n | Run 1 (ms) | Run 2 (ms) | Run 3 (ms) | Average (ms) | T(2n)/T(n) |\n|---:|---:|---:|---:|---:|---:|\n'
    for r in rows:
        vals=[str(r['n'])]+[f"{float(r[k]):.9f}" for k in ['run1_ms','run2_ms','run3_ms','average_ms']]+[f"{float(r['ratio_to_previous_size']):.4f}" if r['ratio_to_previous_size']!='' else '?']
        s+='| '+' | '.join(vals)+' |\n'
    return s

def main():
    p=argparse.ArgumentParser();p.add_argument('--out-dir',default='report');a=p.parse_args()
    calculated=aggregate(read('data/raw/measurements.csv'));rows=read('data/summary/results.csv')
    assert len(rows)==len(calculated)
    for actual,expected in zip(rows,calculated):
        for key,value in expected.items():assert str(value)==actual[key],f'Stale summary: {key}'
    env=json.loads(Path('report/environment.json').read_text());student=json.loads(Path('report/student_info.json').read_text())
    v={k:student.get(k) or '________ (not supplied)' for k in ['STUDENT_NAME','ENROLLMENT_NUMBER','SEMESTER_SECTION','ACTUAL_SUBMISSION_DATE']}
    for key,field in dict(PYTHON_VERSION='python_version',EDITOR_AND_VERSION='editor',MATPLOTLIB_VERSION='matplotlib_version',PYTEST_VERSION='pytest_version',OS_VERSION='os',CPU_INFO='cpu',BENCHMARK_DATE='timestamp_utc',SEED='seed',GIT_COMMIT_OR_NOT_AVAILABLE='git_commit').items():v[key]=str(env.get(field) or 'Not available')
    v['METHODOLOGY_AND_LIMITATIONS']=f"Three trials per condition; deterministic seed {env['seed']}. Integer sorting inputs are generated uniformly from [-n,10n); identical baseline tuples are copied outside timing for each algorithm. Supplemental cases sort/reverse the same seeded values. All sorting functions mutate their supplied copy. Activities use random starts in [-n,10n) and positive durations 1..100. Sorting activities by finish time is included. Reference validation precedes timing; output checks follow it. Timer: perf_counter_ns; resolution {env['timer_resolution']} seconds. Binary input is range(n); present_mid matches the initial midpoint, present_last targets n-1 and absent targets n. A common calibrated batch of {env['batch_calls']} calls is used; totals are divided by calls. Every result enters a checksum checked afterward. Loop/checksum overhead is included without subtraction. Calibration is excluded. No explicit warmup beyond prevalidation. Arithmetic means and sample SD are computed from raw records. Ratios compare each row to the preceding half-size row. OS scheduling, background load, caches, Python overhead and uncontrolled power mode can affect results; three trials do not establish statistical significance. The original assignment PDF was unavailable; source alignment follows plan.md. Identity and actual submission date remain deliberately blank. Experiment date is distinct from the source's printed 15 November 2026 deadline."
    growth=[]
    for idx,(name,case) in enumerate(zip(NAMES,PRIMARY),1):
        group=[r for r in rows if r['algorithm']==name and r['case']==case];ratios=[float(r['ratio_to_previous_size']) for r in group[1:]]
        prefix=f'A{idx}_';v[prefix+'PSEUDOCODE']='```text\n'+PSEUDO[idx-1]+'\n```';v[prefix+'THEORY_COMPLEXITY']=THEORY[idx-1];v[prefix+'CORRECTNESS_SUMMARY']=CORRECT[idx-1]
        v[prefix+'PRIMARY_TABLE']=table(group);v[prefix+'PRIMARY_PLOT']=f'![{name} {case}](../figures/{name}_{case}.png)'
        v[prefix+'PRIMARY_ANALYSIS']=f"Primary case: {case}. Mean time rises from {float(group[0]['average_ms']):.9f} ms to {float(group[-1]['average_ms']):.9f} ms across the tested endpoints. Adjacent ratios span {min(ratios):.3f}?{max(ratios):.3f}. " + ("Quadratic growth suggests ratios near 4; constants differ because bubble swaps adjacent entries while insertion shifts entries." if idx<3 else "Linearithmic growth suggests ratios slightly above 2; allocation, adaptive sorting and interpreter costs can shift these." if idx in [3,5] else "These are amortized per-search times. Logarithmic growth predicts ratios close to 1, not 2; fixed batch-loop overhead can flatten the trend.")
        extra=[]
        for c in sorted({r['case'] for r in rows if r['algorithm']==name and r['case']!=case}):extra.append('### Supplemental '+c+'\n'+table([r for r in rows if r['algorithm']==name and r['case']==c]))
        v[prefix+'CASES_SUMMARY']='\n'.join(extra) or 'Full greedy sorting cost is included; no scan-only experiment was used.'
        if idx<=4:v[prefix+'CASES_SUMMARY']+=f'\n![Case comparison](../figures/{name}_cases.png)\n'+('Sorted bubble/insertion have linear fast paths; reverse input has quadratic work. Merge remains linearithmic across these cases.' if idx<4 and idx!=4 else 'The midpoint case has constant search work; endpoint and absent cases take logarithmically many iterations.')
        growth.append(f"| {name} | {group[0]['expected_complexity']} | {statistics.mean(ratios):.4f} |")
    compare='| n | Fastest | Ranking (fast to slow) | Bubble / Merge | Insertion / Merge |\n|---:|---|---|---:|---:|\n';winners=[]
    for n in SORT_SIZES:
        times={r['algorithm']:float(r['average_ms']) for r in rows if r['algorithm'] in NAMES[:3] and r['case']=='random' and int(r['n'])==n};order=sorted(times,key=times.get);winners.append(order[0]);compare+=f"| {n} | {order[0]} | {' < '.join(order)} | {times['bubble_sort']/times['merge_sort']:.3f} | {times['insertion_sort']/times['merge_sort']:.3f} |\n"
    v['SORTING_COMBINED_PLOT']='![Combined sorting](../figures/sorting_comparison.png)'
    v['SORTING_RANKING_AND_SPEEDUPS']=compare+'\nRatios divide the named numerator runtime by Merge Sort runtime; values above 1 mean Merge is faster.'
    v['SORTING_CROSSOVER_ANALYSIS']='No observed crossover in tested range.' if len(set(winners))==1 else 'The fastest algorithm changes across the tested sizes, as shown in the ranking table.'
    v['THEORY_VS_EMPIRICAL_TABLE']='| Algorithm | Primary expected time | Mean adjacent ratio |\n|---|---|---:|\n'+'\n'.join(growth)+'\nGuides: linear ~2, quadratic ~4, linearithmic slightly above 2, logarithmic and constant near 1. Finite measurements are consistent with or deviate from these guides; they do not prove asymptotic bounds.'
    v['FINAL_CONCLUSION_9_LINES']='\n'.join(f'{i}. {s}' for i,s in enumerate([f"At the largest tested sorting input, {winners[-1]} was fastest.",v['SORTING_CROSSOVER_ANALYSIS'],'Bubble and insertion perform the same task but incur different operation costs.','The supplemental sorted inputs exercise the early-exit and no-shift paths.','Merge uses additional memory to avoid quadratic merging work.','Binary search timings are per call, normalized from checksum-consuming batches.','Activity selection measurements include the prerequisite ordering step.','Measured doubling ratios reflect finite sizes and platform noise as well as growth.','The raw records, deterministic inputs and regeneration commands support independent reproduction.'],1))
    v['RUN_COMMANDS']='See [README](../README.md) for complete commands and [raw measurements](../data/raw/measurements.csv). Source: supplied plan.md, transcribing DAA_Assignment_Dr_Jyoti_Kaushik.pdf (PDF not available for independent review). No repository has been published.'
    v['VALIDATION_CHECKLIST']='See [checks](checks.md) and [test output](../logs/validation.txt). Student identity and submission date must be completed before submission.'
    template=Path('report/report_template.md').read_text(encoding='utf-8')
    for k,value in v.items():template=template.replace('{{'+k+'}}',value)
    assert not re.search(r'\{\{|TODO|TBD',template)
    out=Path(a.out_dir);out.mkdir(parents=True,exist_ok=True)
    for link in re.findall(r'!\[[^]]*\]\(([^)]+)\)',template):assert (out/link).is_file()
    (out/'final_report.md').write_text(template,encoding='utf-8');print('Report generated from validated real measurements')
if __name__=='__main__':main()

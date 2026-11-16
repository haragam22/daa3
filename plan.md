# DAA Assignment — Complete Codex Implementation Plan

> **Status:** IMPLEMENTED / MEASUREMENTS GENERATED / IDENTITY METADATA OUTSTANDING  
> **Selected option:** C  
> **Assignment:** Implementation and Experimental Analysis of Algorithms using an Open-Source Tool  
> **Institution:** Maharaja Agrasen Institute of Technology (MAIT), Delhi, CSE  
> **Faculty:** Dr. Jyoti Kaushik  
> **Paper code:** CIC-311  
> **Source:** `DAA_Assignment_Dr_Jyoti_Kaushik.pdf` (two pages; supplied with this task)  
> **Submission date printed on source:** 15 November 2026 — this date has already passed as of plan preparation (17 November 2026); confirm any late-submission arrangements separately.  
> **Rule:** Never invent measurements, versions, generated paths, screenshots, experiment outcomes, or conclusions. Fill results only after actual, successfully validated runs.

---

## 0. Mission and non-negotiable acceptance criteria

Implement **five algorithms from at least three different groups** using free/open-source software; verify correctness; run systematic experiments; compare measured performance to theoretical asymptotic complexity; create visualizations and a polished report with genuine measurements.

### Selected algorithms — fixed decision

| ID | Algorithm | Assignment group | Key theoretical time complexities | Comparison role |
|---|---|---|---|---|
| A1 | Bubble Sort (standard adjacent swaps, early-exit flag) | Sorting | Best O(n), average O(n²), worst O(n²) | Same-array sorting comparison |
| A2 | Insertion Sort (shift-based implementation) | Sorting | Best O(n), average O(n²), worst O(n²) | Same-array sorting comparison |
| A3 | Merge Sort (handwritten, stable merge) | Sorting | Best/average/worst O(n log n) | Same-array sorting comparison |
| A4 | Binary Search (iterative, on sorted arrays) | Divide and Conquer | Best O(1), average/worst O(log n) | Logarithmic search behavior |
| A5 | Activity Selection (greedy earliest finishing time, including sorting) | Greedy method | O(n log n) total on unsorted activities; O(n) scan if pre-sorted | Greedy behavior |

**Source-aligned deliverables for EACH algorithm:** pseudocode; complexity discussion (best/average/worst when different); own implementation; correctness checks; at least five steadily increasing input sizes; at least three measurement runs per input; results table with `n`, `Run 1 (ms)`, `Run 2 (ms)`, `Run 3 (ms)`, `Average (ms)`, `T(2n)/T(n)`; plot of time against `n`; evidence-based analysis of observed vs theoretical growth. Additionally: at least one combined graph comparing >=2 algorithms solving the same problem; identify winner, size-dependent changes, and measured speedups; 8–10-line conclusion.

**Open-source-only:** Python 3, VS Code/VSCodium (use installed version if open-source licensing is a concern; report the actual chosen editor), pytest, Matplotlib, Git. Avoid MS Excel, MATLAB, proprietary timing packages. CSV + Markdown are preferred, with optional PDF exported via open-source tooling only. Record *real* tool versions using runtime commands.

### Definition of done

1. All five functions implemented from scratch (no calling built-in sort/search as the algorithm itself).
2. Automated unit and property-oriented tests pass; no mutation/data corruption; known boundary cases pass.
3. Experiments produce complete reproducible CSVs with **three or more** measured runs for **five or more** increasing input sizes for every algorithm.
4. All calculations, ratios, comparison graphs, report tables are generated directly from measurements rather than hand-entered.
5. One combined graph for A1, A2, A3 using **identical arrays and common input sizes**.
6. Final report contains theory, pseudocode, methodology, environmental versions, data tables, charts, discussion, conclusions and explicit limitations.
7. Source rubric mapped to checkboxes and checked; no `TODO`, `TBD`, `{{PLACEHOLDER}}`, invented data, or broken image paths remain in the final report.
8. Everything reproducible with documented shell commands on the user's machine; a finished `README.md` and explicit run log exist.

---

## 1. Engineering decisions (Codex must follow)

- **Language:** Python 3, using only the standard library for algorithms and the benchmark runner.
- **Environment:** Python `venv`; VS Code or VSCodium; CLI entrypoints and optionally Jupyter for exploration (not needed for final submission).
- **Graphing:** Matplotlib, open source, using noninteractive `Agg` backend for headless generation; CSV via `csv` from standard library; use `pytest` for tests.
- **Benchmark timer:** `time.perf_counter_ns()`. Convert elapsed nanoseconds to milliseconds: `elapsed_ms = elapsed_ns / 1_000_000`. This is the nanosecond-resolution counterpart to assignment's `time.perf_counter()`.
- **Benchmark location:** run **locally**, with no editor debugger, power saver, or competing heavy jobs. Avoid comparing different machines/modes.
- **Timing runs:** record at least **3 independent runs** per input size and case, and use the **arithmetic mean** in the required tables; optionally include sample SD as a supplemental metric.
- **Seed:** `20261117` or a centrally configurable seed in `config.py`; record it in methodology.
- **Reference tests:** built-in `sorted` is allowed only as a correctness oracle outside the timed implementation.
- **Scope:** exact five algorithms only. Don't add heap/quick sort as separate subjects, database, web UI, ML model, or unrelated complexity.
- **Case labels:** `random` for the main sorting comparison; separate `sorted` and `reverse_sorted` best-/worst-oriented cases. For binary search, separate `present_first` (best) and `present_last` / `absent` (typical logarithmic cases). For greedy, unsorted activities with a sorting step included in the timed function.
- **Data isolation:** generate the inputs **before** starting the timer; copy any mutable lists **outside** the timed region, for each run; do not count setup, input generation, graphing, assertions, print calls, or CSV writes in algorithm time.
- **Correctness timing separation:** validate test instance before benchmark runs; optional output verification after each timed run, never inside the timed region.
- **No falsely ideal scaling:** ratios are approximate and can deviate due to interpreter overhead, fixed costs, input distribution, caching, small times, branch prediction and operating-system noise. Discuss these honestly.

---

## 2. Exact experiment configurations

### 2.1 Sorting main comparison (A1, A2, A3)

Use the **same integer array values for all three sorting algorithms at each `n` and run**. These main-case sizes are chosen to avoid overly slow quadratic Python implementations:

```python
SORT_SIZES = [500, 1000, 2000, 4000, 8000]
SORT_RUNS = 3
SORT_DISTRIBUTION = 'random'  # reproducible integer values, e.g. 0..10*n
```

- Use one immutable baseline tuple of randomly generated integers for each `(n, run_index)` with deterministic RNG seeds.
- Each algorithm receives its own copy, copied **before** the timer. A standard copy is acceptable as long as its cost is excluded for all sorting algorithms.
- Implement a common interface: return a **new sorted list**; internal in-place sorting is permissible on a supplied copy. Do not mix copying inside one algorithm and outside another.
- Sorting must handle duplicates, negative numbers, empty/single-element arrays, and sorted/reverse-sorted arrays.
- Generate and plot a **single combined 3-line graph** of average elapsed milliseconds on common `SORT_SIZES`, in addition to three individual plots.
- Supplemental **best/worst-oriented cases**: use `[250, 500, 1000, 2000, 4000]`, three runs each for `sorted` and `reverse_sorted`. For bubble and insertion these are meaningful O(n) vs O(n²) patterns; Merge remains O(n log n) across all. If runtime is long, keep supplemental sizes smaller but still >=5 sizes in the main random condition.
- Note Bubble Sort with early exit is O(n) on already-sorted data; implementation MUST actually have early termination. For traditional reverse input, bubble and insertion require O(n²) work; Merge Sort remains O(n log n).
- Record data distribution and case in raw CSV. For sorted/reverse cases, use the same numbers as random datasets after sorting or reversing, so comparison is controlled.

### 2.2 Binary Search (A4)

```python
BINARY_SIZES = [1000, 2000, 4000, 8000, 16000]
BINARY_RUNS = 3
BINARY_CASES = ['present_first', 'present_last', 'absent']
```

- `array = list(range(n))` sorted ascending, using distinct integers.
- `present_first`: target `array[(n-1)//2]` to force an immediate match for the chosen midpoint convention; label **`present_mid`** in actual output to avoid misrepresenting it. Expected best O(1).
- `present_last`: target `array[-1]` (worst-ish ~log n; no guarantee of absolute maximum for every `n`).
- `absent`: target `n` (unsuccessful search, O(log n)).
- Validate presence/absence using indexing expectations, compare search result against a slow oracle on small test inputs; no `list.index()` in timed function.
- **Important tiny-time timing problem:** One Python binary search finishes in microseconds; measuring one isolated call yields noisy ratios. For each `(n, case, run)` do a batch of repeated calls with a fixed constant target, **time the whole batch**, and divide by call count. Calibrate batch size **outside** measurement (e.g. doubling until >=100 ms, with a reasonable safety cap), then keep that size consistent across the three trials for the same `(n, case)`. Better: for cross-size comparisons, choose one common batch count large enough to resolve the largest `n` at >=100ms, and use it for *all* binary sizes/cases when practical. Store `batch_calls` in raw and summary outputs.
- Avoid dead-code elimination concerns by consuming every result into a checksum **within** the repeated loop and verifying checksum afterward; clearly state this includes a tiny common loop/checksum overhead. Optionally estimate/subtract empty-loop overhead with an explicitly documented control benchmark, but do not quietly subtract or mix methods.
- Average per-call elapsed milliseconds: `total_batch_ms / batch_calls`. Always label timing as **amortized per search**; do not chart batch totals as single-call times. Never multiply/round until after computation; write 6–9 decimals where necessary to prevent displayed zero times.
- Because `log(2n)/log(n)` is close to 1, for O(log n) the predicted `T(2n)/T(n)` is close to **1**, not 2. For best-case O(1), the ratio also approaches 1. Slope and empirical iteration counts can reinforce claims. Record number of comparisons/iterations via a separate instrumented function or optional debug counter *outside* the primary timed algorithm.

### 2.3 Activity Selection (A5)

```python
ACTIVITY_SIZES = [1000, 2000, 4000, 8000, 16000]
ACTIVITY_RUNS = 3
ACTIVITY_CASE = 'random_unsorted'
```

- Generate `n` activities as `(start, finish, original_id)` tuples. Ensure `finish > start`; allow overlaps and identical finish times; use deterministic, non-pathological duration/start distribution.
- Algorithm sorts activities by `(finish, start, original_id)` and greedily takes each activity with `start >= last_finish` (back-to-back is compatible). Include the sorting step **inside** its measured function; expected total O(n log n).
- Output should be activity records (not just count), in selected order; verify every selected activity comes from the input, IDs are unique, and selected activities do not overlap.
- Validate greedy optimality by comparing **count** to brute force enumeration for small `n <= 12` only, across many random seeds. This expensive oracle MUST NOT run inside timing.
- Additional simple hand-designed cases: all non-overlapping -> select all; all overlapping -> select one (under suitable interval construction); ties in finish times; empty input; one item; activities that touch at boundaries.
- Optionally include a supplementary experiment with **pre-sorted** input and *scan-only* function to illustrate O(n), but do **not** replace the measured full greedy O(n log n) algorithm in the required report and do not count the scan-only function as a sixth assignment algorithm.

### 2.4 Ratios and case constraints

- `T(2n)/T(n)` requires adjacent measured sizes to exactly double. All main size arrays above satisfy this.
- First row's ratio is `—` because no `n/2` row exists. For each subsequent input size calculate `average_time_ms_at_n / average_time_ms_at_n_over_2` (equivalent to `T(2n)/T(n)` at the preceding n).
- Expected approximate ratios: O(n) ~2; O(n log n) a bit above 2; O(n²) ~4; O(n³) ~8; O(log n) ~1 (not a linear ratio); O(1) ~1. Note these are guides, not promises.
- If elapsed time is zero, invalid, overflowed, or a run failed: mark **INVALID** and rerun; do not silently replace with a fabricated number.
- If an experiment exceeds a reasonable threshold, do not silently omit rows or alter `SORT_SIZES`: record the runtime concern, adjust *explicitly* with explanation, rerun entire comparable group, and update plan/report documentation.

---

## 3. Proposed repository and file layout

```text
daa-algorithm-analysis/
├── plan.md                         # This Codex contract; track decisions/checkpoints
├── README.md                       # Setup, reproducibility, execution, evidence
├── requirements.txt                # pinned/compatible matplotlib, pytest; no proprietary deps
├── .gitignore                      # venv, caches, temp files
├── src/
│   ├── __init__.py
│   ├── algorithms.py               # Five algorithm functions ONLY
│   ├── cases.py                    # deterministic input generation + small oracles
│   ├── config.py                   # sizes, seed, cases, runs, paths
│   ├── benchmark.py                # timer + repeated runs + raw CSV
│   ├── analyze.py                  # aggregate, ratios, winner/speedups
│   ├── plots.py                    # individual + comparison plots
│   └── build_report.py             # populate generated report from outputs
├── tests/
│   ├── test_sorting.py
│   ├── test_binary_search.py
│   ├── test_activity_selection.py
│   ├── test_benchmark_contract.py
│   └── test_results_integrity.py
├── data/
│   ├── raw/                        # raw measurement CSVs, 1 record per timed run
│   └── summary/                    # aggregated per (algorithm, case, n)
├── figures/
│   ├── bubble_sort_random.png
│   ├── insertion_sort_random.png
│   ├── merge_sort_random.png
│   ├── binary_search_absent.png
│   ├── activity_selection_random_unsorted.png
│   ├── sorting_comparison.png
│   └── optional_cases/             # case comparison visualizations
├── report/
│   ├── report_template.md          # human-readable template with explicit placeholders
│   ├── final_report.md             # generated only after successful benchmarks
│   ├── environment.json            # actual versions/OS/CPU details where available
│   └── checks.md                   # completed rubric + limitations/evidence
└── logs/
    ├── validation.txt
    ├── benchmark_run.txt
    └── build_report.txt
```

**Important:** Create `report_template.md` before coding; preserve the template throughout the run. `final_report.md` must be generated only when all required data is present and validated. Append a timestamp and git commit hash to report reproducibility info when available; don't invent a hash.

### Suggested Python public interfaces

```python
def bubble_sort(values: list[int]) -> list[int]: ...
def insertion_sort(values: list[int]) -> list[int]: ...
def merge_sort(values: list[int]) -> list[int]: ...
def binary_search(sorted_values: list[int], target: int) -> int: ...
def activity_selection(activities: list[tuple[int, int, int]]) -> list[tuple[int, int, int]]: ...
```

- Sorting functions must not change the caller's list; they may copy internally if a uniform approach is used, but **timed setup must be consistent**. Preferred: functions work in-place on a passed pre-copied list and return it; tests document mutation expectations; wrappers outside the timer make copies. For clarity **choose one standard before coding**: *sorting functions take a mutable list, sort it in place, return that same list*. In that case the public names above fit and tests assert values and object identity; callers must copy before invocation.
- `binary_search`: returns index if target exists, else `-1`; duplicate handling need not specify first occurrence unless tests require it; distinct values used for benchmark.
- `activity_selection`: may sort its own shallow copy inside the timed call; this sort is part of the intended algorithm, not benchmark setup. Do not mutate original list.

---

## 4. Report template: required sections and exact placeholder contract

Codex must create a polished, consistent `report/report_template.md` with the following ordered sections. Use the literal placeholders until verified measurements exist; substitute automatically from computed artifacts, not by manual transcription.

### Cover/metadata

```markdown
# Implementation and Experimental Analysis of Algorithms Using an Open-Source Tool

**Institute:** Maharaja Agrasen Institute of Technology, Delhi  
**Department:** Computer Science & Engineering  
**Faculty:** Dr. Jyoti Kaushik  
**Paper Code:** CIC-311  
**Student Name:** {{STUDENT_NAME}}  
**Enrollment Number:** {{ENROLLMENT_NUMBER}}  
**Semester / Section:** {{SEMESTER_SECTION}}  
**Date Submitted:** {{ACTUAL_SUBMISSION_DATE}}  
**Language / Version:** {{PYTHON_VERSION}}  
**IDE / Version:** {{EDITOR_AND_VERSION}}  
**Timing:** time.perf_counter_ns()  
**Graphing / Version:** {{MATPLOTLIB_VERSION}}  
**Testing / Version:** {{PYTEST_VERSION}}
```

Do not guess student/semester/enrollment details; collect as config values or leave explicit blanks in a **draft**; final report gate requires user-supplied metadata or deliberately blank underscored fields clearly identified.

### Required report outline

1. **Objective** — same scope as assignment, own wording.
2. **Open-source tools and environment** — actual Python/editor/Matplotlib/pytest versions, operating system, hardware details if accessible, measurement clock and test execution date.
3. **Experimental methodology** — seeding, dataset creation, data distributions, correctness checks before timing, timer resolution, runs and averages, batching for binary search, ratio calculation, fairness and limitations.
4. **Algorithm A1: Bubble Sort** — idea, understandable pseudocode, best/average/worst complexity, correctness verification, five-size results table, individual graph, interpretation with ratio.
5. **Algorithm A2: Insertion Sort** — same fields.
6. **Algorithm A3: Merge Sort** — same fields.
7. **Algorithm A4: Binary Search** — same fields; clear sorted-input prerequisite, best O(1), worst O(log n); explain the repeated-call batching/per-search timings; show primary `absent` or `present_last` case and optional best case.
8. **Algorithm A5: Activity Selection** — same fields; earliest finishing time greedy rationale, sorting included in timed workload, O(n log n) total; selected activities correctness and optional brute-force optimality test.
9. **Combined sorting comparison** — combined graph; exact common input sizes; measured ranking, speedup factors and whether any winner crossover exists; if no crossover, explicitly say none was observed.
10. **Theoretical vs practical complexity** — concise cross-algorithm comparison table of expected growth, observed average ratios and caveats; do not compare absolute running times of unrelated tasks as if they solved the same problem.
11. **Conclusion** — exactly **8–10 meaningful lines** (prefer 9), directly grounded in observed data.
12. **Reproducibility instructions / references** — command list, source assignment, code repository (if actually published), library docs if cited.

### REQUIRED table format (repeat per algorithm)

| Input size n | Run 1 (ms) | Run 2 (ms) | Run 3 (ms) | Average (ms) | T(2n)/T(n) |
|---:|---:|---:|---:|---:|---:|
| {{N_1}} | {{RUN_1_1_MS}} | {{RUN_1_2_MS}} | {{RUN_1_3_MS}} | {{AVG_1_MS}} | — |
| {{N_2}} | {{RUN_2_1_MS}} | {{RUN_2_2_MS}} | {{RUN_2_3_MS}} | {{AVG_2_MS}} | {{RATIO_2}} |
| {{N_3}} | {{RUN_3_1_MS}} | {{RUN_3_2_MS}} | {{RUN_3_3_MS}} | {{AVG_3_MS}} | {{RATIO_3}} |
| {{N_4}} | {{RUN_4_1_MS}} | {{RUN_4_2_MS}} | {{RUN_4_3_MS}} | {{AVG_4_MS}} | {{RATIO_4}} |
| {{N_5}} | {{RUN_5_1_MS}} | {{RUN_5_2_MS}} | {{RUN_5_3_MS}} | {{AVG_5_MS}} | {{RATIO_5}} |

Above is a schematic table. Actual template should name placeholders by ID and case (`{{A1_RANDOM_TABLE}}`, `{{A1_RANDOM_PLOT}}`, etc.) and generate full Markdown tables programmatically to eliminate partial replacement errors.

### Fixed placeholders to implement in template

**Metadata**: `{{STUDENT_NAME}}`, `{{ENROLLMENT_NUMBER}}`, `{{SEMESTER_SECTION}}`, `{{ACTUAL_SUBMISSION_DATE}}`, `{{PYTHON_VERSION}}`, `{{EDITOR_AND_VERSION}}`, `{{MATPLOTLIB_VERSION}}`, `{{PYTEST_VERSION}}`, `{{OS_VERSION}}`, `{{CPU_INFO}}`, `{{BENCHMARK_DATE}}`, `{{SEED}}`, `{{GIT_COMMIT_OR_NOT_AVAILABLE}}`.

**Per algorithm `A1` through `A5`:** `{{A1_PSEUDOCODE}}`, `{{A1_THEORY_COMPLEXITY}}`, `{{A1_CORRECTNESS_SUMMARY}}`, `{{A1_PRIMARY_TABLE}}`, `{{A1_PRIMARY_PLOT}}`, `{{A1_PRIMARY_ANALYSIS}}`, and similarly for A2–A5. For alternative/best/worst tests `{{A1_CASES_SUMMARY}}` etc.

**Comparative/conclusion:** `{{SORTING_COMBINED_PLOT}}`, `{{SORTING_RANKING_AND_SPEEDUPS}}`, `{{SORTING_CROSSOVER_ANALYSIS}}`, `{{THEORY_VS_EMPIRICAL_TABLE}}`, `{{METHODOLOGY_AND_LIMITATIONS}}`, `{{FINAL_CONCLUSION_9_LINES}}`, `{{RUN_COMMANDS}}`, `{{VALIDATION_CHECKLIST}}`.

**Unfilled placeholders are intentionally valid in `report_template.md` only.** They are **fatal in `final_report.md`**. Do not produce a polished but ungrounded conclusion from sample values.

---

## 5. Raw data and calculations contract

### Raw CSV schema: `data/raw/measurements.csv`

One row per timed run:

```csv
algorithm_id,algorithm,group,case,n,run_number,seed,batch_calls,elapsed_total_ns,elapsed_per_call_ms,valid,notes
```

- For sorting and greedy `batch_calls=1` and `elapsed_per_call_ms=elapsed_total_ns/1e6`.
- For binary search `batch_calls>1` and `elapsed_per_call_ms=elapsed_total_ns/1e6/batch_calls`.
- Use full precision numeric values (no rounded strings in raw CSV), deterministic identifiers, consistent ordering.
- `valid` must truthfully reflect correctness and benchmarking completion; invalid rows cannot be summarized as successful.

### Summary CSV schema: `data/summary/results.csv`

```csv
algorithm_id,algorithm,group,case,n,run1_ms,run2_ms,run3_ms,average_ms,stddev_ms,ratio_to_previous_size,batch_calls,expected_complexity
```

- If an algorithm/case has more than 3 runs, preserve extra runs in raw CSV, use all successful runs for average, and display first three plus mean across all (explain if that happens). Preferred exactly 3 for neat report.
- Validate expected row counts: main random sorting 3 algorithms × 5 sizes × 3 runs = 45; binary cases 3 × 5 × 3 = 45; greedy main 1 × 5 × 3 = 15. **Main experiments total 105 raw timed rows**, excluding supplemental sort cases. Supplementary sorted and reverse-sorted (3 algorithms × 2 cases × 5 sizes × 3) add 90 rows for **195 rows** overall if all configurations run.
- For primary report use `random` for A1–A3, `absent` for A4, `random_unsorted` for A5. Extra case summaries/plots are supplemental.
- Verify summary averages directly recompute from raw CSV within a tight floating tolerance.
- Ratios use adjacent size doubling; first row blank/`—` in formatted report and blank in CSV (no NaN literal).
- Charts and report must read **summary files generated from raw data**, never directly edited constants.

### Reproducibility/benchmark metadata

Write JSON with keys similar to `python_version`, `matplotlib_version`, `pytest_version`, `os`, `architecture`, `cpu`, `seed`, `timestamp_utc`, `run_count`, `timer`, `data_sizes`, `git_commit` (nullable), `source_file`, `notes`. If exact CPU/editor information is not accessible, report `Not recorded` instead of guessing.

---

## 6. Pseudocode, theory, and correctness specifics

Each algorithm writeup must be independently understandable. Codex should implement these exact variations:

### A1 — Bubble Sort, early exit

```text
BUBBLE_SORT(A):
    for pass = 0 to length(A)-2:
        swapped = false
        for j = 0 to length(A)-pass-2:
            if A[j] > A[j+1]:
                swap A[j], A[j+1]
                swapped = true
        if swapped is false: break
    return A
```

Expected comparisons quadratic except fast-path sorted; stability if swapping only when `>`.

### A2 — Insertion Sort

```text
INSERTION_SORT(A):
    for i = 1 to length(A)-1:
        key = A[i]
        j = i-1
        while j >= 0 and A[j] > key:
            A[j+1] = A[j]
            j = j-1
        A[j+1] = key
    return A
```

Best linear when sorted; quadratic average/worst on typical unsorted/reverse input.

### A3 — Merge Sort

```text
MERGE_SORT(A):
    if length(A) <= 1: return A
    recursively sort left and right halves
    merge both halves in nondecreasing order
    copy merged values into A
    return A
```

Implement an unambiguous concrete split/merge with temp arrays or shared auxiliary storage. O(n log n) time; O(n) auxiliary memory, ignoring recursion stack; stable if ties select left first.

### A4 — Iterative Binary Search

```text
BINARY_SEARCH(A, target):
    low = 0; high = length(A)-1
    while low <= high:
        mid = low + (high-low)//2
        if A[mid] == target: return mid
        if A[mid] < target: low = mid+1
        else: high = mid-1
    return -1
```

Sorted input required. Best O(1); average/worst O(log n); O(1) auxiliary space.

### A5 — Earliest-finish Activity Selection

```text
ACTIVITY_SELECTION(activities):
    ordered = sort activities by (finish, start, original_id)
    selected = []
    last_finish = -infinity
    for activity in ordered:
        if activity.start >= last_finish:
            append activity to selected
            last_finish = activity.finish
    return selected
```

Activities have start < finish. Earliest finish greedy choice achieves maximum number of pairwise compatible activities for the standard unweighted problem. Unsorted input => sorting O(n log n), scan O(n), total O(n log n), O(n) space including output/order list.

---

## 7. Phase-by-phase implementation order and validation gates

**Codex execution policy:** Implement one phase at a time, run its test/gate, record pass/fail in `report/checks.md` or a dedicated checklist, fix defects before next phase. Never label a phase complete solely because files exist.

### Phase 0 — Repository initialization and source traceability

**Work:**
1. Create project folders above, `venv` instructions, `requirements.txt`, `.gitignore`, and initial `README.md`.
2. Copy this plan into project root; keep original PDF as separately supplied reference (do not assume it will be in Codex workspace). Record faculty, paper code and user-selected algorithms.
3. Detect Python, pip, Matplotlib, pytest, operating system, and editor version where possible. Use only installed/runtime facts.
4. Create `src/config.py` containing all fixed parameters, RNG seed, output paths, cases and primary selection.
5. Write the full report template with placeholders **before** running benchmarks.

**Gate G0:** Can create venv and install dependencies; `python -c 'import matplotlib,pytest'` succeeds; directory tree and template exist; all sizes/runs/groups conform to selection; no fabricated environment info.

### Phase 1 — Implement algorithms

**Work:** Add A1–A5 in `src/algorithms.py`; implement the exact variants above; annotate contracts and input assumptions; avoid global state, output printing and external data.

**Gate G1:** All functions import; expected return shapes and side-effect rules pass simple smoke tests; no built-in sorting used in A1/A2/A3 (A5 is allowed to sort by finish time).

### Phase 2 — Correctness tests and independent oracles

**Work:**
1. Sorting: test empties, singleton, negatives, duplicates, ascending, descending, random, larger random; compare with `sorted`. Test stability where reasonable or document it correctly.
2. Binary: empty, 1-item, misses below and above range, all targets across many sorted random arrays, absent target; verify result `-1` or points to target. No assumptions about first matching index with duplicates.
3. Greedy: hand-designed cases, tied finish times, touching intervals, uniqueness, no overlap, count optimality via brute force for small n; input nonmutation.
4. Check reproducibility of generators for same `(seed, algorithm, case, n, run)`.
5. Create pytest tests that validate benchmark schemas/ratio arithmetic and generated-data integrity.

**Gate G2:** `python -m pytest -q` passes 100%; all algorithm correctness checks pass *before* benchmarks. Capture output in `logs/validation.txt`.

### Phase 3 — Dataset generation and benchmark engine

**Work:**
1. Deterministic generation per sample with seed-derived integer seeds (avoid Python's randomized `hash()` for seed derivation).
2. Centralize timer using `perf_counter_ns()`.
3. For each timed invocation, prepare/copy input outside timer; optionally warm up a small run before measuring, document it. Correctness checks happen outside timed region.
4. Implement binary batched timer with calibration outside timing and per-call mean normalization.
5. Write atomic CSV files with honest `valid` flags and exceptions; fail nonzero if any required experiment fails.
6. Ensure one invocation runs all configured experiments and can be rerun with the same configuration (times will vary, input generation must remain deterministic).

**Gate G3:** A small `--smoke` mode uses smaller sizes and finishes successfully, verifies nonnegative elapsed times and full row counts, common sorting datasets, correct units, sensible positive `batch_calls`, and no graphs/printing inside timed blocks.

### Phase 4 — Full benchmarking

**Work:**
1. Run primary cases: A1, A2, A3 random sizes 500…8000; A4 binary cases 1000…16000; A5 random unsorted activities 1000…16000.
2. Run supplemental sorted and reverse-sorted sorting cases 250…4000.
3. Persist raw output and `report/environment.json` with exact execution date and version facts.
4. Log any unusual long pause, interference, input change, error or rerun; invalid tests require full reproducible rerun, not hand-editing CSV.

**Gate G4:** 105 main timing records present and valid, plus 90 supplemental records if those cases were executed; all expected sizes/runs/cases present; all reference correctness checks pass; elapsed units correct; binary cases have batched calls and accurate per-call elapsed times.

### Phase 5 — Statistical aggregation and growth ratios

**Work:**
1. Aggregate raw records into `data/summary/results.csv`.
2. Compute mean, optional SD, and doubling ratio by algorithm/case, in ascending n order.
3. Create summary of theoretical ratios by growth class, and label deviations.
4. Validate every summary row from raw data and reject duplicates/missing entries.

**Gate G5:** Exactly five primary summary rows per algorithm; first ratio absent, four subsequent ratios computed with the correct numerator/denominator; all averages equal raw-run means within floating-point tolerance; no invalid rows.

### Phase 6 — Plots (publication-quality but simple)

**Work:**
1. Plot n on x-axis and average runtime (ms) on y-axis for each algorithm, **five mandatory single-algorithm plots**.
2. Plot A1/A2/A3 on the **same combined axes**, same random datasets and n values; legend; descriptive title; grid; ensure full lines visible. Since the speed gap may compress Merge Sort on a linear plot, make a supplemental log-y figure if desired while retaining at least one standard, clearly-labeled chart.
3. Optional extra cases: best/worst sorting cases; binary best vs miss; activity sorted-scan comparison, only with clear definitions.
4. Use consistent file paths and readable 120–180 dpi figures. Axis labels must specify milliseconds and case condition. **Do not create theoretical curves based on arbitrary fitted constants and label them as measured data.**

**Gate G6:** Five individual primary plot files + combined sorting graph exist, are nonempty, readable, correct axis labels/legends, referenced at correct relative paths in report.

### Phase 7 — Comparative metrics and evidence-based interpretations

**Work:**
1. For each sorting size, compute actual average runtime and rank A1/A2/A3, with speedups defined `slower_ms / faster_ms` (e.g., `bubble_ms / merge_ms`, when merge is faster).
2. Determine the fastest algorithm at each n; identify if fastest algorithm changed between measured n values. If no change, explicitly report **no observed crossover in tested range**, never claim theoretical impossibility of crossover.
3. Report absolute differences only for equivalent sorting inputs; distinguish overhead-dominated small sizes and large input scaling.
4. Compare observed ratios with theory. Avoid asserting O(n log n) ratio is exactly 2, or O(log n) ratio is 2.
5. Explain why bubble and insertion share O(n²) but can differ significantly in constants; why merge sort scales better for large random inputs; why logarithmic search microbenchmarks can be noisy; why activity-selection sorting contributes O(n log n).

**Gate G7:** All claimed wins, speedups, crossovers and ratio interpretations match generated summary CSV; no unsupported universal superiority statements, no invented values.

### Phase 8 — Build report from template

**Work:**
1. Resolve environment + student metadata, algorithm pseudocode and theory, per-algorithm correctness summaries, exact table rows, plots and quantitative analysis.
2. Fill combined comparison, theory/empirical table, clearly written limitations and references.
3. Produce an original **8–10-line conclusion** based on actual results (target 9 lines). Avoid placeholder/trivial filler lines.
4. Preserve `report_template.md` untouched; write new `report/final_report.md`.
5. Optionally generate open-source PDF from final Markdown (e.g., Pandoc/LibreOffice if installed). PDF is optional unless user requests it; no proprietary tools.

**Gate G8:** Final report has exactly five algorithm sections, five table/graph pairs, combined comparison, 8–10 lines of conclusion, real version numbers or explicit `Not recorded`, and no `{{...}}`, `TODO`, `TBD`, fictitious numbers, or broken figure paths.

### Phase 9 — Rubric, quality, and reproducibility audit

**Work:**
1. Audit the source assignment requirements one-by-one using final checklist below.
2. Re-run `pytest`; check all expected CSVs, figures, image links and report sections exist; independently recompute a sample of ratios and speedup figures.
3. Add final `README.md`: setup, full run, no-timing analysis rebuild, folder descriptions, methodology, platform specifics and limitations.
4. Save command outputs to `logs/`. Ensure no secrets or irrelevant caches in distributable tree.
5. If git available, make a clear commit; do not claim publishing to GitHub unless actually done. `Git`/GitHub are mentioned as source options, not mandatory public upload.

**Gate G9:** Validation checklist passes, source alignment confirmed, clean reproducible execution commands and final report exist; no fabricated or copied experimental measurements.

### Phase 10 — Submission packaging and final handoff

**Work:**
1. Create ZIP containing `src`, `tests`, `data/raw`, `data/summary`, `figures`, `report`, `README.md`, `requirements.txt`, `plan.md` and relevant logs; exclude venv and caches.
2. Ensure submission artifacts include `report/final_report.md` and optional PDF if built.
3. Document experiment date distinct from PDF's printed submission date; don't retroactively mislabel experiment timing.
4. Provide a compact handoff summary: test status, exact commands, key results, unusual limitations, artifact paths, and any still-missing user metadata.

**Gate G10:** ZIP opens; all referenced files exist; a fresh checkout/venv can follow README; no placeholder remains in final report except explicitly user-unavailable identity details documented in handoff. If user metadata unavailable, mark submission **not fully ready** rather than invent it.

---

## 8. Required run commands (make Codex implement these entrypoints)

Commands are target interface examples; Codex must make them work exactly or update documentation consistently:

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Linux/macOS:
# source .venv/bin/activate
python -m pip install -r requirements.txt

python -m pytest -q
python -m src.benchmark --smoke
python -m src.benchmark --all
python -m src.analyze
python -m src.plots
python -m src.build_report
python -m pytest -q
```

- Add `--help` for CLI modules and reasonable `--out-dir`, `--seed` overrides if simple.
- `--smoke` must write in a separate `data/smoke/` location and not overwrite final benchmark data.
- Full-run CLI should offer `--main-only` and `--all` if practical.
- Keep plotting/report-generation separate from timing, so building report doesn't rerun expensive experiments.
- `build_report` must fail clearly if any primary result is missing or invalid.

---

## 9. Detailed final report checklist (mapped to assignment)

Use checked boxes only upon verified completion. Maintain a copy with real pass/fail status in `report/checks.md`.

### Selection and tools

- [ ] Exactly five algorithms (Bubble, Insertion, Merge, Binary Search, Activity Selection).
- [ ] Three groups represented: Sorting, Divide and Conquer, Greedy method.
- [ ] Open-source-only implementation and graphing.
- [ ] Actual language, environment, timing tool, graphing tool **and versions** stated.

### Algorithm-by-algorithm mandatory content

- [ ] A1: pseudocode, best/average/worst, correctness, five n, three runs, mean, ratios, plot, discussion.
- [ ] A2: pseudocode, best/average/worst, correctness, five n, three runs, mean, ratios, plot, discussion.
- [ ] A3: pseudocode, best/average/worst, correctness, five n, three runs, mean, ratios, plot, discussion.
- [ ] A4: pseudocode, best/average/worst, correctness, five n, three runs, mean, ratios, plot, discussion; explain batching and sorted prerequisite.
- [ ] A5: pseudocode, best/average/worst where relevant, correctness including optimality check, five n, three runs, mean, ratios, plot, discussion; sorting included in timing.

### Experimental validity

- [ ] Five monotonically increasing n per algorithm; adjacent doubling used for ratios.
- [ ] At least three actual measured runs per n and report Run1/Run2/Run3/Avg.
- [ ] Correctness verified before timed benchmark; no correctness assertion inside timing.
- [ ] Fixed seeded datasets; fair, same input arrays for sorting comparison.
- [ ] Data generation and sorting-list copies excluded from sorting timed sections.
- [ ] Binary search per-call time is correctly normalized by number of batched calls.
- [ ] Raw CSV retained and summary calculations verified against it.
- [ ] Best/worst-oriented tests included where relevant and described without overselling as mathematical worst-case for every size.

### Results and comparison

- [ ] One correctly labeled individual input-size vs runtime plot for each of five algorithms.
- [ ] One clearly labeled combined comparison graph for Bubble vs Insertion vs Merge.
- [ ] Winner identified for each common sorting n using actual measurements.
- [ ] How much faster stated quantitatively (ratios/speedups from raw data).
- [ ] Whether a winner crossover occurred within measured sizes explicitly stated.
- [ ] `T(2n)/T(n)` computed correctly; theory comparison includes n, n log n, n², log n as appropriate.
- [ ] Differences between theoretical and practical behavior explained (overhead, noise, hardware, interpreter, input distributions).
- [ ] Conclusion exactly 8–10 substantive lines, based on results.

### Presentation/handoff

- [ ] Student and course metadata filled from user-supplied facts (do not guess).
- [ ] All final report tables complete, no placeholder text, no broken links.
- [ ] README includes setup, tests, benchmarks, plots, report regeneration.
- [ ] Logs/metadata show when and how results were collected.
- [ ] Deliverable ZIP and optional PDF contain all necessary evidence/code.
- [ ] Final code/report proofread; no fictitious measurements or fabricated conclusions.

---

## 10. Codex instructions — exact implementation handoff prompt

Paste the block below into Codex alongside this `plan.md` and, ideally, the original assignment PDF:

> **Implement this DAA assignment exactly according to `plan.md`.** The five chosen algorithms are Bubble Sort (early exit), Insertion Sort, Merge Sort, iterative Binary Search, and greedy Activity Selection. Follow phases 0–10 in sequence. At each phase, execute the specified validation gate and fix failures before continuing. Implement real deterministic correctness tests, benchmark timings with `time.perf_counter_ns()`, batch very short Binary Search calls, generate raw and summary CSVs, derive all T(2n)/T(n) values and comparison speedups, produce 5 individual plots plus a 3-sort combined plot, and automatically populate `report/final_report.md` from `report/report_template.md` only after real measurements exist. Never fabricate sample timings or claim benchmarks were run when they were not. If you cannot run full benchmarks, leave placeholders in the template, report clearly what's incomplete, and provide exact local commands to finish. Keep `plan.md`, `README.md`, tests, data, figures and report consistent. Conclude with file paths, tests passed, results availability, and remaining user metadata requirements.

### Implementation discipline

- No need for clarifying questions about algorithm choice, stack, test sizes, groups, or outputs: they are fixed above.
- Do not ask Codex to optimize by replacing hand-written algorithms with Python built-ins.
- Do not choose only tiny datasets to produce artificially neat results.
- Do not call `perf_counter_ns()` separately inside each binary search without batching.
- Prefer honest empirical uncertainty over claiming perfect theoretical match.
- If execution is unavailable, **stop before pretending a completed final report exists**; deliver runnable scripts and explicit pending steps.

---

## 11. User-provided metadata intentionally outstanding

These fields may be needed for a submission cover page and cannot be invented:

```text
STUDENT_NAME = {{STUDENT_NAME}}
ENROLLMENT_NUMBER = {{ENROLLMENT_NUMBER}}
SEMESTER_SECTION = {{SEMESTER_SECTION}}
ACTUAL_SUBMISSION_DATE = {{ACTUAL_SUBMISSION_DATE}}
```

The original source PDF lists the faculty, paper code, institute and printed due date, but does **not** supply those student-specific cover fields. Codex should support a tiny metadata config (such as `report/student_info.json`) without blocking code or benchmark implementation, and should not substitute guesses.

---

## 12. Final quality bar

This is an **implementation plus experimental analysis** assignment, not five disconnected code snippets. The finished work should convincingly show correct algorithms, controlled inputs, honest timing, data-driven ratios, thoughtful interpretation, clear graphs and a reproducible handoff. The main comparison must be on three sorting algorithms solving the same task; binary search and greedy activity selection demonstrate additional algorithm groups. **Measurement data are authoritative; report prose must follow them, not the reverse.**

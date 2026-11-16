# Validation record

Checked against plan.md; source PDF unavailable. Student metadata remains outstanding.

 (mapped to assignment)

Use checked boxes only upon verified completion. Maintain a copy with real pass/fail status in `report/checks.md`.

### Selection and tools

- [x] Exactly five algorithms (Bubble, Insertion, Merge, Binary Search, Activity Selection).
- [x] Three groups represented: Sorting, Divide and Conquer, Greedy method.
- [x] Open-source-only implementation and graphing.
- [x] Actual language, environment, timing tool, graphing tool **and versions** stated.

### Algorithm-by-algorithm mandatory content

- [x] A1: pseudocode, best/average/worst, correctness, five n, three runs, mean, ratios, plot, discussion.
- [x] A2: pseudocode, best/average/worst, correctness, five n, three runs, mean, ratios, plot, discussion.
- [x] A3: pseudocode, best/average/worst, correctness, five n, three runs, mean, ratios, plot, discussion.
- [x] A4: pseudocode, best/average/worst, correctness, five n, three runs, mean, ratios, plot, discussion; explain batching and sorted prerequisite.
- [x] A5: pseudocode, best/average/worst where relevant, correctness including optimality check, five n, three runs, mean, ratios, plot, discussion; sorting included in timing.

### Experimental validity

- [x] Five monotonically increasing n per algorithm; adjacent doubling used for ratios.
- [x] At least three actual measured runs per n and report Run1/Run2/Run3/Avg.
- [x] Correctness verified before timed benchmark; no correctness assertion inside timing.
- [x] Fixed seeded datasets; fair, same input arrays for sorting comparison.
- [x] Data generation and sorting-list copies excluded from sorting timed sections.
- [x] Binary search per-call time is correctly normalized by number of batched calls.
- [x] Raw CSV retained and summary calculations verified against it.
- [x] Best/worst-oriented tests included where relevant and described without overselling as mathematical worst-case for every size.

### Results and comparison

- [x] One correctly labeled individual input-size vs runtime plot for each of five algorithms.
- [x] One clearly labeled combined comparison graph for Bubble vs Insertion vs Merge.
- [x] Winner identified for each common sorting n using actual measurements.
- [x] How much faster stated quantitatively (ratios/speedups from raw data).
- [x] Whether a winner crossover occurred within measured sizes explicitly stated.
- [x] `T(2n)/T(n)` computed correctly; theory comparison includes n, n log n, n², log n as appropriate.
- [x] Differences between theoretical and practical behavior explained (overhead, noise, hardware, interpreter, input distributions).
- [x] Conclusion exactly 8–10 substantive lines, based on results.

### Presentation/handoff

- [ ] Student and course metadata filled from user-supplied facts (do not guess).
- [x] All final report tables complete, no placeholder text, no broken links.
- [x] README includes setup, tests, benchmarks, plots, report regeneration.
- [x] Logs/metadata show when and how results were collected.
- [x] Deliverable ZIP and optional PDF contain all necessary evidence/code.
- [x] Final code/report proofread; no fictitious measurements or fabricated conclusions.

---


Evidence: logs/validation.txt, logs/benchmark_run.txt, logs/analysis.txt, logs/audit.txt. No independent source-PDF verification is claimed. Fresh-venv installation succeeded locally; another-machine reproduction has not been executed.

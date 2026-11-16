# DAA algorithm analysis

Five handwritten algorithms, three assignment groups, 195 real timing trials and 65 summary groups. Read report/final_report.md. Student name, enrollment, semester/section and actual submission date are deliberately blank: submission is not fully ready until supplied in report/student_info.json using the uppercase keys shown in plan.md. The original PDF was unavailable; requirements were checked against the supplied plan.

## Reproduce (PowerShell, from project root)

```powershell
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
.venv/Scripts/python -m pytest -q
.venv/Scripts/python -m src.benchmark --smoke
.venv/Scripts/python -m src.benchmark --all
.venv/Scripts/python -m src.analyze
.venv/Scripts/python -m src.plots
.venv/Scripts/python -m src.build_report
.venv/Scripts/python -m pytest -q
.venv/Scripts/python -m src.audit
```

On Linux/macOS replace `.venv/Scripts/python` with `.venv/bin/python`. Each processing module supports --help. For analysis-only rebuild, start at src.analyze; this does not rerun timings. --smoke writes data/smoke separately. --main-only provides exploratory primary timings, but the complete report pipeline requires --all including supplemental cases. --seed and --out-dir are available for benchmark experiments; custom outputs must be explicitly passed to analysis or restored to the canonical paths before report building.

Sorting functions mutate and return the supplied list; benchmark copies are made outside timing. Activity selection preserves its input and includes its internal sort. Binary batches use one calibrated count and include checksum-loop overhead. Inputs are seeded; timing results vary with machine state. Three trials offer limited noise characterization. Power mode/background processes were not controlled. No PDF was requested or generated. No editor was used to implement this project: Python CLI tooling was used; editor version is recorded as unavailable.

src contains algorithms, generators, benchmark and generation modules; tests contains independent correctness and integrity checks; data/raw preserves trials, data/summary contains computed means and ratios; figures contains plots; report contains the preserved template, metadata and generated report; logs contains execution evidence. Requirements pin the installed top-level dependencies. Timings are local observations, not universal rankings.

To package after regeneration:
```powershell
.venv/Scripts/python -m src.package
```
The ZIP excludes virtual environments, caches and smoke data. The experiment timestamp in report/environment.json is distinct from the printed assignment deadline. Identity is never inferred.

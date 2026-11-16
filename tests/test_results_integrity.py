from pathlib import Path
import math,pytest
from src.analyze import read,aggregate

def test_results():
    path=Path('data/raw/measurements.csv')
    if not path.exists():pytest.skip('Full measurements not yet generated')
    rows=read(path);assert len(rows)==195
    computed=aggregate(rows)
    if Path('data/summary/results.csv').exists():
        actual=read('data/summary/results.csv');assert len(actual)==65
        for a,b in zip(actual,computed):
            for k in ['average_ms','stddev_ms','run1_ms','run2_ms','run3_ms']:
                assert math.isclose(float(a[k]),b[k],rel_tol=1e-12)
            if b['ratio_to_previous_size']!='':assert math.isclose(float(a['ratio_to_previous_size']),b['ratio_to_previous_size'],rel_tol=1e-12)
    for damaged in [rows[:-1],rows+[rows[0]], [dict(r,valid='False') if i==0 else r for i,r in enumerate(rows)]]:
        with pytest.raises(AssertionError):aggregate(damaged)

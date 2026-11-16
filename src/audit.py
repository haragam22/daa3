import re,json,zipfile
from pathlib import Path
from .analyze import read,aggregate

def main():
    raw=read('data/raw/measurements.csv');assert len(raw)==195
    expected=aggregate(raw);actual=read('data/summary/results.csv');assert len(actual)==65
    for a,b in zip(actual,expected):
        for k,v in b.items():assert a[k]==str(v)
    report=Path('report/final_report.md').read_text(encoding='utf-8')
    assert len(re.findall(r'^## Algorithm A',report,re.M))==5
    assert not re.search(r'{{|TODO|TBD',report)
    conclusion=report.split('## Conclusion')[1].split('## ')[0]
    assert len(re.findall(r'^\d+\. ',conclusion,re.M))==9
    for target in re.findall(r'\[[^]]*\]\(([^)]+)\)',report):
        assert (Path('report')/target).is_file(),target
    for image in Path('figures').glob('*.png'):
        from PIL import Image
        with Image.open(image) as im:im.verify()
    assert len(list(Path('figures').glob('*.png')))>=6
    assert '{{STUDENT_NAME}}' in Path('report/report_template.md').read_text()
    print('AUDIT PASSED: measurements, calculations, report structure, links and images')
if __name__=='__main__':main()

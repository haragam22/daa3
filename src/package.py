from pathlib import Path
import zipfile
from .audit import main as audit

def main():
    audit()
    roots=['src','tests','data/raw','data/summary','figures','report','logs']
    files=[Path(p) for p in ['README.md','requirements.txt','plan.md','GATES.md','.gitignore']]
    for root in roots:files.extend(p for p in Path(root).rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc')
    with zipfile.ZipFile('daa-submission.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in files:z.write(p,p.as_posix())
    with zipfile.ZipFile('daa-submission.zip') as z:
        assert z.testzip() is None
        assert 'report/final_report.md' in z.namelist()
        assert set(z.namelist())=={p.as_posix() for p in files}
    print('PACKAGE PASSED:',len(files),'files')
if __name__=='__main__':main()

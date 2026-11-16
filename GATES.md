# Gates: DAA assignment
OWNS: src/**, tests/**, report/**, data/**, figures/**, logs/**, README.md, requirements.txt
Scope: five algorithms and all experimental deliverables in plan.md.

- [x] G1: correctness and raw/summary integrity tests pass
  CHECK: .venv\Scripts\python.exe -m pytest -q
  EXPECT: 10 passed
  EVIDENCE: automatic-evidence=v1; definition-sha256=870c340c02e7c2b7681d45e017fb00b80f12ef9c573fa6c7a197219a7af5b88a; exit=0; EXPECT=matched; output-sha256=a7a39fbe03ceecd27db03e687dc2b8cb19caabfd9115d62341f9826375504f85; output-bytes=101; shell=C:\WINDOWS\system32\cmd.exe; cwd=C:\Users\harag\Documents\coding\daa\ass3; path=867dca977851/41 entries

- [x] G2: all measurements, report sections, calculations, image files and links validate
  CHECK: .venv\Scripts\python.exe -m src.audit
  EXPECT: AUDIT PASSED
  EVIDENCE: automatic-evidence=v1; definition-sha256=d72fd574cabe1fae84e66208a8d2501183dd1b65c44a6ae8e864b74d0285783c; exit=0; EXPECT=matched; output-sha256=67189ef9376a23d2c82dd61a012cfc05b509a983c625f5de3ac1512b88f127ba; output-bytes=78; shell=C:\WINDOWS\system32\cmd.exe; cwd=C:\Users\harag\Documents\coding\daa\ass3; path=867dca977851/41 entries

- [x] G3: ZIP opens and contains every selected submission artifact
  CHECK: .venv\Scripts\python.exe -m src.package
  EXPECT: PACKAGE PASSED
  EVIDENCE: automatic-evidence=v1; definition-sha256=2fa1f0ba8f603c94a60abea2212033ea74b6851543d606888abe950b72af5544; exit=0; EXPECT=matched; output-sha256=4bf1095270c30d64599352f68d2b1efd03705a82c812f9f62ae5cae696e00080; output-bytes=104; shell=C:\WINDOWS\system32\cmd.exe; cwd=C:\Users\harag\Documents\coding\daa\ass3; path=867dca977851/41 entries

- [ ] G4: cover identity and actual submission date supplied
  EVIDENCE: unavailable; deliberately blank, submission not fully ready

ABANDON: G4 User identity and actual submission date unavailable; fill report/student_info.json and regenerate report before submission.

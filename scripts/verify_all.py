"""Run existing offline suites with isolated interpreters; no robot I/O."""
import argparse,json,re,subprocess,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser();p.add_argument('--output',default='artifacts/verification');a=p.parse_args()
 out=Path(a.output).resolve();out.mkdir(parents=True,exist_ok=True)
 jobs=[('Epic01',['Epic-01/integration/run.py'])]+[(f'Epic{i:02}',[f'Epic-{i:02}/runtime/run.py']) for i in range(2,7)]+[('Common',['Development/runtime/run.py']),('Epic17',['-m','unittest','discover','-s','Epic-17/tests','-v']),('Stage1',['-m','unittest','discover','-s','Development/Stage1/tests','-v']),('Bringup',['-m','unittest','discover','-s','Development/Stage1/bringup/tests','-v'])]
 rows=[]
 for name,args in jobs:
  try:r=subprocess.run([sys.executable,*args],cwd=ROOT,capture_output=True,text=True,timeout=120);code=r.returncode;log=r.stdout+r.stderr
  except subprocess.TimeoutExpired:code=124;log='Suite exceeded 120 seconds. No pass claimed.\n'
  (out/(name+'.log')).write_text(log);tests=sum(map(int,re.findall(r'Ran (\d+) tests?',log)))
  rows.append({'suite':name,'exit_code':code,'tests':tests});print(name,'PASS' if code==0 else 'FAIL',tests,flush=True)
 def git(*args):
  r=subprocess.run(['git',*args],cwd=ROOT,capture_output=True,text=True);return r.stdout.strip() if r.returncode==0 else None
 report={'source_commit':git('rev-parse','HEAD'),'worktree_status':git('status','--porcelain'),'suites':rows,'tests':sum(r['tests'] for r in rows),'passed':all(r['exit_code']==0 and r['tests']>0 for r in rows),'actual_robot_test':False,'release_ready':False}
 (out/'summary.json').write_text(json.dumps(report,indent=2));print('Evidence:',out)
 return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())

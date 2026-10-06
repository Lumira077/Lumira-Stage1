"""Metadata-only operation counts and conservative release assessment."""
from collections import Counter
from common import require
ALLOWED={'selected','guest','denied','planned','cancel_requested','suppressed','fallback','error'}
class Metrics:
    def __init__(self): self.counts=Counter()
    def record(self,feature,result):
        require(feature in {'F2004','F2005','F2006','F2007','F2157'} and result in ALLOWED,'INVALID_INPUT')
        self.counts[(feature,result)]+=1
    def snapshot(self):
        return [{'feature':k[0],'result':k[1],'operations':v} for k,v in sorted(self.counts.items())]
def release_assessment(report):
    require(isinstance(report,dict) and type(report.get('tests')) is int and report['tests']>0,'INVALID_INPUT')
    passed=report.get('passed') is True and report.get('failures')==0 and report.get('errors')==0
    return {'simulation_passed':passed,'release_ready':False,'actual_participants':0,
            'pending':['physical_robot','real_user_study','operational_rollback','approved_assets',
                       'production_auth','Q1_R1_review'],'scope':'prototype'}

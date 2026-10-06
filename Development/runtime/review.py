"""Inspect a feature contract and list real evidence still required. Never approve a release."""
import json,sys,re
from pathlib import Path
def review(contract):
 required=('feature','jira','epic','work','data','boundary','metrics','stage_work','scope','intervention')
 if not isinstance(contract,dict) or any(not contract.get(k) for k in required):raise ValueError('incomplete contract')
 if not re.fullmatch(r'F\d+',contract['feature']) or not re.fullmatch(r'KR1-\d+',contract['jira']):raise ValueError('identifier')
 if contract['release_ready'] is not False or contract['actual_external_calls']!=0:raise ValueError('draft scope mismatch')
 return {'feature':contract['feature'],'scope':contract['scope'],'partial_utility':contract.get('implementation'),'missing_jira_stages':contract['missing_stages'],'required_inputs':contract['intervention'],'required_real_evidence':['approved design/assumptions and owner','actual target environment/sample/version','integration results/failures/retest','required physical ACK/provider receipt/expert review','release/freeze/rollback approvals'],'release_ready':False}
if __name__=='__main__':print(json.dumps(review(json.loads(Path(sys.argv[1]).read_text())),ensure_ascii=False,indent=2))

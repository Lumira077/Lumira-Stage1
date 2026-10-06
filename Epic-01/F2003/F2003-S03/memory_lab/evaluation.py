"""Fixed synthetic test-set evaluation; not real model or user evidence."""
import tempfile
from memory_contract import extract,Error
from memory_service.fixtures import setup,candidate

def evaluate(rows):
    tp=fp=fn=blocked=exact=0
    for row in rows:
        try:
            extracted=extract(row['utterance'],'a'*32);found=bool(extracted)
            exact+=found and extracted[0]['content']==row['expected_content']
        except Error:found=False;blocked+=1
        expected=row['expected_candidate'];tp+=found and expected;fp+=found and not expected;fn+=not found and expected
    with tempfile.TemporaryDirectory() as tmp:
        p,s,pid=setup(tmp)
        try:
            for i,content in enumerate(('jazz','gardening','산책')):
                r=s.create('demo-owner',pid,'demo-device',candidate(content,topic='fixture_'+str(i)),str(i));s.confirm('demo-owner',pid,'demo-device',r['memory_id'],1,'confirm'+str(i))
            cases=[('jazz','jazz'),('gardening','gardening'),('산책','산책'),('비행기',None)];correct=wrong=0
            for query,expected in cases:
                hits=s.search('demo-owner',pid,'demo-device',query);actual=hits[0]['content'] if hits else None;correct+=actual==expected;wrong+=actual is not None and actual!=expected
        finally:s.close();p.close()
    return {'mode':'synthetic_fixture','extractor':'explicit-preference-rules-v1','search':'normalized-substring-and-bigram-v1',
        'extraction':{'cases':len(rows),'true_positive':tp,'false_positive':fp,'false_negative':fn,'blocked_inputs':blocked,'precision':None if not tp+fp else tp/(tp+fp),'recall':None if not tp+fn else tp/(tp+fn),'exact_content_matches':exact,'exact_content_accuracy':None if not tp+fn else exact/(tp+fn)},
        'retrieval':{'cases':len(cases),'top1_correct':correct,'top1_accuracy':correct/len(cases),'wrong_returned_memory_rate':wrong/len(cases)},
        'limitations':['No LLM, semantic vector search, prompt evaluation, speech recognition or real-user quality measurements.','Small handcrafted examples do not demonstrate generalization or comprehensive sensitive-data detection.']}

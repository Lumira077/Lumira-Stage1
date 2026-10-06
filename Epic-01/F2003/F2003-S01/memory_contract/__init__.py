"""F2003 v1 memory contracts. Candidate extraction is deterministic, not an LLM."""
import math,re,unicodedata
VERSION='0.1.0';EXTRACTOR='explicit-preference-rules-v1';SEARCH='normalized-substring-and-bigram-v1'
KINDS=('preference','fact','promise')
class Error(Exception):
    def __init__(self,code,status=422):self.code,self.status=code,status;super().__init__(code)
def require(ok,code='INVALID_INPUT',status=422):
    if not ok:raise Error(code,status)
def text(value,limit=400):
    require(isinstance(value,str) and 1<=len(value.strip())<=limit and not any(unicodedata.category(c).startswith('C') for c in value))
    return unicodedata.normalize('NFKC',value.strip())
def opaque(value):return isinstance(value,str) and bool(re.fullmatch('[0-9a-f]{32}',value))
def normalized(value):return re.sub(r'\s+',' ',unicodedata.normalize('NFKC',value).casefold()).strip()
def policy(content):
    # Conservative rule filter; never claimed to detect all sensitive or adversarial text.
    value=normalized(text(content))
    sensitive=('비밀번호','패스워드','password','passwd','api key','api_key','token=','계좌','카드번호','주민번호','주민등록','금융','집 내부','가구 배치','도어락','현관 비번','credit card','bank account','private key')
    instruction=('ignore previous','system prompt','system instruction','이전 지시','시스템 지시','권한 변경','sudo ','execute command','모터 실행')
    require(not any(x in value for x in sensitive) and not re.search(r'\b\d{6}-?\d{7}\b',value),'SENSITIVE_MEMORY_FORBIDDEN')
    require(not any(x in value for x in instruction),'INSTRUCTION_MEMORY_FORBIDDEN')
    return value
def validate(data):
    require(isinstance(data,dict) and set(data)=={'kind','topic','content','source_ref','confidence','ttl_seconds'})
    require(data['kind'] in KINDS);require(isinstance(data['topic'],str) and bool(re.fullmatch('[a-z][a-z0-9_]{0,39}',data['topic'])))
    content=text(data['content']);policy(content);require(opaque(data['source_ref']),'OPAQUE_SOURCE_REQUIRED')
    require(type(data['confidence']) in (float,int) and math.isfinite(data['confidence']) and 0<=data['confidence']<=1)
    require(type(data['ttl_seconds']) is int and 60<=data['ttl_seconds']<=31536000)
    return {**data,'content':content}
def extract(utterance,source_ref):
    raw=text(utterance,1000);policy(raw);require(opaque(source_ref),'OPAQUE_SOURCE_REQUIRED')
    patterns=[r'^(?:기억해\s*줘[:：]?\s*)?나는\s+(.{1,120}?)(?:을|를)?\s*좋아해[.!]?$',r'^(?:remember:\s*)?I like (.{1,120}?)[.!]?$']
    for pattern in patterns:
        m=re.fullmatch(pattern,raw,re.IGNORECASE)
        if m:
            return [{'kind':'preference','topic':'favorite_activity','content':m.group(1).strip(),'source_ref':source_ref,'confidence':.8,'ttl_seconds':2592000}]
    # Free-form explicit facts/promises need structured user input; no inference from arbitrary chat.
    return []
def relevance(query,content):
    q,c=normalized(query),normalized(content)
    if q in c:return 1.0
    def grams(x):return {x[i:i+2] for i in range(len(x)-1)}
    a,b=grams(q),grams(c)
    return 0.0 if not a or not b else len(a&b)/len(a|b)

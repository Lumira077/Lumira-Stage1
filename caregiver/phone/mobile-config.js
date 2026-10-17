// Only a service origin is persisted. Credentials and session tokens stay in memory.
export function normalizeOrigin(value){
 if(!value.trim())return '';
 const u=new URL(value.trim());
 if(u.protocol!=='https:'||u.username||u.password||u.pathname!=='/'||u.search||u.hash)throw new Error('HTTPS 서버 주소만 입력하세요. 경로·계정·쿼리는 허용하지 않습니다.');
 return u.origin;
}
export function readOrigin(){try{return normalizeOrigin(localStorage.getItem('lumira.api.origin')||'');}catch{return '';}}
export function saveOrigin(value){const origin=normalizeOrigin(value);if(origin)localStorage.setItem('lumira.api.origin',origin);else localStorage.removeItem('lumira.api.origin');return origin;}

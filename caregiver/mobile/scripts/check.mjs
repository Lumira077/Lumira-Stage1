import { readFile, access } from 'node:fs/promises';
import assert from 'node:assert/strict';
let count=0;function check(value,name){assert(value,name);count++;console.log('PASS '+name);}
const cfg=JSON.parse(await readFile('capacitor.config.json','utf8'));
check(cfg.appId==='kr.lumira.caregiver.dev','development bundle ID');
check(!cfg.server.url&&!cfg.server.cleartext&&!cfg.android.allowMixedContent,'bundled assets and HTTPS only');
const android=await readFile('android/app/src/main/AndroidManifest.xml','utf8');
for(const perm of ['INTERNET','CAMERA','RECORD_AUDIO','MODIFY_AUDIO_SETTINGS'])check(android.includes('android.permission.'+perm),perm+' declared');
check(android.includes('allowBackup="false"')&&android.includes('usesCleartextTraffic="false"'),'no backup or cleartext');
const ios=await readFile('ios/App/App/Info.plist','utf8');
check(ios.includes('NSCameraUsageDescription')&&ios.includes('NSMicrophoneUsageDescription'),'iOS camera and microphone purpose strings');
check(!ios.includes('NSAllowsArbitraryLoads')&&!ios.includes('UIBackgroundModes'),'no ATS exception or unimplemented background calling');
const html=await readFile('www/index.html','utf8');
check(html.includes('Content-Security-Policy')&&html.includes('/native.js'),'packaged CSP and lifecycle module');
for(const file of ['app.js','mobile-config.js','native.js','capacitor-core.js','ui.js','style.css','robot-face.svg']){
 const canonical=await readFile('www/'+file,'utf8');
 for(const prefix of ['android/app/src/main/assets/public/','ios/App/App/public/'])check(canonical===await readFile(prefix+file,'utf8'),prefix+file+' synchronized');
}
const src=await readFile('../phone/mobile-config.js','utf8');
const {normalizeOrigin}=await import('data:text/javascript;base64,'+Buffer.from(src).toString('base64'));
check(normalizeOrigin('https://care.example.com/')==='https://care.example.com','origin normalization');
for(const value of ['http://care.example.com','https://user:pw@care.example.com','https://care.example.com/v1','https://care.example.com/?token=x']){
 let rejected=false;try{normalizeOrigin(value);}catch{rejected=true;}check(rejected,'reject unsafe endpoint '+value.replace('pw','REDACTED'));
}
console.log(JSON.stringify({passed:count,scope:'static native project and endpoint contract; NOT device runtime'}));

const {chromium}=require('playwright');
const {spawn}=require('child_process');const fs=require('fs');const os=require('os');const path=require('path');const crypto=require('crypto');
(async()=>{
const root=path.resolve(__dirname,'..'),tmp=fs.mkdtempSync(path.join(os.tmpdir(),'s02-ui-')),token=crypto.randomBytes(32).toString('hex');
const proc=spawn(process.env.KER_PYTHON||'python3',['-m','ker_onboarding.api','--db',path.join(tmp,'ui.sqlite3'),'--port','18081'],{cwd:root,env:{...process.env,KER_DEMO_TOKEN:token,KER_ADAPTER_MODE:'simulated',KER_SIM_FAIL_ONCE:'tts'},stdio:['ignore','ignore','inherit']});
fs.mkdirSync(root+'/evidence',{recursive:true});
let browser;
try{
for(let i=0;i<100;i++){try{const r=await fetch('http://127.0.0.1:18081/health');if(r.ok)break;}catch{}await new Promise(r=>setTimeout(r,50));}
browser=await chromium.launch({headless:true,args:['--no-sandbox']});const page=await browser.newPage({viewport:{width:1100,height:900}});const errors=[];page.on('pageerror',e=>errors.push(e.message));
await page.goto('http://127.0.0.1:18081/');await page.locator('#token').fill(token);await page.locator('#login').click();await page.locator('#device option').nth(1).waitFor({state:'attached'});
await page.locator('#start').click();await page.locator('#wizard').waitFor({state:'visible'});
for(const heading of ['언어','닉네임·호칭','사용 목적','음성·표현 선호']){await page.locator('#next').click();await page.locator('#heading').filter({hasText:heading}).waitFor({state:'visible'});}
await page.locator('#token').fill('');
await page.screenshot({path:root+'/evidence/01-preferences.png',fullPage:true});
await page.locator('#token').fill(token);
// Reload must restore the saved server-side draft, without persisting the token.
await page.reload();if(await page.locator('#token').inputValue()!=='')throw Error('Token persisted unexpectedly');
await page.locator('#token').fill(token);await page.locator('#login').click();await page.locator('#device option').nth(1).waitFor({state:'attached'});
await page.locator('#resume').click();await page.locator('#heading').filter({hasText:'음성·표현 선호'}).waitFor({state:'visible'});
await page.locator('#skip').click();await page.locator('#heading').filter({hasText:'목적별 동의'}).waitFor({state:'visible'});
await page.locator('#next').click();await page.locator('#heading').filter({hasText:'최종 확인'}).waitFor({state:'visible'});
await page.locator('#f_confirmed').check();await page.locator('#next').click();await page.locator('#complete:enabled').waitFor({state:'visible'});
await page.locator('#complete').click();await page.locator('#result').filter({hasText:'registration_status'}).waitFor({state:'visible'});
await page.locator('#apply').click();await page.locator('#result').filter({hasText:'MODULE_APPLY_FAILED:tts'}).waitFor({state:'visible'});
await page.locator('#apply').click();await page.locator('#result').filter({hasText:'"apply_status": "applied"'}).waitFor({state:'visible'});
await page.locator('#greet').click();await page.locator('#greeting').filter({hasText:'박사님'}).waitFor({state:'visible'});
await page.locator('#token').fill('');
await page.screenshot({path:root+'/evidence/02-first-greeting.png',fullPage:true});
await page.locator('#token').fill(token);
if(errors.length)throw Error(errors.join('\n'));
console.log('UI PASS: wizard, reload/resume, default skip, consent refusal, registration, failure/retry, greeting; zero page errors.');
}catch(e){console.error(e.message);process.exitCode=1;}finally{if(browser)await browser.close();proc.kill('SIGTERM');fs.rmSync(tmp,{recursive:true,force:true});}
})();

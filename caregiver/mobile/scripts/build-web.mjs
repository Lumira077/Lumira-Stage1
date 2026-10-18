import './restore-fonts.mjs';
import { mkdir, cp, copyFile, readFile, writeFile } from 'node:fs/promises';
await mkdir('www',{recursive:true});
for(const file of ['index.html','style.css','app.js','mobile-config.js','ui.js','i18n.js','robot-face.svg','icon.svg','icon-192.png','icon-512.png']) await copyFile('../phone/'+file,'www/'+file);
await cp('../phone/fonts','www/fonts',{recursive:true});
let html=await readFile('www/index.html','utf8');
html=html.replace(/<link\b(?=[^>]*\brel="manifest")[^>]*>/,'');
// Packaged content only. No server.url, remote JS, or cleartext API in native builds.
html=html.replace(/<meta charset="utf-8"\s*\/?\>/,`<meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; connect-src 'self' https:; media-src 'self' blob:; object-src 'none'; base-uri 'self'; form-action 'self'">`);
await writeFile('www/index.html',html);
await copyFile('node_modules/@capacitor/core/dist/index.js','www/capacitor-core.js');
await writeFile('www/native.js',`import { registerPlugin } from './capacitor-core.js';\nimport { endCall, stopMedia } from './app.js';\nconst App=registerPlugin('App');\nif(window.Capacitor?.isNativePlatform()){\n App.addListener('appStateChange',({isActive})=>{if(!isActive)endCall('ended').catch(stopMedia);});\n App.addListener('backButton',()=>{endCall('ended').catch(stopMedia);});\n}\n`);
await writeFile('www/index.html',html.replace('</body>','<script type="module" src="/native.js"></script></body>'));
console.log('Packaged mobile assets generated');

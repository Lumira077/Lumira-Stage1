// Public shell only; never intercept APIs, credentials or other applications.
const BASE=new URL('.',self.location.href);
const CACHE='lumira-caregiver-r4-path-042-'+BASE.pathname;
const FILES=['./','app.js','i18n.js','mobile-config.js','ui.js','robot-face.svg','style.css','manifest.webmanifest','icon.svg','icon-192.png','icon-512.png'].map(p=>new URL(p,BASE).href);
self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES)).then(()=>self.skipWaiting())));
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k.startsWith('lumira-caregiver-r4-path-')&&k!==CACHE).map(k=>caches.delete(k)))).then(()=>self.clients.claim())));
self.addEventListener('fetch',e=>{if(e.request.method!=='GET'||!FILES.includes(e.request.url))return;e.respondWith(fetch(e.request).catch(()=>caches.match(e.request)));});

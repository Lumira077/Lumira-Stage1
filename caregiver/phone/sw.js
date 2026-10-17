// Cache only public shell. Never cache API responses or private robot data.
const CACHE='lumira-caregiver-r4';const FILES=['/','/app.js','/mobile-config.js','/ui.js','/robot-face.svg','/style.css','/manifest.webmanifest','/icon.svg','/icon-192.png','/icon-512.png'];
self.addEventListener('install',e=>e.waitUntil(caches.open(CACHE).then(c=>c.addAll(FILES))));
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==CACHE).map(k=>caches.delete(k))))));
self.addEventListener('fetch',e=>{if(e.request.method!=='GET'||new URL(e.request.url).origin!==self.location.origin||new URL(e.request.url).pathname.startsWith('/v1/'))return;e.respondWith(fetch(e.request).catch(()=>caches.match(e.request)));});

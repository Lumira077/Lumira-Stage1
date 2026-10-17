import {cp,mkdir} from 'node:fs/promises';
await mkdir('../phone/fonts',{recursive:true});
for (const name of ['index.css','LICENSE','files']) await cp('node_modules/@fontsource-variable/noto-sans-kr/'+name,'../phone/fonts/'+name,{recursive:true});

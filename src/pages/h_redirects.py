PAGES = [{"tool": True, "name": "301 redirect generator", "path": "301-redirect-generator/",
 "title": "301 Redirect Generator for .htaccess, Nginx, Netlify, Vercel & Cloudflare (free)",
 "desc": "Free bulk 301 redirect generator. Paste old and new URLs and get ready redirect rules for Apache .htaccess, Nginx, Netlify _redirects, Vercel and Cloudflare, with loop and chain checks.",
 "body": r"""<h1>301 redirect generator</h1>
<p>Paste one redirect per line as <code>old new</code> (space, tab or comma separated). Old paths can be full URLs or paths; the generator keeps only the path and query. Moving a whole site? Use the domain option below.</p>
<div class="card"><label>Redirects (old new)</label><textarea id="v" style="min-height:130px">/old-page /new-page
/blog/2019/hello-world /blog/hello-world
https://example.com/products.php?id=7 /products/blue-widget
/team /about</textarea>
<div class="row"><div><label>Server</label><select id="f"><option value="apache">Apache .htaccess</option><option value="nginx">Nginx</option><option value="netlify">Netlify _redirects</option><option value="vercel">Vercel vercel.json</option><option value="cf">Cloudflare bulk redirects CSV</option></select></div>
<div><label>Status</label><select id="st"><option>301</option><option>302</option><option>308</option></select></div></div>
<label><input type="checkbox" id="dom"> Whole-domain move to</label><input id="nd" placeholder="https://new-domain.com">
<div id="chk"></div><label>Rules</label><textarea id="out" style="min-height:220px" readonly></textarea><button onclick="navigator.clipboard.writeText(out.value)">Copy</button></div>
<div class="card cta"><b>After a migration:</b> our <a href="https://apify.com/extezzu/sitemap-url-validator">Sitemap URL Validator</a> requests every URL in your sitemap and lists redirects, chains, 404s and noindex pages, so you can confirm nothing broke.</div>
<h2>Good redirect practice</h2><ul><li>Use 301 (or 308) for permanent moves so search engines transfer signals; 302 is for temporary changes.</li><li>Redirect each old URL to its closest new equivalent, not everything to the home page (Google treats that as a soft 404).</li><li>Avoid chains (A→B→C): point A straight to C. Update internal links and the sitemap to the new URLs.</li><li>Keep redirects in place for at least a year, ideally permanently.</li></ul>
<script>
function path(s){try{const u=new URL(s);return u.pathname+u.search}catch(e){return s.startsWith('/')?s:'/'+s}}
const reEsc=s=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
function gen(){const code=st.value,w=[];let rows=[];
if(dom.checked){const d=nd.value.trim().replace(/\/$/,'');if(!/^https?:\/\//.test(d))w.push('Enter the new domain with https://');
const m={apache:`RewriteEngine On\nRewriteRule ^(.*)$ ${d}/$1 [R=${code},L]`,nginx:`server {\n    listen 80;\n    listen 443 ssl;\n    server_name old-domain.com www.old-domain.com;\n    return ${code} ${d}$request_uri;\n}`,
netlify:`/*  ${d}/:splat  ${code}!`,vercel:JSON.stringify({redirects:[{source:'/:path*',destination:d+'/:path*',permanent:code!='302'}]},null,2),cf:`Use a Cloudflare Single Redirect rule: wildcard pattern https://old-domain.com/* to ${d}/\${1}, status ${code}, preserve query string.`};
out.value=m[f.value];chk.innerHTML=w.length?'<p class="bad">'+w.join('<br>')+'</p>':'';return}
for(const line of v.value.split(/\n/).map(s=>s.trim()).filter(Boolean)){const p=line.split(/[\s,\t]+/);if(p.length<2){w.push('Missing target: '+line);continue}rows.push([path(p[0]),p[1]])}
const src=new Map(rows.map(r=>[r[0],r[1]]));
for(const [a,b] of rows){const bp=/^https?:/.test(b)?null:path(b);if(bp===a)w.push('Loop: '+a+' redirects to itself');else if(bp&&src.has(bp))w.push(`Chain: ${a} → ${bp} → ${src.get(bp)}. Point ${a} directly to ${src.get(bp)}.`)}
const seen=new Set();for(const [a] of rows){if(seen.has(a))w.push('Duplicate source: '+a);seen.add(a)}
const q=rows.some(r=>r[0].includes('?'));
if(f.value=='apache'){const L=['RewriteEngine On'];for(const [a,b] of rows){const [p,qs]=a.split('?');if(qs)L.push(`RewriteCond %{QUERY_STRING} ^${reEsc(qs)}$`,`RewriteRule ^${reEsc(p.slice(1))}$ ${b}? [R=${code},L]`);else L.push(`RewriteRule ^${reEsc(p.slice(1))}$ ${b} [R=${code},L]`)}out.value=L.join('\n')}
else if(f.value=='nginx'){const L=[];for(const [a,b] of rows){const [p,qs]=a.split('?');if(qs)L.push(`location = ${p} {\n    if ($args = "${qs}") { return ${code} ${b}; }\n}`);else L.push(`location = ${p} { return ${code} ${b}; }`)}out.value=L.join('\n')}
else if(f.value=='netlify'){out.value=rows.map(([a,b])=>{const [p,qs]=a.split('?');if(qs){const kv=qs.split('&').map(x=>x.replace('=','=')).join('  ');return `${p}  ${kv}  ${b}  ${code}`}return `${p}  ${b}  ${code}`}).join('\n');if(q)w.push('Netlify matches query parameters by name (id=:id), not by exact value: check these lines against Netlify's docs.')}
else if(f.value=='vercel'){out.value=JSON.stringify({redirects:rows.map(([a,b])=>{const [p,qs]=a.split('?');const r={source:p,destination:b,statusCode:+code};if(qs)r.has=qs.split('&').map(x=>{const [k,val]=x.split('=');return {type:'query',key:k,value:val||''}});return r})},null,2)}
else{out.value=rows.map(([a,b])=>`example.com${a},${/^https?:/.test(b)?b:'https://example.com'+b},${code}`).join('\n');w.push('Replace example.com with your domain before importing the CSV.')}
chk.innerHTML=w.length?'<p class="bad">'+w.map(s=>s.replace(/</g,'&lt;')).join('<br>')+'</p>':'<p class="ok">No loops, chains or duplicates found.</p>'}
[v,f,st,dom,nd].forEach(e=>e.addEventListener('input',gen));gen();
</script>"""}]

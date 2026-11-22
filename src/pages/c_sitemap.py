PAGES = [{"tool": True, "name": "Sitemap XML validator", "path": "sitemap-validator/",
 "title": "Sitemap XML Validator: check sitemap.xml for errors online (free)",
 "desc": "Free sitemap.xml validator. Paste your sitemap or sitemap index and find invalid or relative URLs, duplicates, wrong lastmod dates, mixed hosts, HTTP URLs and 50,000-URL limit problems.",
 "body": r"""<h1>Sitemap XML validator</h1>
<p>Paste the contents of your <code>sitemap.xml</code> (or a sitemap index). The check runs in your browser.</p>
<div class="card"><textarea id="xml" placeholder="&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot;?&gt;&#10;&lt;urlset xmlns=&quot;http://www.sitemaps.org/schemas/sitemap/0.9&quot;&gt;..."></textarea>
<input type="file" id="file" accept=".xml,.txt" style="margin-top:8px"><button onclick="run()">Validate</button><div id="res"></div></div>
<div class="card cta"><b>Are the URLs actually alive?</b> This page checks the file itself. To fetch every URL and find 404s, redirects, noindex and canonical problems, use our <a href="https://apify.com/extezzu/sitemap-url-validator">Sitemap URL Validator</a> in the cloud (about $2 per 1,000 URLs, schedulable).</div>
<h2>What is checked</h2><ul><li>Well-formed XML and the correct sitemaps.org namespace</li><li>Every &lt;loc&gt; is an absolute http(s) URL, properly escaped</li><li>Duplicate URLs and URLs on a different host than the rest</li><li>HTTP URLs on an HTTPS site</li><li>&lt;lastmod&gt; in W3C date format and not in the future</li><li>Limits: 50,000 URLs and 50 MB per file</li><li>Deprecated &lt;priority&gt;/&lt;changefreq&gt; (Google ignores them)</li></ul>
<script>
file.onchange=async()=>{xml.value=await file.files[0].text();run()};
function run(){const s=xml.value.trim();const out=[];const add=(c,t)=>out.push(`<li class="${c}">${t}</li>`);
if(!s){res.innerHTML='<p class="warn">Paste a sitemap first.</p>';return}
const doc=new DOMParser().parseFromString(s,'application/xml');const pe=doc.getElementsByTagName('parsererror')[0];
if(pe){res.innerHTML='<p class="bad">Not valid XML: '+pe.textContent.slice(0,300).replace(/</g,'&lt;')+'</p>';return}
const root=doc.documentElement;const isIndex=root.localName=='sitemapindex';
if(!['urlset','sitemapindex'].includes(root.localName))add('bad','Root element must be &lt;urlset&gt; or &lt;sitemapindex&gt;, found &lt;'+root.localName+'&gt;.');
if(root.namespaceURI!='http://www.sitemaps.org/schemas/sitemap/0.9')add('bad','Missing or wrong namespace. Use xmlns="http://www.sitemaps.org/schemas/sitemap/0.9".');
const locs=[...doc.getElementsByTagNameNS('*','loc')].map(e=>e.textContent.trim());
const bytes=new Blob([s]).size;if(locs.length>50000)add('bad',`${locs.length} URLs: the limit is 50,000 per file. Split it and use a sitemap index.`);
if(bytes>52428800)add('bad','File is larger than 50 MB uncompressed.');
const seen=new Map(),hosts={};let bad=0,dup=0,http=0;
for(const l of locs){let u;try{u=new URL(l);if(!/^https?:$/.test(u.protocol))throw 0}catch(e){bad++;if(bad<=10)add('bad','Not an absolute http(s) URL: '+l.replace(/</g,'&lt;'));continue}
hosts[u.host]=(hosts[u.host]||0)+1;if(u.protocol=='http:')http++;if(seen.has(l)){dup++;if(dup<=10)add('warn','Duplicate: '+l)}seen.set(l,1)}
const hk=Object.keys(hosts);if(hk.length>1)add('warn','URLs on '+hk.length+' different hosts ('+hk.slice(0,5).join(', ')+'). A sitemap should only list URLs of its own host.');
if(http&&http<locs.length)add('warn',http+' URLs use http:// while others use https://.');
const now=Date.now()+864e5;let lm=0;for(const e of doc.getElementsByTagNameNS('*','lastmod')){const t=e.textContent.trim();
if(!/^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:\d{2}))?$/.test(t)||isNaN(Date.parse(t))){lm++;if(lm<=5)add('bad','Invalid lastmod "'+t+'". Use YYYY-MM-DD or full W3C datetime.')}else if(Date.parse(t)>now){lm++;if(lm<=5)add('warn','lastmod in the future: '+t)}}
if(doc.getElementsByTagNameNS('*','priority').length||doc.getElementsByTagNameNS('*','changefreq').length)add('muted','priority/changefreq found: harmless, but Google ignores them.');
const ok=!out.some(x=>x.includes('class="bad"'));
res.innerHTML=`<p class="${ok?'ok':'bad'}"><b>${ok?'No blocking errors.':'Errors found.'}</b> ${isIndex?'Sitemap index':'Sitemap'} with ${locs.length} ${isIndex?'child sitemaps':'URLs'}, ${(bytes/1024).toFixed(1)} KB.</p><ul>${out.join('')}</ul>`}
</script>"""}]

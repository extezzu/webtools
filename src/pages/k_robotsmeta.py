PAGES = [{"tool": True, "name": "Robots meta & X-Robots-Tag generator", "path": "robots-meta-tag-generator/",
 "title": "Robots Meta Tag & X-Robots-Tag Generator: noindex, nofollow, snippets (free)",
 "desc": "Free robots meta tag and X-Robots-Tag header generator. Pick noindex, nofollow, nosnippet, max-snippet and more, and get HTML plus Apache, Nginx config with warnings about conflicting directives.",
 "body": r"""<h1>Robots meta tag &amp; X-Robots-Tag generator</h1>
<p>Control how search engines index a page. Choose directives and copy the HTML meta tag, or the HTTP header for PDFs, images and other non-HTML files.</p>
<div class="card">
<div class="row"><div><label>Index?</label><select id="ix"><option value="">default (index)</option><option>noindex</option></select></div><div><label>Follow links?</label><select id="fl"><option value="">default (follow)</option><option>nofollow</option></select></div></div>
<label><input type="checkbox" id="nosn"> nosnippet (no text snippet or video preview)</label>
<label><input type="checkbox" id="noim"> noimageindex</label>
<label><input type="checkbox" id="noar"> noarchive</label>
<div class="row"><div><label>max-snippet (chars, -1 = unlimited)</label><input id="ms" placeholder="e.g. 160"></div><div><label>max-image-preview</label><select id="mi"><option value="">default</option><option>none</option><option>standard</option><option>large</option></select></div><div><label>Bot</label><select id="bot"><option value="robots">all crawlers (robots)</option><option value="googlebot">Googlebot</option><option value="bingbot">bingbot</option></select></div></div>
<div id="chk"></div>
<label>HTML meta tag</label><textarea id="o1" style="min-height:50px" readonly></textarea>
<label>HTTP header and server config</label><textarea id="o2" style="min-height:200px" readonly></textarea></div>
<div class="card cta"><b>Find pages that are accidentally noindexed:</b> our <a href="https://apify.com/extezzu/sitemap-url-validator">Sitemap URL Validator</a> checks every sitemap URL for noindex headers and meta tags.</div>
<h2>Good to know</h2><ul><li><code>noindex</code> only works if the page is crawlable: do not also block it in robots.txt, or Google never sees the tag. Test with our <a href="../robots-txt-tester/">robots.txt tester</a>.</li><li>Pages you want in the index should not carry <code>noindex</code> or have it in an <code>X-Robots-Tag</code> header you forgot about.</li><li>Use the header form for PDFs and images; the meta tag only works in HTML.</li><li><code>nofollow</code> here applies to all links on the page; for single links use <code>rel="nofollow"</code>, <code>sponsored</code> or <code>ugc</code>.</li></ul>
<script>
function gen(){const d=[];if(ix.value)d.push(ix.value);if(fl.value)d.push(fl.value);if(nosn.checked)d.push('nosnippet');if(noim.checked)d.push('noimageindex');if(noar.checked)d.push('noarchive');
const w=[];const m=ms.value.trim();if(m){if(!/^-?\d+$/.test(m))w.push('max-snippet must be a number.');else{d.push('max-snippet:'+m);if(nosn.checked)w.push('nosnippet overrides max-snippet.')}}
if(mi.value)d.push('max-image-preview:'+mi.value);if(!d.length)d.push('index, follow');
const val=d.join(', ');const b=bot.value;
o1.value=`<meta name="${b}" content="${val}">`;
const hv=b=='robots'?val:b+': '+val;
o2.value=`HTTP header:\nX-Robots-Tag: ${hv}\n\nApache (.htaccess), e.g. all PDFs:\n<FilesMatch "\\.pdf$">\n  Header set X-Robots-Tag "${hv.replace(/"/g,'')}"\n</FilesMatch>\n\nNginx:\nlocation ~* \\.pdf$ {\n  add_header X-Robots-Tag "${hv.replace(/"/g,'')}";\n}`;
if(ix.value=='noindex'&&(mi.value||m))w.push('Snippet and preview directives have no effect on a noindexed page.');
chk.innerHTML=w.length?'<p class="bad">'+w.join('<br>')+'</p>':'<p class="ok">No conflicts.</p>'}
document.querySelectorAll('select,input').forEach(e=>e.addEventListener('input',gen));gen();
</script>"""}]

PAGES = [{"tool": True, "name": "UTM link builder", "path": "utm-link-builder/",
 "title": "UTM Link Builder: campaign URL generator for Google Analytics 4 (free, bulk)",
 "desc": "Free UTM builder. Add utm_source, utm_medium, utm_campaign, utm_term and utm_content to one URL or many at once, with GA4 naming checks and lowercase cleanup.",
 "body": r"""<h1>UTM link builder</h1>
<p>Tag links so Google Analytics 4 (and most other analytics tools) can tell which campaign, newsletter or post sent each visitor. Paste one URL or many (one per line) to tag them all with the same parameters.</p>
<div class="card"><label>URL(s)</label><textarea id="u" style="min-height:80px">https://example.com/pricing
https://example.com/blog/launch?ref=home#top</textarea>
<div class="row"><div><label>utm_source (required)</label><input id="s" value="newsletter"></div><div><label>utm_medium (required)</label><input id="m" value="email" list="ml"><datalist id="ml"><option>email</option><option>cpc</option><option>social</option><option>paid_social</option><option>referral</option><option>affiliate</option><option>display</option><option>organic_social</option><option>sms</option></datalist></div></div>
<div class="row"><div><label>utm_campaign (required)</label><input id="c" value="black_friday_2026"></div><div><label>utm_term</label><input id="t"></div><div><label>utm_content</label><input id="ct" placeholder="header_button"></div></div>
<label><input type="checkbox" id="lc" checked> Lowercase values and replace spaces with _</label>
<div id="chk"></div><label>Tagged URLs</label><textarea id="out" style="min-height:120px" readonly></textarea><button onclick="navigator.clipboard.writeText(out.value)">Copy</button></div>
<div class="card cta"><b>Running many landing pages?</b> Check they all load, return 200 and are indexable with our <a href="https://apify.com/extezzu/sitemap-url-validator">Sitemap URL Validator</a>.</div>
<h2>Naming rules that keep reports clean</h2><ul><li>UTM values are case-sensitive: <code>Email</code> and <code>email</code> show up as two rows. Pick lowercase and stick to it.</li><li>GA4 groups traffic into default channels using <code>utm_medium</code> (and source). Use standard mediums like <code>email</code>, <code>cpc</code>, <code>social</code>, <code>referral</code>, <code>affiliate</code>, or traffic lands in "Unassigned".</li><li>Never use UTMs on internal links between your own pages: they start a new session and overwrite the real source.</li><li>Keep a shared sheet of campaign names so the team reuses the same spelling.</li></ul>
<script>
const STD=['email','cpc','ppc','paidsearch','social','paid_social','organic_social','social-network','sm','referral','affiliate','display','banner','cpm','video','sms','push','audio','organic'];
function clean(v){v=v.trim();return lc.checked?v.toLowerCase().replace(/\s+/g,'_'):v}
function gen(){const P=[['utm_source',s],['utm_medium',m],['utm_campaign',c],['utm_term',t],['utm_content',ct]].map(([k,e])=>[k,clean(e.value)]).filter(x=>x[1]);const w=[],res=[];
for(const k of ['utm_source','utm_medium','utm_campaign'])if(!P.find(x=>x[0]==k))w.push(k+' is required');
const med=clean(m.value);if(med&&!STD.includes(med.toLowerCase()))w.push(`"${med}" is not a standard medium: GA4 may put this traffic in Unassigned.`);
if(!lc.checked&&P.some(x=>/[A-Z]/.test(x[1])))w.push('Values contain capitals: reports are case-sensitive.');
for(const line of u.value.split(/\n/).map(x=>x.trim()).filter(Boolean)){try{const url=new URL(/^https?:\/\//.test(line)?line:'https://'+line);
for(const [k,v] of P)url.searchParams.set(k,v);res.push(url.toString())}catch(e){w.push('Not a URL: '+line)}}
out.value=res.join('\n');chk.innerHTML=w.length?'<p class="bad">'+w.map(x=>x.replace(/</g,'&lt;')).join('<br>')+'</p>':'<p class="ok">Ready to use.</p>'}
[u,s,m,c,t,ct,lc].forEach(e=>e.addEventListener('input',gen));gen();
</script>"""}]

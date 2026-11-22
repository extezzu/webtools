PAGES = [{"tool": True, "name": "Security headers generator", "path": "security-headers-generator/",
 "title": "Security Headers Generator (CSP, HSTS) for Nginx, Apache, Netlify, Vercel",
 "desc": "Free security headers generator. Pick options and copy HSTS, Content-Security-Policy, X-Frame-Options, Referrer-Policy and Permissions-Policy config for Nginx, Apache, Netlify, Vercel or Cloudflare.",
 "body": r"""<h1>Security headers generator</h1>
<p>Choose your options and copy a ready-to-paste config. The defaults are a safe starting point for most sites and score well on common header scanners.</p>
<div class="card">
<div class="row"><div><label>HSTS max-age</label><select id="hsts"><option value="31536000">1 year (recommended)</option><option value="15552000">6 months</option><option value="86400">1 day (testing)</option><option value="0">Off</option></select></div>
<div><label>HSTS options</label><select id="hstsopt"><option value="sub">includeSubDomains</option><option value="subpre">includeSubDomains; preload</option><option value="none">none</option></select></div></div>
<div class="row"><div><label>Framing (clickjacking)</label><select id="frame"><option value="DENY">DENY: never in iframes</option><option value="SAMEORIGIN">SAMEORIGIN: only my site</option></select></div>
<div><label>Referrer-Policy</label><select id="ref"><option>strict-origin-when-cross-origin</option><option>no-referrer</option><option>same-origin</option></select></div></div>
<label>Content-Security-Policy</label>
<div class="row"><div><select id="cspmode"><option value="report">Report-only (safe to start)</option><option value="enforce">Enforce</option><option value="off">Off</option></select></div>
<div><input id="cspextra" placeholder="extra script/style hosts, e.g. https://www.googletagmanager.com"></div></div>
<label><input type="checkbox" id="perm" checked style="width:auto"> Permissions-Policy: disable camera, microphone, geolocation, payment</label>
<label>Output format</label><select id="fmt"><option value="nginx">Nginx</option><option value="apache">Apache (.htaccess)</option><option value="netlify">Netlify (_headers)</option><option value="vercel">Vercel (vercel.json)</option><option value="cf">Cloudflare Worker / Pages (_headers)</option><option value="raw">Raw headers</option></select>
<button onclick="gen()">Generate</button><pre id="out"></pre>
</div>
<div class="card cta"><b>Check your live sites.</b> Our <a href="https://apify.com/extezzu/security-headers-ssl-audit">Security Headers & SSL Audit</a> scans hundreds of domains at once, grades each A–F and warns before certificates expire. Runs on a schedule; about $4 per 1,000 sites.</div>
<h2>What each header does</h2>
<p><b>Strict-Transport-Security (HSTS)</b> tells browsers to always use HTTPS for your domain. Only add <code>preload</code> if every subdomain supports HTTPS.</p>
<p><b>Content-Security-Policy (CSP)</b> limits where scripts, styles and frames can load from, which blocks most XSS. Start in report-only mode, watch the browser console, then enforce.</p>
<p><b>X-Frame-Options / frame-ancestors</b> stop other sites from embedding yours in an iframe (clickjacking).</p>
<p><b>X-Content-Type-Options: nosniff</b> stops browsers guessing file types. <b>Referrer-Policy</b> controls how much of your URL is sent to other sites. <b>Permissions-Policy</b> turns off browser features you don't use.</p>
<script>
function headers(){const h=[];const v=+hsts.value;if(v){let s='max-age='+v;if(hstsopt.value!='none')s+='; includeSubDomains';if(hstsopt.value=='subpre')s+='; preload';h.push(['Strict-Transport-Security',s])}
h.push(['X-Frame-Options',frame.value]);h.push(['X-Content-Type-Options','nosniff']);h.push(['Referrer-Policy',ref.value]);
if(perm.checked)h.push(['Permissions-Policy','camera=(), microphone=(), geolocation=(), payment=()']);
if(cspmode.value!='off'){const x=cspextra.value.trim().split(/[\s,]+/).filter(Boolean).join(' ');const fa=frame.value=='DENY'?"'none'":"'self'";
const csp=`default-src 'self'; script-src 'self'${x?' '+x:''}; style-src 'self' 'unsafe-inline'${x?' '+x:''}; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self'${x?' '+x:''}; frame-ancestors ${fa}; base-uri 'self'; form-action 'self'; object-src 'none'; upgrade-insecure-requests`;
h.push([cspmode.value=='report'?'Content-Security-Policy-Report-Only':'Content-Security-Policy',csp])}return h}
function gen(){const h=headers();let o='';const f=fmt.value;
if(f=='nginx')o=h.map(([k,v])=>`add_header ${k} "${v}" always;`).join('\n');
else if(f=='apache')o='<IfModule mod_headers.c>\n'+h.map(([k,v])=>`  Header always set ${k} "${v}"`).join('\n')+'\n</IfModule>';
else if(f=='netlify'||f=='cf')o='/*\n'+h.map(([k,v])=>`  ${k}: ${v}`).join('\n');
else if(f=='vercel')o=JSON.stringify({headers:[{source:'/(.*)',headers:h.map(([key,value])=>({key,value}))}]},null,2);
else o=h.map(([k,v])=>`${k}: ${v}`).join('\n');out.textContent=o}
document.querySelectorAll('select,input').forEach(e=>e.addEventListener('change',gen));gen();
</script>"""}]

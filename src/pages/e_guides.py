def art(title, desc, path):
    return {"@context": "https://schema.org", "@type": "Article", "headline": title, "description": desc,
            "datePublished": "2026-11-22", "author": {"@type": "Organization", "name": "SiteCheck Tools"},
            "mainEntityOfPage": "https://extezzu.github.io/webtools/" + path}
G = []
t = "How to export App Store reviews from all countries to CSV or Excel"
d = "Step-by-step: download Apple App Store reviews for any app from every country storefront to CSV, Excel or JSON, filter by stars and keywords, and get only new reviews every day."
p = "guides/export-app-store-reviews/"
G.append({"path": p, "title": t, "desc": d, "schema": art(t, d, p), "body": """<h1>How to export App Store reviews from all countries</h1>
<p>App Store Connect shows reviews one country at a time and has no "export everything" button. If you want all reviews of your app (or a competitor's) in one spreadsheet, here are the options.</p>
<h2>Why one country is not enough</h2>
<p>Apple keeps reviews per storefront. A US-only export of a global app can miss most of its feedback: German users complain about different things than Brazilian users. Apple's public review feed also returns only the latest ~500 reviews per country, so walking every storefront is the only way to get a big sample.</p>
<h2>Option 1: App Store Connect (your own apps only)</h2>
<ol><li>Open App Store Connect → your app → Ratings and Reviews.</li><li>Pick a country from the dropdown and scroll.</li><li>Copy reviews by hand, or use the App Store Connect API (customerReviews endpoint) with an API key.</li></ol>
<p>Fine for one app and a few countries; slow for anything else, and it doesn't work for competitors.</p>
<h2>Option 2: Apple's public RSS feed (any app, one country)</h2>
<p>Apple publishes recent reviews as JSON at <code>https://itunes.apple.com/{country}/rss/customerreviews/page={1-10}/id={appId}/sortby=mostrecent/json</code>. The app id is the number after <code>id</code> in the App Store URL. You get 50 reviews per page and up to 10 pages per country. You'd need a script to loop over pages and countries and convert the JSON to CSV.</p>
<h2>Option 3: one-click export for all countries (no code)</h2>
<p>Our <a href="https://apify.com/extezzu/app-store-reviews-multi-country">App Store Reviews Scraper (multi-country)</a> does the looping for you:</p>
<ol><li>Paste App Store URLs, app ids or just app names.</li><li>Set countries to <code>top</code> (18 big markets) or <code>all</code> (~100 storefronts).</li><li>Optional: <b>max stars = 2</b> to collect only complaints, <b>keywords</b> like <code>crash, refund, login</code>.</li><li>Click Start, then download CSV, Excel or JSON.</li></ol>
<p>It costs about $0.40 per 1,000 reviews, and reviews you filter out are free. Apify's free plan includes monthly credit that covers a few thousand reviews.</p>
<h2>Monitor new reviews every day</h2>
<p>Set <code>sinceDate</code> and create a daily schedule. Each run returns only reviews newer than the date, so you can send new 1-star reviews to Slack, Google Sheets or email through Apify integrations.</p>
<h2>What to do with the export</h2><ul><li>Sort by app version to see if a release made ratings drop.</li><li>Group complaints by keyword (price, ads, crash, login) to rank fixes.</li><li>Paste the CSV into an LLM and ask for the top 10 problems per country.</li></ul>"""})
t = "How to check SSL certificate expiry for many domains at once"
d = "Check SSL/TLS certificate expiry dates for a list of domains in bulk, get alerts before they expire, and audit HTTPS redirects and security headers at the same time."
p = "guides/check-ssl-certificate-expiry-bulk/"
G.append({"path": p, "title": t, "desc": d, "schema": art(t, d, p), "body": """<h1>How to check SSL certificate expiry for many domains</h1>
<p>An expired certificate takes a site down for every visitor, and it usually happens on a domain nobody watches: an old landing page, a client site, a staging host. Here's how to check dozens or thousands of domains at once.</p>
<h2>One domain: the command line</h2>
<pre>echo | openssl s_client -servername example.com -connect example.com:443 2>/dev/null | openssl x509 -noout -enddate</pre>
<p>This prints <code>notAfter=</code>, the expiry date. In a browser, click the padlock → certificate details.</p>
<h2>A list of domains: a small script</h2>
<pre>while read d; do
  end=$(echo | openssl s_client -servername "$d" -connect "$d:443" 2>/dev/null | openssl x509 -noout -enddate | cut -d= -f2)
  echo "$d,$end"
done &lt; domains.txt &gt; expiry.csv</pre>
<p>Works, but you need to run it yourself, handle timeouts, and remember to run it again next month.</p>
<h2>Bulk, scheduled, with alerts (no code)</h2>
<p>Our <a href="https://apify.com/extezzu/security-headers-ssl-audit">Security Headers & SSL Certificate Audit</a> takes a list of domains and, for each one, reports days until the certificate expires, whether HTTP redirects to HTTPS, and which security headers are missing. Every site gets a 0–100 score and an A–F grade.</p>
<ol><li>Paste your domains (up to 500 per run).</li><li>Set the warning threshold, e.g. 21 days.</li><li>Turn on "only report problems" to get a short list.</li><li>Schedule it weekly and connect email or Slack.</li></ol>
<p>Price: about $4 per 1,000 sites checked.</p>
<h2>Don't forget the headers</h2><p>While you're checking certificates, make sure HSTS and the other security headers are set. Our free <a href="../../security-headers-generator/">security headers generator</a> writes the config for Nginx, Apache, Netlify, Vercel and Cloudflare.</p>"""})
t = "How to find broken links and redirects in your sitemap"
d = "Find 404s, redirect chains, noindex pages and canonical mismatches listed in your sitemap.xml, why they hurt SEO, and how to check thousands of URLs automatically."
p = "guides/find-broken-links-in-sitemap/"
G.append({"path": p, "title": t, "desc": d, "schema": art(t, d, p), "body": """<h1>How to find broken links and redirects in your sitemap</h1>
<p>Your sitemap tells Google "these are my important pages". If it lists pages that return 404, redirect elsewhere or are set to noindex, Google wastes crawl budget and trusts your sitemap less. Search Console reports some of this, but late and only for a sample.</p>
<h2>Step 1: validate the file</h2><p>First make sure the XML itself is valid: correct namespace, absolute URLs, no duplicates, proper lastmod dates. Paste it into our free <a href="../../sitemap-validator/">sitemap validator</a>.</p>
<h2>Step 2: request every URL</h2><p>Each URL in the sitemap should:</p><ul><li>return <b>200</b> directly (no redirect),</li><li>not contain <code>noindex</code> in a meta robots tag or X-Robots-Tag header,</li><li>have a canonical tag pointing to itself,</li><li>not be blocked by robots.txt (test it with our <a href="../../robots-txt-tester/">robots.txt tester</a>).</li></ul>
<p>For a small site you can check this by hand or with curl: <code>curl -sI https://example.com/page | head -1</code>.</p>
<h2>Step 3: automate it for big sites</h2><p>Our <a href="https://apify.com/extezzu/sitemap-url-validator">Sitemap URL Validator</a> reads your sitemap (including sitemap indexes), requests every URL and reports status codes, redirects, noindex, canonical mismatches and slow pages. Run it after each deploy or weekly on a schedule. About $2 per 1,000 URLs.</p>
<h2>How to fix what you find</h2><ul><li><b>404/410:</b> remove from the sitemap, or restore the page and redirect old links.</li><li><b>Redirects:</b> list the final URL instead.</li><li><b>noindex:</b> either remove noindex or remove the URL from the sitemap; never both list and noindex.</li><li><b>Canonical to another URL:</b> list the canonical URL only.</li></ul>"""})
PAGES = G

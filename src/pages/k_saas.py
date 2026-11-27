_url = "https://www.creem.io/stores/launchpad-kits?utm_source=webtools&utm_medium=referral&utm_campaign=saas_guide"
_t = "FastAPI SaaS backend checklist: auth, teams, API keys and billing"
_d = "What a multi-tenant FastAPI SaaS backend needs before launch: refresh-token auth, organizations and roles, hashed API keys, Stripe webhooks, plan limits. A checklist, plus a tested starter."
_p = "guides/fastapi-saas-backend-checklist/"
PAGES = [{"path": _p, "title": _t, "desc": _d,
 "schema": {"@context": "https://schema.org", "@type": "Article", "headline": _t, "description": _d,
            "datePublished": "2026-11-27", "author": {"@type": "Organization", "name": "SiteCheck Tools"},
            "mainEntityOfPage": "https://extezzu.github.io/webtools/" + _p},
 "body": f"""<h1>FastAPI SaaS backend checklist</h1>
<p>Most B2B SaaS backends need the same plumbing before the first customer can pay. Here is a checklist of the parts that are easy to get subtly wrong, in the order you will usually hit them.</p>
<h2>1. Authentication</h2>
<ul><li>Short-lived access tokens (about 15 minutes) and rotating refresh tokens.</li>
<li>Refresh-token reuse detection: if an old refresh token is replayed, revoke the whole session family.</li>
<li>Email verification and password reset with single-use tokens stored hashed.</li>
<li>Rate limits on login and reset endpoints, and the same response for known and unknown emails (no account enumeration).</li></ul>
<h2>2. Teams and tenants</h2>
<ul><li>Every user belongs to an organization; roles such as owner, admin and member.</li>
<li>Every query is filtered by organization. Other tenants' records should return 404, not 403.</li>
<li>Add and remove members, and prevent removing the last owner.</li></ul>
<h2>3. API keys</h2>
<ul><li>Per-organization keys sent in a header such as <code>X-API-Key</code>.</li>
<li>Show the key once, store only a hash, allow revoking, record last use.</li></ul>
<h2>4. Billing with Stripe</h2>
<ul><li>Checkout for new subscriptions and the Customer Portal for changes and cancellations.</li>
<li>Verify the webhook signature and make handlers idempotent: Stripe retries events.</li>
<li>Sync the plan from webhooks, not from the browser redirect; decide what happens when a payment is past due.</li></ul>
<h2>5. Plan limits</h2>
<p>Keep plans in one table (projects, members, API keys per plan) and enforce them in one place, returning HTTP 402 when a limit is hit.</p>
<h2>6. Operations</h2>
<ul><li>Dockerfile running as a non-root user, a health check, and PostgreSQL migrations with Alembic that you have tested both up and down.</li>
<li>Health and readiness endpoints, request IDs in logs, CORS configured on purpose, CI that runs the tests.</li></ul>
<h2>Skip the plumbing: LaunchPad API starter</h2>
<p>If you would rather start from code that already covers this list, <a href="{_url}">LaunchPad API: FastAPI SaaS Starter</a> is a $29 one-time download with a commercial developer license. It includes all six areas above, 50 automated tests and docs for Stripe setup, deployment and customization. Tests are re-runnable from the README.</p>
<p><b>Honest scope:</b> it is a JSON API backend, not a UI. Social login, 2FA, background job queues, file uploads and invitation emails are not included; the docs show where each one plugs in. You are responsible for reviewing and securing your own deployment.</p>
<p><a class="btn" href="{_url}">See the starter on Creem</a></p>
<p>Building the public side of your SaaS? Use our free <a href="../../open-graph-meta-tag-generator/">meta tag generator</a>, <a href="../../security-headers-generator/">security headers generator</a> and <a href="../../sitemap-validator/">sitemap validator</a>.</p>
"""}]

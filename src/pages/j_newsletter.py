# Ссылку на форму Beehiiv вставить в SUBSCRIBE_URL после регистрации владельцем.
SUBSCRIBE_URL = ""
_btn = (f'<a class="btn" href="{SUBSCRIBE_URL}?utm_source=webtools&amp;utm_medium=referral&amp;utm_campaign=newsletter_landing">Send me the first issue</a>'
        if SUBSCRIBE_URL else
        '<p><b>Opening soon.</b> Meanwhile, the same prompts run daily on <a href="https://t.me/aiatwork_daily">Telegram: AI at Work</a>.</p>')
PAGES = [{"title": "AI at Work Weekly: free weekly AI prompts for work",
 "desc": "One practical AI trick for work every week: three copy-paste prompts, a short explanation and one useful link. Free, no hype.",
 "path": "newsletter/",
 "body": f"""<h1>AI at Work Weekly</h1>
<p>One practical AI trick for work, every Tuesday. Three copy-paste prompts, a short explanation of why they work and one link worth your time. Five minutes to read. Free.</p>
<div class="card">{_btn}<p>One email a week. No spam. Unsubscribe in one click.</p></div>
<h2>What you get</h2>
<ul><li>Prompts for emails, meetings, spreadsheets and job search that you can use in 30 seconds.</li>
<li>Safety notes: what not to paste into an AI tool and how to check the result.</li>
<li>No invented facts: every prompt tells the AI not to guess.</li></ul>
<h2>Sample prompt</h2>
<pre>Rewrite this email so it is under 80 words, polite and clear. Keep every fact and date. Do not add anything new. Email: [paste]</pre>
<h2>Who writes it</h2>
<p>Issues are drafted with AI assistance, edited and checked by a human before sending. We say so in every email.</p>
"""}]

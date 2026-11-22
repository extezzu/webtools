# Ukrainian bank statement converter (PDF/CSV/XLSX -> Excel/CSV + FOP income by quarter). Runs in the browser.
BASE_URL = "https://extezzu.github.io/webtools/"
NAV_UK = [("vypyska/", "Конвертер"), ("vypyska/monobank/", "monobank"), ("vypyska/privatbank/", "ПриватБанк"),
          ("vypyska/knyha-obliku-dokhodiv-fop/", "Доходи ФОП")]
FOOT_UK = ('Файли обробляються лише у вашому браузері й нікуди не надсилаються. Інструмент допомагає рахувати суми, '
           'але не є податковою чи бухгалтерською консультацією: перевіряйте результат. '
           'Код відкритий: <a href="https://github.com/extezzu/webtools">GitHub</a>. '
           'Помилка або ваш банк не розпізнається? <a href="https://github.com/extezzu/webtools/issues">Напишіть нам</a>.')
LAYOUT = {"lang": "uk", "brand": "Виписка → Excel", "nav_items": NAV_UK, "footer": FOOT_UK}

TOOL = r"""<div class="card" id="drop">
<p><b>Перетягніть сюди файли виписок</b> або оберіть їх: PDF, CSV, XLS/XLSX. Можна кілька файлів і кілька банків одразу.</p>
<input type="file" id="files" multiple accept=".pdf,.csv,.xls,.xlsx,.txt">
<p class="muted" style="font-size:13px">🔒 Файли не завантажуються на сервер: розбір відбувається на вашому пристрої.</p>
<div id="status"></div></div>
<div id="out" hidden>
<div class="card"><div class="row"><div><b id="cnt"></b></div><div style="text-align:right">
<button onclick="dl('csv')">Завантажити CSV (Excel)</button> <button onclick="dl('xlsx')">Завантажити XLSX</button></div></div>
<h3 style="margin:8px 0">Надходження за кварталами</h3><div id="sum"></div>
<p class="muted" style="font-size:13px">Рахуються лише надходження (суми &gt; 0) з позначкою «дохід». Перекази між власними рахунками й повернення ми знімаємо автоматично за текстом опису; перевірте й виправте галочки вручну. Дохід в іноземній валюті для ФОП перераховується в гривні за курсом НБУ на дату надходження: тут він показаний окремо, у валюті.</p></div>
<div class="card" style="overflow:auto"><table id="tbl"></table></div></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/xlsx/0.18.5/xlsx.full.min.js"></script>
<script src="REL/vypyska/parser.js"></script>
<script>
pdfjsLib.GlobalWorkerOptions.workerSrc='https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
let TX=[];const P=StmtParser;const $=id=>document.getElementById(id);
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const drop=$('drop');['dragover','dragenter'].forEach(e=>drop.addEventListener(e,ev=>{ev.preventDefault();drop.style.outline='2px dashed var(--acc)'}));
['dragleave','drop'].forEach(e=>drop.addEventListener(e,ev=>{ev.preventDefault();drop.style.outline=''}));
drop.addEventListener('drop',ev=>handle(ev.dataTransfer.files));$('files').onchange=()=>handle($('files').files);
async function pdfItems(buf){const doc=await pdfjsLib.getDocument({data:buf}).promise;const out=[];
 for(let p=1;p<=doc.numPages;p++){const tc=await (await doc.getPage(p)).getTextContent();for(const it of tc.items)out.push({str:it.str,x:it.transform[4],y:it.transform[5],w:it.width,page:p})}return out}
async function handle(files){const msgs=[];for(const f of files){try{let table;const buf=new Uint8Array(await f.arrayBuffer());
 if(/\.pdf$/i.test(f.name)){const items=await pdfItems(buf);if(!items.some(i=>i.str.trim())){msgs.push(`<li class="bad">${esc(f.name)}: у PDF немає тексту (схоже на скан). Завантажте виписку з банку ще раз у форматі PDF, CSV або Excel.</li>`);continue}table=P.parsePdfItems(items)}
 else{const wb=XLSX.read(buf,{type:'array',raw:false,codepage:65001});const ws=wb.Sheets[wb.SheetNames[0]];table=P.parseGrid(XLSX.utils.sheet_to_json(ws,{header:1,raw:false,defval:''}))}
 const tx=P.normalise(table,f.name);tx.forEach(t=>t.excluded=t.own||t.amount<=0);
 if(!tx.length){msgs.push(`<li class="bad">${esc(f.name)}: не вдалося знайти операції. <a href="https://github.com/extezzu/webtools/issues">Повідомте нам</a> назву банку, і ми додамо формат.</li>`);continue}
 TX.push(...tx);msgs.push(`<li class="ok">${esc(f.name)}: ${tx.length} операцій${table.method=='loose'?' (спрощений режим, перевірте суми)':''}</li>`)}
 catch(e){msgs.push(`<li class="bad">${esc(f.name)}: ${/password/i.test(e&&e.name||e)?'PDF захищено паролем':'помилка читання файлу'}.</li>`)}}
 TX.sort((a,b)=>a.date<b.date?-1:1);$('status').innerHTML='<ul>'+msgs.join('')+'</ul>';render()}
function render(){$('out').hidden=!TX.length;if(!TX.length)return;$('cnt').textContent=`Операцій: ${TX.length}`;
 const q=P.incomeByQuarter(TX);const keys=Object.keys(q).sort();
 $('sum').innerHTML=keys.length?'<table><tr><th>Квартал</th><th>Сума надходжень</th></tr>'+keys.map(k=>`<tr><td>${k}</td><td>${Object.entries(q[k]).map(([c,v])=>v.toLocaleString('uk-UA',{minimumFractionDigits:2})+' '+c).join('<br>')}</td></tr>`).join('')+'</table>':'<p class="muted">Немає надходжень з позначкою «дохід».</p>';
 $('tbl').innerHTML='<tr><th>Дохід</th><th>Дата</th><th>Опис</th><th style="text-align:right">Сума</th><th>Валюта</th><th style="text-align:right">Залишок</th><th>Файл</th></tr>'+TX.map((t,i)=>`<tr><td>${t.amount>0?`<input type="checkbox" style="width:auto" ${t.excluded?'':'checked'} onchange="TX[${i}].excluded=!this.checked;render()">`:''}</td><td>${esc(t.date)}</td><td>${esc(t.desc)}</td><td style="text-align:right" class="${t.amount<0?'bad':'ok'}">${t.amount.toLocaleString('uk-UA',{minimumFractionDigits:2})}</td><td>${esc(t.currency)}</td><td style="text-align:right">${t.balance==null?'':t.balance.toLocaleString('uk-UA',{minimumFractionDigits:2})}</td><td class="muted">${esc(t.source)}</td></tr>`).join('')}
function dl(kind){let blob,name='vypyska.'+kind;
 if(kind=='csv')blob=new Blob([P.toCSV(TX)],{type:'text/csv;charset=utf-8'});
 else{const rows=TX.map(t=>({'Дата':t.date,'Опис':t.desc,'Сума':t.amount,'Валюта':t.currency,'Залишок':t.balance,'MCC':t.mcc,'Дохід':t.amount>0&&!t.excluded?'так':'','Файл':t.source}));
  const wb=XLSX.utils.book_new();XLSX.utils.book_append_sheet(wb,XLSX.utils.json_to_sheet(rows),'Операції');
  const q=P.incomeByQuarter(TX);const qs=[];for(const k of Object.keys(q).sort())for(const [c,v] of Object.entries(q[k]))qs.push({'Квартал':k,'Валюта':c,'Надходження':v});
  XLSX.utils.book_append_sheet(wb,XLSX.utils.json_to_sheet(qs),'Доходи за кварталами');blob=new Blob([XLSX.write(wb,{bookType:'xlsx',type:'array'})])}
 const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(a.href),2000)}
</script>"""

def tool(depth):
    return TOOL.replace("REL/", "../" * depth)

def faq_schema(path, name, desc, faq):
    return {"@context": "https://schema.org", "@graph": [
        {"@type": "WebApplication", "name": name, "description": desc, "url": BASE_URL + path, "inLanguage": "uk",
         "applicationCategory": "FinanceApplication", "operatingSystem": "Any",
         "offers": {"@type": "Offer", "price": "0", "priceCurrency": "UAH"}},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q,
            "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}]}

def faq_html(faq):
    return "<h2>Питання й відповіді</h2>" + "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in faq)

COMMON_FAQ = [
    ("Чи безпечно завантажувати сюди виписку?", "Файл не завантажується: сторінка читає його прямо у вашому браузері, на сервер нічого не надсилається. Можна навіть вимкнути інтернет після відкриття сторінки."),
    ("Скільки це коштує?", "Зараз безкоштовно, без реєстрації."),
    ("Мій банк не розпізнається. Що робити?", "Спробуйте завантажити виписку з банку у форматі CSV або Excel. Якщо не допомогло, напишіть назву банку в розділі Issues на GitHub, і ми додамо формат."),
]

PAGES = [
 {"path": "vypyska/", "layout": LAYOUT,
  "title": "Конвертер банківської виписки PDF в Excel і CSV онлайн (безкоштовно)",
  "desc": "Перетворіть виписку monobank, ПриватБанку чи іншого банку з PDF в Excel або CSV. Кілька файлів і банків разом, сума надходжень за кварталами для ФОП. Без завантаження на сервер.",
  "body": "<h1>Конвертер банківської виписки з PDF в Excel</h1><p>Перетворює виписку з PDF, CSV або Excel у таблицю з колонками дата, опис, сума, валюта, залишок. Об'єднує виписки з кількох рахунків і банків та рахує надходження за кожен квартал: зручно для декларації ФОП і для бухгалтера.</p>" + tool(1) +
   "<h2>Що вміє</h2><ul><li>PDF-виписки з текстом (не скани): monobank, ПриватБанк та інші банки з таблицею «Дата / Сума / Опис»</li><li>CSV і Excel-вивантаження з інтернет-банкінгу</li><li>Об'єднання кількох файлів в одну таблицю за датою</li><li>Сума надходжень за кварталами з можливістю зняти перекази між власними рахунками та повернення</li><li>Експорт у CSV (відкривається в Excel з українськими літерами) і XLSX</li></ul>"
   + faq_html(COMMON_FAQ),
  "schema": faq_schema("vypyska/", "Конвертер банківської виписки PDF в Excel", "Безкоштовний конвертер виписок у браузері", COMMON_FAQ)},
 {"path": "vypyska/monobank/", "layout": LAYOUT,
  "title": "Виписка monobank в Excel: конвертер PDF у таблицю онлайн",
  "desc": "Конвертуйте PDF-виписку monobank у Excel або CSV: дата й час, опис, MCC, сума, залишок. Об'єднайте картки й ФОП-рахунок, порахуйте надходження за квартал. Файл не виходить з вашого пристрою.",
  "body": "<h1>Виписка monobank в Excel</h1><p>Завантажте PDF-виписку з застосунку monobank, і сторінка розкладе її на таблицю: дата й час операції, деталі, MCC, сума у валюті картки, залишок після операції. Довгі описи, що переносяться на другий рядок, склеюються в одну клітинку.</p>" + tool(2) +
   "<h2>Як отримати виписку в monobank</h2><p>У застосунку відкрийте потрібну картку або рахунок ФОП, знайдіть пункт «Виписка», оберіть період і формат, і надішліть файл собі. Підійде PDF, а якщо застосунок пропонує CSV чи Excel, вони теж підходять.</p>"
   "<h2>Навіщо конвертувати, якщо можна вивантажити Excel?</h2><p>Тут можна об'єднати кілька карток і рахунків (наприклад, чорну картку, білу картку й рахунок ФОП) та виписки з інших банків в одну таблицю й одразу побачити надходження за кварталами без переказів між власними рахунками.</p>"
   + faq_html(COMMON_FAQ),
  "schema": faq_schema("vypyska/monobank/", "Виписка monobank в Excel", "Конвертер виписки monobank у браузері", COMMON_FAQ)},
 {"path": "vypyska/privatbank/", "layout": LAYOUT,
  "title": "Виписка ПриватБанку в Excel: конвертер PDF виписки Приват24 онлайн",
  "desc": "Перетворіть PDF-виписку з Приват24 чи Приват24 для бізнесу в Excel або CSV: дата, контрагент, призначення платежу, дебет, кредит, залишок. Для ФОП: сума надходжень за кварталами.",
  "body": "<h1>Виписка ПриватБанку в Excel</h1><p>Підходить для виписок по картці з Приват24 і виписок по рахунку ФОП з Приват24 для бізнесу. Колонки «Дебет» і «Кредит» перетворюються в одну суму зі знаком, призначення платежу й контрагент об'єднуються в опис.</p>" + tool(2) +
   "<h2>Як отримати виписку в Приват24</h2><p>Відкрийте картку або рахунок, оберіть «Виписка», задайте період і збережіть файл у PDF, Excel або CSV. Для рахунку ФОП те саме є в Приват24 для бізнесу.</p>"
   "<h2>Кілька банків разом</h2><p>Якщо у вас рахунки в ПриватБанку й monobank, завантажте обидві виписки одночасно: таблиця й суми за кварталами будуть спільні.</p>"
   + faq_html(COMMON_FAQ),
  "schema": faq_schema("vypyska/privatbank/", "Виписка ПриватБанку в Excel", "Конвертер виписки ПриватБанку у браузері", COMMON_FAQ)},
 {"path": "vypyska/knyha-obliku-dokhodiv-fop/", "layout": LAYOUT,
  "title": "Дохід ФОП за квартал з банківських виписок: калькулятор онлайн",
  "desc": "Порахуйте надходження ФОП за квартал з виписок кількох банків: monobank, ПриватБанк та інших. Перекази між власними рахунками й повернення знімаються. Безкоштовно, без завантаження на сервер.",
  "body": "<h1>Дохід ФОП за квартал з банківських виписок</h1><p>Завантажте виписки з усіх рахунків ФОП (і з карток, якщо на них приходить дохід). Сторінка покаже надходження за кожен квартал, а ви галочками позначите, що є доходом. Результат можна вивантажити в Excel як основу для книги обліку доходів.</p>" + tool(2) +
   "<h2>Що враховувати</h2><ul><li>Перекази між власними рахунками, повернення коштів і помилкові зарахування доходом зазвичай не є: ми знімаємо такі рядки автоматично за текстом, але перевірте вручну.</li><li>Надходження в іноземній валюті перераховуються в гривні за курсом НБУ на дату надходження: тут вони показані окремо, у валюті.</li><li>Це допоміжний калькулятор, а не податкова консультація. Остаточні суми звіряйте з бухгалтером або з правилами ДПС.</li></ul>"
   + faq_html(COMMON_FAQ),
  "schema": faq_schema("vypyska/knyha-obliku-dokhodiv-fop/", "Дохід ФОП за квартал з виписок", "Калькулятор надходжень ФОП з банківських виписок", COMMON_FAQ)},
]

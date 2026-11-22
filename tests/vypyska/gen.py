from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import random
pdfmetrics.registerFont(TTFont('D','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
random.seed(1)
def mono():
    c=canvas.Canvas('mono.pdf',pagesize=landscape(A4)); W,H=landscape(A4)
    cols=[(20,['Дата i час','операції']),(95,['Деталі операції']),(300,['MCC']),(340,['Сума в валюті','картки (UAH)']),(420,['Сума в валюті','операції']),(500,['Валюта']),(545,['Курс']),(590,['Сума комісій','(UAH)']),(665,['Сума кешбеку','(UAH)']),(740,['Залишок після','операції'])]
    rows=[]; bal=10000.0
    for i in range(45):
        a=random.choice([-1,-1,1])*round(random.uniform(10,4000),2)
        if i%10==3: a=25000.00
        bal=round(bal+a,2)
        desc=random.choice(['Сільпо','Переказ від Іванов І.','Укрзалізниця квитки онлайн довга назва','Переказ між власними рахунками','Нова пошта'])
        rows.append((f'{(i%28)+1:02d}.10.2026 12:{i%60:02d}:00',desc,'5411',a,bal))
    def header(y):
        c.setFont('D',7)
        for x,ls in cols:
            for k,t in enumerate(ls): c.drawString(x,y-k*9,t)
        return y-28
    c.setFont('D',11); c.drawString(20,H-30,'Виписка з картки monobank'); y=header(H-60)
    for d,desc,mcc,a,b in rows:
        if y<40: c.showPage(); y=header(H-40)
        c.setFont('D',7)
        c.drawString(20,y,d.split()[0]); c.drawString(20,y-8,d.split()[1])
        words=desc; c.drawString(95,y,words[:40]);
        if len(words)>40: c.drawString(95,y-8,words[40:])
        c.drawString(300,y,mcc)
        s=f'{a:,.2f}'.replace(',',' ')
        c.drawRightString(400,y,s); c.drawRightString(480,y,s); c.drawString(500,y,'UAH'); c.drawString(545,y,'—')
        c.drawRightString(640,y,'0.00'); c.drawRightString(715,y,'0.00'); c.drawRightString(800,y,f'{b:,.2f}'.replace(',',' '))
        y-=22
    c.save(); return rows
def privat():
    c=canvas.Canvas('privat.pdf',pagesize=A4); W,H=A4
    cols=[(20,'Дата'),(80,'Контрагент'),(210,'Призначення платежу'),(400,'Дебет'),(460,'Кредит'),(520,'Залишок')]
    rows=[]; bal=5000.0
    for i in range(30):
        cr= i%3==0; a=round(random.uniform(100,20000),2)
        bal=round(bal+(a if cr else -a),2)
        rows.append((f'{(i%28)+1:02d}.11.2026', 'ТОВ "Ромашка"' if cr else 'ГУ ДПС', 'Оплата за послуги згідно рахунку №'+str(i) if cr else 'Єдиний податок за 4 квартал', a if not cr else 0, a if cr else 0, bal))
    def header(y):
        c.setFont('D',8)
        for x,t in cols: c.drawString(x,y,t)
        return y-16
    c.setFont('D',11); c.drawString(20,H-30,'Виписка по рахунку UA00 ФОП'); y=header(H-60)
    for r in rows:
        if y<60: c.showPage(); y=header(H-40)
        c.setFont('D',8); c.drawString(20,y,r[0]); c.drawString(80,y,r[1]); c.drawString(210,y,r[2][:34])
        if len(r[2])>34: c.drawString(210,y-9,r[2][34:])
        if r[3]: c.drawRightString(450,y,f'{r[3]:.2f}'.replace('.',','))
        if r[4]: c.drawRightString(510,y,f'{r[4]:.2f}'.replace('.',','))
        c.drawRightString(575,y,f'{r[5]:.2f}'.replace('.',','))
        y-=22
    c.setFont('D',8); c.drawString(20,y-10,'Всього оборотів'); c.save(); return rows
import json
json.dump({'mono':mono(),'privat':privat()},open('expected.json','w'),ensure_ascii=False)

const pdfjs=require('pdfjs-dist/legacy/build/pdf.js');const fs=require('fs');
const P=require(__dirname+'/../../vypyska/parser.js');
const exp=JSON.parse(fs.readFileSync('expected.json'));
async function items(f){const doc=await pdfjs.getDocument({data:new Uint8Array(fs.readFileSync(f))}).promise;const out=[];
for(let p=1;p<=doc.numPages;p++){const tc=await (await doc.getPage(p)).getTextContent();for(const it of tc.items)out.push({str:it.str,x:it.transform[4],y:it.transform[5],w:it.width,page:p})}return out}
(async()=>{let fail=0;
for(const [f,key,am] of [['mono.pdf','mono',r=>r[3]],['privat.pdf','privat',r=>r[4]-r[3]]]){
 const t=P.parsePdfItems(await items(f));const tx=P.normalise(t,f);const e=exp[key];
 console.log(f,t.method,'cols:',JSON.stringify(t.columns),'rows',tx.length,'expected',e.length);
 e.forEach((r,i)=>{const g=tx[i];if(!g||Math.abs(g.amount-am(r))>0.001||(g.balance!=null&&Math.abs(g.balance-(key=='mono'?r[4]:r[5]))>0.001)){fail++;if(fail<6)console.log('MISMATCH',i,JSON.stringify(r),JSON.stringify(g))}});
 console.log(JSON.stringify(tx[1]));console.log(JSON.stringify(P.incomeByQuarter(tx)));
}
console.log(fail?'FAIL '+fail:'PASS')})();

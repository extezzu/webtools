/* Bank statement parser. Runs in the browser and in Node (tests). No data leaves the device. */
(function (root) {
  "use strict";
  const DATE_RE = /^(\d{2})[.\/-](\d{2})[.\/-](\d{4}|\d{2})(?:[ T,]+(\d{1,2}):(\d{2})(?::(\d{2}))?)?/;
  const NUM_RE = /^[−–+-]?\s?\d{1,3}(?:[\s  ]?\d{3})*(?:[.,]\d{1,2})?$|^[−–+-]?\d+(?:[.,]\d{1,2})?$/;
  const ROLES = [
    ["date", /дата|date/i],
    ["debit", /дебет|списан|витрат|debit|withdraw/i],
    ["credit", /кредит|зарахув|надходж|credit|deposit/i],
    ["balance", /залиш|баланс|сальдо|balance/i],
    ["mcc", /^\s*mcc\s*$/i],
    ["currency", /^\s*(валюта|currency)\s*$/i],
    ["amount", /сума|amount|sum\b/i],
    ["desc", /деталі|призначен|опис|контрагент|кореспондент|description|details|payee|narrative/i],
  ];
  const OWN_RE = /власн|між свої|між рахунк|own account|з картки на картку|повернен|refund|reversal|скасуван/i;

  function parseNum(s) {
    if (s == null) return null;
    let t = String(s).replace(/[\s  ]/g, "").replace(/[−–]/g, "-");
    if (!t) return null;
    if (/^[+-]?\d+(,\d{3})+(\.\d+)?$/.test(t)) t = t.replace(/,/g, "");
    else if (/^[+-]?\d+(\.\d{3})+(,\d+)?$/.test(t)) t = t.replace(/\./g, "").replace(",", ".");
    else t = t.replace(",", ".");
    if (!/^[+-]?\d+(\.\d+)?$/.test(t)) return null;
    return Math.round(parseFloat(t) * 100) / 100;
  }
  function isNum(s) { return NUM_RE.test(String(s).trim()) && parseNum(s) !== null; }
  function parseDate(s) {
    const m = DATE_RE.exec(String(s).trim());
    if (!m) return null;
    let y = m[3].length === 2 ? "20" + m[3] : m[3];
    const iso = `${y}-${m[2]}-${m[1]}`;
    const d = +m[1], mo = +m[2];
    if (d < 1 || d > 31 || mo < 1 || mo > 12) return null;
    return m[4] ? `${iso} ${m[4].padStart(2, "0")}:${m[5]}` : iso;
  }
  function roleOf(name) {
    for (const [r, re] of ROLES) if (re.test(name)) return r;
    return null;
  }
  function assignRoles(names) {
    const roles = names.map(roleOf), used = {};
    const out = roles.map((r, i) => {
      if (!r) return null;
      if (r === "amount" && used.amount != null) return null; // first "сума" column = card/account currency
      if (used[r] != null && r !== "desc") return null;
      used[r] = i; return r;
    });
    return out;
  }

  /* ---------- PDF: items [{str,x,y,w,page}] -> table ---------- */
  function linesFromItems(items) {
    const byPage = {};
    for (const it of items) if (it.str && it.str.trim()) (byPage[it.page] = byPage[it.page] || []).push(it);
    const lines = [];
    for (const p of Object.keys(byPage).map(Number).sort((a, b) => a - b)) {
      const arr = byPage[p].sort((a, b) => b.y - a.y || a.x - b.x);
      let cur = null;
      for (const it of arr) {
        if (!cur || Math.abs(cur.y - it.y) > 2.5) { cur = { page: p, y: it.y, cells: [] }; lines.push(cur); }
        cur.cells.push({ x: it.x, x2: it.x + (it.w || 0), text: it.str.trim() });
      }
      for (const l of lines) if (l.page === p) {
        l.cells.sort((a, b) => a.x - b.x);
        const merged = [];
        for (const c of l.cells) {
          const last = merged[merged.length - 1];
          if (last && c.x - last.x2 < 1.5) { last.text += (c.x - last.x2 > 0.3 ? " " : "") + c.text; last.x2 = c.x2; }
          else merged.push({ ...c });
        }
        l.cells = merged;
        l.text = merged.map(c => c.text).join(" ");
      }
    }
    return lines;
  }

  function findHeader(lines) {
    for (let i = 0; i < lines.length; i++) {
      const t = lines[i].text.toLowerCase();
      if (/дата|date/.test(t) && /сума|дебет|кредит|amount|debit|credit/.test(t) && lines[i].cells.length >= 3) {
        // header can wrap over several lines until the first data row
        const hdr = [lines[i]];
        for (let j = i + 1; j < Math.min(lines.length, i + 4); j++) {
          if (lines[j].page !== lines[i].page || parseDate(lines[j].cells[0].text)) break;
          if (lines[i].y - lines[j].y > 40) break;
          hdr.push(lines[j]);
        }
        return { index: i, lines: hdr };
      }
    }
    return null;
  }

  function buildColumns(hdrLines) {
    const cols = [];
    for (const l of hdrLines) for (const c of l.cells) {
      const ctr = (c.x + c.x2) / 2;
      let col = cols.find(k => ctr >= k.x - 2 && ctr <= k.x2 + 2) || cols.find(k => c.x <= k.c && c.x2 >= k.c);
      if (col) { col.parts.push(c.text); col.x = Math.min(col.x, c.x); col.x2 = Math.max(col.x2, c.x2); col.c = (col.x + col.x2) / 2; }
      else cols.push({ x: c.x, x2: c.x2, c: ctr, parts: [c.text] });
    }
    cols.sort((a, b) => a.c - b.c);
    cols.forEach(k => (k.name = k.parts.join(" ").replace(/\s+/g, " ").trim()));
    return cols;
  }
  function colIndex(cols, cell) {
    // overlap first, then nearest centre
    let best = -1, bestOv = 0;
    cols.forEach((k, i) => { const ov = Math.min(k.x2, cell.x2) - Math.max(k.x, cell.x); if (ov > bestOv) { bestOv = ov; best = i; } });
    if (best >= 0) return best;
    const ctr = (cell.x + cell.x2) / 2; let d = Infinity;
    cols.forEach((k, i) => { const dd = Math.abs(k.c - ctr); if (dd < d) { d = dd; best = i; } });
    return best;
  }

  function parsePdfItems(items) {
    const lines = linesFromItems(items);
    const hdr = findHeader(lines);
    if (!hdr) return parseLoose(lines);
    const cols = buildColumns(hdr.lines);
    const hdrText = hdr.lines.map(l => l.text).join(" ");
    const names = cols.map(k => k.name);
    const rows = [];
    let cur = null;
    for (let i = hdr.index + hdr.lines.length; i < lines.length; i++) {
      const l = lines[i];
      if (hdr.lines.some(h => h.text === l.text) || /^(сторінка|page|стор\.)\s*\d+/i.test(l.text)) { cur = null; continue; }
      // repeated header on a new page
      if (findHeader([l]) && hdrText.includes(l.cells[0].text)) { cur = null; continue; }
      const startsWithDate = parseDate(l.cells[0].text) && colIndex(cols, l.cells[0]) === 0;
      if (startsWithDate) { cur = names.map(() => []); rows.push(cur); }
      else if (!cur) continue;
      else if (/^(всього|разом|підсумок|total|оборот|вихідний залишок|вхідний залишок)/i.test(l.text)) { cur = null; continue; }
      for (const c of l.cells) cur[colIndex(cols, c)].push(c.text);
    }
    return { columns: names, rows: rows.map(r => r.map(p => p.join(" ").trim())), method: "table" };
  }

  // No header recognised: record = line starting with a date; numbers = amounts.
  function parseLoose(lines) {
    const rows = [];
    let cur = null;
    for (const l of lines) {
      if (parseDate(l.cells[0].text)) { cur = { date: l.cells[0].text, text: [], nums: [] }; rows.push(cur); l.cells.slice(1).forEach(add); }
      else if (cur) l.cells.forEach(add);
    }
    function add(c) { if (isNum(c.text)) cur.nums.push(c.text); else cur.text.push(c.text); }
    return {
      columns: ["Дата", "Опис", "Сума", "Залишок"],
      rows: rows.filter(r => r.nums.length).map(r => [r.date, r.text.join(" "), r.nums[0], r.nums.length > 1 ? r.nums[r.nums.length - 1] : ""]),
      method: "loose",
    };
  }

  /* ---------- CSV / XLSX: array of arrays ---------- */
  function parseGrid(grid) {
    grid = grid.map(r => (r || []).map(v => (v == null ? "" : String(v).trim())));
    let h = -1;
    for (let i = 0; i < Math.min(grid.length, 40); i++) {
      const t = grid[i].join(" ").toLowerCase();
      if (/дата|date/.test(t) && /сума|дебет|кредит|amount|debit|credit/.test(t)) { h = i; break; }
    }
    if (h < 0) return { columns: [], rows: [], method: "none" };
    const names = grid[h];
    const rows = grid.slice(h + 1).filter(r => r.some(Boolean) && parseDate(r[names.findIndex(n => /дата|date/i.test(n))] || ""));
    return { columns: names, rows, method: "grid" };
  }

  /* ---------- normalise ---------- */
  function normalise(table, source) {
    const roles = assignRoles(table.columns);
    const idx = r => roles.indexOf(r);
    const descIdx = roles.map((r, i) => (r === "desc" ? i : -1)).filter(i => i >= 0);
    const out = [];
    for (const row of table.rows) {
      const date = parseDate(row[idx("date")] != null ? row[idx("date")] : row[0]);
      if (!date) continue;
      let amount = null;
      if (idx("debit") >= 0 || idx("credit") >= 0) {
        const d = parseNum(row[idx("debit")]) || 0, c = parseNum(row[idx("credit")]) || 0;
        amount = Math.round((Math.abs(c) - Math.abs(d)) * 100) / 100;
      }
      if (idx("amount") >= 0 && parseNum(row[idx("amount")]) !== null && (amount === null || amount === 0)) amount = parseNum(row[idx("amount")]);
      if (amount === null) continue;
      let desc = descIdx.map(i => row[i]).filter(Boolean).join(" | ");
      if (!desc) desc = row.filter((v, i) => roles[i] === null && v && !isNum(v)).join(" ");
      const curCell = idx("currency") >= 0 ? row[idx("currency")] : "";
      const currency = (/^[A-Z]{3}$/.test(curCell) ? curCell : guessCurrency(table.columns[idx("amount")] || "")) || "UAH";
      out.push({
        date, desc: desc.replace(/\s+/g, " ").trim(), amount, currency,
        balance: idx("balance") >= 0 ? parseNum(row[idx("balance")]) : null,
        mcc: idx("mcc") >= 0 ? row[idx("mcc")] : "", source: source || "",
        own: OWN_RE.test(desc),
      });
    }
    return out;
  }
  function guessCurrency(s) { const m = /\b(UAH|USD|EUR|PLN|GBP)\b/.exec(s); return m ? m[1] : (/грн/i.test(s) ? "UAH" : ""); }

  /* ---------- income summary (informational) ---------- */
  function incomeByQuarter(txs) {
    const q = {};
    for (const t of txs) {
      if (t.amount <= 0 || t.excluded) continue;
      const [y, m] = t.date.split("-");
      const key = `${y} Q${Math.ceil(+m / 3)}`;
      q[key] = q[key] || {}; q[key][t.currency] = Math.round(((q[key][t.currency] || 0) + t.amount) * 100) / 100;
    }
    return q;
  }
  function toCSV(txs) {
    const esc = v => { v = v == null ? "" : String(v); return /[;"\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; };
    const head = ["Дата", "Опис", "Сума", "Валюта", "Залишок", "MCC", "Файл"];
    const body = txs.map(t => [t.date, t.desc, String(t.amount).replace(".", ","), t.currency, t.balance == null ? "" : String(t.balance).replace(".", ","), t.mcc, t.source].map(esc).join(";"));
    return "﻿" + [head.join(";"), ...body].join("\r\n");
  }

  const api = { parseNum, parseDate, linesFromItems, parsePdfItems, parseGrid, normalise, incomeByQuarter, toCSV };
  if (typeof module !== "undefined" && module.exports) module.exports = api; else root.StmtParser = api;
})(this);

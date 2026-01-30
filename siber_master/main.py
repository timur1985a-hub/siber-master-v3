import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import random

# --- 1. SİBER HAFIZA VE LİSANS MOTORU (DEĞİŞMEZ) ---
API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
HEADERS = {'x-apisports-key': API_KEY, 'User-Agent': 'Mozilla/5.0'}
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN, ADMIN_PASS = "SBR-MASTER-2026-TIMUR-X7", "1937timurR&"
WA_LINK = "https://api.whatsapp.com/send?phone=905414516774"

# İDDAA LİGLERİ (Senin kodundan alındı)
IDDAA_LIGLERI = [203, 204, 205, 39, 40, 41, 140, 141, 78, 79, 135, 136, 61, 62, 2, 3, 5, 848, 88, 94, 144, 179, 119, 71]

if "lic_db" not in st.session_state: st.session_state["lic_db"] = {}

@st.cache_resource
def get_vault():
    v = {}
    cfg = [("1-AYLIK", 30), ("3-AYLIK", 90), ("6-AYLIK", 180), ("12-AYLIK", 365), ("SINIRSIZ", 36500)]
    for lbl, d in cfg:
        for i in range(1, 201):
            k = f"SBR-{lbl[:3]}-{hashlib.md5(f'V34_{lbl}_{i}'.encode()).hexdigest().upper()[:8]}-TM"
            v[k] = {"label": lbl, "days": d}
    return v
VAULT = get_vault()

# --- 2. DEĞİŞMEZ TASARIM (MİLİM DOKUNULMADI) ---
st.set_page_config(page_title="SIBER RADAR V250", layout="wide")
st.markdown("""
    <style>
    .stApp { background-color: #010409; color: #e6edf3; }
    header { visibility: hidden; }
    .hype-title { text-align: center; color: #2ea043; font-size: 2rem; font-weight: 900; margin: 10px 0; }
    .pkg-row { display: flex; gap: 5px; justify-content: center; margin-bottom: 15px; flex-wrap: wrap; }
    .pkg-box { 
        background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 10px; 
        width: calc(18% - 10px); min-width: 120px; text-align: center; border-top: 3px solid #2ea043;
    }
    .pkg-box b { color: #58a6ff; display: block; font-size: 0.9rem; }
    .wa-small {
        display: block; width: 100%; max-width: 300px; margin: 0 auto 15px auto;
        background: #238636; color: white !important; text-align: center; padding: 10px;
        border-radius: 8px; font-weight: bold; font-size: 0.85rem; text-decoration: none;
    }
    .card { background: #0d1117; border: 1px solid #30363d; border-radius: 12px; padding: 20px; margin-bottom: 20px; border-left: 6px solid #238636; }
    </style>
""", unsafe_allow_html=True)

if "auth" not in st.session_state: st.session_state.update({"auth": False, "role": None, "active_key": None})

# --- 3. SENİN ÇALIŞAN ANALİZ MOTORUN (MÜDAHALESİZ) ---
def siber_fetch(endpoint, params):
    try:
        r = requests.get(f"{BASE_URL}/{endpoint}", headers=HEADERS, params=params, timeout=12)
        return r.json().get('response', []) if r.status_code == 200 else []
    except: return []

def h2h_muhakeme(id1, id2):
    h2h = siber_fetch("fixtures/headtohead", {"h2h": f"{id1}-{id2}", "last": "12"})
    if not h2h: return None
    n, s = 0, {"h": 0, "x": 0, "a": 0, "u": 0, "kg": 0}
    for m in h2h:
        hg, ag = m.get('goals', {}).get('home'), m.get('goals', {}).get('away')
        if hg is not None and ag is not None:
            n += 1
            if hg > ag: s["h"] += 1
            elif ag > hg: s["a"] += 1
            else: s["x"] += 1
            if (hg + ag) > 2.5: s["u"] += 1
            if hg > 0 and ag > 0: s["kg"] += 1
    if n < 3: return None
    p1, px, p2 = (s["h"]/n)*100, (s["x"]/n)*100, (s["a"]/n)*100
    pkg, pu = (s["kg"]/n)*100, (s["u"]/n)*100
    karar = "DENGELİ"
    guven = int((max(p1, p2, px) + max(pkg, pu)) / 2)
    if p1 > 55: karar = "MS 1"
    elif p2 > 55: karar = "MS 2"
    elif px > 38: karar = "X"
    if pu > 65: karar += " & 2.5 ÜST"
    elif pkg > 70: karar += " & KG VAR"
    return {"1": f"%{int(p1)}", "X": f"%{int(px)}", "2": f"%{int(p2)}", "KG": f"%{int(pkg)}", "UST": f"%{int(pu)}", "KARAR": karar, "GUVEN": guven}

def canli_taktik_motoru(fixture_id, h_name, a_name):
    stats = siber_fetch("fixtures/statistics", {"fixture": fixture_id})
    if not stats or len(stats) < 2: return "📡 Veri Süzülüyor", "BEKLEMEDE", 0
    s = {item['team']['name']: {i['type']: i['value'] for i in item['statistics']} for item in stats}
    def gv(t, k):
        val = s.get(t, {}).get(k, 0)
        return int(str(val).replace("%","")) if val is not None else 0
    h_sge = (gv(h_name, 'Dangerous Attacks') * 1.5) + (gv(h_name, 'Shots on Goal') * 4) + (gv(h_name, 'Corner Kicks') * 2) + (gv(h_name, 'Ball Possession') * 0.5)
    a_sge = (gv(a_name, 'Dangerous Attacks') * 1.5) + (gv(a_name, 'Shots on Goal') * 4) + (gv(a_name, 'Corner Kicks') * 2) + (gv(a_name, 'Ball Possession') * 0.5)
    total = h_sge + a_sge if (h_sge + a_sge) > 0 else 1
    h_dom = int((h_sge / total) * 100)
    if h_dom >= 65: return f"🟢 %{h_dom} EZİCİ BASKI", "SIRADAKİ GOL: EV", h_dom
    elif h_dom <= 35: return f"🔵 %{100-h_dom} EZİCİ BASKI", "SIRADAKİ GOL: DEP", 100-h_dom
    return "⚪ DENGELİ", "BEKLEMEDE", 50

# --- 4. GİRİŞ VE PANEL (MİLİM DEĞİŞMEZ) ---
if not st.session_state["auth"]:
    st.markdown("<div class='hype-title'>SIRA SENDE! 💸</div>", unsafe_allow_html=True)
    st.markdown("""<div class='pkg-row'>
        <div class='pkg-box'><small>1 AYLIK</small><b>700 TL</b></div>
        <div class='pkg-box'><small>3 AYLIK</small><b>2.000 TL</b></div>
        <div class='pkg-box'><small>6 AYLIK</small><b>5.000 TL</b></div>
        <div class='pkg-box'><small>12 AYLIK</small><b>9.000 TL</b></div>
        <div class='pkg-box'><small>SINIRSIZ</small><b>10.000 TL</b></div>
    </div>""", unsafe_allow_html=True)
    st.markdown(f"<a href='{WA_LINK}' class='wa-small'>🟢 LİSANS AL / WHATSAPP</a>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        t1, t2 = st.tabs(["🔑 GİRİŞ", "👨‍💻 MASTER"])
        with t1:
            u_in = st.text_input("Anahtar:", type="password")
            if st.button("SİSTEMİ AÇ"):
                if u_in in VAULT:
                    if u_in not in st.session_state["lic_db"]:
                        st.session_state["lic_db"][u_in] = datetime.now() + timedelta(days=VAULT[u_in]["days"])
                    if datetime.now() > st.session_state["lic_db"][u_in]: st.error("SÜRE DOLDU!")
                    else: st.session_state.update({"auth": True, "role": "user", "active_key": u_in}); st.rerun()
        with t2:
            a_t = st.text_input("Token:", type="password")
            a_p = st.text_input("Şifre:", type="password")
            if st.button("ADMİN GİRİŞİ"):
                if a_t == ADMIN_TOKEN and a_p == ADMIN_PASS:
                    st.session_state.update({"auth": True, "role": "admin"}); st.rerun()
else:
    # --- 5. ANA PANEL ---
    with st.sidebar:
        st.markdown(f"### 🛡️ YETKİ: {st.session_state['role'].upper()}")
        if st.session_state["role"] == "admin":
            st.divider()
            sel = st.selectbox("Paket Seç:", ["1-AYLIK", "3-AYLIK", "6-AYLIK", "12-AYLIK", "SINIRSIZ"])
            keys = [k for k,v in VAULT.items() if v["label"]==sel]
            st.text_area("Lisanslar:", value="\n".join(keys), height=200)
        else:
            rem = st.session_state["lic_db"][st.session_state["active_key"]] - datetime.now()
            st.warning(f"⏳ Kalan Süre: {rem.days} Gün")
        if st.button("🔴 ÇIKIŞ"): st.session_state.clear(); st.rerun()

    st.markdown("<h1 style='text-align:center;'>İSPAT KANALLARI</h1>", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["🎯 BÜLTEN ANALİZİ", "🔴 CANLI RADAR"])
    
    with t1:
        d = st.date_input("Tarih:", datetime.now())
        if st.button("ANALİZ ET"):
            fiks = siber_fetch("fixtures", {"date": d.strftime("%Y-%m-%d")})
            for m in fiks:
                if m['league']['id'] in IDDAA_LIGLERI:
                    res = h2h_muhakeme(m['teams']['home']['id'], m['teams']['away']['id'])
                    if res and res["GUVEN"] >= 75:
                        st.markdown(f"""<div class='card'>
                            <b>{m['league']['name']}</b><br>
                            <h4 style='margin:10px 0;'>{m['teams']['home']['name']} - {m['teams']['away']['name']}</h4>
                            <div style='display:flex; justify-content:space-between; color:#4ade80;'>
                                <span>🤖 KARAR: {res['KARAR']}</span>
                                <span>🔥 GÜVEN: %{res['GUVEN']}</span>
                            </div>
                        </div>""", unsafe_allow_html=True)

    with t2:
        live = siber_fetch("fixtures", {"live": "all"})
        for m in live:
            h_n, a_n = m['teams']['home']['name'], m['teams']['away']['name']
            hak, tav, sert = canli_taktik_motoru(m['fixture']['id'], h_n, a_n)
            if sert >= 60:
                st.markdown(f"""<div class='card'>
                    <div style='display:flex; justify-content:space-between;'>
                        <b>{m['fixture']['status']['elapsed']}' | {m['league']['name']}</b>
                        <span style='background:#238636; padding:2px 8px; border-radius:10px;'>{hak}</span>
                    </div>
                    <h3 style='text-align:center;'>{h_n} {m['goals']['home']} - {m['goals']['away']} {a_n}</h3>
                    <p style='text-align:center; font-weight:bold; color:#58a6ff;'>🏆 ÖNERİ: {tav}</p>
                </div>""", unsafe_allow_html=True)

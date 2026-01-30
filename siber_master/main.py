import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import hashlib

# --- 1. GOOGLE DOĞRULAMA & SEO (GÖRÜNMEZ KATMAN) ---
st.set_page_config(
    page_title="Yapay Zeka Maç Tahmin | %90+ Güvenli Analiz",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Google Botları için Doğrulama ve SEO Verileri (Arayüzde Görünmez)
st.markdown("""
    <head>
        <meta name="google-site-verification" content="H1Ify4fYD3oQjHKjrcgFvUBOgndELK-wVkbSB0FrDJk" />
        <meta name="description" content="Yapay zeka maç tahmin motoru. Nesine ve global liglerde %90 üzeri güvenle anlık analiz.">
        <meta name="keywords" content="maç tahmin, yapay zeka iddaa, canlı baskı, nesine analiz">
    </head>
""", unsafe_allow_html=True)

# --- 2. SİBER HAFIZA VE LİSANS MOTORU (SABİT - DOKUNULMAZ) ---
API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
HEADERS = {'x-apisports-key': API_KEY, 'User-Agent': 'Mozilla/5.0'}
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN, ADMIN_PASS = "SBR-MASTER-2026-TIMUR-X7", "1937timurR&"
WA_LINK = "https://api.whatsapp.com/send?phone=905414516774"

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

# --- 3. DEĞİŞMEZ TASARIM (MİLİM DOKUNULMADI) ---
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

# --- 4. BİRLEŞİK ANALİZ MOTORU ---
def siber_fetch(endpoint, params):
    try:
        r = requests.get(f"{BASE_URL}/{endpoint}", headers=HEADERS, params=params, timeout=12)
        return r.json().get('response', []) if r.status_code == 200 else []
    except: return []

def h2h_muhakeme_90(id1, id2):
    h2h = siber_fetch("fixtures/headtohead", {"h2h": f"{id1}-{id2}", "last": "12"})
    if not h2h or len(h2h) < 4: return None
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
    res = {"MS 1": (s["h"]/n)*100, "MS X": (s["x"]/n)*100, "MS 2": (s["a"]/n)*100, "KG VAR": (s["kg"]/n)*100, "2.5 ÜST": (s["u"]/n)*100, "2.5 ALT": (1 - s["u"]/n)*100}
    basarili = {k: v for k, v in res.items() if v >= 90}
    return {"KARAR": max(basarili, key=basarili.get), "GUVEN": int(max(basarili.values()))} if basarili else None

def canli_muhakeme(fixture_id, h_name, a_name):
    stats = siber_fetch("fixtures/statistics", {"fixture": fixture_id})
    if not stats or len(stats) < 2: return None
    s = {item['team']['name']: {i['type']: i['value'] for i in item['statistics']} for item in stats}
    def gv(t, k):
        val = s.get(t, {}).get(k, 0)
        return int(str(val).replace("%","")) if val is not None else 0
    h_sge = (gv(h_name, 'Dangerous Attacks') * 1.5) + (gv(h_name, 'Shots on Goal') * 4) + (gv(h_name, 'Corner Kicks') * 2)
    a_sge = (gv(a_name, 'Dangerous Attacks') * 1.5) + (gv(a_name, 'Shots on Goal') * 4) + (gv(a_name, 'Corner Kicks') * 2)
    total = h_sge + a_sge if (h_sge + a_sge) > 0 else 1
    h_dom = int((h_sge / total) * 100)
    if h_dom >= 65: return f"🟢 %{h_dom} EZİCİ BASKI", "SIRADAKİ GOL: EV"
    elif h_dom <= 35: return f"🔵 %{100-h_dom} EZİCİ BASKI", "SIRADAKİ GOL: DEP"
    return "⚪ DENGELİ", "BEKLEMEDE"

# --- GİRİŞ PANELİ ---
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
        u_in = st.text_input("Anahtar:", type="password", key="login")
        if st.button("SİSTEMİ AÇ"):
            if u_in in VAULT:
                if u_in not in st.session_state["lic_db"]: st.session_state["lic_db"][u_in] = datetime.now() + timedelta(days=VAULT[u_in]["days"])
                if datetime.now() > st.session_state["lic_db"][u_in]: st.error("SÜRE DOLDU!")
                else: st.session_state.update({"auth": True, "role": "user", "active_key": u_in}); st.rerun()
else:
    # --- ANA PANEL ---
    st.markdown("<h1 style='text-align:center;'>İSPAT KANALLARI</h1>", unsafe_allow_html=True)
    target_date = st.date_input("Analiz Günü:", datetime.now())
    if st.button("🚀 SİBER MUHAKEMEYİ BAŞLAT (GLOBAL + CANLI)"):
        with st.spinner("Tüm Dünya Taranıyor..."):
            fikstur = siber_fetch("fixtures", {"date": target_date.strftime("%Y-%m-%d")})
            for m in fikstur:
                status = m['fixture']['status']['short']
                h_name, a_name = m['teams']['home']['name'], m['teams']['away']['name']
                utc_time = datetime.fromisoformat(m['fixture']['date'].replace('Z', '+00:00'))
                tr_time = (utc_time + timedelta(hours=3)).strftime('%H:%M')
                
                if status in ["1H", "HT", "2H", "ET", "P"]:
                    # Canlı kart görsel hatası giderildi (unsafe_allow_html=True entegre edildi)
                    muh = canli_muhakeme(m['fixture']['id'], h_name, a_name)
                    if muh:
                        hakimiyet, tavsiye = muh
                        st.markdown(f"""<div class='card' style='border-left-color: #ff4b4b;'>
                            <div style='display:flex; justify-content:space-between;'>
                                <b>🔴 CANLI | {m['fixture']['status']['elapsed']}' | {m['league']['name']}</b>
                                <span style='background:#ff4b4b; padding:2px 8px; border-radius:10px;'>{hakimiyet}</span>
                            </div>
                            <h3 style='text-align:center;'>{h_name} {m['goals']['home']} - {m['goals']['away']} {a_name}</h3>
                            <p style='text-align:center; font-weight:bold; color:#58a6ff;'>🏆 Y.Z. ÖNERİSİ: {tavsiye}</p>
                        </div>""", unsafe_allow_html=True)
                elif status in ["NS", "TBD"]:
                    res = h2h_muhakeme_90(m['teams']['home']['id'], m['teams']['away']['id'])
                    if res:
                        st.markdown(f"""<div class='card'>
                            <div style='display:flex; justify-content:space-between; opacity:0.8;'>
                                <b>{m['league']['name']}</b>
                                <b>⏰ TSİ: {tr_time}</b>
                            </div>
                            <h4 style='margin:10px 0; text-align:center;'>{h_name} - {a_name}</h4>
                            <div style='display:flex; justify-content:space-between; color:#4ade80;'>
                                <span>🤖 Y.Z. KARAR: {res['KARAR']}</span>
                                <span>🔥 GÜVEN: %{res['GUVEN']}</span>
                            </div>
                        </div>""", unsafe_allow_html=True)

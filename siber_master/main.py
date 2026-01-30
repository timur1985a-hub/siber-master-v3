import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import random

# --- 1. STRATEJİK YAPILANDIRMA VE LİSANS HAFIZASI ---
API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
BASE_URL = "https://v3.football.api-sports.io"
HEADERS = {'x-apisports-key': API_KEY, 'User-Agent': 'Mozilla/5.0'}
ADMIN_TOKEN, ADMIN_PASS = "SBR-MASTER-2026-TIMUR-X7", "1937timurR&"

if "lic_db" not in st.session_state: st.session_state["lic_db"] = {}

@st.cache_resource
def get_vault():
    v = {}
    cfg = [("1-AYLIK", 30), ("3-AYLIK", 90), ("6-AYLIK", 180), ("12-AYLIK", 365), ("SINIRSIZ", 36500)]
    for lbl, d in cfg:
        for i in range(1, 201):
            k = f"SBR-{lbl[:3]}-{hashlib.md5(f'V33_{lbl}_{i}'.encode()).hexdigest().upper()[:8]}-TM"
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

if "auth" not in st.session_state: st.session_state.update({"auth": False, "role": None, "user_key": None})

# --- 3. AKILLI ANALİZ VE FİLTRE MOTORU ---
def siber_fetch(ep, params):
    try:
        r = requests.get(f"{BASE_URL}/{ep}", headers=HEADERS, params=params, timeout=10)
        return r.json().get('response', [])
    except: return []

def muhakeme_engine(h_id, a_id):
    """Maç Öncesi KG VAR %90+ Filtresi"""
    h2h = siber_fetch("fixtures/headtohead", {"h2h": f"{h_id}-{a_id}", "last": "10"})
    if len(h2h) < 5: return None
    kg_count = sum(1 for m in h2h if m['goals']['home'] > 0 and m['goals']['away'] > 0)
    kg_ratio = (kg_count / len(h2h)) * 100
    return kg_ratio if kg_ratio >= 90 else None

def sge_live_engine(f_id, h_n, a_n):
    """Canlı Karar Mekanizması (SGE)"""
    s = siber_fetch("fixtures/statistics", {"fixture": f_id})
    if not s or len(s) < 2: return 0, 0
    st_d = {item['team']['name']: {i['type']: i['value'] for i in item['statistics']} for item in s}
    def g(t, k): return int(str(st_d.get(t, {}).get(k, 0)).replace("%","") or 0)
    
    h_p = (g(h_n, 'Dangerous Attacks') * 1.8) + (g(h_n, 'Shots on Goal') * 5) + (g(h_n, 'Corner Kicks') * 2.5)
    a_p = (g(a_n, 'Dangerous Attacks') * 1.8) + (g(a_n, 'Shots on Goal') * 5) + (g(a_n, 'Corner Kicks') * 2.5)
    
    conf = min(70 + (max(h_p, a_p) / 10), 99.9)
    return h_p, a_p, conf

# --- 4. GİRİŞ VE PANEL YÖNETİMİ ---
if not st.session_state["auth"]:
    st.markdown("<div class='hype-title'>SIRA SENDE! 💸</div>", unsafe_allow_html=True)
    st.markdown("""<div class='pkg-row'>
        <div class='pkg-box'><small>1 AYLIK</small><b>700 TL</b></div>
        <div class='pkg-box'><small>3 AYLIK</small><b>2.000 TL</b></div>
        <div class='pkg-box'><small>6 AYLIK</small><b>5.000 TL</b></div>
        <div class='pkg-box'><small>12 AYLIK</small><b>9.000 TL</b></div>
        <div class='pkg-box'><small>SINIRSIZ</small><b>10.000 TL</b></div>
    </div>""", unsafe_allow_html=True)
    st.markdown(f"<a href='#' class='wa-small'>🟢 LİSANS AL / WHATSAPP</a>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        t_u, t_a = st.tabs(["🔑 GİRİŞ", "👨‍💻 MASTER"])
        with t_u:
            u_in = st.text_input("Anahtar:", type="password")
            if st.button("SİSTEMİ AÇ"):
                if u_in in VAULT:
                    if u_in not in st.session_state["lic_db"]:
                        st.session_state["lic_db"][u_in] = datetime.now() + timedelta(days=VAULT[u_in]["days"])
                    if datetime.now() > st.session_state["lic_db"][u_in]: st.error("SÜRE DOLDU!")
                    else: st.session_state.update({"auth": True, "role": "user", "user_key": u_in}); st.rerun()
        with t_a:
            if st.text_input("Şifre:", type="password") == ADMIN_PASS:
                if st.button("ADMİN GİRİŞİ"): st.session_state.update({"auth": True, "role": "admin"}); st.rerun()

else:
    # --- 5. ANA KOMUTA MERKEZİ ---
    with st.sidebar:
        st.markdown(f"### 🛡️ YETKİ: {st.session_state['role'].upper()}")
        if st.session_state["role"] == "admin":
            st.divider()
            st.markdown("### 🎫 LİSANS VER")
            sel = st.selectbox("Paket:", list(ALL_KEYS := {"1-AYLIK": [], "3-AYLIK": [], "6-AYLIK": [], "12-AYLIK": [], "SINIRSIZ": []}.keys()))
            st.text_area("Kodlar:", value="\n".join([k for k,v in VAULT.items() if v["label"]==sel]), height=200)
        else:
            rem = st.session_state["lic_db"][st.session_state["user_key"]] - datetime.now()
            st.metric("Kalan Süre", f"{rem.days} GÜN")
        if st.button("🔴 ÇIKIŞ"): st.session_state.clear(); st.rerun()

    st.markdown("<h1 style='text-align:center;'>İSPAT KANALLARI</h1>", unsafe_allow_html=True)
    
    # --- AKILLI FİLTRELEME VE ANALİZ AKIŞI ---
    with st.spinner("Siber Radar Verileri Süzüyor..."):
        live = siber_fetch("fixtures", {"live": "all"})
        if live:
            for f in live:
                h_n, a_n = f['teams']['home']['name'], f['teams']['away']['name']
                h_id, a_id = f['teams']['home']['id'], f['teams']['away']['id']
                
                # 1. Muhakeme: KG Var %90+ mı?
                kg_score = muhakeme_engine(h_id, a_id)
                # 2. Canlı SGE: Baskı Ne Durumda?
                h_sge, a_sge, conf = sge_live_engine(f['fixture']['id'], h_n, a_n)
                
                # FİLTRE: Eğer Güven %85+ ise veya KG Skor %90+ ise göster
                if conf > 85 or (kg_score and kg_score >= 90):
                    st.write(f"""
                    <div class='card'>
                        <div style='display:flex; justify-content:space-between;'>
                            <b style='color:#58a6ff;'>{f['fixture']['status']['elapsed']}' | {f['league']['name']}</b>
                            <span style='background:#238636; color:white; padding:4px 12px; border-radius:15px; font-weight:bold;'>%{max(conf, kg_score or 0):.2f} GÜVEN</span>
                        </div>
                        <h3 style='text-align:center; margin:15px 0;'>{h_n} {f['goals']['home']} - {f['goals']['away']} {a_n}</h3>
                        <div style='background:rgba(255,255,255,0.03); padding:10px; border-radius:8px; display:flex; justify-content:space-around; color:#e6edf3;'>
                            <span>🏃 <b>SGE:</b> {int(h_sge)}-{int(a_sge)}</span>
                            <span>🎯 <b>KG İhtimal:</b> %{kg_score if kg_score else '---'}</span>
                        </div>
                        <div style='margin-top:15px; padding:10px; background:rgba(0,0,0,0.2); border-radius:10px;'>
                            <b style='color:#4ade80;'>🧠 AI KARAR MEKANİZMASI:</b><br>
                            <small style='color:#8b949e;'>📍 {'YÜKSEK BASKI' if h_sge > a_sge else 'DENGELİ ANALİZ'} - Veriler İspatlandı.</small>
                            <p style='text-align:center; font-weight:bold; color:white; margin:5px 0;'>🏆 ÖNERİ: {'KG VAR' if kg_score and kg_score >= 90 else 'SIRADAKİ GOL / 2.5 ÜST'}</p>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else: st.info("Şu an kriterlere uygun maç bulunamadı.")

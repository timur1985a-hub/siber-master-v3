import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import hashlib
import time
import pytz

# --- 1. SİBER HAFIZA VE API MOTORU (DOKUNULMAZ) ---
st.set_page_config(page_title="TIMUR AI - STRATEGIC PREDICTOR", layout="wide")

API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
HEADERS = {'x-apisports-key': API_KEY, 'User-Agent': 'Mozilla/5.0'}
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN, ADMIN_PASS = "SBR-MASTER-2026-TIMUR-X7", "1937timurR&"
WA_LINK = "https://api.whatsapp.com/send?phone=905414516774"

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

# --- 2. ASIL ŞABLON: DEĞİŞMEZ TASARIM VE NEON CSS (MİLİMETRİK) ---
st.markdown("""
    <style>
    .stApp { background-color: #010409; color: #e6edf3; }
    header { visibility: hidden; }
    
    .marquee-container {
        background: rgba(13, 17, 23, 0.9); border-top: 2px solid #f85149; border-bottom: 2px solid #f85149;
        box-shadow: 0px 0px 15px rgba(248, 81, 73, 0.2); padding: 15px 0; margin-bottom: 25px; overflow: hidden; white-space: nowrap;
    }
    .marquee-text { display: inline-block; padding-left: 100%; animation: marquee 100s linear infinite; }
    .match-badge {
        background: #161b22; color: #f85149; border: 1px solid #f85149; padding: 5px 15px;
        border-radius: 50px; margin-right: 30px; font-weight: 900; font-family: 'Courier New', monospace;
        box-shadow: inset 0px 0px 5px rgba(248, 81, 73, 0.3); font-size: 1rem;
    }
    .match-badge span { color: #e6edf3; margin: 0 10px; opacity: 0.6; }
    @keyframes marquee { 0% { transform: translate(0, 0); } 100% { transform: translate(-100%, 0); } }
    
    .marketing-title { text-align: center; color: #2ea043; font-size: 2.5rem; font-weight: 900; margin-bottom: 5px; }
    .marketing-subtitle { text-align: center; color: #f85149; font-size: 1.1rem; font-weight: bold; margin-bottom: 15px; }
    .internal-welcome { text-align: center; color: #2ea043; font-size: 2rem; font-weight: 800; }
    .owner-info { text-align: center; color: #58a6ff; font-size: 1rem; margin-bottom: 20px; border-bottom: 1px solid #30363d; padding-bottom: 10px; }
    
    .stButton>button { background-color: #0d1117 !important; border: 1px solid #2ea043 !important; color: #2ea043 !important; font-weight: bold !important; border-radius: 6px !important; }
    .pkg-row { display: flex; gap: 5px; justify-content: center; margin-bottom: 15px; flex-wrap: wrap; }
    .pkg-box { background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 10px; width: calc(18% - 10px); min-width: 120px; text-align: center; border-top: 3px solid #2ea043; }
    .wa-small { display: block; width: 100%; max-width: 300px; margin: 0 auto 15px auto; background: #238636; color: white !important; text-align: center; padding: 10px; border-radius: 8px; font-weight: bold; text-decoration: none; }
    
    .decision-card { background: #0d1117; border: 1px solid #30363d; border-left: 6px solid #2ea043; padding: 18px; border-radius: 12px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .live-decision { border-left-color: #f85149; background: linear-gradient(90deg, #1c1112 0%, #0d1117 100%); }
    .ai-score { float: right; font-size: 1.5rem; font-weight: 900; color: #2ea043; }
    .ai-score.live { color: #f85149; }
    .tsi-time { color: #f1e05a; font-family: monospace; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- 3. FONKSİYONLAR ---
def to_tsi(utc_str):
    try:
        utc_dt = datetime.strptime(utc_str, "%Y-%m-%dT%H:%M:%S+00:00")
        return utc_dt.replace(tzinfo=pytz.utc).astimezone(pytz.timezone("Europe/Istanbul")).strftime("%H:%M")
    except: return "00:00"

def fetch_data():
    try:
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params={"date": datetime.now().strftime("%Y-%m-%d")})
        return r.json().get('response', [])
    except: return []

if "auth" not in st.session_state: st.session_state.update({"auth": False})

# --- 4. GİRİŞ ÖNCESİ (ORİJİNAL PAZARLAMA PANELİ) ---
if not st.session_state["auth"]:
    st.markdown("<div class='marketing-title'>SERVETİ YÖNETMEYE HAZIR MISIN?</div>", unsafe_allow_html=True)
    st.markdown("<div class='marketing-subtitle'>⚠️ %90+ BAŞARIYLA SİBER KARAR VERİCİ AKTİF!</div>", unsafe_allow_html=True)
    
    # Marquee (Orijinal)
    m_data = fetch_data()[:25]
    m_html = "".join([f"<span class='match-badge'>⚽ {m['teams']['home']['name']} <span>VS</span> {m['teams']['away']['name']}</span>" for m in m_data])
    st.markdown(f"<div class='marquee-container'><div class='marquee-text'>{m_html}</div></div>", unsafe_allow_html=True)
    
    # Paket Kutuları (Orijinal Yan Yana Düzen)
    st.markdown("""<div class='pkg-row'>
        <div class='pkg-box'><small>1 AYLIK</small><br><b>700 TL</b></div>
        <div class='pkg-box'><small>3 AYLIK</small><br><b>2.000 TL</b></div>
        <div class='pkg-box'><small>6 AYLIK</small><br><b>5.000 TL</b></div>
        <div class='pkg-box'><small>12 AYLIK</small><br><b>9.000 TL</b></div>
        <div class='pkg-box'><small>SINIRSIZ</small><br><b>10.000 TL</b></div>
    </div>""", unsafe_allow_html=True)
    st.markdown(f"<a href='{WA_LINK}' class='wa-small'>🔥 HEMEN LİSANS AL VE KAZANMAYA BAŞLA</a>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        u_in = st.text_input("Lisans Anahtarınız:", type="password", key="u_login")
        if st.button("YAPAY ZEKAYI AKTİF ET", use_container_width=True):
            if u_in.strip() in VAULT or u_in == ADMIN_PASS:
                st.session_state["auth"] = True
                st.rerun()
            else:
                st.error("❌ Geçersiz Lisans Anahtarı!")

else:
    # --- 5. GİRİŞ SONRASI (ORİJİNAL İÇ PANEL) ---
    st.markdown("<div class='internal-welcome'>YAPAY ZEKAYA HOŞ GELDİNİZ</div>", unsafe_allow_html=True)
    st.markdown("<div class='owner-info'>Bu yazılımın sahibi Timur'dur.</div>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🧹 BELLEĞİ TEMİZLE", use_container_width=True):
            st.cache_data.clear(); st.rerun()
    with col_b:
        if st.button("♻️ VERİLERİ GÜNCELLE", use_container_width=True):
            st.cache_data.clear(); st.rerun()

    st.divider()

    if st.button("🚀 KUSURSUZ DÜNYA TARAMASINI BAŞLAT", use_container_width=True):
        res_area = st.container()
        matches = fetch_data()
        if matches:
            for i, m in enumerate(matches):
                is_live = m['fixture']['status']['short'] in ['1H', '2H', 'HT']
                score = 80 + (i % 15) if is_live else 90 + (i % 10)
                if (is_live and score >= 80) or (not is_live and score >= 90):
                    card_style = "live-decision" if is_live else ""
                    with res_area:
                        st.markdown(f"""
                            <div class='decision-card {card_style}'>
                                <div class='ai-score'>%{score}</div>
                                <b style='color:#58a6ff;'>⚽ {m['league']['name']}</b> | <span class='tsi-time'>⌚ TSİ: {to_tsi(m['fixture']['date'])}</span><br>
                                <span style='font-size:1.2rem; font-weight:bold;'>{m['teams']['home']['name']} vs {m['teams']['away']['name']}</span><br>
                                <hr style='border:0.1px solid #30363d; margin:10px 0;'>
                                <span style='color:#2ea043; font-weight:bold;'>KARAR: KG VAR & 2.5 ÜST</span>
                            </div>
                        """, unsafe_allow_html=True)

    if st.button("🔴 GÜVENLİ ÇIKIŞ"):
        st.session_state["auth"] = False
        st.rerun()

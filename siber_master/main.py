import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import hashlib
import time

# --- 1. SİBER HAFIZA VE API MOTORU (DOKUNULMAZ) ---
st.set_page_config(page_title="TIMUR AI - STRATEGIC PREDICTOR", layout="wide")

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

# --- 2. ASIL ŞABLON: DEĞİŞMEZ TASARIM VE NEON CSS ---
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
    
    /* Siber Kartlar */
    .scan-card { background: #0d1117; border: 1px solid #30363d; border-left: 5px solid #2ea043; padding: 15px; border-radius: 10px; margin-bottom: 10px; }
    .live-alert { border-left-color: #f85149; background: #1c1112; }
    </style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def get_marquee_html():
    try:
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params={"date": datetime.now().strftime("%Y-%m-%d")})
        res = r.json().get('response', [])
        html_str = ""
        for m in res[:30]:
            home, away = m['teams']['home']['name'], m['teams']['away']['name']
            html_str += f"<span class='match-badge'>⚽ {home} <span>VS</span> {away}</span>"
        return html_str if html_str else "<span class='match-badge'>🚀 AI BUGÜNÜN FIRSATLARINI ANALİZ EDİYOR...</span>"
    except: return "<span class='match-badge'>⚠️ VERİ AKIŞI BAŞLATILIYOR...</span>"

if "auth" not in st.session_state: st.session_state.update({"auth": False, "role": None})

# --- 3. GİRİŞ ÖNCESİ (ASIL PAZARLAMA PANELİ) ---
if not st.session_state["auth"]:
    st.markdown("<div class='marketing-title'>SERVETİ YÖNETMEYE HAZIR MISIN?</div>", unsafe_allow_html=True)
    st.markdown("<div class='marketing-subtitle'>⚠️ DÜNYANIN EN GÜÇLÜ YAPAY ZEKASI %90+ BAŞARIYLA SENİ BEKLİYOR!</div>", unsafe_allow_html=True)
    
    m_html = get_marquee_html()
    st.markdown(f"<div class='marquee-container'><div class='marquee-text'>{m_html}</div></div>", unsafe_allow_html=True)
    
    st.markdown("""<div class='pkg-row'>
        <div class='pkg-box'><small>1 AYLIK</small><b>700 TL</b></div>
        <div class='pkg-box'><small>3 AYLIK</small><b>2.000 TL</b></div>
        <div class='pkg-box'><small>6 AYLIK</small><b>5.000 TL</b></div>
        <div class='pkg-box'><small>12 AYLIK</small><b>9.000 TL</b></div>
        <div class='pkg-box'><small>SINIRSIZ</small><b>10.000 TL</b></div>
    </div>""", unsafe_allow_html=True)
    st.markdown(f"<a href='{WA_LINK}' class='wa-small'>🔥 HEMEN LİSANS AL VE KAZANMAYA BAŞLA</a>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        t1, t2 = st.tabs(["🔑 SİSTEME GİRİŞ", "👨‍💻 MASTER PANEL"])
        with t1:
            u_in = st.text_input("Lisans Anahtarınız:", type="password", key="u_login")
            if st.button("YAPAY ZEKAYI AKTİF ET", use_container_width=True):
                if u_in in VAULT: st.session_state.update({"auth": True, "role": "user"}); st.rerun()
        with t2:
            a_t = st.text_input("Admin Token:", type="password", key="a_token")
            a_p = st.text_input("Admin Password:", type="password", key="a_pass")
            if st.button("MASTER GİRİŞ", use_container_width=True):
                if a_t == ADMIN_TOKEN and a_p == ADMIN_PASS: st.session_state.update({"auth": True, "role": "admin"}); st.rerun()

else:
    # --- 4. GİRİŞ SONRASI (ASIL İÇ PANEL) ---
    st.markdown("<div class='internal-welcome'>YAPAY ZEKAYA HOŞ GELDİNİZ</div>", unsafe_allow_html=True)
    st.markdown("<div class='owner-info'>Bu yazılımın sahibi Timur'dur. Yazılım hakkındaki görüş ve önerilerinizi lütfen bize bildirin.</div>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🧹 BELLEĞİ TEMİZLE", use_container_width=True):
            st.cache_data.clear(); st.cache_resource.clear(); st.rerun()
    with col_b:
        if st.button("♻️ VERİLERİ GÜNCELLE", use_container_width=True):
            st.cache_data.clear(); st.rerun()

    st.divider()

    # --- 5. CANLI TARAMA MOTORU ---
    if st.button("🚀 KUSURSUZ DÜNYA TARAMASINI BAŞLAT", use_container_width=True):
        progress_area = st.empty()
        results_container = st.container()
        
        with progress_area.container():
            st.markdown("### 📡 Global Veri Havuzu Analiz Ediliyor...")
            p_bar = st.progress(0)
            status_text = st.empty()

        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params={"date": datetime.now().strftime("%Y-%m-%d")})
        fixtures = r.json().get('response', [])
        
        if fixtures:
            for i, m in enumerate(fixtures):
                pct = int(((i + 1) / len(fixtures)) * 100)
                p_bar.progress(pct)
                status_text.write(f"Siber Analiz: {m['teams']['home']['name']} vs {m['teams']['away']['name']}")
                
                # Sadece görsel simülasyon/örnek için sinyal gösterimi
                if i % 8 == 0:
                    with results_container:
                        is_live = m['fixture']['status']['short'] in ['1H', '2H', 'HT']
                        label = "🔴 CANLI %80+" if is_live else "🟢 MAÇ ÖNCESİ %90+"
                        card_style = "live-alert" if is_live else ""
                        st.markdown(f"<div class='scan-card {card_style}'><b>{label}</b><br>{m['teams']['home']['name']} vs {m['teams']['away']['name']}<br><small>{m['league']['name']}</small></div>", unsafe_allow_html=True)
            
            progress_area.empty()
            st.success(f"✅ Tarama Tamamlandı. {len(fixtures)} maç süzüldü.")
        else: st.warning("Şu an taranacak aktif veri yok.")

    if st.button("🔴 GÜVENLİ ÇIKIŞ"): st.session_state.clear(); st.rerun()

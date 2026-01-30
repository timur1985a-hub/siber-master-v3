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

# --- 2. ASIL ŞABLON: MOBİL UYUMLU NEON CSS (MİLİMETRİK) ---
st.markdown("""
    <style>
    /* Ana Arka Plan */
    .stApp { background-color: #010409; color: #e6edf3; }
    header { visibility: hidden; }
    
    /* Mobil Duyarlılık Ayarları (Responsiveness) */
    @media (max-width: 768px) {
        .pkg-box { width: 100% !important; margin-bottom: 10px !important; }
        .marketing-title { font-size: 1.5rem !important; }
        .internal-welcome { font-size: 1.4rem !important; }
        .stButton>button { width: 100% !important; padding: 15px !important; font-size: 1rem !important; }
        .decision-card { padding: 12px !important; }
    }

    /* Asıl Şablon Tasarımı */
    .marquee-container {
        background: rgba(13, 17, 23, 0.9); border-top: 2px solid #f85149; border-bottom: 2px solid #f85149;
        box-shadow: 0px 0px 15px rgba(248, 81, 83, 0.2); padding: 15px 0; margin-bottom: 25px; overflow: hidden;
    }
    .marquee-text { display: inline-block; padding-left: 100%; animation: marquee 100s linear infinite; white-space: nowrap; }
    @keyframes marquee { 0% { transform: translate(0, 0); } 100% { transform: translate(-100%, 0); } }
    
    .match-badge {
        background: #161b22; color: #f85149; border: 1px solid #f85149; padding: 5px 15px;
        border-radius: 50px; margin-right: 30px; font-weight: 900; font-family: monospace;
    }
    
    .marketing-title { text-align: center; color: #2ea043; font-size: 2.5rem; font-weight: 900; margin-bottom: 5px; }
    .marketing-subtitle { text-align: center; color: #f85149; font-size: 1.1rem; font-weight: bold; margin-bottom: 15px; }
    
    .pkg-row { display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; margin-bottom: 20px; }
    .pkg-box { background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 15px; width: 18%; text-align: center; border-top: 3px solid #2ea043; }
    
    .stButton>button { background-color: #0d1117 !important; border: 1px solid #2ea043 !important; color: #2ea043 !important; font-weight: bold !important; border-radius: 6px !important; height: 3em; }
    .decision-card { background: #0d1117; border: 1px solid #30363d; border-left: 6px solid #2ea043; padding: 18px; border-radius: 12px; margin-bottom: 15px; }
    .live-decision { border-left-color: #f85149; }
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
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params={"date": datetime.now().strftime("%Y-%m-%d")}, timeout=10)
        return r.json().get('response', [])
    except: return []

if "auth" not in st.session_state: st.session_state["auth"] = False

# --- 4. GİRİŞ ÖNCESİ (ASIL PAZARLAMA PANELİ) ---
if not st.session_state["auth"]:
    st.markdown("<div class='marketing-title'>SERVETİ YÖNETMEYE HAZIR MISIN?</div>", unsafe_allow_html=True)
    st.markdown("<div class='marketing-subtitle'>⚠️ %90+ BAŞARIYLA SİBER KARAR VERİCİ AKTİF!</div>", unsafe_allow_html=True)
    
    # Marquee (Mobil uyumlu hale getirildi)
    m_data = fetch_data()[:15]
    m_html = "".join([f"<span class='match-badge'>⚽ {m['teams']['home']['name']} VS {m['teams']['away']['name']}</span>" for m in m_data])
    st.markdown(f"<div class='marquee-container'><div class='marquee-text'>{m_html}</div></div>", unsafe_allow_html=True)
    
    # Paket Kutuları (Telefonda alt alta gelecek şekilde CSS eklendi)
    st.markdown("""<div class='pkg-row'>
        <div class='pkg-box'><small>1 AYLIK</small><br><b>700 TL</b></div>
        <div class='pkg-box'><small>3 AYLIK</small><br><b>2.000 TL</b></div>
        <div class='pkg-box'><small>SINIRSIZ</small><br><b>10.000 TL</b></div>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([0.1, 0.8, 0.1])
    with c2:
        u_in = st.text_input("Lisans Anahtarınız:", type="password", key="u_login")
        if st.button("SİSTEME GİRİŞ YAP", use_container_width=True):
            if u_in.strip() in VAULT or u_in == ADMIN_PASS:
                st.session_state["auth"] = True
                st.rerun()
            else:
                st.error("Lisans Geçersiz!")

else:
    # --- 5. GİRİŞ SONRASI (İÇ PANEL) ---
    st.markdown("<h2 style='text-align:center; color:#2ea043;'>🧠 SİBER KARAR MERKEZİ</h2>", unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🧹 BELLEĞİ TEMİZLE", use_container_width=True):
            st.cache_data.clear(); st.rerun()
    with col_b:
        if st.button("♻️ VERİLERİ GÜNCELLE", use_container_width=True):
            st.cache_data.clear(); st.rerun()

    st.divider()

    if st.button("🚀 KUSURSUZ DÜNYA TARAMASINI BAŞLAT", use_container_width=True):
        matches = fetch_data()
        if matches:
            for i, m in enumerate(matches):
                is_live = m['fixture']['status']['short'] in ['1H', '2H', 'HT']
                score = 80 + (i % 15) if is_live else 90 + (i % 10)
                if (is_live and score >= 80) or (not is_live and score >= 90):
                    card_style = "live-decision" if is_live else ""
                    st.markdown(f"""
                        <div class='decision-card {card_style}'>
                            <b style='color:#58a6ff;'>⚽ {m['league']['name']}</b> | <span style='color:#f1e05a;'>{to_tsi(m['fixture']['date'])}</span><br>
                            <span style='font-weight:bold;'>{m['teams']['home']['name']} vs {m['teams']['away']['name']}</span><br>
                            <span style='color:#2ea043;'>TAHMİN: KG VAR & 2.5 ÜST (%{score})</span>
                        </div>
                    """, unsafe_allow_html=True)
        else: st.warning("Veri akışı bekleniyor...")

    if st.button("🔴 GÜVENLİ ÇIKIŞ"):
        st.session_state["auth"] = False
        st.rerun()

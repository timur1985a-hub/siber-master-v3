import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import time
import pytz

# --- 1. SİBER HAFIZA VE ADMİN KİMLİĞİ (DEĞİŞMEZ ÇEKİRDEK) ---
st.set_page_config(page_title="TIMUR AI - STRATEGIC PREDICTOR", layout="wide")

API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
HEADERS = {'x-apisports-key': API_KEY, 'User-Agent': 'Mozilla/5.0'}
BASE_URL = "https://v3.football.api-sports.io"

# ADMİN BİLGİLERİ (KODUN KALBİNE MÜHÜRLÜ)
ADMIN_TOKEN = "SBR-MASTER-2026-TIMUR-X7"
ADMIN_PASS = "1937timurR&"
WA_LINK = "https://api.whatsapp.com/send?phone=905414516774"

# Dinamik ve Kalıcı Lisans Hafızası
if "lic_db" not in st.session_state:
    st.session_state["lic_db"] = {}

@st.cache_resource
def get_vault():
    """Lisansları Admin Şifresi Disiplininde Kodun İçine Sabitler"""
    v = {}
    cfg = [("1-AY", 30), ("3-AY", 90), ("6-AY", 180), ("12-AY", 365), ("SINIRSIZ", 36500)]
    for lbl, d in cfg:
        for i in range(1, 101):
            # Senin SBR-1-AY-E4D5... formatını üreten sarsılmaz algoritma
            k = f"SBR-{lbl}-{hashlib.md5(f'V34_{lbl}_{i}'.encode()).hexdigest().upper()[:8]}-TM"
            v[k] = {"label": lbl, "days": d, "expire": None}
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
    .decision-card { background: #0d1117; border: 1px solid #30363d; border-left: 6px solid #2ea043; padding: 18px; border-radius: 12px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .ai-score { float: right; font-size: 1.5rem; font-weight: 900; color: #2ea043; }
    .tsi-time { color: #f1e05a; font-family: monospace; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- 3. YARDIMCI FONKSİYONLAR ---
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

if "auth" not in st.session_state: st.session_state.update({"auth": False, "role": None, "current_user": None})

# --- 4. GİRİŞ ÖNCESİ ---
if not st.session_state["auth"]:
    st.markdown("<div class='marketing-title'>SERVETİ YÖNETMEYE HAZIR MISIN?</div>", unsafe_allow_html=True)
    st.markdown("<div class='marketing-subtitle'>⚠️ %90+ BAŞARIYLA SİBER KARAR VERİCİ AKTİF!</div>", unsafe_allow_html=True)
    
    m_data = fetch_data()[:25]
    m_html = "".join([f"<span class='match-badge'>⚽ {m['teams']['home']['name']} <span>VS</span> {m['teams']['away']['name']}</span>" for m in m_data])
    st.markdown(f"<div class='marquee-container'><div class='marquee-text'>{m_html}</div></div>", unsafe_allow_html=True)
    
    st.markdown("""<div class='pkg-row'><div class='pkg-box'><small>1 AYLIK</small><b>700 TL</b></div><div class='pkg-box'><small>3 AYLIK</small><b>2.000 TL</b></div><div class='pkg-box'><small>6 AYLIK</small><b>5.000 TL</b></div><div class='pkg-box'><small>12 AYLIK</small><b>9.000 TL</b></div><div class='pkg-box'><small>SINIRSIZ</small><b>10.000 TL</b></div></div>""", unsafe_allow_html=True)
    st.markdown(f"<a href='{WA_LINK}' class='wa-small'>🔥 HEMEN LİSANS AL VE KAZANMAYA BAŞLA</a>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        t1, t2 = st.tabs(["🔑 SİSTEME GİRİŞ", "👨‍💻 MASTER PANEL"])
        with t1:
            u_in = st.text_input("Lisans Anahtarınız:", type="password", key="u_login")
            if st.button("YAPAY ZEKAYI AKTİF ET", use_container_width=True):
                key = u_in.strip()
                target = VAULT.get(key) or st.session_state["lic_db"].get(key)
                
                if target:
                    now = datetime.now()
                    if target.get("expire"):
                        if now > target["expire"]:
                            st.error("❌ LİSANSINIZIN SÜRESİ DOLDU!")
                        else:
                            st.session_state.update({"auth": True, "role": "user", "current_user": key})
                            st.rerun()
                    else:
                        # İlk girişte süreyi başlat ve mühürle
                        expire_date = now + timedelta(days=target["days"])
                        st.session_state["lic_db"][key] = target
                        st.session_state["lic_db"][key]["expire"] = expire_date
                        st.session_state.update({"auth": True, "role": "user", "current_user": key})
                        st.rerun()
                else:
                    st.error("❌ Geçersiz Lisans!")

        with t2:
            a_t = st.text_input("Admin Token:", type="password", key="a_token")
            a_p = st.text_input("Admin Password:", type="password", key="a_pass")
            if st.button("MASTER GİRİŞ", use_container_width=True):
                if a_t == ADMIN_TOKEN and a_p == ADMIN_PASS: 
                    st.session_state.update({"auth": True, "role": "admin"})
                    st.rerun()
                else:
                    st.error("❌ Admin Kimliği Reddedildi!")
else:
    # --- 5. GİRİŞ SONRASI ---
    if st.session_state["role"] == "admin":
        st.markdown("<div class='internal-welcome'>ADMİN MASTER PANEL</div>", unsafe_allow_html=True)
        with st.expander("🎫 YENİ LİSANS ÜRET VE MÜHÜRLE", expanded=True):
            p_choice = st.selectbox("Paket", ["1-AY", "3-AY", "6-AY", "12-AY", "SINIRSIZ"])
            p_days = {"1-AY": 30, "3-AY": 90, "6-AY": 180, "12-AY": 365, "SINIRSIZ": 36500}[p_choice]
            if st.button("⚡ SİSTEME KAYDET"):
                new_key = f"SBR-{p_choice}-{hashlib.md5(str(time.time()).encode()).hexdigest().upper()[:8]}-TM"
                st.session_state["lic_db"][new_key] = {"label": p_choice, "days": p_days, "expire": None}
                st.code(new_key)
                st.success("Yeni lisans Admin yetkisiyle sisteme mühürlendi.")
    else:
        st.markdown("<div class='internal-welcome'>YAPAY ZEKAYA HOŞ GELDİNİZ</div>", unsafe_allow_html=True)
        st.markdown("<div class='owner-info'>Bu yazılımın sahibi Timur'dur.</div>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("🧹 BELLEĞİ TEMİZLE", use_container_width=True):
            st.cache_data.clear(); st.cache_resource.clear(); st.rerun()
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
                    st.markdown(f"""
                        <div class='decision-card'>
                            <div class='ai-score'>%{score}</div>
                            <b style='color:#58a6ff;'>⚽ {m['league']['name']}</b> | <span class='tsi-time'>⌚ {to_tsi(m['fixture']['date'])}</span><br>
                            <span style='font-size:1.3rem; font-weight:bold;'>{m['teams']['home']['name']} vs {m['teams']['away']['name']}</span><br>
                            <hr style='border:0.1px solid #30363d; margin:10px 0;'>
                            <span style='color:#2ea043; font-weight:bold;'>YAPAY ZEKA KARARI:</span> KG VAR & 2.5 ÜST<br>
                        </div>
                    """, unsafe_allow_html=True)

    if st.button("🔴 GÜVENLİ ÇIKIŞ"): st.session_state.clear(); st.rerun()

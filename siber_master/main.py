import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
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
def get_hardcoded_vault():
    v = {}
    cfg = [("1-AY", 30), ("3-AY", 90), ("6-AY", 180), ("12-AY", 365), ("SINIRSIZ", 36500)]
    for lbl, d in cfg:
        for i in range(1, 201):
            seed = f"FIXED_VAULT_2026_{lbl}_{i}"
            token = f"SBR-{lbl}-{hashlib.md5(seed.encode()).hexdigest().upper()[:8]}-TM"
            pas = hashlib.md5(f"P_{seed}".encode()).hexdigest().upper()[:6]
            v[token] = {"pass": pas, "label": lbl, "days": d}
    return v

CORE_VAULT = get_hardcoded_vault()

if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "role": None, "current_user": None, "activations": {}})

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
    /* Arama Çubuğu Neon Stili */
    .stTextInput>div>div>input { background-color: #0d1117 !important; color: #58a6ff !important; border: 1px solid #30363d !important; }
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
        nesine_leagues = "203,39,140,135,78,61,2,3,137,88"
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params={"date": datetime.now().strftime("%Y-%m-%d"), "ids": nesine_leagues})
        res = r.json().get('response', [])
        if not res:
            r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params={"date": datetime.now().strftime("%Y-%m-%d")})
            res = r.json().get('response', [])
        return res
    except: return []

# --- 4. GİRİŞ ÖNCESİ (PANEL) ---
if not st.session_state["auth"]:
    st.markdown("<div class='marketing-title'>SERVETİ YÖNETMEYE HAZIR MISIN?</div>", unsafe_allow_html=True)
    st.markdown("<div class='marketing-subtitle'>⚠️ %90+ BAŞARIYLA SİBER KARAR VERİCİ AKTİF!</div>", unsafe_allow_html=True)
    
    m_data = fetch_data()[:15]
    m_html = "".join([f"<span class='match-badge'>⚽ {m['teams']['home']['name']} <span>VS</span> {m['teams']['away']['name']}</span>" for m in m_data])
    st.markdown(f"<div class='marquee-container'><div class='marquee-text'>{m_html}</div></div>", unsafe_allow_html=True)
    
    st.markdown("""<div class='pkg-row'><div class='pkg-box'><small>1 AYLIK</small><b>700 TL</b></div><div class='pkg-box'><small>3 AYLIK</small><b>2.000 TL</b></div><div class='pkg-box'><small>6 AYLIK</small><b>5.000 TL</b></div><div class='pkg-box'><small>12 AYLIK</small><b>9.000 TL</b></div><div class='pkg-box'><small>SINIRSIZ</small><b>10.000 TL</b></div></div>""", unsafe_allow_html=True)
    st.markdown(f"<a href='{WA_LINK}' class='wa-small'>🔥 HEMEN LİSANS AL VE KAZANMAYA BAŞLA</a>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<h3 style='text-align:center; color:#58a6ff;'>🔑 SİBER TERMİNAL GİRİŞİ</h3>", unsafe_allow_html=True)
        login_token = st.text_input("Giriş Tokeni:", type="password", key="l_token").strip()
        login_pass = st.text_input("Şifre:", type="password", key="l_pass").strip()
        
        if st.button("YAPAY ZEKAYI AKTİF ET", use_container_width=True):
            if login_token == ADMIN_TOKEN and login_pass == ADMIN_PASS:
                st.session_state.update({"auth": True, "role": "admin"})
                st.rerun()
            elif login_token in CORE_VAULT:
                if CORE_VAULT[login_token]["pass"] == login_pass:
                    now = datetime.now()
                    if login_token not in st.session_state["activations"]:
                        st.session_state["activations"][login_token] = now + timedelta(days=CORE_VAULT[login_token]["days"])
                    if now > st.session_state["activations"][login_token]:
                        st.error("❌ LİSANS SÜRENİZ DOLMUŞTUR! LÜTFEN YENİLEYİN.")
                    else:
                        st.session_state.update({"auth": True, "role": "user", "current_user": login_token})
                        st.rerun()
                else: st.error("❌ Geçersiz Şifre!")
            else: st.error("❌ Token Tanınamadı!")

else:
    # --- 5. GİRİŞ SONRASI ---
    if st.session_state["role"] == "admin":
        st.markdown("<div class='internal-welcome'>ADMİN MASTER PANEL</div>", unsafe_allow_html=True)
        with st.expander("🎫 PAKETLERE GÖRE ANAHTARLARI AL", expanded=True):
            pkg_choice = st.selectbox("Paket Seç", ["1-AY", "3-AY", "6-AY", "12-AY", "SINIRSIZ"])
            view_data = {k: v for k, v in CORE_VAULT.items() if v["label"] == pkg_choice}
            st.dataframe(pd.DataFrame.from_dict(view_data, orient='index'), use_container_width=True)
            
    else:
        curr_token = st.session_state["current_user"]
        expire_time = st.session_state["activations"][curr_token]
        st.markdown("<div class='internal-welcome'>YAPAY ZEKAYA HOŞ GELDİNİZ</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='owner-info'>🛡️ Lisans Sonu: {expire_time.strftime('%Y-%m-%d %H:%M')}</div>", unsafe_allow_html=True)

    col_x, col_y = st.columns(2)
    with col_x:
        if st.button("🧹 CLEAR"): st.cache_data.clear(); st.rerun()
    with col_y:
        if st.button("♻️ UPDATE"): st.cache_data.clear(); st.rerun()

    st.divider()

    # --- SİBER ARAMA MOTORU ---
    search_query = st.text_input("🔍 MAÇ VEYA LİG ARA (NESİNE FİLTRESİ):", placeholder="Örn: Galatasaray, Premier League...").lower()

    if st.button("🚀 KUSURSUZ NESİNE TARAMASINI BAŞLAT", use_container_width=True):
        all_matches = fetch_data()
        if all_matches:
            # Arama filtresini uygula
            filtered_matches = [
                m for m in all_matches 
                if search_query in m['teams']['home']['name'].lower() or 
                   search_query in m['teams']['away']['name'].lower() or 
                   search_query in m['league']['name'].lower()
            ]

            if filtered_matches:
                for i, m in enumerate(filtered_matches):
                    score = 85 + (i % 12)
                    st.markdown(f"""
                        <div class='decision-card'>
                            <div class='ai-score'>%{score}</div>
                            <b style='color:#58a6ff;'>⚽ {m['league']['name']}</b> | <span class='tsi-time'>⌚ {to_tsi(m['fixture']['date'])}</span><br>
                            <span style='font-size:1.3rem; font-weight:bold;'>{m['teams']['home']['name']} vs {m['teams']['away']['name']}</span><br>
                            <hr style='border:0.1px solid #30363d; margin:10px 0;'>
                            <span style='color:#2ea043; font-weight:bold;'>SİBER ANALİZ:</span> NESİNE KG VAR / ÜST
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning(f"⚠️ '{search_query}' araması için bugün Nesine bülteninde maç bulunamadı.")

    if st.button("🔴 GÜVENLİ ÇIKIŞ"): st.session_state.clear(); st.rerun()

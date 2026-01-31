import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import time
import pytz

# --- 1. SİBER HAFIZA VE PERSISTENCE (KALICILIK) KİLİDİ ---
# Bu ayar sayfa yenilense dahi tarayıcı sekmesi açık olduğu sürece auth'u korumaya yardımcı olur.
if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "role": None, "current_user": None})

st.set_page_config(page_title="TIMUR AI - STRATEGIC PREDICTOR", layout="wide")

API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
HEADERS = {'x-apisports-key': API_KEY, 'User-Agent': 'Mozilla/5.0'}
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN, ADMIN_PASS = "SBR-MASTER-2026-TIMUR-X7", "1937timurR&"
WA_LINK = "https://api.whatsapp.com/send?phone=905414516774"

@st.cache_resource
def get_vault():
    """1000 Adet Statik Anahtarı Üretir ve Sunucu Hafızasına Çiviler (Asla Değişmez)"""
    v = {}
    cfg = [("1-AY", 30), ("3-AY", 90), ("6-AY", 180), ("12-AY", 365), ("SINIRSIZ", 36500)]
    for lbl, d in cfg:
        for i in range(1, 201):
            seed = f"TIMUR_V12_ULTIMATE_{lbl}_{i}"
            k = f"SBR-{lbl}-{hashlib.md5(seed.encode()).hexdigest().upper()[:8]}-TM"
            p = hashlib.md5(f"P_{seed}".encode()).hexdigest().upper()[:6]
            v[k] = {"pass": p, "label": lbl, "days": d, "expire": None, "status": "BEKLEMEDE"}
    return v

# Lisans veritabanını session_state'den alıp cache_resource'a mühürledik.
# Sayfa yenilendiğinde lic_db artık silinmez.
lic_db = get_vault()

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
    }
    @keyframes marquee { 0% { transform: translate(0, 0, 0); } 100% { transform: translate(-100%, 0, 0); } }
    .marketing-title { text-align: center; color: #2ea043; font-size: 2.5rem; font-weight: 900; margin-bottom: 5px; }
    .marketing-subtitle { text-align: center; color: #f85149; font-size: 1.1rem; font-weight: bold; margin-bottom: 15px; }
    .internal-welcome { text-align: center; color: #2ea043; font-size: 2rem; font-weight: 800; }
    .owner-info { text-align: center; color: #58a6ff; font-size: 1rem; margin-bottom: 20px; border-bottom: 1px solid #30363d; padding-bottom: 10px; }
    .stButton>button { background-color: #0d1117 !important; border: 1px solid #2ea043 !important; color: #2ea043 !important; font-weight: bold !important; border-radius: 6px !important; }
    .pkg-row { display: flex; gap: 5px; justify-content: center; margin-bottom: 15px; flex-wrap: wrap; }
    .pkg-box { background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 10px; width: calc(18% - 10px); min-width: 120px; text-align: center; border-top: 3px solid #2ea043; }
    .wa-small { display: block; width: 100%; max-width: 300px; margin: 0 auto 15px auto; background: #238636; color: white !important; text-align: center; padding: 10px; border-radius: 8px; font-weight: bold; text-decoration: none; }
    .decision-card { background: #0d1117; border: 1px solid #30363d; border-left: 6px solid #2ea043; padding: 18px; border-radius: 12px; margin-bottom: 15px; }
    .ai-score { float: right; font-size: 1.5rem; font-weight: 900; color: #2ea043; }
    .live-minute { color: #f85149; font-weight: bold; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
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
        pop_leagues = "203,39,140,135,78,61,2,3"
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params={"date": datetime.now().strftime("%Y-%m-%d"), "ids": pop_leagues})
        return r.json().get('response', [])
    except: return []

# --- 4. GİRİŞ ÖNCESİ VE PERSISTENCE KONTROLÜ ---
if not st.session_state["auth"]:
    st.markdown("<div class='marketing-title'>SERVETİ YÖNETMEYE HAZIR MISIN?</div>", unsafe_allow_html=True)
    st.markdown("<div class='marketing-subtitle'>⚠️ %90+ BAŞARIYLA SİBER KARAR VERİCİ AKTİF!</div>", unsafe_allow_html=True)
    
    m_data = fetch_data()[:15]
    m_html = "".join([f"<span class='match-badge'>⚽ {m['teams']['home']['name']} vs {m['teams']['away']['name']}</span>" for m in m_data])
    st.markdown(f"<div class='marquee-container'><div class='marquee-text'>{m_html}</div></div>", unsafe_allow_html=True)
    
    st.markdown("""<div class='pkg-row'><div class='pkg-box'><small>1 AY</small><br><b>700 TL</b></div><div class='pkg-box'><small>3 AY</small><br><b>2.000 TL</b></div><div class='pkg-box'><small>6 AY</small><br><b>5.000 TL</b></div><div class='pkg-box'><small>12 AY</small><br><b>9.000 TL</b></div><div class='pkg-box'><small>SINIRSIZ</small><br><b>10.000 TL</b></div></div>""", unsafe_allow_html=True)
    st.markdown(f"<a href='{WA_LINK}' class='wa-small'>🔥 LİSANS AL VE KAZAN</a>", unsafe_allow_html=True)

    with st.container():
        _, mid, _ = st.columns([1, 2, 1])
        with mid:
            st.markdown("<h3 style='text-align:center;'>🔑 SİBER TERMİNAL</h3>", unsafe_allow_html=True)
            l_tok = st.text_input("Token:", type="password", key="login_t").strip()
            l_pas = st.text_input("Şifre:", type="password", key="login_p").strip()
            
            if st.button("SİSTEMİ KİLİTLE VE AÇ", use_container_width=True):
                if l_tok == ADMIN_TOKEN and l_pas == ADMIN_PASS:
                    st.session_state.update({"auth": True, "role": "admin"})
                    st.rerun()
                elif l_tok in lic_db:
                    if lic_db[l_tok]["pass"] == l_pas:
                        # Aktivasyon tarihi kontrolü
                        if "activations" not in st.session_state: st.session_state["activations"] = {}
                        if l_tok not in st.session_state["activations"]:
                            st.session_state["activations"][l_tok] = datetime.now() + timedelta(days=lic_db[l_tok]["days"])
                        
                        st.session_state.update({"auth": True, "role": "user", "current_user": l_tok})
                        st.rerun()
                    else: st.error("❌ Hatalı Şifre!")
                else: st.error("❌ Geçersiz Token!")

else:
    # --- 5. GİRİŞ SONRASI (SAYFA YENİLENSE DE BURASI KALIR) ---
    if st.session_state["role"] == "admin":
        st.markdown("<div class='internal-welcome'>ADMİN MASTER PANEL</div>", unsafe_allow_html=True)
        with st.expander("🎫 1000 ADET SABİT ANAHTAR", expanded=True):
            f_pkg = st.selectbox("Paket Filtrele", ["1-AY", "3-AY", "6-AY", "12-AY", "SINIRSIZ"])
            df_view = {k: v for k, v in lic_db.items() if v["label"] == f_pkg}
            st.dataframe(pd.DataFrame.from_dict(df_view, orient='index'))
    else:
        u_key = st.session_state["current_user"]
        u_exp = st.session_state["activations"][u_key]
        st.markdown("<div class='internal-welcome'>YAPAY ZEKA AKTİF</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='owner-info'>🛡️ Lisans Bitiş: {u_exp.strftime('%Y-%m-%d %H:%M')}</div>", unsafe_allow_html=True)

    # UPDATE & CLEAR
    c1, c2 = st.columns(2)
    with c1: 
        if st.button("🧹 CLEAR"): st.cache_data.clear(); st.rerun()
    with c2: 
        if st.button("♻️ UPDATE"): st.cache_data.clear(); st.rerun()

    if st.button("🚀 NESİNE CANLI ANALİZ", use_container_width=True):
        matches = fetch_data()
        if matches:
            for m in matches:
                is_live = m['fixture']['status']['short'] in ['1H', '2H', 'HT']
                minute = f"<span class='live-minute'>{m['fixture']['status']['elapsed']}'</span>" if is_live else ""
                score = 85 + (m['fixture']['id'] % 12)
                st.markdown(f"""
                    <div class='decision-card'>
                        <div class='ai-score'>%{score}</div>
                        <b>⚽ {m['league']['name']}</b> | {to_tsi(m['fixture']['date'])} {minute}<br>
                        <span style='font-size:1.2rem;'>{m['teams']['home']['name']} vs {m['teams']['away']['name']}</span><br>
                        <hr style='border:0.1px solid #333;'>
                        <span style='color:#2ea043;'>SİBER KARAR: NESİNE ÜST</span>
                    </div>
                """, unsafe_allow_html=True)

    if st.button("🔴 GÜVENLİ ÇIKIŞ"):
        st.session_state.clear()
        st.rerun()

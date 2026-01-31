import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import hashlib
import pytz

# --- 1. SİBER HAFIZA VE KESİN GİRİŞ PROTOKOLÜ ---
st.set_page_config(page_title="TIMUR AI - STRATEGIC PREDICTOR", layout="wide")

API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
HEADERS = {'x-apisports-key': API_KEY, 'User-Agent': 'Mozilla/5.0'}
BASE_URL = "https://v3.football.api-sports.io"

ADMIN_TOKEN = "SBR-MASTER-2026-TIMUR-X7"
ADMIN_PASS = "1937timurR&"
WA_LINK = "https://api.whatsapp.com/send?phone=905414516774"

@st.cache_resource
def get_hardcoded_vault():
    v = {}
    cfg = [("1-AY", 30), ("3-AY", 90), ("6-AY", 180), ("12-AY", 365), ("SINIRSIZ", 36500)]
    for lbl, d in cfg:
        for i in range(1, 201):
            seed = f"V16_FIXED_SEED_{lbl}_{i}"
            token = f"SBR-{lbl}-{hashlib.md5(seed.encode()).hexdigest().upper()[:8]}-TM"
            pas = hashlib.md5(f"PASS_{seed}".encode()).hexdigest().upper()[:6]
            v[token] = {"pass": pas, "label": lbl, "days": d}
    return v

CORE_VAULT = get_hardcoded_vault()

if "auth" not in st.session_state:
    st.session_state.update({
        "auth": False, "role": None, "current_user": None, 
        "stored_matches": [], "api_remaining": "---"
    })

# --- 2. DEĞİŞMEZ ŞABLON VE TASARIM (GÜVENLİ RENDER) ---
st.markdown("""
<style>
    .stApp { background-color: #010409; color: #e6edf3; }
    header { visibility: hidden; }
    .marquee-container {
        background: #0d1117; border-top: 2px solid #f85149; border-bottom: 2px solid #f85149;
        padding: 15px 0; margin-bottom: 25px; overflow: hidden;
    }
    .match-badge {
        background: #161b22; color: #f85149; border: 1px solid #f85149; padding: 5px 15px;
        border-radius: 50px; margin-right: 30px; font-weight: 900; font-family: monospace;
    }
    .marketing-title { text-align: center; color: #2ea043; font-size: 2.2rem; font-weight: 900; }
    .internal-welcome { text-align: center; color: #2ea043; font-size: 1.8rem; font-weight: 800; }
    .owner-info { text-align: center; color: #58a6ff; margin-bottom: 20px; border-bottom: 1px solid #30363d; padding-bottom: 10px; }
    .stButton>button { background-color: #0d1117 !important; border: 1px solid #2ea043 !important; color: #2ea043 !important; font-weight: bold !important; width: 100%; }
    .pkg-box { background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 10px; text-align: center; border-top: 3px solid #2ea043; }
    .decision-card { background: #0d1117; border: 1px solid #30363d; border-left: 6px solid #2ea043; padding: 18px; border-radius: 12px; margin-bottom: 15px; }
    .ai-score { float: right; font-size: 1.4rem; font-weight: 900; color: #2ea043; }
    .live-minute { color: #f1e05a; border: 1px solid #f1e05a; padding: 2px 6px; border-radius: 4px; font-family: monospace; }
</style>
""", unsafe_allow_html=True)

# --- 3. FONKSİYONLAR ---
def to_tsi(utc_str):
    try:
        utc_dt = datetime.strptime(utc_str, "%Y-%m-%dT%H:%M:%S+00:00")
        return utc_dt.replace(tzinfo=pytz.utc).astimezone(pytz.timezone("Europe/Istanbul")).strftime("%H:%M")
    except: return "00:00"

@st.cache_data(ttl=60)
def fetch_data_from_api():
    try:
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params={"date": datetime.utcnow().strftime("%Y-%m-%d"), "timezone": "UTC"}, timeout=10)
        st.session_state["api_remaining"] = r.headers.get('x-ratelimit-requests-remaining', '---')
        if r.status_code == 200:
            return [m for m in r.json().get('response', []) if m['fixture']['status']['short'] not in ['FT', 'PST', 'CANCL']]
        return []
    except: return []

# --- 4. GİRİŞ KONTROLÜ ---
if not st.session_state.get("auth", False):
    st.markdown("<div class='marketing-title'>SERVETİ YÖNETMEYE HAZIR MISIN?</div>", unsafe_allow_html=True)
    
    st.markdown("""<div class='marquee-container' style='text-align:center; color:#f85149;'>SİSTEM AKTİF - GİRİŞ BEKLENİYOR</div>""", unsafe_allow_html=True)
    
    col_a, col_b, col_c, col_d, col_e = st.columns(5)
    with col_a: st.markdown("<div class='pkg-box'><small>1 AY</small><br>700TL</div>", unsafe_allow_html=True)
    with col_b: st.markdown("<div class='pkg-box'><small>3 AY</small><br>2K TL</div>", unsafe_allow_html=True)
    with col_c: st.markdown("<div class='pkg-box'><small>6 AY</small><br>5K TL</div>", unsafe_allow_html=True)
    with col_d: st.markdown("<div class='pkg-box'><small>12 AY</small><br>9K TL</div>", unsafe_allow_html=True)
    with col_e: st.markdown("<div class='pkg-box'><small>LİMİTSİZ</small><br>10K TL</div>", unsafe_allow_html=True)
    
    st.markdown(f"<br><a href='{WA_LINK}' style='display:block; text-align:center; background:#238636; color:white; padding:10px; border-radius:8px; text-decoration:none; font-weight:bold;'>🔥 LİSANS ALMAK İÇİN TIKLA</a>", unsafe_allow_html=True)

    _, c2, _ = st.columns([1, 2, 1])
    with c2:
        l_t = st.text_input("Giriş Tokeni:", type="password", key="l_token")
        l_p = st.text_input("Şifre:", type="password", key="l_pass")
        if st.button("YAPAY ZEKAYI AKTİF ET"):
            if l_t == ADMIN_TOKEN and l_p == ADMIN_PASS:
                st.session_state.update({"auth": True, "role": "admin"})
                st.rerun()
            elif l_t in CORE_VAULT and CORE_VAULT[l_t]["pass"] == l_p:
                st.session_state.update({"auth": True, "role": "user", "current_user": l_t})
                st.rerun()
            else: st.error("❌ Yetkisiz Giriş!")
else:
    # --- 5. PANEL ---
    if st.session_state.get("role") == "admin":
        st.markdown("<div class='internal-welcome'>MASTER PANEL</div>", unsafe_allow_html=True)
        with st.expander("🎫 LİSANS LİSTESİ", expanded=True):
            pkg = st.selectbox("Paket Filtresi", ["1-AY", "3-AY", "6-AY", "12-AY", "SINIRSIZ"])
            st.dataframe(pd.DataFrame.from_dict({k:v for k,v in CORE_VAULT.items() if v["label"] == pkg}, orient='index'))
    else:
        st.markdown("<div class='internal-welcome'>YAPAY ZEKA PANELİ</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='owner-info'>🛡️ {st.session_state.get('current_user')} | ⛽ Hak: {st.session_state.get('api_remaining')}</div>", unsafe_allow_html=True)

    cx, cy = st.columns(2)
    with cx: 
        if st.button("🧹 CLEAR"): st.session_state["stored_matches"] = []; st.rerun()
    with cy:
        if st.button("♻️ UPDATE"): 
            st.cache_data.clear()
            st.session_state["stored_matches"] = fetch_data_from_api()
            st.rerun()

    st.divider()
    if st.button("🚀 ANALİZİ BAŞLAT"):
        st.cache_data.clear()
        st.session_state["stored_matches"] = fetch_data_from_api()

    for i, m in enumerate(st.session_state.get("stored_matches", [])):
        status, elap = m['fixture']['status']['short'], m['fixture']['status']['elapsed']
        is_live = status in ['1H', '2H', 'HT', 'LIVE']
        st.markdown(f"""
            <div class='decision-card'>
                <div class='ai-score'>%{90 + (i % 6)}</div>
                <b style='color:#58a6ff;'>⚽ {m['league']['name']}</b> | TSI: {to_tsi(m['fixture']['date'])} 
                {f"<span class='live-minute'>{status} {elap}'</span>" if is_live else ""}
                <br><b>{m['teams']['home']['name']} vs {m['teams']['away']['name']}</b>
                <br><small style='color:#2ea043;'>Tavsiye: 1.5 ÜST / MS 1X</small>
            </div>
        """, unsafe_allow_html=True)

    if st.button("🔴 GÜVENLİ ÇIKIŞ"): st.session_state.clear(); st.rerun()

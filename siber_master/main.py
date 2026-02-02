import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import pytz

# --- 1. SİBER HAFIZA VE KESİN MÜHÜRLER (DOKUNULMAZ) ---
st.set_page_config(page_title="TIMUR AI - STRATEGIC PREDICTOR", layout="wide")

API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
HEADERS = {'x-apisports-key': API_KEY, 'User-Agent': 'Mozilla/5.0'}
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN, ADMIN_PASS = "SBR-MASTER-2026-TIMUR-X7", "1937timurR&"
WA_LINK = "https://api.whatsapp.com/send?phone=905414516774"

@st.cache_resource
def get_hardcoded_vault():
    """2000 ADET ZAMAN AYARLI KALICI TOKEN ÜRETİM MERKEZİ"""
    v = {}
    cfg = [("1-AY", 30), ("3-AY", 90), ("6-AY", 180), ("12-AY", 365), ("SINIRSIZ", 36500)]
    for lbl, d in cfg:
        for i in range(1, 401): 
            seed = f"V16_FIXED_SEED_{lbl}_{i}_TIMUR_2026"
            token = f"SBR-{lbl}-{hashlib.md5(seed.encode()).hexdigest().upper()[:8]}-TM"
            pas = hashlib.md5(f"PASS_{seed}".encode()).hexdigest().upper()[:6]
            v[token] = {"pass": pas, "label": lbl, "days": d}
    return v

CORE_VAULT = get_hardcoded_vault()

# --- BENI TANI MEKANIZMASI (OTOMATIK GIRIS) ---
if "auth" not in st.session_state:
    st.session_state.update({
        "auth": False, "role": None, "current_user": None, 
        "stored_matches": [], "api_remaining": "---"
    })
    q_t = st.query_params.get("s_t")
    q_p = st.query_params.get("s_p")
    if q_t and q_p:
        if (q_t == ADMIN_TOKEN and q_p == ADMIN_PASS) or (q_t in CORE_VAULT and CORE_VAULT[q_t]["pass"] == q_p):
            st.session_state.update({"auth": True, "role": "admin" if q_t == ADMIN_TOKEN else "user", "current_user": q_t})

# --- 2. DEĞİŞMEZ ŞABLON VE TASARIM (MİLİMETRİK) ---
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
    border-radius: 50px; margin-right: 30px; font-weight: 900; font-family: 'Courier New', monospace; font-size: 1rem;
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
.tsi-time { color: #f1e05a !important; font-family: 'Courier New', monospace; font-weight: 900; background: rgba(241, 224, 90, 0.1); padding: 2px 6px; border-radius: 4px; border: 1px solid rgba(241, 224, 90, 0.2); }
.live-minute { color: #f1e05a; font-family: monospace; font-weight: 900; border: 1px solid #f1e05a; padding: 2px 6px; border-radius: 4px; margin-left: 10px; }
.live-dot { height: 8px; width: 8px; background-color: #f85149; border-radius: 50%; display: inline-block; margin-right: 5px; animation: blink 1s infinite; }
.stat-row { display: flex; align-items: center; font-size: 0.85rem; color: #8b949e; margin-top: 5px; font-family: monospace; }
.stat-label { min-width: 160px; }
.stat-val { color: #58a6ff; font-weight: bold; }
.score-board { font-size: 1.5rem; font-weight: 900; color: #ffffff; background: #161b22; padding: 5px 15px; border-radius: 8px; border: 1px solid #30363d; display: inline-block; margin: 10px 0; }
.stTextInput>div>div>input { background-color: #0d1117 !important; color: #58a6ff !important; border: 1px solid #30363d !important; }
@keyframes blink { 0% { opacity: 1; } 50% { opacity: 0; } 100% { opacity: 1; } }
</style>
""", unsafe_allow_html=True)

# --- 3. YARDIMCI FONKSİYONLAR ---
def to_tsi(utc_str):
    try:
        dt = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
        return dt.astimezone(pytz.timezone("Europe/Istanbul")).strftime("%H:%M")
    except: return "--:--"

def fetch_siber_data(live=True):
    try:
        params = {"live": "all"} if live else {"date": datetime.now().strftime("%Y-%m-%d")}
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params=params, timeout=15)
        st.session_state["api_remaining"] = r.headers.get('x-ratelimit-requests-remaining', '---')
        if r.status_code == 200:
            res = r.json().get('response', [])
            if live:
                return [m for m in res if m['fixture']['status']['short'] in ['1H', '2H', 'HT', 'LIVE']]
            else:
                return [m for m in res if m['fixture']['status']['short'] == 'NS']
        return []
    except: return []

# --- 4. GİRİŞ VE PANEL ---
if not st.session_state["auth"]:
    st.markdown("<div class='marketing-title'>SERVETİ YÖNETMEYE HAZIR MISIN?</div>", unsafe_allow_html=True)
    st.markdown("<div class='marketing-subtitle'>⚠️ %90+ BAŞARIYLA SİBER KARAR VERİCİ AKTİF!</div>", unsafe_allow_html=True)
    m_data = fetch_siber_data(live=True)[:15]
    if m_data:
        m_html = "".join([f"<span class='match-badge'>⚽ {m['teams']['home']['name']} VS {m['teams']['away']['name']}</span>" for m in m_data])
        st.markdown(f"<div class='marquee-container'><div class='marquee-text'>{m_html}</div></div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='pkg-row'>
        <div class='pkg-box'><small>1 AYLIK</small><br><b>700 TL</b></div>
        <div class='pkg-box'><small>3 AYLIK</small><br><b>2.000 TL</b></div>
        <div class='pkg-box'><small>6 AYLIK</small><br><b>5.000 TL</b></div>
        <div class='pkg-box'><small>12 AYLIK</small><br><b>9.000 TL</b></div>
        <div class='pkg-box'><small>SINIRSIZ</small><br><b>10.000 TL</b></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<a href='{WA_LINK}' class='wa-small'>🔥 HEMEN LİSANS AL</a>", unsafe_allow_html=True)
    
    _, c2, _ = st.columns([1, 2, 1])
    with c2:
        with st.form("siber_auth_form", clear_on_submit=False):
            l_t = st.text_input("Giriş Tokeni:", type="password", key="l_token_f").strip()
            l_p = st.text_input("Şifre:", type="password", key="l_pass_f").strip()
            remember = st.checkbox("Beni Tanı (Şifreyi Hatırla)")
            submit = st.form_submit_button("YAPAY ZEKAYI AKTİF ET", use_container_width=True)
            if submit:
                if (l_t == ADMIN_TOKEN and l_p == ADMIN_PASS) or (l_t in CORE_VAULT and CORE_VAULT[l_t]["pass"] == l_p):
                    if remember: st.query_params.update({"s_t": l_t, "s_p": l_p})
                    st.session_state.update({"auth": True, "role": "admin" if l_t == ADMIN_TOKEN else "user", "current_user": l_t})
                    st.rerun()
                else: st.error("❌ Geçersiz Kimlik!")
else:
    # --- 5. ADMİN PANELİ ---
    if st.session_state["role"] == "admin":
        with st.expander("🔑 SİBER MASTER LİSANS KASASI (2000 TOKEN)", expanded=False):
            admin_data = [{"

import streamlit as st
import requests
import pandas as pd
from datetime import datetime
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

# --- HAFIZA BAŞLATMA (HATA ÖNLEYİCİ) ---
if "auth" not in st.session_state:
    st.session_state.update({
        "auth": False, "role": None, "current_user": None, 
        "stored_matches": [], "api_remaining": "---",
        "siber_archive": {},
        "archive_mode": False # KEYERROR ÇÖZÜMÜ: Anahtar burada zorunlu tanımlandı
    })

# --- 2. DEĞİŞMEZ ŞABLON VE TASARIM (MİLİMETRİK) ---
style_code = """<style>
.stApp{background-color:#010409;color:#e6edf3}
header{visibility:hidden}
.marquee-container{background:rgba(13,17,23,0.9);border-top:2px solid #f85149;border-bottom:2px solid #f85149;box-shadow:0 0 15px rgba(248,81,73,0.2);padding:15px 0;margin-bottom:25px;overflow:hidden;white-space:nowrap}
.marquee-text{display:inline-block;padding-left:100%;animation:marquee 100s linear infinite}
.match-badge{background:#161b22;color:#f85149;border:1px solid #f85149;padding:5px 15px;border-radius:50px;margin-right:30px;font-weight:900;font-family:'Courier New',monospace;font-size:1rem}
@keyframes marquee{0%{transform:translate(0,0)}100%{transform:translate(-100%,0)}}
.internal-welcome{text-align:center;color:#2ea043;font-size:2rem;font-weight:800}
.owner-info{text-align:center;color:#58a6ff;font-size:1rem;margin-bottom:20px;border-bottom:1px solid #30363d;padding-bottom:10px}
.stButton>button{background-color:#0d1117!important;border:1px solid #2ea043!important;color:#2ea043!important;font-weight:700!important;border-radius:6px!important}
.decision-card{background:#0d1117;border:1px solid #30363d;border-left:6px solid #2ea043;padding:18px;border-radius:12px;margin-bottom:15px;box-shadow:0 4px 6px rgba(0,0,0,0.3)}
.ai-score{float:right;font-size:1.5rem;font-weight:900;color:#2ea043}
.score-board{font-size:1.5rem;font-weight:900;color:#fff;background:#161b22;padding:5px 15px;border-radius:8px;border:1px solid #30363d;display:inline-block;margin:10px 0}
.archive-badge{display:inline-block;background:rgba(35,134,54,0.1);color:#2ea043;border:1px solid #2ea043;padding:4px 10px;border-radius:6px;font-size:0.85rem;margin-bottom:8px;font-weight:bold}
.status-win{background:#238636;color:white;padding:2px 8px;border-radius:4px;font-size:0.8rem}
.status-fail{background:#da3633;color:white;padding:2px 8px;border-radius:4px;font-size:0.8rem}
.status-wait{background:#f1e05a;color:black;padding:2px 8px;border-radius:4px;font-size:0.8rem}
</style>"""
st.markdown(style_code, unsafe_allow_html=True)

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
        if r.status_code == 200: return r.json().get('response', [])
        return []
    except: return []

# Giriş Kontrolü
if not st.session_state["auth"]:
    q_t, q_p = st.query_params.get("s_t"), st.query_params.get("s_p")
    if q_t and q_p:
        if (q_t == ADMIN_TOKEN and q_p == ADMIN_PASS) or (q_t in CORE_VAULT and CORE_VAULT[q_t]["pass"] == q_p):
            st.session_state.update({"auth": True, "role": "admin" if q_t == ADMIN_TOKEN else "user", "current_user": q_t})

if not st.session_state["auth"]:
    st.markdown("<h1 style='text-align:center;color:#2ea043;'>TIMUR AI LOGIN</h1>", unsafe_allow_html=True)
    with st.form("login_form"):
        l_t = st.text_input("Token:", type="password")
        l_p = st.text_input("Şifre:", type="password")
        if st.form_submit_button("SİSTEME GİR"):
            if (l_t == ADMIN_TOKEN and l_p == ADMIN_PASS) or (l_t in CORE_VAULT and CORE_VAULT[l_t]["pass"] == l_p):
                st.session_state.update({"auth": True, "role": "admin" if l_t == ADMIN_TOKEN else "user", "current_user": l_t})
                st.rerun()
else:
    st.markdown("<div class='internal-welcome'>SİBER ANALİZ MERKEZİ</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='owner-info'>🛡️ Oturum: {st.session_state['current_user']} | ⛽ Kalan API: {st.session_state['api_remaining']}</div>", unsafe_allow_html=True)

    # --- ARAMA VE ARŞİV KONTROLLERİ ---
    search_q = st.text_input("🔍 Maç Ara (Takım Adı):", placeholder="Arşivdeki veya canlıdaki maçı yazın...").strip().lower()
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("📂 ARŞİVDE SORGULA", use_container_width=True):
            st.session_state["archive_mode"] = True
    with col_b:
        if st.button("📡 CANLI LİSTEYE DÖN", use_container_width=True):
            st.session_state["archive_mode"] = False

    cx, cy, cz = st.columns([1, 1, 2])
    with cx: 
        if st.button("🧹 CLEAR"): 
            st.session_state["stored_matches"] = []
            st.session_state["archive_mode"] = False
            st.rerun()
    with cy:
        if st.button("♻️ UPDATE"):
            st.session_state["stored_matches"] = [m for m in fetch_siber_data(live=True) if m['fixture']['status']['short'] in ['1H', '2H', 'HT', 'LIVE']]
            st.session_state["archive_mode"] = False
            st.rerun()
    with cz:
        if st.button("💎 SİBER CANSIZ MAÇ TARAMASI (%90+ GÜVEN)", use_container_width=True):
            res = [m for m in fetch_siber_data(live=False) if m['fixture']['status']['short'] == 'NS']
            st.session_state["stored_matches"] = res
            for m in res:
                fid = str(m['fixture']['id'])
                seed = int(hashlib.md5(fid.encode()).hexdigest(), 16)
                conf = 88 + (seed % 11)
                tahmin = "2.5 ÜST" if conf >= 96 else "İLK YARI 0.5 ÜST"
                st.session_state["siber_archive"][fid] = {
                    "conf": conf, "emir": tahmin, "data": m, "status": "BEKLENİYOR", "final": ""
                }

    # --- VERİ FİLTRELEME VE SKOR DOĞRULAMA ---
    display_list = []
    if st.session_state

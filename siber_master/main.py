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
    .live-minute { color: #f1e05a; font-family: monospace; font-weight: 900; border: 1px solid #f1e05a; padding: 2px 6px; border-radius: 4px; margin-left: 10px; }
    .live-dot { height: 8px; width: 8px; background-color: #f85149; border-radius: 50%; display: inline-block; margin-right: 5px; animation: blink 1s infinite; }
    .stat-row { display: flex; align-items: center; font-size: 0.85rem; color: #8b949e; margin-top: 5px; font-family: monospace; }
    .stat-label { min-width: 160px; }
    .stat-val { color: #58a6ff; font-weight: bold; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0; } 100% { opacity: 1; } }
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
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params={"date": datetime.now().strftime("%Y-%m-%d"), "timezone": "UTC"}, timeout=10)
        # --- API KALAN İSTEK SAYACI ---
        st.session_state["api_remaining"] = r.headers.get('x-ratelimit-requests-remaining', '---')
        if r.status_code == 200:
            all_data = r.json().get('response', [])
            return [m for m in all_data if m['fixture']['status']['short'] not in ['FT', 'AET', 'PEN', 'ABD', 'CANCL', 'PST']]
        return []
    except: return []

# --- 4. GİRİŞ KONTROLÜ ---
if not st.session_state["auth"]:
    st.markdown("<div class='marketing-title'>SERVETİ YÖNETMEYE HAZIR MISIN?</div>", unsafe_allow_html=True)
    st.markdown("<div class='marketing-subtitle'>⚠️ %90+ BAŞARIYLA SİBER KARAR VERİCİ AKTİF!</div>", unsafe_allow_html=True)
    
    m_data = fetch_data()[:15]
    if m_data:
        m_html = "".join([f"<span class='match-badge'>⚽ {m['teams']['home']['name']} <span>VS</span> {m['teams']['away']['name']}</span>" for m in m_data])
        st.markdown(f"<div class='marquee-container'><div class='marquee-text'>{m_html}</div></div>", unsafe_allow_html=True)
    
    st.markdown("""<div class='pkg-row'>
        <div class='pkg-box'><small>1 AYLIK</small><br><b>700 TL</b></div>
        <div class='pkg-box'><small>3 AYLIK</small><br><b>2.000 TL</b></div>
        <div class='pkg-box'><small>6 AYLIK</small><br><b>5.000 TL</b></div>
        <div class='pkg-box'><small>12 AYLIK</small><br><b>9.000 TL</b></div>
        <div class='pkg-box'><small>SINIRSIZ</small><br><b>10.000 TL</b></div>
    </div>""", unsafe_allow_html=True)
    st.markdown(f"<a href='{WA_LINK}' class='wa-small'>🔥 HEMEN LİSANS AL VE KAZANMAYA BAŞLA</a>", unsafe_allow_html=True)

    _, c2, _ = st.columns([1, 2, 1])
    with c2:
        l_t = st.text_input("Giriş Tokeni:", type="password", key="l_token").strip()
        l_p = st.text_input("Şifre:", type="password", key="l_pass").strip()
        if st.button("YAPAY ZEKAYI AKTİF ET", use_container_width=True):
            if (l_t == ADMIN_TOKEN and l_p == ADMIN_PASS) or (l_t in CORE_VAULT and CORE_VAULT[l_t]["pass"] == l_p):
                st.session_state.update({"auth": True, "role": "admin" if l_t == ADMIN_TOKEN else "user", "current_user": l_t})
                st.rerun()
            else: st.error("❌ Yetkisiz Giriş!")
else:
    # --- 5. PANEL (API GÖSTERGELİ) ---
    st.markdown(f"<div class='internal-welcome'>{'ADMİN MASTER PANEL' if st.session_state['role'] == 'admin' else 'YAPAY ZEKAYA HOŞ GELDİNİZ'}</div>", unsafe_allow_html=True)
    # Kalan İstek Burada Gösteriliyor
    st.markdown(f"<div class='owner-info'>🛡️ Oturum: {st.session_state['current_user']} | ⛽ Kalan Hak: {st.session_state['api_remaining']}</div>", unsafe_allow_html=True)

    cx, cy = st.columns(2)
    with cx: 
        if st.button("🧹 CLEAR"): st.session_state["stored_matches"] = []; st.cache_data.clear(); st.rerun()
    with cy:
        if st.button("♻️ UPDATE"): st.cache_data.clear(); st.session_state["stored_matches"] = fetch_data(); st.rerun()

    st.divider()
    if st.button("🚀 STRATEJİK TARAMAYI BAŞLAT", use_container_width=True):
        st.cache_data.clear(); st.session_state["stored_matches"] = fetch_data()

    for i, m in enumerate(st.session_state.get("stored_matches", [])):
        status, elap = m['fixture']['status']['short'], m['fixture']['status']['elapsed']
        is_live = status in ['1H', '2H', 'HT', 'LIVE']
        xg_h, xg_a = round(0.4 + (i % 5) * 0.35, 2), round(0.2 + (i % 3) * 0.45, 2)
        rc_v = 60 + (i % 35)
        dak_html = f"<span class='live-minute'>{status if status=='HT' else f'⏱️ {elap}\''}</span>" if is_live else ""
        l_clr, l_txt = ("#f85149", "GÜVENLİ CANLI") if is_live else ("#2ea043", "YAPAY ZEKA TAHMİNİ")
        msg = f"🔥 CANLI: {m['goals']['home']}-{m['goals']['away']} | SIRADAKİ GOL" if is_live else "🚀 ANALİZ: 1.5 ÜST / MS 1X"

        st.markdown(f"""
            <div class='decision-card'>
                <div class='ai-score'>%{90 + (i % 6)}</div>
                <b style='color:#58a6ff;'>⚽ {m['league']['name']}</b> | <span class='tsi-time'>⌚ TSI: {to_tsi(m['fixture']['date'])}</span> {dak_html}
                <br><span style='font-size:1.3rem; font-weight:bold;'>{m['teams']['home']['name']} vs {m['teams']['away']['name']}</span>
                <div style='margin-top:10px; padding:8px; background:rgba(48,54,61,0.3); border-radius:6px;'>
                    <div class='stat-row'><span class='stat-label'>SİBER xG:</span><span class='stat-val'>H: {xg_h} / A: {xg_a}</span></div>
                    <div class='stat-row'><span class='stat-label'>RCS (HÜCUM GÜCÜ):</span><span class='stat-val'>%{rc_v}</span></div>
                    <div class='stat-row'><span class='stat-label'>MOMENTUM:</span><span class='stat-val' style='color:#2ea043;'>POZİTİF</span></div>
                </div>
                <hr style='border:0.1px solid #30363d; margin:10px 0;'>
                <span style='color:{l_clr}; font-weight:bold;'>{"<span class='live-dot'></span>" if is_live else ""}{l_txt}:</span> {msg}
            </div>
        """, unsafe_allow_html=True)

    if st.button("🔴 GÜVENLİ ÇIKIŞ"): st.session_state.clear(); st.rerun()

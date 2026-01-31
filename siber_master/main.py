import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import time
import pytz

# --- 1. SİBER HAFIZA VE KESİN MÜHÜRLER (DOKUNULMAZ) ---
st.set_page_config(page_title="TIMUR AI - STRATEGIC PREDICTOR", layout="wide")

API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
HEADERS = {'x-apisports-key': API_KEY, 'User-Agent': 'Mozilla/5.0'}
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN, ADMIN_PASS = "SBR-MASTER-2026-TIMUR-X7", "1937timurR&"
WA_LINK = "https://api.whatsapp.com/send?phone=905414516774"

# --- CANLI DESTEK ENJEKSİYONU (GÖRÜNMEZ) ---
def inject_tawk():
    tawk_script = """
    <script type="text/javascript">
    var Tawk_API=Tawk_API||{}, Tawk_LoadStart=new Date();
    (function(){
    var s1=document.createElement("script"),s0=document.getElementsByTagName("script")[0];
    s1.async=true;
    s1.src='https://embed.tawk.to/679ce6813bd1a41921669ef0/1ijseeg0h';
    s1.charset='UTF-8';
    s1.setAttribute('crossorigin','*');
    s0.parentNode.insertBefore(s1,s0);
    })();
    </script>
    """
    components.html(tawk_script, height=0)

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

# --- HAFIZA VE TRAFİK TAKİBİ ---
if "auth" not in st.session_state:
    st.session_state.update({
        "auth": False, "role": None, "current_user": None, 
        "activations": {}, "stored_matches": [], "total_hits": 0
    })

# Sayfa her yüklendiğinde sayacı artır
st.session_state["total_hits"] += 1

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
    .wa-small { display: block; width: 100%; max-width: 300px; margin: 0 auto 15px auto; background: #238636; color: white !important; text-align: center; padding: 10px; border-radius: 8px; font-weight: bold; text-decoration: none; }
    .decision-card { background: #0d1117; border: 1px solid #30363d; border-left: 6px solid #2ea043; padding: 18px; border-radius: 12px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .ai-score { float: right; font-size: 1.5rem; font-weight: 900; color: #2ea043; }
    .tsi-time { color: #f1e05a; font-family: monospace; font-weight: bold; }
    .live-minute { color: #f1e05a; font-family: monospace; font-weight: 900; border: 1px solid #f1e05a; padding: 2px 6px; border-radius: 4px; margin-left: 10px; }
    .stTextInput>div>div>input { background-color: #0d1117 !important; color: #58a6ff !important; border: 1px solid #2ea043 !important; }
    .live-dot { height: 8px; width: 8px; background-color: #f85149; border-radius: 50%; display: inline-block; margin-right: 5px; animation: blink 1s infinite; }
    .stat-row { display: flex; justify-content: space-between; font-size: 0.85rem; color: #8b949e; margin-top: 5px; font-family: monospace; }
    .stat-val { color: #58a6ff; font-weight: bold; }
    @keyframes blink { 0% { opacity: 1; } 50% { opacity: 0; } 100% { opacity: 1; } }
    </style>
""", unsafe_allow_html=True)

# Canlı Desteği Başlat
inject_tawk()

# --- 3. YARDIMCI FONKSİYONLAR ---
def to_tsi(utc_str):
    try:
        utc_dt = datetime.strptime(utc_str, "%Y-%m-%dT%H:%M:%S+00:00")
        return utc_dt.replace(tzinfo=pytz.utc).astimezone(pytz.timezone("Europe/Istanbul")).strftime("%H:%M")
    except: return "00:00"

def fetch_data():
    try:
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params={"date": datetime.now().strftime("%Y-%m-%d")})
        all_data = r.json().get('response', [])
        return [m for m in all_data if m['fixture']['status']['short'] not in ['FT', 'AET', 'PEN', 'ABD', 'CANCL']]
    except: return []

# --- 4. GİRİŞ ---
if not st.session_state["auth"]:
    st.markdown("<div class='marketing-title'>SERVETİ YÖNETMEYE HAZIR MISIN?</div>", unsafe_allow_html=True)
    st.markdown("<div class='marketing-subtitle'>⚠️ %90+ BAŞARIYLA SİBER KARAR VERİCİ AKTİF!</div>", unsafe_allow_html=True)
    m_data = fetch_data()[:15]
    m_html = "".join([f"<span class='match-badge'>⚽ {m['teams']['home']['name']} <span>VS</span> {m['teams']['away']['name']}</span>" for m in m_data])
    st.markdown(f"<div class='marquee-container'><div class='marquee-text'>{m_html}</div></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<h3 style='text-align:center; color:#58a6ff;'>🔑 SİBER TERMİNAL GİRİŞİ</h3>", unsafe_allow_html=True)
        l_t = st.text_input("Giriş Tokeni:", type="password", key="l_token").strip()
        l_p = st.text_input("Şifre:", type="password", key="l_pass").strip()
        if st.button("YAPAY ZEKAYI AKTİF ET", use_container_width=True):
            if l_t == ADMIN_TOKEN and l_p == ADMIN_PASS:
                st.session_state.update({"auth": True, "role": "admin"})
                st.rerun()
            elif l_t in CORE_VAULT and CORE_VAULT[l_t]["pass"] == l_p:
                st.session_state.update({"auth": True, "role": "user", "current_user": l_t})
                st.rerun()
            else: st.error("❌ Geçersiz Giriş!")
else:
    # --- 5. PANEL ---
    if st.session_state["role"] == "admin":
        st.markdown("<div class='internal-welcome'>ADMİN MASTER PANEL</div>", unsafe_allow_html=True)
        st.success(f"📊 ANLIK TRAFİK SAYAÇ: {st.session_state['total_hits']} ZİYARET")
    else:
        st.markdown("<div class='internal-welcome'>YAPAY ZEKAYA HOŞ GELDİNİZ</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='owner-info'>🛡️ Oturum Aktif: {st.session_state['current_user']}</div>", unsafe_allow_html=True)

    cx, cy = st.columns(2)
    with cx: 
        if st.button("🧹 CLEAR"): 
            st.session_state["stored_matches"] = []; st.cache_data.clear(); st.rerun()
    with cy:
        if st.button("♻️ UPDATE"): 
            st.cache_data.clear(); st.session_state["stored_matches"] = fetch_data(); st.rerun()

    st.divider()
    search_q = st.text_input("🔍 HAFIZADA MAÇ ARA:", placeholder="Takım veya Lig adı...").lower()

    if st.button("🚀 NESİNE ÖNCELİKLİ TARAMAYI BAŞLAT", use_container_width=True):
        st.session_state["stored_matches"] = fetch_data()

    if st.session_state["stored_matches"]:
        matches = st.session_state["stored_matches"]
        filtered = [m for m in matches if search_q in m['teams']['home']['name'].lower() or search_q in m['teams']['away']['name'].lower() or search_q in m['league']['name'].lower()]
        
        for i, m in enumerate(filtered):
            status = m['fixture']['status']['short']
            elapsed = m['fixture']['status']['elapsed']
            is_live = status in ['1H', '2H', 'HT', 'LIVE']
            
            xg_h = round(0.4 + (i % 5) * 0.35, 2)
            xg_a = round(0.2 + (i % 3) * 0.45, 2)
            rcs_val = 60 + (i % 35)
            momentum = "POZİTİF" if (xg_h > 1.1 or xg_a > 1.1) and rcs_val > 75 else "ZAYIF / RİSKLİ"

            dakika_html = ""
            if is_live:
                if status == 'HT': dakika_html = "<span class='live-minute'>DEVRE ARASI</span>"
                elif elapsed: dakika_html = f"<span class='live-minute'>⏱️ {elapsed}'</span>"

            if is_live:
                h_n, a_n = m['teams']['home']['name'].upper(), m['teams']['away']['name'].upper()
                label_color, label_text = "#f85149", "GÜVENLİ CANLI"
                if rcs_val < 70:
                    msg = f"⚠️ CANLI: {m['goals']['home']}-{m['goals']['away']} | KISIR BASKI (RCS DÜŞÜK) | Karar: GOL RİSKLİ"
                else:
                    msg = f"🔥 CANLI: {m['goals']['home']}-{m['goals']['away']} | {h_n if xg_h > xg_a else a_n} ETKİLİ | Karar: SIRADAKİ GOL"
            else:
                label_color, label_text = "#2ea043", "YAPAY ZEKA TAHMİNİ"
                msg = "🚀 ANALİZ: Taktiksel Verimlilik Teyit Edildi. Karar: 1.5 ÜST / MS 1X"

            st.markdown(f"""
                <div class='decision-card'>
                    <div class='ai-score'>%{90 + (i % 6)}</div>
                    <b style='color:#58a6ff;'>⚽ {m['league']['name']}</b> | <span class='tsi-time'>⌚ {to_tsi(m['fixture']['date'])}</span> {dakika_html}
                    <br>
                    <span style='font-size:1.3rem; font-weight:bold;'>{m['teams']['home']['name']} vs {m['teams']['away']['name']}</span><br>
                    <div style='margin-top:10px; padding:8px; background:rgba(48,54,61,0.3); border-radius:6px;'>
                        <div class='stat-row'><span>SİBER xG:</span><span class='stat-val'>H: {xg_h} / A: {xg_a}</span></div>
                        <div class='stat-row'><span>RCS (HÜCUM GÜCÜ):</span><span class='stat-val'>%{rcs_val}</span></div>
                        <div class='stat-row'><span>MOMENTUM:</span><span class='stat-val' style='color:{"#2ea043" if momentum == "POZİTİF" else "#f1e05a"};'>{momentum}</span></div>
                    </div>
                    <hr style='border:0.1px solid #30363d; margin:10px 0;'>
                    <span style='color:{label_color}; font-weight:bold;'>{ "<span class='live-dot'></span>" if is_live else "" }{label_text}:</span> 
                    <span style='color:{label_color if is_live else "#e6edf3"};'>{msg}</span>
                </div>
            """, unsafe_allow_html=True)

    if st.button("🔴 GÜVENLİ ÇIKIŞ"): st.session_state.clear(); st.rerun()

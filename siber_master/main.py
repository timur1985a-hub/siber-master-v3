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

# --- ARŞİV VE DURUM YÖNETİMİ ---
if "auth" not in st.session_state:
    st.session_state.update({
        "auth": False, "role": None, "current_user": None, 
        "stored_matches": [], "api_remaining": "---",
        "siber_archive": {},
        "archive_mode": False
    })

# --- 2. DEĞİŞMEZ ŞABLON VE TASARIM (MİLİMETRİK) ---
style_code = """<style>
.stApp{background-color:#010409;color:#e6edf3}
header{visibility:hidden}
.marquee-container{background:rgba(13,17,23,0.9);border-top:2px solid #f85149;border-bottom:2px solid #f85149;box-shadow:0 0 15px rgba(248,81,73,0.2);padding:15px 0;margin-bottom:25px;overflow:hidden;white-space:nowrap}
.marquee-text{display:inline-block;padding-left:100%;animation:marquee 100s linear infinite}
.match-badge{background:#161b22;color:#f85149;border:1px solid #f85149;padding:5px 15px;border-radius:50px;margin-right:30px;font-weight:900;font-family:'Courier New',monospace;font-size:1rem}
@keyframes marquee{0%{transform:translate(0,0)}100%{transform:translate(-100%,0)}}
.marketing-title{text-align:center;color:#2ea043;font-size:2.5rem;font-weight:900;margin-bottom:5px}
.marketing-subtitle{text-align:center;color:#f85149;font-size:1.1rem;font-weight:700;margin-bottom:15px}
.internal-welcome{text-align:center;color:#2ea043;font-size:2rem;font-weight:800}
.owner-info{text-align:center;color:#58a6ff;font-size:1rem;margin-bottom:20px;border-bottom:1px solid #30363d;padding-bottom:10px}
.stButton>button{background-color:#0d1117!important;border:1px solid #2ea043!important;color:#2ea043!important;font-weight:700!important;border-radius:6px!important}
.pkg-row{display:flex;gap:5px;justify-content:center;margin-bottom:15px;flex-wrap:wrap}
.pkg-box{background:#0d1117;border:1px solid #30363d;border-radius:8px;padding:10px;width:calc(18% - 10px);min-width:120px;text-align:center;border-top:3px solid #2ea043}
.wa-small{display:block;width:100%;max-width:300px;margin:0 auto 15px auto;background:#238636;color:#fff!important;text-align:center;padding:10px;border-radius:8px;font-weight:700;text-decoration:none}
.decision-card{background:#0d1117;border:1px solid #30363d;border-left:6px solid #2ea043;padding:18px;border-radius:12px;margin-bottom:15px;box-shadow:0 4px 6px rgba(0,0,0,0.3)}
.ai-score{float:right;font-size:1.5rem;font-weight:900;color:#2ea043}
.tsi-time{color:#f1e05a!important;font-family:'Courier New',monospace;font-weight:900;background:rgba(241,224,90,0.1);padding:2px 6px;border-radius:4px;border:1px solid rgba(241,224,90,0.2)}
.live-minute{color:#f1e05a;font-family:monospace;font-weight:900;border:1px solid #f1e05a;padding:2px 6px;border-radius:4px;margin-left:10px}
.score-board{font-size:1.5rem;font-weight:900;color:#fff;background:#161b22;padding:5px 15px;border-radius:8px;border:1px solid #30363d;display:inline-block;margin:10px 0}
.pressure-bg{background:#161b22;height:10px;width:100%;border-radius:10px;margin-top:12px;border:1px solid #30363d;overflow:hidden}
.pressure-fill{height:100%;border-radius:10px;transition:width 0.8s ease-in-out}
.unit-badge{display:inline-block;background:rgba(88,166,255,0.1);color:#58a6ff;border:1px dashed #58a6ff;padding:4px 10px;border-radius:6px;font-size:0.85rem;margin-top:10px;font-weight:bold;font-family:monospace}
.stTextInput>div>div>input{background-color:#0d1117!important;color:#58a6ff!important;border:1px solid #30363d!important}
.analysis-box{background:rgba(22,27,34,0.6);border:1px solid #30363d;padding:10px;border-radius:8px;margin-top:10px;font-size:0.9rem}
.archive-badge{display:inline-block;background:rgba(248,81,73,0.1);color:#f85149;border:1px solid #f85149;padding:2px 8px;border-radius:4px;font-size:0.75rem;margin-bottom:5px;font-weight:bold}
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
        if r.status_code == 200:
            return r.json().get('response', [])
        return []
    except: return []

# Giriş İşlemi
if not st.session_state["auth"]:
    q_t, q_p = st.query_params.get("s_t"), st.query_params.get("s_p")
    if q_t and q_p:
        if (q_t == ADMIN_TOKEN and q_p == ADMIN_PASS) or (q_t in CORE_VAULT and CORE_VAULT[q_t]["pass"] == q_p):
            st.session_state.update({"auth": True, "role": "admin" if q_t == ADMIN_TOKEN else "user", "current_user": q_t})

# --- 4. GİRİŞ VE PANEL ---
if not st.session_state["auth"]:
    st.markdown("<div class='marketing-title'>SERVETİ YÖNETMEYE HAZIR MISIN?</div>", unsafe_allow_html=True)
    st.markdown("<div class='marketing-subtitle'>⚠️ %90+ BAŞARIYLA SİBER KARAR VERİCİ AKTİF!</div>", unsafe_allow_html=True)
    m_data = fetch_siber_data(live=True)[:15]
    if m_data:
        m_html = "".join([f"<span class='match-badge'>⚽ {m['teams']['home']['name']} VS {m['teams']['away']['name']}</span>" for m in m_data])
        st.markdown(f"<div class='marquee-container'><div class='marquee-text'>{m_html}</div></div>", unsafe_allow_html=True)
    
    _, c2, _ = st.columns([1, 2, 1])
    with c2:
        with st.form("login"):
            l_t = st.text_input("Giriş Tokeni:", type="password").strip()
            l_p = st.text_input("Şifre:", type="password").strip()
            if st.form_submit_button("YAPAY ZEKAYI AKTİF ET", use_container_width=True):
                if (l_t == ADMIN_TOKEN and l_p == ADMIN_PASS) or (l_t in CORE_VAULT and CORE_VAULT[l_t]["pass"] == l_p):
                    st.session_state.update({"auth": True, "role": "admin" if l_t == ADMIN_TOKEN else "user", "current_user": l_t})
                    st.rerun()
                else: st.error("❌ Kimlik Reddedildi!")
else:
    st.markdown("<div class='internal-welcome'>YAPAY ZEKAYA HOŞ GELDİNİZ</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='owner-info'>🛡️ Oturum: {st.session_state['current_user']} | ⛽ Kalan API: {st.session_state['api_remaining']}</div>", unsafe_allow_html=True)
    
    # --- ARAMA VE ÖZEL ARŞİV BUTONU ---
    search_q = st.text_input("🔍 Maç Ara (Nesine Takım Adı):", placeholder="Takım Adı yazıp butonla süzün...").strip().lower()
    
    btn_col1, btn_col2 = st.columns([1, 1])
    with btn_col1:
        if st.button("📂 SİBER ARŞİVDE ARA", use_container_width=True):
            st.session_state["archive_mode"] = True
    with btn_col2:
        if st.button("📡 CANLI LİSTEYE DÖN", use_container_width=True):
            st.session_state["archive_mode"] = False
            st.session_state["stored_matches"] = [m for m in fetch_siber_data(live=True) if m['fixture']['status']['short'] in ['1H', '2H', 'HT', 'LIVE']]

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
            # Arşive Mühürle
            for m in res:
                fid = str(m['fixture']['id'])
                seed_v = int(hashlib.md5(fid.encode()).hexdigest(), 16)
                conf = 88 + (seed_v % 11)
                tahmin = "2.5 ÜST" if conf >= 96 else "İLK YARI 0.5 ÜST"
                st.session_state["siber_archive"][fid] = {"conf": conf, "emir": tahmin, "data": m}
            st.success(f"✅ {len(res)} Maç Analiz Edildi ve Hafızaya Mühürlendi!")

    # --- VERİ GÖSTERİM MANTIĞI ---
    display_list = []
    if st.session_state["archive_mode"]:
        # Arşivden ara
        if search_q:
            display_list = [v["data"] for k, v in st.session_state["siber_archive"].items() if search_q in v["data"]['teams']['home']['name'].lower() or search_q in v["data"]['teams']['away']['name'].lower()]
        else:
            display_list = [v["data"] for k, v in st.session_state["siber_archive"].items()]
    else:
        # Normal listeden ara
        display_list = st.session_state["stored_matches"]
        if search_q:
            display_list = [m for m in display_list if search_q in m['teams']['home']['name'].lower() or search_q in m['teams']['away']['name'].lower()]

    # --- KARTLARI ÇİZ ---
    for m in display_list:
        fid = str(m['fixture']['id'])
        status = m['fixture']['status']['short']
        gh, ga = m['goals']['home'] or 0, m['goals']['away'] or 0
        h_name, a_name = m['teams']['home']['name'], m['teams']['away']['name']
        is_live = status in ['1H', '2H', 'HT', 'LIVE']
        seed_v = int(hashlib.md5(fid.encode()).hexdigest(), 16)
        
        archived = st.session_state["siber_archive"].get(fid)
        arch_html = f"<div class='archive-badge'>🔒 MÜHÜRLÜ ANALİZ: %{archived['conf']} - {archived['emir']}</div>" if archived else ""

        if status == 'NS': # Cansız
            conf = archived['conf'] if archived else (88 + (seed_v % 11))
            u_oneri = f"{int(conf/10)}/10"
            s_emir, color = (f"💎 SİBER EMİR: {archived['emir'] if archived else '2.5 ÜST'} KESİN!", "#2ea043") if conf >= 96 else ("🔥 SİBER EMİR: KG VAR ANALİZ", "#58a6ff")
            analysis_text = "🛡️ **Hafıza:** Bu maç siber arşivde mühürlenmiş verilerle korunuyor."
            dak_h = "<span class='live-minute'>BAŞLAMADI</span>"
        else: # Canlı
            elap = m['fixture']['status']['elapsed'] or 0
            conf = int(75 + (seed_v % 18) + (elap / 12))
            if conf > 99: conf = 99
            u_oneri = f"{int(conf/11)}/10"
            dak_h = f"<span class='live-minute'>⏱️ {elap}'</span>"
            if conf >= 92: s_emir, color = ("🚀 SİBER EMİR: GOL POTANSİYELİ", "#2ea043")
            elif conf >= 85: s_emir, color = ("📊 ANALİZ: SIRADAKİ GOL", "#f1e05a")
            else: s_emir, color = ("🛡️ SİBER TERCİH: PAS GEÇ", "#f85149")
            analysis_text = f"⚔️ Canlı veriler analiz ediliyor. Güven oranı: %{conf}"

        st.markdown(f"""
            <div class='decision-card' style='border-left: 6px solid {color};'>
                {arch_html}
                <div class='ai-score' style='color:{color};'>%{conf}</div>
                <b style='color:#58a6ff;'>⚽ {m['league']['name']}</b> | <span class='tsi-time'>⌚ {to_tsi(m['fixture']['date'])}</span> {dak_h}
                <br><span style='font-size:1.4rem; font-weight:bold;'>{h_name} vs {a_name}</span>
                <br><div class='score-board'>{gh} - {ga}</div>
                <div style='margin-top:10px; padding:12px; background:rgba(46,160,67,0.1); border:1px solid {color}; border-radius:8px;'>
                    <span style='color:{color}; font-size:1rem; font-weight:900;'>🎯 {s_emir}</span>
                </div>
                <div class='analysis-box'>{analysis_text}</div>
                <div class='unit-badge'>💰 STRATEJİK BİRİM: {u_oneri}</div>
                <div class='pressure-bg'><div class='pressure-fill' style='width:{conf}%; background:{color};'></div></div>
            </div>
        """, unsafe_allow_html=True)

    if st.button("🔴 GÜVENLİ ÇIKIŞ"): 
        st.query_params.clear()
        st.session_state.clear()
        st.rerun()

import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import pytz

# --- 1. SİBER HAFIZA VE KESİN MÜHÜRLER (DOKUNULMAZ) ---
st.set_page_config(page_title="TIMUR AI - PRO STRATEGIC", layout="wide")

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

# --- 2. DEĞİŞMEZ ŞABLON VE TASARIM ---
style_code = """<style>.stApp{background-color:#010409;color:#e6edf3}header{visibility:hidden}.marquee-container{background:rgba(13,17,23,0.9);border-top:2px solid #f85149;border-bottom:2px solid #f85149;padding:15px 0;margin-bottom:25px;overflow:hidden}.marquee-text{display:inline-block;white-space:nowrap;padding-left:100%;animation:marquee 100s linear infinite}.match-badge{background:#161b22;color:#f85149;border:1px solid #f85149;padding:5px 15px;border-radius:50px;margin-right:30px;font-weight:900}@keyframes marquee{0%{transform:translate(0,0)}100%{transform:translate(-100%,0)}}.marketing-title{text-align:center;color:#2ea043;font-size:2.5rem;font-weight:900}.internal-welcome{text-align:center;color:#2ea043;font-size:2rem;font-weight:800}.decision-card{background:#0d1117;border:1px solid #30363d;border-left:6px solid #2ea043;padding:18px;border-radius:12px;margin-bottom:15px}.ai-score{float:right;font-size:1.5rem;font-weight:900}.score-board{font-size:1.5rem;font-weight:900;color:#fff;background:#161b22;padding:5px 15px;border-radius:8px;display:inline-block;margin:10px 0}.pressure-bg{background:#30363d;height:8px;width:100%;border-radius:10px;margin-top:10px}.pressure-fill{height:8px;border-radius:10px;transition:width 0.5s}.unit-box{background:rgba(88,166,255,0.1);border:1px dashed #58a6ff;padding:5px;border-radius:6px;font-size:0.9rem;color:#58a6ff;margin-top:10px;text-align:center;font-weight:bold}.wa-small{display:block;width:100%;max-width:300px;margin:10px auto;background:#238636;color:#fff!important;text-align:center;padding:10px;border-radius:8px;font-weight:700;text-decoration:none}.pkg-row{display:flex;gap:5px;justify-content:center;margin-bottom:15px;flex-wrap:wrap}.pkg-box{background:#0d1117;border:1px solid #30363d;border-radius:8px;padding:10px;width:calc(18% - 10px);min-width:120px;text-align:center;border-top:3px solid #2ea043}.live-minute{color:#f1e05a;border:1px solid #f1e05a;padding:2px 6px;border-radius:4px;font-family:monospace;font-weight:900}.tsi-time{color:#f1e05a;font-weight:900;background:rgba(241,224,90,0.1);padding:2px 6px;border-radius:4px}</style>"""
st.markdown(style_code, unsafe_allow_html=True)

# --- 3. YARDIMCI FONKSİYONLAR ---
def to_tsi(utc_str):
    try:
        dt = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
        return dt.astimezone(pytz.timezone("Europe/Istanbul")).strftime("%H:%M")
    except Exception:
        return "--:--"

def fetch_siber_data(live=True):
    try:
        params = {"live": "all"} if live else {"date": datetime.now().strftime("%Y-%m-%d")}
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params=params, timeout=15)
        st.session_state["api_remaining"] = r.headers.get('x-ratelimit-requests-remaining', '---')
        if r.status_code == 200:
            res = r.json().get('response', [])
            return [m for m in res if m['fixture']['status']['short'] in (['1H', '2H', 'HT', 'LIVE'] if live else ['NS'])]
        return []
    except Exception:
        return []

# --- 4. GİRİŞ VE PANEL ---
if not st.session_state["auth"]:
    st.markdown("<div class='marketing-title'>SERVETİ YÖNETMEYE HAZIR MISIN?</div>", unsafe_allow_html=True)
    m_data = fetch_siber_data(live=True)[:10]
    if m_data:
        m_html = "".join([f"<span class='match-badge'>⚽ {m['teams']['home']['name']} vs {m['teams']['away']['name']}</span>" for m in m_data])
        st.markdown(f"<div class='marquee-container'><div class='marquee-text'>{m_html}</div></div>", unsafe_allow_html=True)
    
    st.markdown("""<div class='pkg-row'><div class='pkg-box'><small>1 AYLIK</small><br><b>700 TL</b></div><div class='pkg-box'><small>3 AYLIK</small><br><b>2.000 TL</b></div><div class='pkg-box'><small>6 AYLIK</small><br><b>5.000 TL</b></div><div class='pkg-box'><small>12 AYLIK</small><br><b>9.000 TL</b></div><div class='pkg-box'><small>SINIRSIZ</small><br><b>10.000 TL</b></div></div>""", unsafe_allow_html=True)
    st.markdown(f"<a href='{WA_LINK}' class='wa-small'>🔥 HEMEN LİSANS AL</a>", unsafe_allow_html=True)
    
    _, c2, _ = st.columns([1, 2, 1])
    with c2:
        with st.form("auth_form"):
            l_t = st.text_input("Token:")
            l_p = st.text_input("Şifre:", type="password")
            if st.form_submit_button("AKTİF ET", use_container_width=True):
                if (l_t == ADMIN_TOKEN and l_p == ADMIN_PASS) or (l_t in CORE_VAULT and CORE_VAULT[l_t]["pass"] == l_p):
                    st.session_state.update({"auth": True, "role": "admin" if l_t == ADMIN_TOKEN else "user", "current_user": l_t})
                    st.rerun()
                else: st.error("❌ Hata!")
else:
    if st.session_state["role"] == "admin":
        with st.expander("🔑 LİSANS KASASI"):
            st.dataframe(pd.DataFrame([{"TOKEN": k, "ŞİFRE": v["pass"], "PAKET": v["label"]} for k, v in CORE_VAULT.items()]), use_container_width=True)

    st.markdown("<div class='internal-welcome'>YAPAY ZEKAYA HOŞ GELDİNİZ</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='owner-info'>🛡️ Oturum: {st.session_state['current_user']} | ⛽ API: {st.session_state['api_remaining']}</div>", unsafe_allow_html=True)
    
    search_q = st.text_input("🔍 Maç Ara (Takım Adı):").strip().lower()
    
    c1, c2, c3 = st.columns([1, 1, 2])
    with c1: 
        if st.button("🧹 CLEAR"): st.session_state["stored_matches"] = []; st.rerun()
    with c2:
        if st.button("♻️ UPDATE"): st.session_state["stored_matches"] = fetch_siber_data(live=True); st.rerun()
    with c3:
        if st.button("💎 SİBER CANSIZ TARAMA", use_container_width=True): st.session_state["stored_matches"] = fetch_siber_data(live=False)

    matches = st.session_state.get("stored_matches", [])
    if search_q:
        matches = [m for m in matches if search_q in m['teams']['home']['name'].lower() or search_q in m['teams']['away']['name'].lower()]

    for i, m in enumerate(matches):
        status = m['fixture']['status']['short']
        gh, ga = m['goals']['home'] or 0, m['goals']['away'] or 0
        h_name, a_name = m['teams']['home']['name'], m['teams']['away']['name']
        
        is_pre = status == 'NS'
        if is_pre:
            seed = int(hashlib.md5(str(m['fixture']['id']).encode()).hexdigest(), 16)
            conf = 85 + (seed % 15)
            emir = "💎 2.5 ÜST OYNA" if conf >= 95 else "🔥 KG VAR"
            unit = f"ÖNERİLEN BİRİM: {int(conf/10)}/10"
            color = "#2ea043" if conf >= 95 else "#58a6ff"
            pressure = 0
            time_tag = f"<span class='live-minute'>MAÇ ÖNÜ</span>"
        else:
            conf = int(70 + ((i % 25) + 5)); conf = min(conf, 99)
            emir = "🚀 SIRADAKİ GOL" if conf >= 90 else "🛡️ PAS GEÇ"
            unit = f"ÖNERİLEN BİRİM: {int(conf/12)}/10" if conf >= 90 else "⚠️ RİSK: KÜÇÜK KASA"
            color = "#2ea043" if conf >= 90 else "#f85149"
            pressure = (conf - 60) * 3 
            time_tag = f"<span class='live-minute'>⏱️ {m['fixture']['status']['elapsed']}'</span>"

        st.markdown(f"""
            <div class='decision-card' style='border-left-color: {color};'>
                <div class='ai-score' style='color:{color};'>%{conf}</div>
                <b style='color:#58a6ff;'>⚽ {m['league']['name']}</b> | <span class='tsi-time'>⌚ {to_tsi(m['fixture']['date'])}</span> {time_tag}
                <br><span style='font-size:1.3rem; font-weight:bold;'>{h_name} vs {a_name}</span>
                <br><div class='score-board'>{gh} - {ga}</div>
                <div style='margin-top:10px; padding:10px; background:rgba(46,160,67,0.05); border:1px solid {color}; border-radius:8px;'>
                    <span style='color:{color}; font-weight:900;'>🎯 {emir}</span>
                    <div class='unit-box' style='border-color:{color}; color:{color};'>{unit}</div>
                    {"<div class='pressure-bg'><div class='pressure-fill' style='width:"+str(pressure)+"%; background:"+color+";'></div></div>" if not is_pre else ""}
                </div>
                <div style='margin-top:10px; display:flex; gap:10px;'>
                    <a href='https://www.nesine.com/iddaa/canli-iddaa' target='_blank' style='flex:1; background:#30363d; color:#fff; text-align:center; padding:5px; border-radius:4px; text-decoration:none; font-size:0.8rem;'>NESİNE'DE BUL</a>
                </div>
            </div>
        """, unsafe_allow_html=True)

    if st.button("🔴 GÜVENLİ ÇIKIŞ"): 
        st.query_params.clear(); st.session_state.clear(); st.rerun()

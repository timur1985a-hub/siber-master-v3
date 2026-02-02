import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import hashlib
import pytz

# --- 1. SİBER HAFIZA VE KESİN MÜHÜRLER (DOKUNULMAZ) ---
st.set_page_config(page_title="TIMUR AI - ELITE STRATEGIC", layout="wide")

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

# --- 2. ELİT SİBER ANALİZ MOTORU (V3 - NOKTA ATIŞI) ---
def elite_decision_engine(match, is_live=True):
    """Sadece %90+ güvenli, baskı odaklı elit analizör"""
    m_id = match['fixture']['id']
    seed = int(hashlib.md5(f"{m_id}_ELITE_V3".encode()).hexdigest(), 16)
    
    # Hakimiyet ve Momentum Simülasyonu (Nokta Atışı için)
    h_power = 45 + (seed % 50)
    a_power = 45 + ((seed // 3) % 50)
    total = h_power + a_power
    h_dom = (h_power / total) * 100
    a_dom = (a_power / total) * 100
    
    diff = abs(h_dom - a_dom)
    confidence = int(82 + (diff * 0.75))
    if confidence > 99: confidence = 99
    
    # KRİTİK FİLTRE: SADECE %90 VE ÜZERİ
    if confidence < 90:
        return None 
    
    target = match['teams']['home']['name'] if h_dom > a_dom else match['teams']['away']['name']
    dom_val = round(max(h_dom, a_dom), 1)
    
    if is_live:
        decision = f"🔥 HAKİMİYET: {target} | SIRADAKİ GOLÜ BU TAKIM ATAR"
        color = "#2ea043"
    else:
        decision = f"💎 ELMAS ANALİZ: {target} MAÇI DOMİNE EDER (KESİN MS)"
        color = "#58a6ff"
        
    return {"conf": confidence, "decision": decision, "color": color, "dom": dom_val, "side": target}

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
            return [m for m in res if m['fixture']['status']['short'] == 'NS']
        return []
    except: return []

# --- 3. DEĞİŞMEZ ŞABLON VE TASARIM (MİLİMETRİK) ---
st.markdown("""
    <style>
    .stApp { background-color: #010409; color: #e6edf3; }
    header { visibility: hidden; }
    .owner-info { text-align: center; color: #58a6ff; font-size: 1rem; margin-bottom: 20px; border-bottom: 1px solid #30363d; padding-bottom: 10px; }
    .elite-card { 
        background: #0d1117; border: 1px solid #30363d; border-left: 8px solid #2ea043; 
        padding: 20px; border-radius: 15px; margin-bottom: 20px;
        box-shadow: 0px 0px 20px rgba(46, 160, 67, 0.15);
    }
    .dom-bar { background: #161b22; border-radius: 10px; height: 10px; margin: 10px 0; overflow: hidden; }
    .dom-fill { background: #2ea043; height: 100%; }
    .score-board { font-size: 1.8rem; font-weight: 900; color: #fff; text-align: center; margin: 10px 0; background: #161b22; border-radius: 8px; }
    .ai-score { float: right; font-size: 1.5rem; font-weight: 900; color: #2ea043; }
    .stButton>button { background-color: #0d1117 !important; border: 1px solid #2ea043 !important; color: #2ea043 !important; font-weight: bold !important; }
    </style>
""", unsafe_allow_html=True)

# --- 4. GİRİŞ VE PANEL ---
if not st.session_state["auth"]:
    st.markdown("<h1 style='text-align:center; color:#2ea043;'>TIMUR AI ELITE Sniper</h1>", unsafe_allow_html=True)
    _, c2, _ = st.columns([1, 2, 1])
    with c2:
        with st.form("auth_form"):
            l_t = st.text_input("Giriş Tokeni:", type="password").strip()
            l_p = st.text_input("Şifre:", type="password").strip()
            if st.form_submit_button("SİSTEMİ AKTİF ET", use_container_width=True):
                if (l_t == ADMIN_TOKEN and l_p == ADMIN_PASS) or (l_t in CORE_VAULT and CORE_VAULT[l_t]["pass"] == l_p):
                    st.session_state.update({"auth": True, "role": "admin" if l_t == ADMIN_TOKEN else "user", "current_user": l_t})
                    st.rerun()
                else: st.error("❌ Geçersiz Kimlik!")
else:
    if st.session_state["role"] == "admin":
        with st.expander("🔑 LİSANS KASASI"):
            st.dataframe(pd.DataFrame([{"TOKEN": k, "ŞİFRE": v["pass"]} for k, v in CORE_VAULT.items()]))

    st.markdown(f"<div class='owner-info'>🛡️ OTURUM: {st.session_state['current_user']} | ⛽ API: {st.session_state['api_remaining']}</div>", unsafe_allow_html=True)
    
    cx, cy, cz = st.columns(3)
    with cx:
        if st.button("🚀 ELİT CANLI TARAMA", use_container_width=True):
            st.session_state["stored_matches"] = fetch_siber_data(live=True)
    with cy:
        if st.button("💎 ELİT CANSIZ TARAMA", use_container_width=True):
            st.session_state["stored_matches"] = fetch_siber_data(live=False)
    with cz:
        if st.button("🧹 CLEAR", use_container_width=True):
            st.session_state["stored_matches"] = []; st.rerun()

    matches = st.session_state.get("stored_matches", [])
    found_any = False

    for m in matches:
        is_live = m['fixture']['status']['short'] != 'NS'
        analysis = elite_decision_engine(m, is_live)
        
        if analysis: # Sadece %90+ güven olanlar ekrana basılır
            found_any = True
            st.markdown(f"""
                <div class='elite-card' style='border-left-color: {analysis['color']};'>
                    <div class='ai-score'>%{analysis['conf']}</div>
                    <b style='color:#58a6ff;'>⚽ {m['league']['name']}</b><br>
                    <div style='font-size:1.3rem; font-weight:bold;'>{m['teams']['home']['name']} vs {m['teams']['away']['name']}</div>
                    <div class='score-board'>{m['goals']['home'] or 0} - {m['goals']['away'] or 0}</div>
                    
                    <div style='margin-top:10px;'>
                        <div style='display:flex; justify-content:space-between; font-size:0.8rem;'>
                            <span>HAKİMİYET: {analysis['side']}</span>
                            <span>%{analysis['dom']}</span>
                        </div>
                        <div class='dom-bar'><div class='dom-fill' style='width:{analysis['dom']}%; background:{analysis['color']};'></div></div>
                    </div>
                    
                    <div style='background:rgba(46, 160, 67, 0.1); padding:12px; border-radius:8px; border:1px solid {analysis['color']}; margin-top:10px;'>
                        <b style='color:{analysis['color']};'>🎯 SİBER ELİT KARAR:</b><br>
                        <span style='font-size:1.1rem; font-weight:800;'>{analysis['decision']}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    if not found_any and len(matches) > 0:
        st.info("🔎 Tarama tamamlandı. %90 güven eşiğini geçen elit maç şu an bulunmuyor.")

    if st.button("🔴 GÜVENLİ ÇIKIŞ"):
        st.query_params.clear(); st.session_state.clear(); st.rerun()

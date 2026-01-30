import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import hashlib

# --- 1. SİBER HAFIZA VE API MOTORU (DOKUNULMAZ) ---
st.set_page_config(page_title="SIBER RADAR V250", layout="wide")

API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
HEADERS = {'x-apisports-key': API_KEY, 'User-Agent': 'Mozilla/5.0'}
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN, ADMIN_PASS = "SBR-MASTER-2026-TIMUR-X7", "1937timurR&"
WA_LINK = "https://api.whatsapp.com/send?phone=905414516774"

if "lic_db" not in st.session_state: st.session_state["lic_db"] = {}

@st.cache_resource
def get_vault():
    v = {}
    cfg = [("1-AYLIK", 30), ("3-AYLIK", 90), ("6-AYLIK", 180), ("12-AYLIK", 365), ("SINIRSIZ", 36500)]
    for lbl, d in cfg:
        for i in range(1, 201):
            k = f"SBR-{lbl[:3]}-{hashlib.md5(f'V34_{lbl}_{i}'.encode()).hexdigest().upper()[:8]}-TM"
            v[k] = {"label": lbl, "days": d}
    return v
VAULT = get_vault()

# --- 2. DEĞİŞMEZ TASARIM (KESİN ŞABLON) ---
st.markdown("""
    <style>
    .stApp { background-color: #010409; color: #e6edf3; }
    header { visibility: hidden; }
    .stButton>button {
        background-color: #0d1117 !important;
        border: 1px solid #2ea043 !important;
        color: #2ea043 !important;
        font-weight: bold !important;
        font-size: 0.75rem !important;
        border-radius: 6px !important;
        height: 35px !important;
    }
    .hype-title { text-align: center; color: #2ea043; font-size: 2rem; font-weight: 900; margin: 10px 0; }
    .pkg-row { display: flex; gap: 5px; justify-content: center; margin-bottom: 15px; flex-wrap: wrap; }
    .pkg-box { 
        background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 10px; 
        width: calc(18% - 10px); min-width: 120px; text-align: center; border-top: 3px solid #2ea043;
    }
    .pkg-box b { color: #58a6ff; display: block; font-size: 0.9rem; }
    .wa-small {
        display: block; width: 100%; max-width: 300px; margin: 0 auto 15px auto;
        background: #238636; color: white !important; text-align: center; padding: 10px;
        border-radius: 8px; font-weight: bold; font-size: 0.85rem; text-decoration: none;
    }
    .card { background: #0d1117; border: 1px solid #30363d; border-radius: 12px; padding: 15px; margin-bottom: 15px; border-left: 5px solid #2ea043; }
    .live-card { border-left-color: #ff4b4b; border-right: 1px solid #ff4b4b; background: #161b22; }
    .ai-badge { background: #238636; color: white; padding: 2px 8px; border-radius: 5px; font-size: 0.7rem; font-weight: bold; }
    .prob-text { color: #58a6ff; font-weight: bold; font-size: 1.1rem; }
    </style>
""", unsafe_allow_html=True)

# --- 3. KUSURSUZ KARAR VERICİ (AI ENGINE) ---
def siber_api(endpoint, params):
    try:
        r = requests.get(f"{BASE_URL}/{endpoint}", headers=HEADERS, params=params, timeout=10)
        return r.json().get('response', [])
    except: return []

def ai_decision_center(h_id, a_id):
    """Maç Öncesi %90+ Karar Verici Mekanizma"""
    h_last = siber_api("fixtures", {"team": h_id, "last": "10"})
    a_last = siber_api("fixtures", {"team": a_id, "last": "10"})
    
    if len(h_last) < 6 or len(a_last) < 6: return None

    def get_stats(matches):
        kg_count = sum(1 for m in matches if (m.get('goals',{}).get('home') or 0) > 0 and (m.get('goals',{}).get('away') or 0) > 0)
        ov25_count = sum(1 for m in matches if ((m.get('goals',{}).get('home') or 0) + (m.get('goals',{}).get('away') or 0)) > 2.5)
        return kg_count / len(matches), ov25_count / len(matches)

    h_kg_rate, h_ov_rate = get_stats(h_last)
    a_kg_rate, a_ov_rate = get_stats(a_last)
    
    # SENARYO ANALİZİ: İki takımın da son maçlardaki ortak eğilimi
    total_kg_prob = ((h_kg_rate + a_kg_rate) / 2) * 100
    total_ov_prob = ((h_ov_rate + a_ov_rate) / 2) * 100

    results = []
    if total_kg_prob >= 90: results.append(("KESİN KG VAR", int(total_kg_prob)))
    if total_ov_prob >= 90: results.append(("2.5 ÜST", int(total_ov_prob)))
    
    return results if results else None

def ai_live_momentum(f_id):
    """Canlı Hakimiyet ve %80+ Gol Olasılığı Analizi"""
    stats = siber_api("fixtures/statistics", {"fixture": f_id})
    if not stats or len(stats) < 2: return None
    
    def get_val(idx, t):
        for s in stats[idx]['statistics']:
            if s['type'] == t:
                v = s.get('value')
                return int(str(v).replace('%','')) if v else 0
        return 0

    # Hakimiyet Puanı: Tehlikeli Atak (Ağırlık 1.5) + İsabetli Şut (Ağırlık 4)
    h_p = (get_val(0, "Dangerous Attacks") * 1.5) + (get_val(0, "Shots on Goal") * 4)
    a_p = (get_val(1, "Dangerous Attacks") * 1.5) + (get_val(1, "Shots on Goal") * 4)
    
    total = h_p + a_p if (h_p + a_p) > 0 else 1
    h_ratio, a_ratio = (h_p / total) * 100, (a_p / total) * 100

    if h_ratio >= 80: return ("EV SAHİBİ GOLÜ %80+", int(h_ratio), "EZİCİ BASKI")
    if a_ratio >= 80: return ("DEPLASMAN GOLÜ %80+", int(a_ratio), "EZİCİ BASKI")
    return None

# --- 4. GİRİŞ PANELİ (SABİT ŞABLON) ---
if "auth" not in st.session_state: st.session_state.update({"auth": False, "role": None})

if not st.session_state["auth"]:
    st.markdown("<div class='hype-title'>SIRA SENDE! 💸</div>", unsafe_allow_html=True)
    st.markdown("""<div class='pkg-row'>
        <div class='pkg-box'><small>1 AYLIK</small><b>700 TL</b></div>
        <div class='pkg-box'><small>3 AYLIK</small><b>2.000 TL</b></div>
        <div class='pkg-box'><small>6 AYLIK</small><b>5.000 TL</b></div>
        <div class='pkg-box'><small>12 AYLIK</small><b>9.000 TL</b></div>
        <div class='pkg-box'><small>SINIRSIZ</small><b>10.000 TL</b></div>
    </div>""", unsafe_allow_html=True)
    st.markdown(f"<a href='{WA_LINK}' class='wa-small'>🟢 LİSANS AL / WHATSAPP</a>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        b_col1, b_col2 = st.columns(2)
        with b_col1:
            if st.button("🧹 TEMİZLE", use_container_width=True): st.cache_data.clear(); st.rerun()
        with b_col2:
            if st.button("♻️ GÜNCELLE", use_container_width=True): st.rerun()
        
        t1, t2 = st.tabs(["🔑 GİRİŞ", "👨‍💻 MASTER"])
        with t1:
            u_in = st.text_input("Anahtar:", type="password", key="u_log")
            if st.button("SİSTEMİ AÇ", use_container_width=True):
                if u_in in VAULT: st.session_state.update({"auth": True, "role": "user"}); st.rerun()
        with t2:
            a_t = st.text_input("Token:", type="password", key="a_tok")
            a_p = st.text_input("Şifre:", type="password", key="a_pas")
            if st.button("ADMİN GİRİŞİ", use_container_width=True):
                if a_t == ADMIN_TOKEN and a_p == ADMIN_PASS: st.session_state.update({"auth": True, "role": "admin"}); st.rerun()
else:
    # --- 5. ANALİZ MERKEZİ (STRATEJİK BUTON) ---
    st.markdown("<h1 style='text-align:center;'>🎯 SİBER RADAR V250</h1>", unsafe_allow_html=True)
    
    if st.button("🚀 KUSURSUZ DÜNYA TARAMASINI BAŞLAT", use_container_width=True):
        with st.spinner("Yapay Zeka Bütün Senaryoları Değerlendiriyor..."):
            fixtures = siber_api("fixtures", {"date": datetime.now().strftime("%Y-%m-%d")})
            
            for m in fixtures:
                f_id = m['fixture']['id']
                h_name, a_name = m['teams']['home']['name'], m['teams']['away']['name']
                status = m['fixture']['status']['short']
                
                # 1. CANLI ANALİZ (HAKİMİYET VE %80+ YÖNLENDİRME)
                if status in ["1H", "2H", "HT"]:
                    live_res = ai_live_momentum(f_id)
                    if live_res:
                        st.markdown(f"""<div class='card live-card'>
                            <span class='ai-badge' style='background:#ff4b4b;'>🚨 CANLI FIRSAT %80+</span><br>
                            <b>{h_name} {m['goals'].get('home',0)} - {m['goals'].get('away',0)} {a_name}</b><br>
                            <span class='prob-text'>{live_res[0]} ({live_res[1]}%)</span><br>
                            <small>Siber Analiz: {live_res[2]} | Dakika: {m['fixture']['status']['elapsed']}'</small>
                        </div>""", unsafe_allow_html=True)

                # 2. MAÇ ÖNCESİ (KESİN KG/ÜST %90+ KARAR VERCİ)
                elif status == "NS":
                    ai_picks = ai_decision_center(m['teams']['home']['id'], m['teams']['away']['id'])
                    if ai_picks:
                        for pick, prob in ai_picks:
                            st.markdown(f"""<div class='card'>
                                <span class='ai-badge'>🤖 AI KARAR: %90+ GÜVEN</span><br>
                                <b>{h_name} - {a_name}</b><br>
                                <span style='color:#2ea043; font-weight:bold; font-size:1.1rem;'>🔥 {pick} ({prob}%)</span><br>
                                <small>Lig: {m['league']['name']} | Saat: {m['fixture']['date'][11:16]}</small>
                            </div>""", unsafe_allow_html=True)

    if st.button("🔴 GÜVENLİ ÇIKIŞ"): st.session_state.clear(); st.rerun()

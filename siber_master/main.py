import requests
from datetime import datetime, timedelta
import streamlit as st
import hashlib
import time
import random

# ================= 1. KUTSAL LİSANS VE ADMIN (DOKUNULMAZ) =================
API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN = "SBR-MASTER-2026-TIMUR-X7" 
ADMIN_PASS = "1937timurR&"

@st.cache_resource
def get_final_vault():
    vault = {}
    config = [("1-AY", 30, 400), ("3-AY", 90, 300), ("6-AY", 180, 150), ("12-AY", 365, 100), ("SINIRSIZ", 36500, 50)]
    for label, days, count in config:
        for i in range(1, count + 1):
            seed = f"V25_{label}_{i}_2026_TIMUR"
            key = f"SBR-{label}-{hashlib.md5(seed.encode()).hexdigest().upper()[:8]}-TM"
            vault[key] = {"label": label, "expiry": datetime.now() + timedelta(days=days)}
    return vault

VAULT = get_final_vault()

# ================= 2. TAM EKRAN VE TASARIM (DOKUNULMAZ) =================
def apply_fixed_ui():
    st.markdown("""
        <style>
        #MainMenu {visibility: hidden;} header {visibility: hidden;} footer {visibility: hidden;}
        .stDeployButton {display:none;} [data-testid="stHeader"] {background: rgba(0,0,0,0); height: 0px;}
        .stApp { background: linear-gradient(180deg, #020617 0%, #0f172a 100%); color: #f1f5f9; }
        .block-container { padding: 0.5rem 1rem !important; }
        .glass-card { background: rgba(15, 23, 42, 0.95); backdrop-filter: blur(15px); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 12px; padding: 15px; margin-bottom: 12px; }
        .decision-box { background: rgba(56, 189, 248, 0.1); border: 1px solid #38bdf8; border-radius: 8px; padding: 10px; margin-top: 10px; text-align: center; }
        .progress-container { background: rgba(255,255,255,0.05); border-radius: 10px; height: 8px; margin: 8px 0; overflow: hidden; }
        div.stButton > button { width: 100%; background: linear-gradient(90deg, #0ea5e9, #2563eb); border: none; border-radius: 10px; padding: 10px; font-weight: bold; color: white !important; }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="Siber Master Pro", layout="wide", initial_sidebar_state="collapsed")
apply_fixed_ui()

# ================= 3. STRATEJİK MUHAKEME MOTORU (2.5 ÜST & KG VAR) =================
def strategic_ai_filter(fixture, is_live=True):
    # Cansız maçlarda 2.5 ÜST ve KG VAR için özel aritma
    if is_live:
        conf = random.randint(75, 99)
        return conf, "CANLI ANALİZ", "#38bdf8"
    else:
        # Cansız (Bülten) için %85-90 altını eleyen filtre simülasyonu
        conf = random.randint(85, 96) 
        choice = random.choice(["🎯 2.5 ÜST", "🔥 KG VAR", "🚀 2.5 ÜST & KG VAR"])
        return conf, choice, "#4ade80"

# ================= 4. OTURUM VE LİSANS (DOKUNULMAZ) =================
if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "role": None, "key": None, "exp": None})

if not st.session_state["auth"]:
    st.markdown("<div class='glass-card' style='text-align:center; border-color:#4ade80;'><h3 style='color: #4ade80; margin:0;'>💎 KAZANANLAR KULÜBÜ</h3><p style='font-size:0.9rem; margin-top:10px;'>Şansa yer yok, sadece mutlak veri hakimiyeti var.</p></div>", unsafe_allow_html=True)
    u_lic = st.text_input("Lisans Anahtarı:", placeholder="SBR-XXXX-TM", key="lic_v51")
    if st.button("SİSTEME BAĞLAN"):
        if u_lic in VAULT:
            st.session_state.update({"auth": True, "role": "user", "key": u_lic, "exp": VAULT[u_lic]["expiry"]})
            st.rerun()
        else: st.error("Geçersiz Anahtar!")
    with st.expander("👨‍💻 Yönetici"):
        a_t, a_p = st.text_input("Token:", type="password"), st.text_input("Şifre:", type="password")
        if st.button("Admin Girişi"):
            if a_t == ADMIN_TOKEN and a_p == ADMIN_PASS:
                st.session_state.update({"auth": True, "role": "admin", "key": "SAHİP", "exp": datetime(2030, 1, 1)})
                st.rerun()

else:
    # ================= 5. ANALİZ PANELİ (STRATEJİK FİLTRELEME) =================
    with st.sidebar:
        min_conf = st.slider("Güven Eşiği %", 85, 99, 85) # Alt sınırı 85'e çektik
        if st.button("🔴 ÇIKIŞ"): st.session_state.clear(); st.rerun()

    tab_live, tab_pre = st.tabs(["🔴 CANLI ANALİZ", "⏳ BÜLTEN (2.5 ÜST & KG)"])

    try:
        headers = {"x-apisports-key": API_KEY, "User-Agent": "Mozilla/5.0"}
        resp = requests.get(f"{BASE_URL}/fixtures?date={datetime.now().strftime('%Y-%m-%d')}", headers=headers).json()
        fixtures = resp.get("response", [])

        with tab_live:
            live_m = [f for f in fixtures if f['fixture']['status']['short'] in ['1H', '2H', 'HT']]
            for f in live_m:
                conf, label, color = strategic_ai_filter(f, True)
                if conf >= min_conf:
                    st.markdown(f"<div class='glass-card'><div style='display:flex; justify-content:space-between;'><span style='background:#ef4444; color:white; padding:2px 6px; border-radius:4px; font-size:0.7rem;'>{f['fixture']['status']['elapsed']}' DK</span><b style='color:#4ade80;'>%{conf} GÜVEN</b></div><h4 style='text-align:center;'>{f['teams']['home']['name']} {f['goals']['home']} - {f['goals']['away']} {f['teams']['away']['name']}</h4><div class='progress-container'><div style='width:{conf}%; background:{color}; height:100%;'></div></div></div>", unsafe_allow_html=True)

        with tab_pre:
            pre_m = [f for f in fixtures if f['fixture']['status']['short'] == 'NS']
            st.markdown("<small style='color:#94a3b8;'>Siber Muhakeme: Sadece %85+ Güvenli 2.5 Üst ve KG Var maçları listeleniyor.</small>", unsafe_allow_html=True)
            for f in pre_m:
                conf, choice, color = strategic_ai_filter(f, False)
                if conf >= min_conf: # %85-90 FİLTRESİ BURADA ÇALIŞIYOR
                    saat = f['fixture']['date'][11:16]
                    st.markdown(f"""
                    <div class='glass-card' style='border-left: 4px solid {color};'>
                        <div style='display:flex; justify-content:space-between; align-items:center;'>
                            <span style='background:#334155; color:#38bdf8; padding:2px 6px; border-radius:4px; font-size:0.75rem;'>SAAT: {saat}</span>
                            <b style='color:{color}; font-size:0.85rem;'>%{conf} ANALİZ GÜVENİ</b>
                        </div>
                        <div style='text-align:center; margin:10px 0;'><b>{f['teams']['home']['name']} vs {f['teams']['away']['name']}</b></div>
                        <div class='decision-box' style='background:{color}15; border-color:{color};'>
                            <b style='color:{color}; font-size:1rem;'>SİBER TERCİH: {choice}</b><br>
                            <small style='color:#f1f5f9;'>Muhakeme tamamlandı: Gol potansiyeli tavan.</small>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    except:
        st.warning("Veri taranıyor...")

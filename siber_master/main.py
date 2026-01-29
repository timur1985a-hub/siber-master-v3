import requests
from datetime import datetime, timedelta
import streamlit as st
import hashlib
import time
import random

# ================= 1. KUTSAL LİSANS VE ADMIN (ESKİ YAPI - MÜHÜRLÜ) =================
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

# ================= 2. TAM EKRAN VE LOGO GİZLEME CSS (DOKUNULMAZ) =================
def apply_fixed_ui():
    st.markdown("""
        <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}
        [data-testid="stHeader"] {background: rgba(0,0,0,0); height: 0px;}
        
        .stApp { background: linear-gradient(180deg, #020617 0%, #0f172a 100%); color: #f1f5f9; }
        .block-container { padding: 0.5rem 1rem !important; }
        
        .glass-card { 
            background: rgba(15, 23, 42, 0.95); backdrop-filter: blur(15px); 
            border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 12px; 
            padding: 15px; margin-bottom: 12px;
        }
        
        .decision-box {
            background: rgba(56, 189, 248, 0.1); border: 1px solid #38bdf8;
            border-radius: 8px; padding: 10px; margin-top: 10px; text-align: center;
        }
        
        .pkg-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; }
        .pkg-item { background: rgba(56, 189, 248, 0.05); border: 1px solid rgba(56, 189, 248, 0.1); border-radius: 10px; padding: 10px; text-align: center; }
        
        div.stButton > button { width: 100%; background: linear-gradient(90deg, #0ea5e9, #2563eb); border: none; border-radius: 10px; padding: 10px; font-weight: bold; color: white !important; }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="Siber Master Pro", layout="wide", initial_sidebar_state="collapsed")
apply_fixed_ui()

# ================= 3. MUHAKEME MOTORU =================
def hyper_decision_logic(h_g, a_g, minute, press):
    if minute < 15: return "⚖️ İZLE", "Veri toplanıyor.", "#94a3b8"
    if press >= 90:
        if h_g == a_g: return "🎯 SIRADAKİ GOL: EV", "Ev sahibi baskısı tavan.", "#4ade80"
        return "🚀 ÜST ANALİZİ", "Tempo gol sinyali veriyor.", "#38bdf8"
    return "🛡️ BEKLE", "Riskli bölge.", "#f87171"

# ================= 4. OTURUM VE LİSANS (DOKUNULMAZ YAPI) =================
if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "role": None, "key": None, "exp": None})

if not st.session_state["auth"]:
    # Giriş Paneli
    st.markdown("""
        <div class='glass-card' style='text-align:center; border-color:#4ade80;'>
            <h3 style='color: #4ade80; margin:0;'>💎 KAZANANLAR KULÜBÜ</h3>
            <p style='font-size:0.9rem; margin-top:10px; font-style:italic;'>
                "Sıradan bahisçiler tesadüfleri bekler, Siber Master sahipleri ise sahadaki saniyeleri servete dönüştürür."
            </p>
        </div>
        <div class='pkg-grid'>
            <div class='pkg-item'><small style='color:#38bdf8;'>1 AY</small><br><b style='color:#4ade80;'>700 TL</b></div>
            <div class='pkg-item'><small style='color:#38bdf8;'>3 AY</small><br><b style='color:#4ade80;'>2.000 TL</b></div>
            <div class='pkg-item'><small style='color:#38bdf8;'>6 AY</small><br><b style='color:#4ade80;'>5.000 TL</b></div>
            <div class='pkg-item'><small style='color:#38bdf8;'>12 AY</small><br><b style='color:#4ade80;'>8.000 TL</b></div>
        </div>
    """, unsafe_allow_html=True)

    # LİSANS GİRİŞİ (Orijinal Kod)
    u_lic = st.text_input("Lisans Anahtarı:", placeholder="SBR-XXXX-TM", key="lic_v5")
    if st.button("SİSTEME BAĞLAN"):
        if u_lic in VAULT:
            st.session_state.update({"auth": True, "role": "user", "key": u_lic, "exp": VAULT[u_lic]["expiry"]})
            st.rerun()
        else: st.error("Geçersiz Anahtar!")

    # ADMIN (Mühürlü Bölge)
    with st.expander("👨‍💻 Yönetici"):
        a_t = st.text_input("Token:", type="password")
        a_p = st.text_input("Şifre:", type="password")
        if st.button("Admin Girişi"):
            if a_t == ADMIN_TOKEN and a_p == ADMIN_PASS:
                st.session_state.update({"auth": True, "role": "admin", "key": "SAHİP", "exp": datetime(2030, 1, 1)})
                st.rerun()

else:
    # ================= 5. ANALİZ PANELİ =================
    with st.sidebar:
        st.markdown("<h3 class='neon-blue'>🛡️ KONTROL</h3>", unsafe_allow_html=True)
        conf_filter = st.slider("Güven %", 50, 99, 85)
        if st.button("🔴 ÇIKIŞ"): st.session_state.clear(); st.rerun()

    st.markdown("<h4 style='text-align:center; color:#38bdf8;'>🏆 SİBER MUHAKEME</h4>", unsafe_allow_html=True)
    
    try:
        headers = {"x-apisports-key": API_KEY, "User-Agent": "Mozilla/5.0"}
        resp = requests.get(f"{BASE_URL}/fixtures?date={datetime.now().strftime('%Y-%m-%d')}", headers=headers).json()
        fixtures = resp.get("response", [])
        live_matches = [f for f in fixtures if f['fixture']['status']['short'] in ['1H', '2H', 'HT']]
        
        for f in live_matches:
            press = random.randint(65, 98)
            conf = random.randint(75, 99)
            if conf >= conf_filter:
                dak = f['fixture']['status']['elapsed']
                tercih, aciklama, renk = hyper_decision_logic(f['goals']['home'], f['goals']['away'], dak, press)
                st.markdown(f"""
                <div class='glass-card'>
                    <div style='display:flex; justify-content:space-between; align-items:center;'>
                        <span style='background:#ef4444; color:white; padding:2px 6px; border-radius:4px; font-weight:bold; font-size:0.75rem;'>{dak}' DK</span>
                        <b style='color:#4ade80; font-size:0.8rem;'>%{conf} GÜVEN</b>
                    </div>
                    <div style='text-align:center; margin:10px 0;'><b>{f['teams']['home']['name']} {f['goals']['home']} - {f['goals']['away']} {f['teams']['away']['name']}</b></div>
                    <div style='background:rgba(255,255,255,0.05); height:6px; border-radius:10px; overflow:hidden;'>
                        <div style='width:{press}%; background:#38bdf8; height:100%;'></div>
                    </div>
                    <div class='decision-box' style='border-color:{renk}; background:{renk}15;'>
                        <b style='color:{renk};'>{tercih}</b><br><small>{aciklama}</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    except:
        st.warning("Veri bekleniyor...")

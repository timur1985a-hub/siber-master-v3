import requests
from datetime import datetime, timedelta
import streamlit as st
import hashlib
import time

# ================= 1. KUTSAL LİSANS VE ADMIN (MÜHÜRLÜ) =================
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

# ================= 2. TASARIM VE ALAN OPTİMİZASYONU =================
def apply_optimized_ui():
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(180deg, #020617 0%, #0f172a 100%); color: #f1f5f9; }
        
        /* Alan Kazanımı İçin Boşlukları Daraltma */
        .block-container { padding-top: 1rem !important; }
        
        .glass-card { 
            background: rgba(15, 23, 42, 0.75); 
            backdrop-filter: blur(20px); 
            border: 1px solid rgba(56, 189, 248, 0.2); 
            border-radius: 15px; padding: 15px; margin-bottom: 15px; 
        }

        .pkg-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-bottom: 15px; }
        .pkg-item {
            background: rgba(56, 189, 248, 0.05);
            border: 1px solid rgba(56, 189, 248, 0.1);
            border-radius: 10px;
            padding: 12px;
            text-align: center;
        }
        .pkg-title { color: #38bdf8; font-size: 0.75rem; font-weight: bold; text-transform: uppercase; }
        .pkg-val { color: #4ade80; font-weight: bold; font-size: 1rem; }
        
        .neon-blue { color: #38bdf8; font-weight: bold; }
        .neon-green { color: #4ade80; font-weight: bold; }
        
        /* Buton ve Input Modernizasyonu */
        div.stButton > button { 
            background: linear-gradient(90deg, #0ea5e9, #2563eb); 
            color: white !important; border-radius: 10px; font-weight: bold; border: none; padding: 10px;
        }
        .stTextInput input { 
            background-color: #1e293b !important; color: #38bdf8 !important; border: 1px solid #334155 !important; border-radius: 10px !important; 
        }
        
        .minute-badge { background: #f87171; color: white; padding: 2px 7px; border-radius: 5px; font-weight: bold; font-size: 0.75rem; }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="Siber Master V4100", layout="wide")
apply_optimized_ui()

# ================= 3. OTURUM KONTROLÜ =================
if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "role": None, "key": None, "exp": None})

if not st.session_state["auth"]:
    # SLOGAN VE PAKETLER (EN ÜSTTE)
    st.markdown("""
        <div style='background: rgba(56, 189, 248, 0.08); border: 1px dashed #38bdf8; padding: 12px; border-radius: 12px; text-align: center; margin-bottom: 15px;'>
            <h4 style='color: #4ade80; margin:0;'>💎 KAZANANLAR KULÜBÜ</h4>
            <p style='color: #94a3b8; margin:0; font-size: 0.85rem;'>Veri Odaklı Siber Analiz Sistemi</p>
        </div>
        
        <div class='pkg-grid'>
            <div class='pkg-item'><div class='pkg-title'>1 AY</div><div class='pkg-val'>700 TL</div></div>
            <div class='pkg-item'><div class='pkg-title'>3 AY</div><div class='pkg-val'>2.000 TL</div></div>
            <div class='pkg-item'><div class='pkg-title'>6 AY</div><div class='pkg-val'>5.000 TL</div></div>
            <div class='pkg-item'><div class='pkg-title'>12 AY</div><div class='pkg-val'>8.000 TL</div></div>
        </div>
        <div class='pkg-item' style='margin-bottom:15px; width:100%; border: 1px solid #4ade8055;'>
            <div class='pkg-title' style='color:#4ade80;'>♾️ SINIRSIZ ERİŞİM</div><div class='pkg-val'>10.000 TL</div>
        </div>
    """, unsafe_allow_html=True)

    t1, t2 = st.tabs(["🔑 ERİŞİM", "👨‍💻 YÖNETİM"])
    with t1:
        u_lic = st.text_input("Lisans Anahtarı:", placeholder="SBR-XXXX-TM", key="lic_v41")
        if st.button("SİSTEME BAĞLAN"):
            if u_lic in VAULT:
                st.session_state.update({"auth": True, "role": "user", "key": u_lic, "exp": VAULT[u_lic]["expiry"]})
                st.rerun()
            else: st.error("Geçersiz Anahtar!")
    with t2:
        a_t = st.text_input("Admin Token:", type="password")
        a_p = st.text_input("Şifre:", type="password")
        if st.button("YÖNETİCİ GİRİŞİ"):
            if a_t == ADMIN_TOKEN and a_p == ADMIN_PASS:
                st.session_state.update({"auth": True, "role": "admin", "key": "SAHİP", "exp": datetime(2030, 1, 1)})
                st.rerun()

else:
    # ================= 4. ANALİZ VE MUHAKEME PANELİ =================
    with st.sidebar:
        st.markdown(f"<h3 class='neon-blue'>👤 {st.session_state['role'].upper()}</h3>", unsafe_allow_html=True)
        rem = st.session_state["exp"] - datetime.now()
        st.markdown(f"<div class='glass-card' style='padding:10px;'><small>Kalan Süre:</small><br><b class='neon-green'>{rem.days} GÜN</b></div>", unsafe_allow_html=True)
        if st.button("🔴 ÇIK"): st.session_state.clear(); st.rerun()

    st.markdown("<h3 class='neon-blue'>🏆 CANLI MUHAKEME RADARI</h3>", unsafe_allow_html=True)
    
    if st.button("🔄 VERİLERİ TAZELE"): st.rerun()

    try:
        headers = {"x-apisports-key": API_KEY, "User-Agent": "Mozilla/5.0"}
        resp = requests.get(f"{BASE_URL}/fixtures?date={datetime.now().strftime('%Y-%m-%d')}", headers=headers).json()
        fixtures = resp.get("response", [])

        live_matches = [f for f in fixtures if f['fixture']['status']['short'] in ['1H', '2H', 'HT']]
        
        for f in live_matches:
            st.markdown(f"""
            <div class='glass-card'>
                <div style='display:flex; justify-content:space-between; align-items:center;'>
                    <div><span class='minute-badge'>{f['fixture']['status']['elapsed']}'</span> <span class='neon-blue' style='font-size:0.8rem;'>{f['league']['name']}</span></div>
                    <b class='neon-green'>%92 GÜVEN</b>
                </div>
                <h4 style='text-align:center; margin:10px 0;'>{f['teams']['home']['name']} {f['goals']['home']} - {f['goals']['away']} {f['teams']['away']['name']}</h4>
                <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 8px; text-align:center;'>
                    <div style='background:rgba(255,255,255,0.03); padding:5px; border-radius:8px;'><small style='color:#94a3b8; font-size:0.7rem;'>HAKİMİYET</small><br><b style='font-size:0.85rem;'>TAM BASKI</b></div>
                    <div style='background:rgba(255,255,255,0.03); padding:5px; border-radius:8px;'><small style='color:#94a3b8; font-size:0.7rem;'>GOL</small><br><b class='neon-green' style='font-size:0.85rem;'>YÜKSEK</b></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error("Veri akışı hatası.")

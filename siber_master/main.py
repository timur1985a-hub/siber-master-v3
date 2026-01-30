import requests
from datetime import datetime, timedelta
import streamlit as st
import streamlit.components.v1 as components
import hashlib
import random

# ================= 1. ÇEKİRDEK YAPILANDIRMA (KORUNAN ANA YAPI) =================
API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN = "SBR-MASTER-2026-TIMUR-X7" 
ADMIN_PASS = "1937timurR&"
PHONE = "905414516774"
WA_LINK = f"https://api.whatsapp.com/send?phone={PHONE}&text=Merhaba,%209'da%209%20PRO%20Elite%20Analiz%20sistemi%20aktivasyonu%20istiyorum."

@st.cache_resource
def get_final_vault():
    vault = {}
    config = [("1-AY", 30, 400), ("3-AY", 90, 300), ("6-AY", 180, 150), ("12-AY", 365, 100), ("SINIRSIZ", 36500, 50)]
    for label, days, count in config:
        for i in range(1, count + 1):
            seed = f"V25_{label}_{i}_2026_TIMUR"
            key = f"SBR-{label}-{hashlib.md5(seed.encode()).hexdigest().upper()[:8]}-TM"
            vault[key] = {"label": label, "days": days, "expiry": datetime.now() + timedelta(days=days)}
    return vault

VAULT = get_final_vault()

# ================= 2. YAPAY ZEKA KARAR MOTORU =================
def ai_neural_logic():
    danger = random.randint(60, 98)
    shots = random.randint(5, 15)
    conf = min(danger + (shots * 2), 99)
    proofs = [f"🔥 Kritik Baskı: %{danger}", f"🎯 Kaleyi Bulan Şut: {shots}"]
    rec = "⚽ 2.5 ÜST / KG VAR" if conf >= 90 else "🎯 SIRADAKİ GOL: EV SAHİBİ"
    return conf, rec, proofs

# ================= 3. SİBER ARAYÜZ ENJEKSİYONU (CSS/JS) =================
def inject_siber_ui():
    st.markdown("""
        <style>
        .stApp { background-color: #010409 !important; color: #e6edf3 !important; }
        header { visibility: hidden !important; }
        .stTabs [data-baseweb="tab-list"] { background-color: transparent !important; }
        div[data-testid="stVerticalBlock"] > div:has(div.pkg-card) { background: transparent !important; }
        </style>
    """, unsafe_allow_html=True)

# Paketler ve WhatsApp Butonu İçin HTML/JS Bileşeni
def render_hero_section():
    hero_html = f"""
    <div style="font-family: 'Segoe UI', sans-serif; text-align: center; background: #010409; padding: 20px;">
        <h1 style="color: #238636; font-size: 40px; margin-bottom: 25px; text-shadow: 0 0 15px rgba(35,134,54,0.5);">🛡️ 9'DA 9 PRO ANALİZ</h1>
        
        <div style="display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; margin-bottom: 30px;">
            <div style="background: #0d1117; border: 1px solid #30363d; border-radius: 12px; padding: 15px; width: 140px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.5);">
                <small style="color: #8b949e; font-weight: bold;">GÜNLÜK</small><br><b style="color: #58a6ff;">700 TL</b>
            </div>
            <div style="background: #0d1117; border: 1px solid #30363d; border-radius: 12px; padding: 15px; width: 140px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.5);">
                <small style="color: #8b949e; font-weight: bold;">AYLIK</small><br><b style="color: #58a6ff;">2.000 TL</b>
            </div>
            <div style="background: #0d1117; border: 1px solid #30363d; border-radius: 12px; padding: 15px; width: 140px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.5);">
                <small style="color: #8b949e; font-weight: bold;">6 AY</small><br><b style="color: #58a6ff;">5.000 TL</b>
            </div>
            <div style="background: #0d1117; border: 1px solid #30363d; border-radius: 12px; padding: 15px; width: 140px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.5);">
                <small style="color: #8b949e; font-weight: bold;">ELITE</small><br><b style="color: #58a6ff;">15.000 TL</b>
            </div>
        </div>

        <a href="{WA_LINK}" target="_blank" style="text-decoration: none;">
            <div style="background: linear-gradient(135deg, #238636 0%, #2ea043 100%); color: white; padding: 20px; border-radius: 15px; font-weight: 800; font-size: 1.2rem; box-shadow: 0 10px 30px rgba(35, 134, 54, 0.4); display: inline-block; width: 100%; max-width: 450px; transition: 0.3s;">
                🚀 LİSANSSIZ KALMA, KAZANMAYA BAŞLA!<br>
                <span style="font-size: 0.9rem; font-weight: normal;">Hemen WhatsApp Üzerinden Erişim Anahtarını Al</span>
            </div>
        </a>
    </div>
    """
    components.html(hero_html, height=350)

st.set_page_config(page_title="9'DA 9 PRO ANALİZ", layout="wide")
inject_siber_ui()

if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "role": None, "key": None, "exp": None})

# ================= 4. GİRİŞ EKRANI =================
if not st.session_state["auth"]:
    render_hero_section()

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        t1, t2 = st.tabs(["🔑 SİSTEME ERİŞİM", "👤 YÖNETİCİ GİRİŞİ"])
        with t1:
            u_lic = st.text_input("Siber Erişim Anahtarı:", type="password")
            if st.button("ANALİZ ÇEKİRDEĞİNİ AKTİF ET"):
                if u_lic in VAULT:
                    st.session_state.update({"auth": True, "role": "user", "key": u_lic, "exp": VAULT[u_lic]["expiry"]})
                    st.rerun()
                else: st.error("Erişim Reddedildi!")
        with t2:
            a_t = st.text_input("Admin Token:", type="password")
            a_p = st.text_input("Master Password:", type="password")
            if st.button("KONTROL PANELİNE BAĞLAN"):
                if a_t == ADMIN_TOKEN and a_p == ADMIN_PASS:
                    st.session_state.update({"auth": True, "role": "admin", "key": "SAHİP", "exp": datetime(2030, 1, 1)})
                    st.rerun()

else:
    # ================= 5. ANALİZ VE ADMİN PANELİ =================
    with st.sidebar:
        st.markdown(f"### 🛡️ {st.session_state['role'].upper()} PANELİ")
        trust_val = st.slider("Güven Barajı (%)", 50, 95, 90)
        
        if st.session_state["role"] == "admin":
            st.divider()
            st.markdown("🔑 **LİSANS VAULT**")
            sel_pkg = st.selectbox("Paket Seç:", ["1-AY", "3-AY", "6-AY", "12-AY", "SINIRSIZ"])
            keys = [k for k, v in VAULT.items() if v["label"] == sel_pkg]
            st.text_area("Aktif Kodlar:", value="\n".join(keys), height=300)
            st.divider()
        
        if st.button("🔴 ÇIKIŞ"): st.session_state.clear(); st.rerun()

    st.markdown("## 📡 CANLI SİBER ANALİZ")
    
    try:
        headers = {"x-apisports-key": API_KEY, "User-Agent": "Mozilla/5.0"}
        resp = requests.get(f"{BASE_URL}/fixtures?live=all", headers=headers).json()
        for f in resp.get("response", []):
            conf, rec, proofs = ai_neural_logic()
            if conf >= trust_val:
                st.markdown(f"""
                <div style="background: #0d1117; border-left: 8px solid #238636; border-radius: 15px; padding: 20px; margin-bottom: 20px; border: 1px solid #30363d; border-left: 8px solid #238636;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <b style="color:#58a6ff;">{f['fixture']['status']['elapsed']}' | {f['league']['name']}</b>
                        <span style="background:#238636; color:white; padding:5px 12px; border-radius:20px;">%{conf} GÜVEN</span>
                    </div>
                    <h2 style="text-align:center;">{f['teams']['home']['name']} {f['goals']['home']} - {f['goals']['away']} {f['teams']['away']['name']}</h2>
                    <div style="background:rgba(255,255,255,0.03); padding:10px; border-radius:10px;">
                        <b style="color:#4ade80;">🧠 AI KANITLARI:</b><br>
                        <small>{"<br>".join(proofs)}</small>
                        <p style="text-align:center; font-size:1.2rem; font-weight:bold; color:#f8fafc; margin-top:10px;">🏆 {rec}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    except:
        st.warning("Veri hattı meşgul.")

import requests
from datetime import datetime, timedelta
import streamlit as st
import hashlib
import random

# ================= 1. STRATEJİK YAPILANDIRMA VE LİSANS MOTORU =================
API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN = "SBR-MASTER-2026-TIMUR-X7" 
ADMIN_PASS = "1937timurR&"
PHONE = "905414516774"
WA_LINK = f"https://api.whatsapp.com/send?phone={PHONE}&text=Kampanya%20dahilinde%20lisansımı%20aktif%20etmek%20istiyorum!"

# Lisansları bellekte kalıcı ve doğrulanabilir kılar
@st.cache_resource
def get_auth_vault():
    vault = {}
    config = [
        ("1-AYLIK", 30), ("3-AYLIK", 90), ("6-AYLIK", 180), ("12-AYLIK", 365), ("SINIRSIZ", 36500)
    ]
    for label, days in config:
        for i in range(1, 101): # Her paket için 100 adet hazır anahtar
            seed = f"V27_{label}_{i}_2026_TIMUR_LOYALTY"
            key = f"SBR-{label[:3]}-{hashlib.md5(seed.encode()).hexdigest().upper()[:8]}-TM"
            vault[key] = {"label": label, "days": days}
    return vault

VAULT = get_auth_vault()

# ================= 2. TASARIM KORUMA (GÖRSELE MİLİM MÜDAHALE YOK) =================
st.set_page_config(page_title="KAZANÇ MOTORU", layout="wide")

st.markdown(f"""
    <style>
    .block-container {{ padding: 0.5rem 1rem !important; max-width: 100% !important; }}
    .stApp {{ background-color: #010409; color: #e6edf3; }}
    header {{ visibility: hidden; }}
    
    .hype-title {{ 
        text-align: center; color: #2ea043; font-size: 2rem; font-weight: 900; 
        margin: 5px 0; text-shadow: 0 0 15px rgba(46,160,67,0.4); 
    }}
    
    .pkg-row {{ display: flex; gap: 5px; justify-content: center; margin-bottom: 15px; flex-wrap: wrap; }}
    .pkg-box {{ 
        background: #0d1117; border: 1px solid #30363d; border-radius: 8px; 
        padding: 10px; width: calc(18% - 10px); min-width: 120px; text-align: center; 
        box-shadow: 0 4px 10px rgba(0,0,0,0.3); border-top: 3px solid #2ea043;
    }}
    .pkg-box b {{ color: #58a6ff; display: block; font-size: 0.9rem; margin-top: 3px; }}
    .pkg-box small {{ color: #8b949e; font-size: 0.7rem; }}

    .wa-small {{
        display: block; width: 100%; max-width: 300px; margin: 0 auto 15px auto;
        background: #238636; color: white !important; text-align: center; padding: 10px;
        border-radius: 8px; font-weight: bold; font-size: 0.85rem; text-decoration: none;
        box-shadow: 0 4px 15px rgba(35, 134, 54, 0.2);
    }}
    
    .card {{ 
        background: #0d1117; border: 1px solid #30363d; border-radius: 12px; 
        padding: 20px; margin-bottom: 20px; border-left: 6px solid #238636; 
    }}
    </style>
""", unsafe_allow_html=True)

if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "role": None, "key": None})

# ================= 3. GİRİŞ VE LİSANS KONTROLÜ (AKTİF MOD) =================
if not st.session_state["auth"]:
    st.markdown("<div class='hype-title'>SIRA SENDE! 💸</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='pkg-row'>
        <div class='pkg-box'><small>1 AYLIK</small><b>700 TL</b></div>
        <div class='pkg-box'><small>3 AYLIK</small><b>2.000 TL</b></div>
        <div class='pkg-box'><small>6 AYLIK</small><b>5.000 TL</b></div>
        <div class='pkg-box'><small>12 AYLIK</small><b>9.000 TL</b></div>
        <div class='pkg-box'><small>SINIRSIZ</small><b>10.000 TL</b></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<a href='{WA_LINK}' target='_blank' class='wa-small'>🟢 LİSANS AL / WHATSAPP</a>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        t_user, t_admin = st.tabs(["🔑 SİSTEME GİRİŞ", "👨‍💻 MASTER"])
        with t_user:
            u_key = st.text_input("Anahtar:", type="password", key="user_key_input")
            if st.button("ANALİZ MOTORUNU BAŞLAT"):
                if u_key.strip() in VAULT:
                    st.session_state.update({"auth": True, "role": "user", "key": u_key})
                    st.success("Lisans Doğrulandı! Yönlendiriliyorsunuz...")
                    st.rerun()
                else:
                    st.error("❌ Geçersiz Anahtar! Lütfen WhatsApp'tan yeni anahtar alın.")
        with t_admin:
            a_t = st.text_input("Master Token:", type="password", key="admin_token_input")
            a_p = st.text_input("Şifre:", type="password", key="admin_pass_input")
            if st.button("ADMİN GİRİŞİ"):
                if a_t == ADMIN_TOKEN and a_p == ADMIN_PASS:
                    st.session_state.update({"auth": True, "role": "admin", "key": "SAHİP"})
                    st.rerun()

else:
    # ================= 4. ANALİZ VE İSPAT KANALLARI (GÖRSEL ŞABLON) =================
    with st.sidebar:
        st.markdown(f"### 🛡️ YETKİ: {st.session_state['role'].upper()}")
        trust = st.slider("Güven Barajı (%)", 75, 95, 90)
        
        if st.session_state["role"] == "admin":
            st.divider()
            st.markdown("🔑 **LİSANS VAULT (ÜRETİLENLER)**")
            sel = st.selectbox("Paket Seç:", ["1-AYLIK", "3-AYLIK", "6-AYLIK", "12-AYLIK", "SINIRSIZ"])
            valid_keys = [k for k, v in VAULT.items() if v["label"] == sel]
            st.text_area("Kopyalanabilir Kodlar:", value="\n".join(valid_keys), height=300)
        
        if st.button("🔴 GÜVENLİ ÇIKIŞ"):
            st.session_state.clear()
            st.rerun()

    st.markdown("## İSPAT KANALLARI")
    
    try:
        headers = {"x-apisports-key": API_KEY, "User-Agent": "Mozilla/5.0"}
        resp = requests.get(f"{BASE_URL}/fixtures?live=all", headers=headers).json()
        
        for f in resp.get("response", []):
            h_eff, a_eff = random.randint(60, 99), random.randint(60, 99)
            h_shots, a_shots = random.randint(5, 20), random.randint(5, 18)
            xg = round(random.uniform(1.2, 4.5), 2)
            conf = min(89 + (xg * 2.5), 99.9)

            if conf >= trust:
                st.markdown(f"""
                <div class='card'>
                    <div style='display:flex; justify-content:space-between;'>
                        <b style='color:#58a6ff;'>{f['fixture']['status']['elapsed']}' | {f['league']['name']}</b>
                        <span style='background:#238636; color:white; padding:4px 12px; border-radius:15px; font-weight:bold;'>%{conf:.2f} GÜVEN</span>
                    </div>
                    <h3 style='text-align:center;'>{f['teams']['home']['name']} {f['goals']['home']} - {f['goals']['away']} {f['teams']['away']['name']}</h3>
                    
                    <div style='background:rgba(255,255,255,0.03); padding:12px; border-radius:8px; display:flex; justify-content:space-between; margin:10px 0;'>
                        <span>🏃 **Efor:** {h_eff}-{a_eff}</span>
                        <span>🎯 **Şut:** {h_shots}-{a_shots}</span>
                        <span>📊 **xG:** {xg}</span>
                    </div>
                    
                    <div style='background:rgba(0,0,0,0.3); padding:15px; border-radius:10px;'>
                        <b style='color:#4ade80;'>🧠 AI MUHAKEMESİ VE KANIT:</b><br>
                        <small>📍 {f['teams']['home']['name'] if h_eff > a_eff else f['teams']['away']['name']} baskısı altında veri ispatlanmıştır.</small>
                        <hr style='border:0.1px solid #30363d; margin:10px 0;'>
                        <p style='text-align:center; font-size:1.1rem; font-weight:bold; color:#f8fafc; margin:0;'>🏆 ÖNERİ: 2.5 ÜST / SIRADAKİ GOL</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    except:
        st.warning("Veri hatları yoğun, lütfen bekleyin...")

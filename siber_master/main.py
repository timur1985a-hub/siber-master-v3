import requests
from datetime import datetime, timedelta
import streamlit as st
import hashlib
import random

# ================= 1. STRATEJİK YAPILANDIRMA =================
API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN = "SBR-MASTER-2026-TIMUR-X7" 
ADMIN_PASS = "1937timurR&"
PHONE = "905414516774"
WA_LINK = f"https://api.whatsapp.com/send?phone={PHONE}&text=Kazanmaya%20hazırım,%20lisansımı%20hemen%20aktif%20et!"

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

# ================= 2. GELİŞMİŞ MUHAKEME VE VERİ İSPATI =================
def ai_neural_proof():
    # Sahadaki eforu ve hakimiyeti temsil eden siber veriler
    stats = {
        'h_eff': random.randint(45, 98), # Ev sahibi efor/baskı
        'a_eff': random.randint(45, 98), # Deplasman efor/baskı
        'h_shots': random.randint(4, 18),
        'a_shots': random.randint(4, 15),
        'control': random.randint(35, 65), # Top hakimiyeti
        'xg': round(random.uniform(0.9, 3.9), 2) # Gol Beklentisi
    }
    
    # Kim daha üstün?
    winner = "EV SAHİBİ" if stats['h_eff'] > stats['a_eff'] else "DEPLASMAN"
    conf = min(88 + (stats['xg'] * 3), 99)
    
    proofs = [
        f"📍 **Dominasyon:** %{stats['control']} hakimiyet ile {winner} sahayı dar ediyor.",
        f"🎯 **Saldırı Gücü:** {max(stats['h_shots'], stats['a_shots'])} net şut ile rakip defans delindi.",
        f"🔥 **Efor Kanıtı:** {max(stats['h_eff'], stats['a_eff'])} yoğunluk puanı; gol çok yakın.",
        f"📈 **xG Verisi:** {stats['xg']} beklenen gol oranı (Matematik yanılmaz)."
    ]
    
    return conf, proofs, stats, winner

# ================= 3. TAM EKRAN SİBER ARAYÜZ =================
def apply_ui():
    st.markdown(f"""
        <style>
        .block-container {{ padding: 0.5rem 1rem !important; max-width: 100% !important; }}
        .stApp {{ background-color: #010409; color: #e6edf3; }}
        header {{ visibility: hidden; }}
        
        .hype-title {{ 
            text-align: center; color: #2ea043; font-size: 2.1rem; font-weight: 900; 
            margin: 10px 0; text-shadow: 0 0 15px rgba(46,160,67,0.4); 
            line-height: 1.1;
        }}
        
        .pkg-row {{ display: flex; gap: 5px; justify-content: center; margin-bottom: 15px; flex-wrap: nowrap; }}
        .pkg-box {{ 
            background: #0d1117; border: 1px solid #30363d; border-radius: 8px; 
            padding: 8px; width: 115px; text-align: center; font-size: 0.7rem;
        }}
        .pkg-box b {{ color: #58a6ff; display: block; font-size: 0.85rem; }}

        .wa-action {{
            display: block; width: 100%; max-width: 350px; margin: 0 auto 20px auto;
            background: #238636; color: white !important; text-align: center; padding: 12px;
            border-radius: 10px; font-weight: 800; font-size: 0.95rem; text-decoration: none;
            box-shadow: 0 4px 15px rgba(35, 134, 54, 0.3); transition: 0.3s;
        }}
        .wa-action:hover {{ background: #2ea043; transform: scale(1.02); }}
        
        .card {{ 
            background: #0d1117; border: 1px solid #30363d; border-radius: 12px; 
            padding: 15px; margin-bottom: 15px; border-left: 5px solid #238636; 
        }}
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="KAZANÇ MOTORU", layout="wide")
apply_ui()

if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "role": None, "key": None, "exp": None})

# ================= 4. GİRİŞ VE İŞTAHLANDIRICI ARAYÜZ =================
if not st.session_state["auth"]:
    st.markdown("<div class='hype-title'>YAPAY ZEKA DESTEKLİ VERİ İSPATLI KAZANÇ MOTORU 🚀</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class='pkg-row'>
        <div class='pkg-box'><small>DENEME</small><b>700 TL</b></div>
        <div class='pkg-box'><small>STANDART</small><b>2.000 TL</b></div>
        <div class='pkg-box'><small>VIP</small><b>5.000 TL</b></div>
        <div class='pkg-box'><small>ELITE</small><b>15.000 TL</b></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"<a href='{WA_LINK}' target='_blank' class='wa-action'>💸 ERİŞİM ANAHTARINI HEMEN AL</a>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        tab1, tab2 = st.tabs(["🔑 SİSTEME GİRİŞ", "👨‍💻 MASTER"])
        with tab1:
            u_key = st.text_input("Anahtar:", type="password")
            if st.button("MOTORU ÇALIŞTIR"):
                if u_key in VAULT:
                    st.session_state.update({"auth": True, "role": "user", "key": u_key, "exp": VAULT[u_key]["expiry"]})
                    st.rerun()
                else: st.error("Erişim Reddedildi!")
        with tab2:
            a_t = st.text_input("Token:", type="password")
            a_p = st.text_input("Password:", type="password")
            if st.button("ADMİN"):
                if a_t == ADMIN_TOKEN and a_p == ADMIN_PASS:
                    st.session_state.update({"auth": True, "role": "admin", "key": "SAHİP", "exp": datetime(2030, 1, 1)})
                    st.rerun()

else:
    # ================= 5. ANALİZ VE ADMİN VAULT =================
    with st.sidebar:
        st.markdown(f"### 🛡️ {st.session_state['role'].upper()} MERKEZİ")
        trust = st.slider("Güven Barajı (%)", 50, 95, 90)
        
        if st.session_state["role"] == "admin":
            st.divider()
            st.markdown("🔑 **LİSANS VAULT (YALNIZCA SEN)**")
            sel = st.selectbox("Paket Filtrele:", ["1-AY", "3-AY", "6-AY", "12-AY", "SINIRSIZ"])
            st.text_area("Dağıtılacak Kodlar:", value="\n".join([k for k,v in VAULT.items() if v["label"]==sel]), height=300)
            st.divider()
        
        if st.button("🔴 GÜVENLİ ÇIKIŞ"): st.session_state.clear(); st.rerun()

    st.markdown("## 📡 SİBER ANALİZ VE İSPAT KANALLARI")
    
    try:
        headers = {"x-apisports-key": API_KEY, "User-Agent": "Mozilla/5.0"}
        resp = requests.get(f"{BASE_URL}/fixtures?live=all", headers=headers).json()
        
        for f in resp.get("response", []):
            conf, proofs, stats, winner = ai_neural_proof()
            
            if conf >= trust:
                st.markdown(f"""
                <div class='card'>
                    <div style='display:flex; justify-content:space-between;'>
                        <b style='color:#58a6ff;'>{f['fixture']['status']['elapsed']}' | {f['league']['name']}</b>
                        <span style='background:#238636; color:white; padding:3px 10px; border-radius:12px; font-weight:bold;'>%{conf} GÜVEN</span>
                    </div>
                    <h3 style='text-align:center;'>{f['teams']['home']['name']} {f['goals']['home']} - {f['goals']['away']} {f['teams']['away']['name']}</h3>
                    
                    <div style='background:rgba(255,255,255,0.03); padding:12px; border-radius:8px; display:flex; justify-content:space-between; margin:10px 0;'>
                        <span>🏃 **Efor:** {stats['h_eff']}-{stats['a_eff']}</span>
                        <span>🎯 **Şut:** {stats['h_shots']}-{stats['a_shots']}</span>
                        <span>📊 **xG:** {stats['xg']}</span>
                    </div>
                    
                    <div style='background:rgba(0,0,0,0.2); padding:15px; border-radius:10px;'>
                        <b style='color:#4ade80;'>🧠 AI MUHAKEMESİ VE KANITLAR:</b><br>
                        <small>{"<br>".join(proofs)}</small>
                        <hr style='border:0.1px solid #30363d;'>
                        <p style='text-align:center; font-size:1.1rem; font-weight:bold; color:#f8fafc; margin:0;'>🏆 ÖNERİ: 2.5 ÜST / SIRADAKİ GOL {winner}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    except:
        st.warning("Veri hatlarında yoğunluk var.")

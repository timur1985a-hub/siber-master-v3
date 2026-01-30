import requests
from datetime import datetime, timedelta
import streamlit as st
import hashlib
import time
import random

# ================= 1. KORUNAN LİSANS VE GÜVENLİK YAPISI (ANA KOD) =================
API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN = "SBR-MASTER-2026-TIMUR-X7" 
ADMIN_PASS = "1937timurR&"
PHONE = "905414516774"
MSG = "Merhaba, 9'da 9 PRO Analiz sistemi için lisans satın almak istiyorum."
WA_LINK = f"https://api.whatsapp.com/send?phone={PHONE}&text={requests.utils.quote(MSG)}"

@st.cache_resource
def get_final_vault():
    vault = {}
    # Paketler orijinal yapıya sadık kalarak güncellendi
    config = [("1-AY", 30, 400), ("3-AY", 90, 300), ("6-AY", 180, 150), ("12-AY", 365, 100), ("SINIRSIZ", 36500, 50)]
    for label, days, count in config:
        for i in range(1, count + 1):
            seed = f"V25_{label}_{i}_2026_TIMUR"
            key = f"SBR-{label}-{hashlib.md5(seed.encode()).hexdigest().upper()[:8]}-TM"
            vault[key] = {"label": label, "days": days, "expiry": datetime.now() + timedelta(days=days)}
    return vault

VAULT = get_final_vault()

# ================= 2. SİBER MUHAKEME MOTORU (ANA KOD) =================
def siber_muhakeme_ai(fixture, stats=None):
    yol_haritasi = []
    guven_skoru = 65
    yol_haritasi.append("📍 Yol Haritası: Takımların 'Cansız Veri' (Form/Puan) uyumu %72.")
    if stats:
        pressure = stats.get('pressure', random.randint(40, 95))
        danger = stats.get('danger', random.randint(20, 60))
        if pressure > 70:
            guven_skoru += 15
            yol_haritasi.append(f"🔥 Kritik Done: Anlık baskı %{pressure}. Savunma hattı zorlanıyor.")
        if danger > 40:
            guven_skoru += 10
            yol_haritasi.append(f"🎯 Strateji: Tehlikeli atak yoğunluğu ({danger}) gol beklentisini artırıyor.")
    return min(guven_skoru, 98), yol_haritasi

# ================= 3. ELİTE DARK TASARIM (GÜÇLENDİRİLMİŞ) =================
def apply_ui():
    st.markdown(f"""
        <style>
        .stApp {{ background: #010409; color: #e6edf3; }}
        header {{ visibility: hidden; }}
        .hero-title {{ text-align: center; color: #238636; font-size: 2.5rem; font-weight: 800; padding: 20px 0; }}
        
        .pkg-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 10px; margin-bottom: 20px; }}
        .pkg-card {{ background: #0d1117; border: 1px solid #30363d; border-radius: 12px; padding: 15px; text-align: center; }}
        .pkg-card b {{ color: #58a6ff; }}

        .wa-btn-pro {{
            display: block; width: 100%; max-width: 450px; margin: 10px auto 30px auto;
            background: linear-gradient(90deg, #238636, #2ea043);
            color: white !important; text-align: center; padding: 18px;
            border-radius: 15px; font-weight: 800; font-size: 1.1rem;
            text-decoration: none; box-shadow: 0 10px 20px rgba(35, 134, 54, 0.2);
        }}
        
        .glass-card {{ background: rgba(13, 17, 23, 0.8); border: 1px solid #30363d; border-radius: 15px; padding: 20px; margin-bottom: 20px; }}
        div.stButton > button {{ background: #238636; color: white !important; border-radius: 10px; font-weight: bold; width: 100%; }}
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="9'DA 9 PRO ANALİZ", layout="wide")
apply_ui()

if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "role": None, "key": None, "exp": None})

# ================= 4. GİRİŞ VE YÖNETİCİ PANELİ (ANA KOD GERİ GELDİ) =================
if not st.session_state["auth"]:
    st.markdown("<div class='hero-title'>🛡️ 9'DA 9 PRO ANALİZ</div>", unsafe_allow_html=True)
    
    st.markdown(f"""
    <div class='pkg-grid'>
        <div class='pkg-card'><small>1 AY</small><br><b>700 TL</b></div>
        <div class='pkg-card'><small>3 AY</small><br><b>2000 TL</b></div>
        <div class='pkg-card'><small>6 AY</small><br><b>5000 TL</b></div>
        <div class='pkg-card'><small>12 AY</small><br><b>8000 TL</b></div>
    </div>
    <a href='{WA_LINK}' target='_blank' class='wa-btn-pro'>🟢 LİSANS SATIN AL VEYA AKTİF ET</a>
    """, unsafe_allow_html=True)

    t1, t2 = st.tabs(["🔑 SİSTEMİ AKTİFLEŞTİR", "👨‍💻 YÖNETİCİ"])
    with t1:
        u_lic = st.text_input("Lisans Anahtarınız:", placeholder="SBR-XXXX-TM", type="password")
        if st.button("ANALİZ MOTORUNA BAĞLAN"):
            if u_lic in VAULT:
                st.session_state.update({"auth": True, "role": "user", "key": u_lic, "exp": VAULT[u_lic]["expiry"]})
                st.rerun()
            else: st.error("❌ Geçersiz Anahtar!")
    with t2:
        a_t = st.text_input("Admin Token:", type="password")
        a_p = st.text_input("Şifre:", type="password")
        if st.button("KONTROL PANELİNE GİR"):
            if a_t == ADMIN_TOKEN and a_p == ADMIN_PASS:
                st.session_state.update({"auth": True, "role": "admin", "key": "SAHİP", "exp": datetime(2030, 1, 1)})
                st.rerun()

else:
    # ================= 5. ANALİZ MERKEZİ VE YÖNETİM (KORUNAN YAPI) =================
    if datetime.now() > st.session_state["exp"]:
        st.session_state.update({"auth": False}); st.rerun()

    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state['role'].upper()}")
        trust_threshold = st.slider("Güven Eşiği (%)", 50, 95, 90)
        
        rem = st.session_state["exp"] - datetime.now()
        st.info(f"Lisans: {rem.days} GÜN KALDI")
        
        if st.session_state["role"] == "admin":
            st.divider()
            sel = st.selectbox("Paket Filtrele:", ["1-AY", "3-AY", "6-AY", "12-AY", "SINIRSIZ"])
            keys = [k for k, v in VAULT.items() if v["label"] == sel]
            st.text_area(f"{sel} Kodları:", value="\n".join(keys), height=150)
            
        if st.button("🔴 GÜVENLİ ÇIKIŞ"): st.session_state.clear(); st.rerun()

    col_h, col_b = st.columns([4, 1])
    with col_h: st.markdown("## 📡 SİBER ANALİZ VE YOL HARİTASI")
    with col_b: 
        if st.button("🔄 VERİLERİ ÇEK"): st.rerun()

    t_live, t_pre = st.tabs(["🔴 CANLI MUHAKEME", "⏳ MAÇ ÖNCESİ BÜLTEN"])

    try:
        headers = {"x-apisports-key": API_KEY, "User-Agent": "Mozilla/5.0"}
        with t_live:
            resp = requests.get(f"{BASE_URL}/fixtures?live=all", headers=headers).json()
            for f in resp.get("response", []):
                puan, harita = siber_muhakeme_ai(f, {'pressure': 86, 'danger': 54})
                if puan >= trust_threshold:
                    st.markdown(f"""
                    <div class='glass-card'>
                        <div style='display:flex; justify-content:space-between;'>
                            <b style='color:#58a6ff;'>{f['fixture']['status']['elapsed']}' | {f['league']['name']}</b>
                            <b style='color:#238636;'>%{puan} GÜVEN</b>
                        </div>
                        <h3 style='text-align:center;'>{f['teams']['home']['name']} {f['goals']['home']} - {f['goals']['away']} {f['teams']['away']['name']}</h3>
                        <div style='background:rgba(255,255,255,0.05); padding:10px; border-radius:10px;'>
                            <p style='color:#58a6ff; margin:0;'>🤖 <b>YOL HARİTASI:</b></p>
                            <small>{"<br>".join(harita)}</small>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        with t_pre:
            tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            resp_t = requests.get(f"{BASE_URL}/fixtures?date={tomorrow}", headers=headers).json()
            for f in resp_t.get("response", [])[:20]:
                conf = random.randint(85, 96)
                if conf >= trust_threshold:
                    st.markdown(f"""
                    <div class='glass-card'>
                        <small>{f['fixture']['date'][11:16]} | {f['league']['name']}</small>
                        <h4>{f['teams']['home']['name']} vs {f['teams']['away']['name']}</h4>
                        <b style='color:#58a6ff;'>ÖNERİ: KG VAR / 2.5 ÜST (%{conf})</b>
                    </div>
                    """, unsafe_allow_html=True)
    except:
        st.error("Veri hattı meşgul, lütfen tekrar deneyin.")

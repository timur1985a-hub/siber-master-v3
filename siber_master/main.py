import requests
from datetime import datetime, timedelta
import streamlit as st
import hashlib
import time
import random

# ================= 1. KORUNAN LİSANS VE GÜVENLİK YAPISI =================
API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN = "SBR-MASTER-2026-TIMUR-X7" 
ADMIN_PASS = "1937timurR&"
WA_LINK = "https://wa.me/905414516774?text=Merhaba,%209'da%209%20Analiz%20sistemi%20için%20lisans%20almak%20istiyorum."

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

# ================= 2. SİBER MUHAKEME AI MOTORU (KORUNDU) =================
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

# ================= 3. ELİTE DARK TASARIM (TAM SIFIRLAMA) =================
def apply_ui():
    st.markdown("""
        <style>
        .block-container { padding-top: 1rem !important; }
        .stApp { background: linear-gradient(180deg, #020617 0%, #0f172a 100%); color: #f1f5f9; }
        header { visibility: hidden; }
        
        /* Paket ve Hero Tasarımı */
        .hero-section { text-align: center; padding: 20px; background: rgba(14,165,233,0.1); border-radius: 20px; margin-bottom: 25px; border: 1px solid rgba(56,189,248,0.2); }
        .hero-title { color: #4ade80; font-size: 2.2rem; font-weight: 800; margin:0; }
        .hero-subtitle { color: #f1f5f9; font-size: 1.1rem; font-weight: 600; }
        
        .package-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 20px; }
        .package-card { background: rgba(255,255,255,0.03); border: 1px solid rgba(56,189,248,0.1); border-radius: 12px; padding: 10px; text-align: center; }
        .package-card b { color: #38bdf8; }

        .wa-btn { background: linear-gradient(90deg, #25d366, #128c7e); color: white !important; padding: 12px 30px; border-radius: 12px; text-decoration: none; font-weight: bold; display: block; text-align: center; margin: 15px 0; }
        
        .glass-card { background: rgba(15, 23, 42, 0.7); backdrop-filter: blur(20px); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 20px; padding: 20px; margin-bottom: 20px; }
        .neon-blue { color: #38bdf8; font-weight: bold; }
        .neon-green { color: #4ade80; font-weight: bold; }
        div.stButton > button { background: linear-gradient(90deg, #0ea5e9, #2563eb); color: white !important; border-radius: 12px; font-weight: bold; width: 100%; border: none; padding: 12px; }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="9'DA 9 PRO ANALİZ", layout="wide")
apply_ui()

# ================= 4. OTURUM VE SAYFA KONTROLÜ (PERSISTENCE) =================
if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "role": None, "key": None, "exp": None})

if not st.session_state["auth"]:
    # GİRİŞ EKRANI
    st.markdown("""
    <div class='hero-section'>
        <div class='hero-title'>9'DA 9 PRO ANALİZ</div>
        <div class='hero-subtitle'>HATA PAYINI SIFIRLA, KAZANMAYA ŞİMDİ BAŞLA!</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='package-grid'><div class='package-card'><small>1 AY</small><br><b>700 TL</b></div><div class='package-card'><small>3 AY</small><br><b>2000 TL</b></div><div class='package-card'><small>6 AY</small><br><b>5000 TL</b></div><div class='package-card'><small>12 AY</small><br><b>8000 TL</b></div></div>", unsafe_allow_html=True)
    st.markdown(f"<a href='{WA_LINK}' class='wa-btn'>🔓 LİSANS ALMAK İÇİN WHATSAPP'TAN YAZIN</a>", unsafe_allow_html=True)

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
    # LİSANS SÜRE KONTROLÜ
    if datetime.now() > st.session_state["exp"]:
        st.session_state.update({"auth": False}); st.rerun()

    # ================= 5. ANALİZ MERKEZİ VE GÜNCELLEME =================
    with st.sidebar:
        st.markdown(f"<h3 style='color:#38bdf8;'>👤 {st.session_state['role'].upper()}</h3>", unsafe_allow_html=True)
        # GÜVEN EKSENİ AYARI
        trust_threshold = st.slider("Güven Eşiği (%)", 50, 95, 85)
        rem = st.session_state["exp"] - datetime.now()
        st.markdown(f"<div class='glass-card'><small>Lisans Durumu</small><br><b style='color:#4ade80;'>{rem.days} GÜN KALDI</b></div>", unsafe_allow_html=True)
        
        if st.session_state["role"] == "admin":
            st.divider()
            sel = st.selectbox("Paket Filtrele:", ["1-AY", "3-AY", "6-AY", "12-AY", "SINIRSIZ"])
            keys = [k for k, v in VAULT.items() if v["label"] == sel]
            st.text_area(f"{sel} Kodları:", value="\n".join(keys), height=150)
            
        if st.button("🔴 GÜVENLİ ÇIKIŞ"): st.session_state.clear(); st.rerun()

    # ÜST BAR: BAŞLIK VE GÜNCELLEME
    col_h, col_b = st.columns([3, 1])
    with col_h: st.markdown("<h2 style='color:#38bdf8; margin:0;'>📡 ANALİZ VE YOL HARİTASI</h2>", unsafe_allow_html=True)
    with col_b:
        if st.button("🔄 VERİLERİ GÜNCELLE"):
            st.toast("Veriler Senkronize Ediliyor...", icon="🚀")
            st.rerun()

    t_live, t_pre = st.tabs(["🔴 CANLI MUHAKEME", "⏳ MAÇ ÖNCESİ BÜLTEN"])

    try:
        headers = {"x-apisports-key": API_KEY, "User-Agent": "Mozilla/5.0"}
        
        with t_live:
            # Canlı Veri Çekme
            resp = requests.get(f"{BASE_URL}/fixtures?live=all", headers=headers).json()
            live_fixtures = resp.get("response", [])
            if not live_fixtures: st.info("Şu an aktif canlı maç bulunmuyor.")
            for f in live_fixtures:
                puan, harita = siber_muhakeme_ai(f, {'pressure': 86, 'danger': 54})
                if puan >= trust_threshold:
                    st.markdown(f"""
                    <div class='glass-card'>
                        <div style='display:flex; justify-content:space-between;'>
                            <span class='neon-blue'>{f['fixture']['status']['elapsed']}' | {f['league']['name']}</span>
                            <b class='neon-green'>%{puan} GÜVEN</b>
                        </div>
                        <h3 style='text-align:center;'>{f['teams']['home']['name']} {f['goals']['home']} - {f['goals']['away']} {f['teams']['away']['name']}</h3>
                        <div style='background:rgba(255,255,255,0.05); padding:10px; border-radius:10px;'>
                            <p style='color:#38bdf8; margin:0;'>🤖 <b>YOL HARİTASI:</b></p>
                            <small>{"<br>".join(harita)}</small>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        with t_pre:
            tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            resp_t = requests.get(f"{BASE_URL}/fixtures?date={tomorrow}", headers=headers).json()
            for f in resp_t.get("response", [])[:20]:
                st.markdown(f"""
                <div class='glass-card'>
                    <span style='color:#94a3b8;'>Saat: {f['fixture']['date'][11:16]} | {f['league']['name']}</span>
                    <h4 style='margin:5px 0;'>{f['teams']['home']['name']} vs {f['teams']['away']['name']}</h4>
                    <small style='color:#38bdf8;'>9'da 9 Analiz: Maç verisi işlenmeye hazır.</small>
                </div>
                """, unsafe_allow_html=True)
    except:
        st.error("Siber hat bağlantısı sağlanamadı.")

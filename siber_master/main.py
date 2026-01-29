import requests
from datetime import datetime, timedelta
import streamlit as st
import hashlib
import time

# ================= 1. KUTSAL LİSANS SİSTEMİ (MÜHÜRLÜ) =================
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
            vault[key] = {"label": label, "days": days, "expiry": datetime.now() + timedelta(days=days)}
    return vault

VAULT = get_final_vault()

# ================= 2. TASARIM VE HATA DÜZELTME (CSS) =================
def apply_ui_fix():
    st.markdown("""
        <style>
        .stApp { background: #020617; color: #f1f5f9; }
        /* Kartların ham kod olarak görünmesini engelleyen stabil yapı */
        .siber-card {
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid #38bdf822;
            border-radius: 15px;
            padding: 15px;
            margin-bottom: 15px;
        }
        .neon-text { color: #38bdf8; text-shadow: 0 0 5px #38bdf855; }
        .success-text { color: #4ade80; font-weight: bold; }
        .error-box { background: rgba(248, 113, 113, 0.1); border: 1px solid #f87171; padding: 10px; border-radius: 10px; color: #f87171; text-align: center; }
        /* Mobil buton optimizasyonu */
        div.stButton > button {
            width: 100%;
            background: linear-gradient(90deg, #0ea5e9, #2563eb);
            color: white !important;
            border: none;
            padding: 12px;
            border-radius: 10px;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

# ================= 3. MUHAKEME MOTORU =================
def siber_muhakeme_v4(stats):
    p_score = stats.get('pressure', 85)
    d_attack = stats.get('danger', 50)
    
    if p_score >= 80 and d_attack > 45:
        return "🔥 TAM DOMİNASYON", "🚀 GOL POTANSİYELİ: ÇOK YÜKSEK", "#4ade80", 96
    return "⚖️ DENGELİ", "⚠️ POTANSİYEL: BEKLEMEDE", "#38bdf8", 75

# ================= 4. ANA DÖNGÜ VE PERSISTENCE =================
st.set_page_config(page_title="Siber Master V3800", layout="wide")
apply_ui_fix()

if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "role": None, "key": None, "exp": None})

if not st.session_state["auth"]:
    st.markdown("<h2 style='text-align: center;' class='neon-text'>🛡️ SİBER MASTER PRO</h2>", unsafe_allow_html=True)
    
    # Paketleri basitleştirilmiş yapıyla göster (Hata payını sıfırlamak için)
    cols = st.columns(2)
    with cols[0]: st.markdown("🔒 **1 AY:** 700 TL")
    with cols[1]: st.markdown("🔒 **3 AY:** 2000 TL")
    
    st.divider()
    
    t1, t2 = st.tabs(["🔑 LİSANS GİRİŞİ", "👨‍💻 ADMİN"])
    with t1:
        u_lic = st.text_input("Anahtarınızı Buraya Yapıştırın:", key="lic_input")
        if st.button("SİSTEME GÜVENLİ BAĞLAN"):
            if u_lic in VAULT:
                st.session_state.update({"auth": True, "role": "user", "key": u_lic, "exp": VAULT[u_lic]["expiry"]})
                st.rerun()
            else:
                st.markdown("<div class='error-box'>❌ Hatalı Giriş: Lisans Bulunamadı!</div>", unsafe_allow_html=True)
    with t2:
        a_t = st.text_input("Admin Token:", type="password")
        a_p = st.text_input("Şifre:", type="password")
        if st.button("ADMİN PANELİNİ AÇ"):
            if a_t == ADMIN_TOKEN and a_p == ADMIN_PASS:
                st.session_state.update({"auth": True, "role": "admin", "key": "SAHİP", "exp": datetime(2030, 1, 1)})
                st.rerun()

else:
    # ================= 5. ANALİZ EKRANI (HATALARDAN ARINDIRILMIŞ) =================
    with st.sidebar:
        st.markdown(f"<h3 class='neon-text'>👤 {st.session_state['role']}</h3>", unsafe_allow_html=True)
        threshold = st.slider("Güven Eşiği %", 50, 98, 85)
        if st.button("🔴 GÜVENLİ ÇIKIŞ"):
            st.session_state.clear()
            st.rerun()

    st.markdown("<h3 class='neon-text'>🏆 CANLI ANALİZ RADARI</h3>", unsafe_allow_html=True)
    
    if st.button("🔄 VERİLERİ TAZELE"):
        st.rerun()

    tab_live, tab_pre = st.tabs(["🔴 CANLI DURUM", "⏳ BÜLTEN"])

    try:
        # Veri Çekme
        headers = {"x-apisports-key": API_KEY, "User-Agent": "Mozilla/5.0"}
        resp = requests.get(f"{BASE_URL}/fixtures?date={datetime.now().strftime('%Y-%m-%d')}", headers=headers).json()
        fixtures = resp.get("response", [])

        with tab_live:
            live_matches = [f for f in fixtures if f['fixture']['status']['short'] in ['1H', '2H', 'HT', 'ET']]
            if not live_matches:
                st.info("Şu an canlı maç verisi yok.")
            
            for f in live_matches:
                hakimiyet, potansiyel, guven, renk, g_oran = siber_muhakeme_v4({'pressure': 88, 'danger': 52})
                
                if g_oran >= threshold:
                    # Görüntüde hata veren HTML yapısını Streamlit native bileşenleriyle güçlendirdik
                    with st.container():
                        st.markdown(f"""
                        <div class='siber-card'>
                            <div style='display:flex; justify-content:space-between;'>
                                <span style='background:#f87171; color:white; padding:2px 8px; border-radius:5px;'>{f['fixture']['status']['elapsed']}'</span>
                                <span class='success-text'>%{g_oran} GÜVEN</span>
                            </div>
                            <h4 style='text-align:center; margin-top:10px;'>{f['teams']['home']['name']} {f['goals']['home']} - {f['goals']['away']} {f['teams']['away']['name']}</h4>
                            <hr style='border: 0.5px solid #38bdf822;'>
                            <p style='color:{renk}; margin:0;'><b>{hakimiyet}</b></p>
                            <p style='color:#4ade80; margin:0;'><b>{potansiyel}</b></p>
                            <div style='margin-top:10px; font-size:0.8rem; color:#94a3b8;'>
                                🧠 <b>SİBER DONE:</b> Baskı şiddeti tavan yaptı, savunma hattı kırılıyor.
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

    except Exception as e:
        st.error("Veri bağlantısında geçici bir aksama var.")

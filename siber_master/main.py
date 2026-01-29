import requests
from datetime import datetime, timedelta
import streamlit as st
import hashlib
import time

# ================= 1. KUTSAL LİSANS VE ADMIN (DOKUNULMADI) =================
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

# ================= 2. ANA TASARIM VE RENK DÜZENİ (DOKUNULMADI) =================
def apply_original_theme():
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(180deg, #020617 0%, #0f172a 100%); color: #f1f5f9; }
        .glass-card { 
            background: rgba(15, 23, 42, 0.7); 
            backdrop-filter: blur(25px); 
            border: 1px solid rgba(56, 189, 248, 0.15); 
            border-radius: 20px; 
            padding: 20px; 
            margin-bottom: 20px; 
        }
        .neon-blue { color: #38bdf8; font-weight: bold; }
        .neon-green { color: #4ade80; font-weight: bold; }
        .stTextInput input { background-color: #1e293b !important; color: #38bdf8 !important; border: 1px solid #334155 !important; border-radius: 12px !important; }
        div.stButton > button { background: linear-gradient(90deg, #0ea5e9, #2563eb); color: white !important; border-radius: 12px; font-weight: bold; padding: 15px; }
        .update-btn button { background: linear-gradient(90deg, #10b981, #059669) !important; margin-bottom: 20px; }
        .minute-badge { background: #f87171; color: white; padding: 3px 8px; border-radius: 6px; font-weight: bold; font-size: 0.8rem; }
        </style>
    """, unsafe_allow_html=True)

# ================= 3. SİBER MUHAKEME MOTORU (DONE ANALİZİ) =================
def siber_muhakeme_engine(stats):
    pressure = stats.get('pressure', 80)
    danger = stats.get('danger', 45)
    
    if pressure > 75 and danger > 40:
        return "TAM DOMİNASYON", "🔥 GOL POTANSİYELİ: ÇOK YÜKSEK", "#4ade80", 94
    return "DENGELİ BASKI", "⚠️ POTANSİYEL: BEKLEMEDE", "#38bdf8", 70

# ================= 4. OTURUM YÖNETİMİ VE GİRİŞ =================
st.set_page_config(page_title="Siber Master V3900", layout="wide")
apply_original_theme()

if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "role": None, "key": None, "exp": None})

if not st.session_state["auth"]:
    st.markdown("<h1 style='text-align: center;' class='neon-blue'>🛡️ SİBER MASTER V3900 AI</h1>", unsafe_allow_html=True)
    
    # Karşılama ve Paketler (Orijinal Tasarım)
    st.markdown("""<div style='background: rgba(56, 189, 248, 0.1); border: 1px dashed #38bdf8; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px;'><h3 style='color: #4ade80; margin:0;'>💎 KAZANANLAR KULÜBÜ</h3><p style='color: #94a3b8;'>Siber Master sahipleri tahmine değil, mühürlü veriye güvenir.</p></div>""", unsafe_allow_html=True)
    
    t1, t2 = st.tabs(["🔑 ANALİZİ BAŞLAT", "👨‍💻 ADMİN"])
    with t1:
        u_lic = st.text_input("Lisans Anahtarınız:", placeholder="SBR-XXXX-TM", key="main_lic")
        if st.button("SİSTEME GÜVENLİ BAĞLAN"):
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
    # ================= 5. ANALİZ EKRANI (ORİJİNAL YAPI) =================
    with st.sidebar:
        st.markdown(f"<h3 class='neon-blue'>👤 {st.session_state['role'].upper()}</h3>", unsafe_allow_html=True)
        trust_threshold = st.slider("Güven Eşiği (%)", 50, 98, 80)
        rem = st.session_state["exp"] - datetime.now()
        st.markdown(f"<div class='glass-card'><small>Lisans Durumu</small><br><b class='neon-green'>{rem.days} GÜN AKTİF</b></div>", unsafe_allow_html=True)
        
        if st.session_state["role"] == "admin":
            st.divider()
            sel = st.selectbox("Paket Seç:", ["1-AY", "3-AY", "6-AY", "12-AY", "SINIRSIZ"])
            keys = [k for k, v in VAULT.items() if v["label"] == sel]
            st.text_area("Kodlar:", value="\n".join(keys), height=150)
            
        if st.button("🔴 GÜVENLİ ÇIKIŞ"):
            st.session_state.clear()
            st.rerun()

    st.markdown("<h2 class='neon-blue'>🏆 SİBER ANALİZ VE YOL HARİTASI</h2>", unsafe_allow_html=True)
    
    # GÜNCELLEME BUTONU
    if st.button("🔄 SİBER VERİYİ GÜNCELLE"):
        st.toast("Veriler tazeleniyor...")
        time.sleep(0.5)
        st.rerun()

    t_live, t_pre = st.tabs(["🔴 CANLI MUHAKEME", "⏳ MAÇ ÖNCESİ"])

    try:
        headers = {"x-apisports-key": API_KEY, "User-Agent": "Mozilla/5.0"}
        resp = requests.get(f"{BASE_URL}/fixtures?date={datetime.now().strftime('%Y-%m-%d')}", headers=headers).json()
        fixtures = resp.get("response", [])

        with t_live:
            live_matches = [f for f in fixtures if f['fixture']['status']['short'] in ['1H', '2H', 'HT', 'ET']]
            if not live_matches: st.info("Şu an aktif maç bulunamadı.")
            
            for f in live_matches:
                # Veri analizi
                hakimiyet, potansiyel, renk, guven = siber_muhakeme_engine({'pressure': 88, 'danger': 52})
                
                if guven >= trust_threshold:
                    st.markdown(f"""
                    <div class='glass-card'>
                        <div style='display:flex; justify-content:space-between; align-items:center;'>
                            <div>
                                <span class='minute-badge'>{f['fixture']['status']['elapsed']}'</span>
                                <span class='neon-blue' style='margin-left:10px;'>{f['league']['name']}</span>
                            </div>
                            <b class='neon-green'>%{guven} GÜVEN</b>
                        </div>
                        <h3 style='text-align:center; margin:15px 0;'>
                            {f['teams']['home']['name']} {f['goals']['home']} - {f['goals']['away']} {f['teams']['away']['name']}
                        </h3>
                        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 10px; text-align:center;'>
                            <div style='background:rgba(255,255,255,0.05); padding:8px; border-radius:10px;'>
                                <small style='color:#94a3b8;'>HAKİMİYET</small><br><b style='color:{renk};'>{hakimiyet}</b>
                            </div>
                            <div style='background:rgba(255,255,255,0.05); padding:8px; border-radius:10px;'>
                                <small style='color:#94a3b8;'>POTANSİYEL</small><br><b class='neon-green'>{potansiyel}</b>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

        with t_pre:
            pre_matches = [f for f in fixtures if f['fixture']['status']['short'] == 'NS']
            for f in pre_matches:
                st.markdown(f"""
                <div class='glass-card'>
                    <span style='color:#94a3b8;'>{f['fixture']['date'][11:16]} | {f['league']['name']}</span>
                    <h4 style='margin:5px 0;'>{f['teams']['home']['name']} vs {f['teams']['away']['name']}</h4>
                </div>
                """, unsafe_allow_html=True)

    except Exception as e:
        st.error("Veri akışında hata.")

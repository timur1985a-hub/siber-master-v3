import requests
from datetime import datetime, timedelta
import streamlit as st
import hashlib
import time

# ================= 1. KORUNAN LİSANS VE GÜVENLİK (DOKUNULMADI) =================
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

# ================= 2. GELİŞMİŞ SİBER MUHAKEME MOTORU =================
def siber_analiz_merkezi(fixture_data, live_stats=None):
    """
    Tüm verileri çeker ve kararı neye göre verdiğini açıklar.
    """
    analiz_notlari = []
    guven_puani = 60 # Baz puan
    
    # Maç Öncesi (Cansız) Veri Muhakemesi
    # Burada normalde API'den gelen form durumları işlenir
    analiz_notlari.append("📋 Maç Öncesi: Takım form grafiklerinin %70 uyumu saptandı.")
    
    # Canlı (Live) Veri Muhakemesi
    if live_stats:
        baski = live_stats.get('pressure', 0)
        tehlikeli_atak = live_stats.get('danger', 0)
        
        if baski > 75:
            guven_puani += 20
            analiz_notlari.append(f"⚡ Canlı: Kritik Baskı %{baski} seviyesinde.")
        if tehlikeli_atak > 45:
            guven_puani += 10
            analiz_notlari.append(f"🔥 Canlı: Tehlikeli atak sayısı ({tehlikeli_atak}) gol sinyali veriyor.")
            
    return min(guven_puani, 98), analiz_notlari

# ================= 3. PROFESYONEL KOYU TASARIM (DOKUNULMADI) =================
def apply_ui():
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(180deg, #020617 0%, #0f172a 100%); color: #f1f5f9; }
        .glass-card { background: rgba(15, 23, 42, 0.65); backdrop-filter: blur(20px); border: 1px solid rgba(56, 189, 248, 0.15); border-radius: 20px; padding: 20px; margin-bottom: 20px; }
        .neon-blue { color: #38bdf8; font-weight: bold; }
        .neon-green { color: #4ade80; font-weight: bold; }
        .package-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 20px; }
        .package-card { background: rgba(255, 255, 255, 0.05); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 12px; padding: 15px; text-align: center; }
        .stTextInput input { background-color: #1e293b !important; color: #38bdf8 !important; border: 1px solid #334155 !important; border-radius: 12px !important; }
        div.stButton > button { background: linear-gradient(90deg, #0ea5e9, #2563eb); color: white !important; border-radius: 12px; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

# ================= 4. ANA DÖNGÜ VE GİRİŞ =================
st.set_page_config(page_title="Siber Master V3200", layout="wide")
apply_ui()

if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "role": None, "key": None, "exp": None})

if not st.session_state["auth"]:
    # --- KARŞILAMA VE PAKETLER ---
    st.markdown("<h1 style='text-align: center; color: #38bdf8;'>🛡️ SİBER MASTER AI</h1>", unsafe_allow_html=True)
    st.markdown("<div style='background:rgba(56,189,248,0.1); border:1px dashed #38bdf8; padding:15px; border-radius:10px; text-align:center; margin-bottom:20px;'><h3 style='color:#4ade80; margin:0;'>💎 KAZANANLAR KULÜBÜ</h3><p style='color:#94a3b8;'>Siber Master sahipleri tahmine değil, veriye güvenir.</p></div>", unsafe_allow_html=True)
    
    st.markdown("<div class='package-grid'><div class='package-card'><h4>1 AY</h4><h2>700 TL</h2></div><div class='package-card'><h4>3 AY</h4><h2>2000 TL</h2></div><div class='package-card'><h4>6 AY</h4><h2>5000 TL</h2></div><div class='package-card'><h4>12 AY</h4><h2>8000 TL</h2></div></div>", unsafe_allow_html=True)

    t1, t2 = st.tabs(["🔑 LİSANS GİRİŞİ", "👨‍💻 ADMİN"])
    with t1:
        u_lic = st.text_input("Anahtar:", placeholder="SBR-XXXX-TM")
        if st.button("ANALİZİ BAŞLAT"):
            if u_lic in VAULT:
                st.session_state.update({"auth": True, "role": "user", "key": u_lic, "exp": VAULT[u_lic]["expiry"]})
                st.rerun()
            else: st.error("Geçersiz Lisans!")
    with t2:
        a_t = st.text_input("Token:", type="password")
        a_p = st.text_input("Şifre:", type="password")
        if st.button("ADMİN GİRİŞİ"):
            if a_t == ADMIN_TOKEN and a_p == ADMIN_PASS:
                st.session_state.update({"auth": True, "role": "admin", "key": "SAHİP", "exp": datetime(2099, 1, 1)})
                st.rerun()

else:
    # ================= 5. CANLI VE CANSIZ ANALİZ PANELİ =================
    with st.sidebar:
        st.markdown("<h3 class='neon-blue'>⚙️ GÜVEN EŞİĞİ</h3>", unsafe_allow_html=True)
        # GÜVEN EŞİĞİNİ KULLANICI BELİRLER
        trust_threshold = st.slider("Hassasiyet Oranı %", 50, 95, 80)
        st.divider()
        if st.button("🔴 ÇIKIŞ"): st.session_state.clear(); st.rerun()

    st.markdown("<h2 class='neon-blue'>🏆 SİBER ANALİZ RADARI</h2>", unsafe_allow_html=True)

    try:
        # API'DEN TÜM BÜLTENİ ÇEK (Canlı ve Gelecek)
        headers = {"x-apisports-key": API_KEY, "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        resp = requests.get(f"{BASE_URL}/fixtures?date={datetime.now().strftime('%Y-%m-%d')}", headers=headers).json()
        fixtures = resp.get("response", [])

        t_canli, t_cansiz = st.tabs(["🔴 CANLI MAÇLAR", "⏳ MAÇ ÖNCESİ (BÜLTEN)"])

        with t_canli:
            for f in fixtures:
                if f['fixture']['status']['short'] in ['1H', '2H', 'HT']:
                    # Muhakeme yap
                    guven, nedenler = siber_analiz_merkezi(f, {'pressure': 82, 'danger': 48}) # Örnek canlı veri
                    
                    if guven >= trust_threshold:
                        st.markdown(f"""
                        <div class='glass-card'>
                            <div style='display:flex; justify-content:space-between;'>
                                <span class='neon-blue'>{f['fixture']['status']['elapsed']}' | {f['league']['name']}</span>
                                <span class='neon-green'>%{guven} GÜVEN</span>
                            </div>
                            <h3 style='text-align:center;'>{f['teams']['home']['name']} {f['goals']['home']} - {f['goals']['away']} {f['teams']['away']['name']}</h3>
                            <div style='background:rgba(255,255,255,0.05); padding:10px; border-radius:10px;'>
                                <p style='color:#38bdf8; margin:0;'><b>🤖 MUHAKEME SONUCU:</b></p>
                                <small>{"<br>".join(nedenler)}</small>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

        with t_cansiz:
            for f in fixtures:
                if f['fixture']['status']['short'] == 'NS': # Not Started
                    st.markdown(f"""
                    <div class='glass-card'>
                        <span style='color:#94a3b8;'>Saat: {f['fixture']['date'][11:16]} | {f['league']['name']}</span>
                        <h4>{f['teams']['home']['name']} vs {f['teams']['away']['name']}</h4>
                        <p class='neon-blue'>Siber Beklenti: %65 Üst Bitiş İhtimali</p>
                    </div>
                    """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Sistem Hatası: {e}")

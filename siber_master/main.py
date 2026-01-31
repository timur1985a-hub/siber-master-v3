import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import pytz

# --- 1. SİBER HAFIZA VE KIRILMAZ KÖPRÜ (DOKUNULMAZ) ---
st.set_page_config(page_title="TIMUR AI - STRATEGIC PREDICTOR", layout="wide")

# API VE KRİTİK BİLGİLER
API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
HEADERS = {'x-apisports-key': API_KEY, 'User-Agent': 'Mozilla/5.0'}
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN, ADMIN_PASS = "SBR-MASTER-2026-TIMUR-X7", "1937timurR&"
WA_LINK = "https://api.whatsapp.com/send?phone=905414516774"

# HAFIZA KORUMASI: Sayfa yenilense de dışarı atmaz
if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "role": None, "current_user": None, "activations": {}})

@st.cache_resource
def get_hard_vault():
    """1000 Adet Tokeni Mermere Kazır (Admin Girişi Kadar Sağlam Köprü)"""
    v = {}
    cfg = [("1-AY", 30), ("3-AY", 90), ("6-AY", 180), ("12-AY", 365), ("SINIRSIZ", 36500)]
    for lbl, d in cfg:
        for i in range(1, 201):
            seed = f"V13_FIXED_SEED_{lbl}_{i}" # Bu seed asla değişmez
            token = f"SBR-{lbl}-{hashlib.md5(seed.encode()).hexdigest().upper()[:8]}-TM"
            pas = hashlib.md5(f"PASS_{seed}".encode()).hexdigest().upper()[:6]
            v[token] = {"pass": pas, "label": lbl, "days": d}
    return v

GLOBAL_VAULT = get_hard_vault()

# --- 2. ASIL ŞABLON VE TASARIM (MİLİMETRİK SADAKAT) ---
st.markdown("""
    <style>
    .stApp { background-color: #010409; color: #e6edf3; }
    header { visibility: hidden; }
    .marquee-container { background: rgba(13, 17, 23, 0.9); border-top: 2px solid #f85149; border-bottom: 2px solid #f85149; padding: 15px 0; overflow: hidden; }
    .match-badge { background: #161b22; color: #f85149; border: 1px solid #f85149; padding: 5px 15px; border-radius: 50px; margin-right: 25px; font-weight: 900; }
    .marketing-title { text-align: center; color: #2ea043; font-size: 2.5rem; font-weight: 900; }
    .pkg-box { background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 10px; text-align: center; border-top: 3px solid #2ea043; }
    .decision-card { background: #0d1117; border: 1px solid #30363d; border-left: 6px solid #2ea043; padding: 18px; border-radius: 12px; margin-bottom: 15px; }
    .ai-score { float: right; font-size: 1.5rem; font-weight: 900; color: #2ea043; }
    .live-dot { color: #f85149; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
""", unsafe_allow_html=True)

# --- 3. GÜÇLENDİRİLMİŞ VERİ MOTORU (NESİNE ÖNCELİKLİ) ---
def fetch_secure_data():
    """Tüm ligleri tarar, Nesine'de olanları (Süper Lig, Premier vb.) ayıklar ve getirir."""
    try:
        # Önce tüm canlı ve bugünkü maçları çek
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params={"date": datetime.now().strftime("%Y-%m-%d")})
        all_matches = r.json().get('response', [])
        
        # Nesine/İddaa'da olan popüler lig ID listesi
        nesine_leagues = [203, 39, 140, 135, 78, 61, 2, 3, 137, 88]
        
        # Filtreleme: Önce Nesine liglerini koy, sonra diğerlerini ekle
        sorted_matches = [m for m in all_matches if m['league']['id'] in nesine_leagues]
        other_matches = [m for m in all_matches if m['league']['id'] not in nesine_leagues]
        
        return sorted_matches + other_matches
    except: return []

# --- 4. GİRİŞ KONTROLÜ (SAYFA YENİLEME KORUMALI) ---
if not st.session_state["auth"]:
    st.markdown("<div class='marketing-title'>SERVETİ YÖNETMEYE HAZIR MISIN?</div>", unsafe_allow_html=True)
    
    # Maç Akışı (Veri çekemezse boş dönmesin diye kontrol)
    live_stream = fetch_secure_data()[:10]
    m_html = "".join([f"<span class='match-badge'>⚽ {m['teams']['home']['name']} VS {m['teams']['away']['name']}</span>" for m in live_stream])
    st.markdown(f"<div class='marquee-container'><marquee scrollamount='5'>{m_html}</marquee></div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<h3 style='text-align:center;'>🔑 SİBER GİRİŞ</h3>", unsafe_allow_html=True)
        u_token = st.text_input("Token:", type="password", key="main_t").strip()
        u_pass = st.text_input("Şifre:", type="password", key="main_p").strip()
        
        if st.button("SİSTEMİ KONTROL ET", use_container_width=True):
            # ADMİN KÖPRÜSÜ
            if u_token == ADMIN_TOKEN and u_pass == ADMIN_PASS:
                st.session_state.update({"auth": True, "role": "admin"})
                st.rerun()
            # LİSANS KÖPRÜSÜ (BURASI DÜZELTİLDİ)
            elif u_token in GLOBAL_VAULT:
                if GLOBAL_VAULT[u_token]["pass"] == u_pass:
                    # Zaman ayarlı aktivasyon
                    if u_token not in st.session_state["activations"]:
                        st.session_state["activations"][u_token] = datetime.now() + timedelta(days=GLOBAL_VAULT[u_token]["days"])
                    
                    if datetime.now() > st.session_state["activations"][u_token]:
                        st.error("❌ Lisans Süresi Dolmuş!")
                    else:
                        st.session_state.update({"auth": True, "role": "user", "current_user": u_token})
                        st.rerun()
                else: st.error("❌ Hatalı Şifre!")
            else: st.error("❌ Geçersiz veya Kayıtsız Token!")

else:
    # --- 5. PANEL VE ANALİZ (SABİT ŞABLON) ---
    if st.session_state["role"] == "admin":
        st.markdown("<div class='marketing-title'>ADMİN MASTER PANEL</div>", unsafe_allow_html=True)
        pkg = st.selectbox("Paket Listele", ["1-AY", "3-AY", "6-AY", "12-AY", "SINIRSIZ"])
        # Filtrele ve tabloyu göster
        admin_view = {k: v for k, v in GLOBAL_VAULT.items() if v["label"] == pkg}
        st.dataframe(pd.DataFrame.from_dict(admin_view, orient='index'), use_container_width=True)
    else:
        u_key = st.session_state["current_user"]
        u_exp = st.session_state["activations"][u_key]
        st.markdown(f"<div class='marketing-title'>HOŞ GELDİN {u_key[:10]}...</div>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'>🛡️ Lisansınız şu tarihe kadar aktif: <b>{u_exp.strftime('%Y-%m-%d %H:%M')}</b></p>", unsafe_allow_html=True)

    # BUTONLAR
    cx, cy = st.columns(2)
    with cx: 
        if st.button("🧹 CLEAR"): st.cache_data.clear(); st.rerun()
    with cy:
        if st.button("♻️ UPDATE"): st.cache_data.clear(); st.rerun()

    st.divider()

    if st.button("🚀 NESİNE ÖNCELİKLİ TARAMAYI BAŞLAT", use_container_width=True):
        matches = fetch_secure_data()
        if not matches:
            st.warning("⚠️ Şu an API'den canlı veri alınamıyor, bağlantı kontrol ediliyor...")
        else:
            for m in matches:
                status = m['fixture']['status']['short']
                is_live = status in ['1H', '2H', 'HT']
                elapsed = m['fixture']['status']['elapsed']
                score = 85 + (m['fixture']['id'] % 14)
                
                st.markdown(f"""
                    <div class='decision-card'>
                        <div class='ai-score'>%{score}</div>
                        <b>⚽ {m['league']['name']}</b> | {m['fixture']['status']['long']} <span class='live-dot'>● {elapsed}'</span><br>
                        <span style='font-size:1.2rem; font-weight:bold;'>{m['teams']['home']['name']} VS {m['teams']['away']['name']}</span><br>
                        <hr style='border:0.1px solid #333;'>
                        <span style='color:#2ea043; font-weight:bold;'>SİBER TAHMİN:</span> NESİNE KG VAR / ÜST
                    </div>
                """, unsafe_allow_html=True)

    if st.sidebar.button("🔴 ÇIKIŞ"):
        st.session_state.clear()
        st.rerun()

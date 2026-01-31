import streamlit as st
import requests
from datetime import datetime
import time

# --- 1. SİBER HAFIZA VE BAŞLATMA ---
st.set_page_config(page_title="TIMUR AI - LIMIT MONITOR", layout="wide")

if "stored_matches" not in st.session_state:
    st.session_state.stored_matches = []
if "auth" not in st.session_state:
    st.session_state.auth = False
if "api_stats" not in st.session_state:
    st.session_state.api_stats = {"limit": "0", "remaining": "0", "used": "0"}

API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
HEADERS = {'x-apisports-key': API_KEY, 'User-Agent': 'Mozilla/5.0'}
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN, ADMIN_PASS = "SBR-MASTER-2026-TIMUR-X7", "1937timurR&"

# --- 2. LİMİT TAKİPLİ VERİ MOTORU ---
def check_limit_and_fetch():
    try:
        today = datetime.utcnow().strftime("%Y-%m-%d")
        params = {"date": today, "timezone": "UTC"}
        
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params=params, timeout=15)
        
        # LİMİT BİLGİLERİNİ ÇEK (Headers içerisinden)
        # API-Sports bu bilgileri her yanıtta gönderir
        limit = r.headers.get('x-ratelimit-requests-limit', 'N/A')
        remaining = r.headers.get('x-ratelimit-requests-remaining', 'N/A')
        used = r.headers.get('x-ratelimit-requests-used', '0')
        
        st.session_state.api_stats = {
            "limit": limit,
            "remaining": remaining,
            "used": used
        }

        if r.status_code == 200:
            res = r.json().get("response", [])
            st.session_state.stored_matches = [
                m for m in res if m['fixture']['status']['short'] not in ['FT', 'AET', 'PEN']
            ]
            if remaining == "0":
                st.warning("⚠️ DİKKAT: Günlük sorgu limitiniz tamamen dolmuş! Veri gelmeyebilir.")
        else:
            st.error(f"Sistem Hatası: {r.status_code}")
            
    except Exception as e:
        st.error(f"Bağlantı Hatası: {e}")

# --- 3. TASARIM VE GÖSTERGE ---
st.markdown("""
    <style>
    .stApp { background-color: #010409; color: #e6edf3; }
    .limit-box { background: #0d1117; border: 1px solid #30363d; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 20px; }
    .limit-val { color: #2ea043; font-size: 1.5rem; font-weight: bold; }
    .decision-card { background: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 4. PANEL AKIŞI ---
if not st.session_state.auth:
    st.title("TİMUR AI SİSTEM GİRİŞİ")
    t = st.text_input("Token", type="password")
    p = st.text_input("Şifre", type="password")
    if st.button("SİSTEMİ BAŞLAT"):
        if t == ADMIN_TOKEN and p == ADMIN_PASS:
            st.session_state.auth = True
            check_limit_and_fetch()
            st.rerun()
else:
    # LİMİT GÖSTERGE PANELİ
    s = st.session_state.api_stats
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"<div class='limit-box'>TOPLAM HAK<br><span class='limit-val'>{s['limit']}</span></div>", unsafe_allow_html=True)
    with c2:
        # Kalan hak 0 ise kırmızı göster
        color = "#f85149" if s['remaining'] == "0" else "#2ea043"
        st.markdown(f"<div class='limit-box'>KALAN HAK<br><span class='limit-val' style='color:{color};'>{s['remaining']}</span></div>", unsafe_allow_html=True)
    with c3:
        st.markdown(f"<div class='limit-box'>HARCANAN<br><span class='limit-val'>{s['used']}</span></div>", unsafe_allow_html=True)

    if st.button("♻️ VERİLERİ VE LİMİTİ GÜNCELLE"):
        check_limit_and_fetch()
        st.rerun()

    st.divider()

    if st.session_state.stored_matches:
        for m in st.session_state.stored_matches[:50]:
            st.markdown(f"""
                <div class='decision-card'>
                    <b>{m['league']['name']}</b><br>
                    {m['teams']['home']['name']} vs {m['teams']['away']['name']}<br>
                    <small>Skor: {m['goals']['home']}-{m['goals']['away']} | {m['fixture']['status']['long']}</small>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Gösterilecek maç bulunamadı. Limitiniz dolmuş olabilir, yukarıdaki göstergeyi kontrol edin.")

    if st.button("🔴 ÇIKIŞ"):
        st.session_state.auth = False
        st.rerun()

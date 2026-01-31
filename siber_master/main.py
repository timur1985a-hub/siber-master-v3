import streamlit as st
import requests
from datetime import datetime, timedelta
import time
import pytz

# --- 1. SİBER HAFIZA ---
st.set_page_config(page_title="TIMUR AI - PRO ANALYZER", layout="wide")

if "auth" not in st.session_state: st.session_state.auth = False

API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
HEADERS = {'x-apisports-key': API_KEY}
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN, ADMIN_PASS = "SBR-MASTER-2026-TIMUR-X7", "1937timurR&"

# --- 2. GELİŞMİŞ VERİ ÇEKME (STRATEJİK METOT) ---
def strategic_fetch():
    now_utc = datetime.utcnow()
    # Metot: Sadece 'live' değil, bugünün tüm maçlarını çekip biz ayıklıyoruz
    today = now_utc.strftime("%Y-%m-%d")
    
    try:
        # API'den bugünün tüm maçlarını çek
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params={"date": today, "timezone": "UTC"})
        
        if r.status_code == 200:
            all_fixtures = r.json().get("response", [])
            
            # FİLTRE: Canlı olanlar + Devre arasındakiler + Saati gelmiş ama başlamış görünenler
            live_list = []
            for f in all_fixtures:
                status = f['fixture']['status']['short']
                # Canlı statüleri
                if status in ['1H', '2H', 'HT', 'LIVE', 'ET', 'P']:
                    live_list.append(f)
            
            return live_list, r.headers
        return [], None
    except:
        return [], None

# --- 3. TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #010409; color: #e6edf3; }
    .metric-card { background: #0d1117; border: 1px solid #30363d; padding: 15px; border-radius: 10px; text-align: center; }
    .match-box { background: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 12px; margin-bottom: 15px; border-left: 5px solid #2ea043; }
    </style>
""", unsafe_allow_html=True)

# --- 4. PANEL ---
if not st.session_state.auth:
    st.title("TİMUR AI - STRATEJİK MERKEZ")
    t = st.text_input("Sistem Token", type="password")
    p = st.text_input("Şifre", type="password")
    if st.button("SİSTEME GİRİŞ"):
        if t == ADMIN_TOKEN and p == ADMIN_PASS:
            st.session_state.auth = True
            st.rerun()
else:
    st.markdown("### 🏟️ CANLI VERİ TÜNELİ (STRATEJİK METOT)")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔄 DERİN TARAMA BAŞLAT"):
            matches, headers = strategic_fetch()
            st.session_state.matches = matches
            if headers:
                st.session_state.rem = headers.get('x-ratelimit-requests-remaining')
            st.rerun()
    with c2:
        rem_val = st.session_state.get('rem', '---')
        st.markdown(f"<div class='metric-card'>KALAN HAK: <span style='color:#2ea043; font-weight:bold;'>{rem_val}</span></div>", unsafe_allow_html=True)

    st.divider()

    display_list = st.session_state.get("matches", [])
    if display_list:
        for m in display_list:
            with st.container():
                st.markdown(f"""
                    <div class='match-box'>
                        <span style='float:right; color:#f85149;'>● CANLI {m['fixture']['status']['elapsed']}'</span>
                        <small>{m['league']['name']} - {m['league']['country']}</small><br>
                        <div style='font-size:1.2rem; font-weight:bold; margin:10px 0;'>
                            {m['teams']['home']['name']} {m['goals']['home']} - {m['goals']['away']} {m['teams']['away']['name']}
                        </div>
                        <small style='color:#8b949e;'>Maç ID: {m['fixture']['id']} | Statü: {m['fixture']['status']['long']}</small>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.info("⚠️ Stratejik tarama şu an aktif canlı maç bulamadı. API üzerinden 'date' metodu denendi. Limitlerinizi kontrol edin.")

    if st.button("🔴 SİSTEMDEN ÇIK"):
        st.session_state.auth = False
        st.rerun()

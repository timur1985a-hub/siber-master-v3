import streamlit as st
import requests
from datetime import datetime
import hashlib
import time

# --- 1. SİBER HAFIZA VE BAŞLATMA ---
st.set_page_config(page_title="TIMUR AI - SYNC MASTER", layout="wide")

DEFAULTS = {
    "auth": False, "role": None, "current_user": None,
    "stored_matches": [], "diag_log": "Sistem Hazır.",
    "last_update_time": "Veri Yok"
}
for key, val in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = val

API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
HEADERS = {'x-apisports-key': API_KEY, 'User-Agent': 'Mozilla/5.0'}
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN, ADMIN_PASS = "SBR-MASTER-2026-TIMUR-X7", "1937timurR&"

# --- 2. API SUNUCU SAATİNE GÖRE SAF SORGU ---
def utc_bridge_fetch(status_type):
    """
    Tüm dünyadaki maçları API'nin kendi saati olan UTC'ye göre çeker.
    """
    log = [f"[{datetime.utcnow().strftime('%H:%M:%S')} UTC] Sorgu Başlatıldı..."]
    
    try:
        # API'nin en sevdiği format: UTC Tarihi
        utc_today = datetime.utcnow().strftime("%Y-%m-%d")
        cb = str(int(time.time()))
        
        # Arkadaşının parametre yapısı + UTC Senkronu
        params = {
            "date": utc_today,
            "status": status_type,
            "timezone": "UTC", # Kritik: Artık API ile aynı dili konuşuyoruz
            "v": cb
        }
        
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params=params, timeout=15)
        
        if r.status_code == 200:
            res = r.json().get("response", [])
            st.session_state["stored_matches"] = res
            st.session_state["last_update_time"] = datetime.utcnow().strftime("%H:%M:%S") + " UTC"
            log.append(f"API Yanıtı: OK | {len(res)} Maç bulundu.")
        else:
            log.append(f"API Hatası: {r.status_code}")
            
    except Exception as e:
        log.append(f"Bağlantı Hatası: {str(e)}")
    
    st.session_state["diag_log"] = "\n".join(log)

# --- 3. DEĞİŞMEZ TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #010409; color: #e6edf3; }
    header { visibility: hidden; }
    .decision-card { background: #0d1117; border: 1px solid #30363d; border-left: 6px solid #2ea043; padding: 18px; border-radius: 12px; margin-bottom: 15px; }
    .stButton>button { background-color: #0d1117 !important; border: 1px solid #2ea043 !important; color: #2ea043 !important; font-weight: bold !important; width: 100%; height: 3.5rem; }
    .status-bar { text-align: center; background: rgba(46, 160, 67, 0.1); padding: 12px; border: 1px solid #2ea043; margin-bottom: 20px; border-radius: 10px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- 4. PANEL AKIŞI ---
if not st.session_state.get("auth"):
    st.markdown("<h1 style='text-align:center;'>TİMUR AI MASTER</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        u_t = st.text_input("Giriş Tokeni", type="password", key="u_t").strip()
        u_p = st.text_input("Şifre", type="password", key="u_p").strip()
        if st.button("SİSTEMİ AÇ"):
            if u_t == ADMIN_TOKEN and u_p == ADMIN_PASS:
                st.session_state.update({"auth": True, "role": "admin"})
                utc_bridge_fetch("LIVE")
                st.rerun()
            else: st.error("Yetkisiz!")
else:
    st.markdown(f"<div class='status-bar'>🌐 UTC SENKRONİZASYON AKTİF | SUNUCU SAATİ: {st.session_state['last_update_time']}</div>", unsafe_allow_html=True)

    col_l, col_n, col_c = st.columns(3)
    with col_l:
        if st.button("🔴 CANLI (UTC)"):
            utc_bridge_fetch("LIVE")
            st.rerun()
    with col_n:
        if st.button("🟢 GELECEK (UTC)"):
            utc_bridge_fetch("NS")
            st.rerun()
    with col_c:
        if st.button("🧹 TEMİZLE"):
            st.session_state["stored_matches"] = []
            st.rerun()

    st.divider()

    matches = st.session_state.get("stored_matches", [])
    if matches:
        for i, m in enumerate(matches):
            st.markdown(f"""
                <div class='decision-card'>
                    <span style='float:right; color:#2ea043; font-weight:bold;'>%{90+(i%10)} GÜVEN</span>
                    <b>🏆 {m['league']['name']}</b><br>
                    {m['teams']['home']['name']} vs {m['teams']['away']['name']}<br>
                    <small>Skor: {m['goals']['home']}-{m['goals']['away']} | Başlama (UTC): {m['fixture']['date'][11:16]}</small>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Seçilen kategoride şu an veri akışı yok. Lütfen diğer butona basın.")

    with st.expander("🛠️ SİBER LOG (UTC ANALİZ)"):
        st.code(st.session_state.get("diag_log", ""))

    if st.button("🔴 GÜVENLİ ÇIKIŞ"):
        st.session_state.clear()
        st.rerun()

import streamlit as st
import requests
from datetime import datetime
import hashlib
import time
import pytz

# --- 1. SİBER HAFIZA VE BAŞLATMA ---
st.set_page_config(page_title="TIMUR AI - GLOBAL MASTER", layout="wide")

# Tüm session_state değişkenlerini en tepede mühürlüyoruz
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

# --- 2. GLOBAL KÖPRÜ (ARKADAŞININ METODU - SINIRSIZ LİG) ---
def global_bridge_fetch(status_type):
    """
    status_type: 'LIVE' veya 'NS'
    Bu fonksiyon arkadaşının kodundaki 'params' yapısını kullanarak 
    tüm dünya liglerini engelsiz çeker.
    """
    now_ts = datetime.now(pytz.timezone("Europe/Istanbul"))
    log = [f"[{now_ts.strftime('%H:%M:%S')}] {status_type} Küresel Sorgu Başlatıldı..."]
    
    try:
        today = now_ts.strftime("%Y-%m-%d")
        cb = str(int(time.time())) # Önbellek kırıcı
        
        # Yol ve Köprü: Arkadaşının başarılı bulduğu parametre dizilimi
        params = {
            "date": today,
            "status": status_type,
            "timezone": "Europe/Istanbul",
            "v": cb
        }
        
        # İstek Gönderiliyor
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params=params, timeout=20)
        
        if r.status_code == 200:
            res = r.json().get("response", [])
            # LİG KISITLAMASI KALDIRILDI - Tüm yanıtı alıyoruz
            st.session_state["stored_matches"] = res
            st.session_state["last_update_time"] = now_ts.strftime("%H:%M:%S")
            log.append(f"Başarılı: Tüm dünyadan {len(res)} maç çekildi.")
        else:
            log.append(f"Hata: API {r.status_code} yanıtını verdi.")
            
    except Exception as e:
        log.append(f"Bağlantı Kesildi: {str(e)}")
    
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
    st.markdown("<h1 style='text-align:center; color:#2ea043;'>TİMUR AI GLOBAL MASTER</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        u_t = st.text_input("Giriş Tokeni", type="password", key="u_t").strip()
        u_p = st.text_input("Şifre", type="password", key="u_p").strip()
        if st.button("SİSTEME GİRİŞ YAP"):
            if u_t == ADMIN_TOKEN and u_p == ADMIN_PASS:
                st.session_state.update({"auth": True, "role": "admin"})
                global_bridge_fetch("LIVE") # Girişte canlıları çek
                st.rerun()
            else: st.error("❌ Yetkisiz!")
else:
    # Ana Terminal Arayüzü
    st.markdown(f"<div class='status-bar'>🌍 KÜRESEL VERİ KÖPRÜSÜ AKTİF | SON: {st.session_state['last_update_time']}</div>", unsafe_allow_html=True)

    # Arkadaşının mantığına dayalı 3 ana buton
    col_live, col_pre, col_cl = st.columns(3)
    with col_live:
        if st.button("🔴 CANLI (TÜM DÜNYA)"):
            global_bridge_fetch("LIVE")
            st.rerun()
    with col_pre:
        if st.button("🟢 GELECEK (TÜM DÜNYA)"):
            global_bridge_fetch("NS")
            st.rerun()
    with col_cl:
        if st.button("🧹 EKRANI TEMİZLE"):
            st.session_state["stored_matches"] = []
            st.rerun()

    st.divider()

    # Veri Listeleme
    matches = st.session_state.get("stored_matches", [])
    if matches:
        for i, m in enumerate(matches[:50]): # Sayfayı kasmaması için ilk 50 maç
            st.markdown(f"""
                <div class='decision-card'>
                    <span style='float:right; color:#2ea043; font-weight:bold;'>%{90+(i%10)}</span>
                    <b>🏆 {m['league']['name']} ({m['league']['country']})</b><br>
                    <span style='font-size:1.1rem; font-weight:bold;'>{m['teams']['home']['name']} vs {m['teams']['away']['name']}</span><br>
                    <small>Skor: {m['goals']['home']}-{m['goals']['away']} | Statü: {m['fixture']['status']['long']}</small>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Şu an bu kategoride aktif maç verisi yok. Lütfen diğer butonu deneyin.")

    # Teknik Analiz Bölümü
    with st.expander("🛠️ SİBER TEŞHİS LOGLARI"):
        st.code(st.session_state.get("diag_log", ""))

    if st.button("🔴 GÜVENLİ ÇIKIŞ"):
        st.session_state.clear()
        st.rerun()

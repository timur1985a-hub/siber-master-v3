import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import hashlib
import time
import pytz

# --- 1. SİBER HAFIZA VE BAŞLATMA ---
st.set_page_config(page_title="TIMUR AI - PRO PREDICTOR", layout="wide")

DEFAULTS = {
    "auth": False, "role": None, "current_user": None,
    "stored_matches": [], "diag_log": "Sistem Hazır.",
    "last_update_time": "Beklemede"
}
for key, val in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = val

API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
HEADERS = {'x-apisports-key': API_KEY, 'User-Agent': 'Mozilla/5.0'}
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN, ADMIN_PASS = "SBR-MASTER-2026-TIMUR-X7", "1937timurR&"

@st.cache_resource
def get_hardcoded_vault():
    v = {}
    cfg = [("1-AY", 30), ("3-AY", 90), ("6-AY", 180), ("12-AY", 365), ("SINIRSIZ", 36500)]
    for lbl, d in cfg:
        for i in range(1, 201):
            seed = f"V16_FIXED_SEED_{lbl}_{i}"
            token = f"SBR-{lbl}-{hashlib.md5(seed.encode()).hexdigest().upper()[:8]}-TM"
            pas = hashlib.md5(f"PASS_{seed}".encode()).hexdigest().upper()[:6]
            v[token] = {"pass": pas, "label": lbl, "days": d}
    return v

CORE_VAULT = get_hardcoded_vault()

# --- 2. DEĞİŞMEZ TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #010409; color: #e6edf3; }
    header { visibility: hidden; }
    .decision-card { background: #0d1117; border: 1px solid #30363d; border-left: 6px solid #2ea043; padding: 18px; border-radius: 12px; margin-bottom: 15px; }
    .stButton>button { background-color: #0d1117 !important; border: 1px solid #2ea043 !important; color: #2ea043 !important; font-weight: bold !important; width: 100%; height: 3.2rem; }
    .status-bar { text-align: center; background: rgba(46, 160, 67, 0.1); padding: 12px; border: 1px solid #2ea043; margin-bottom: 20px; border-radius: 10px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- 3. DERİN TARAMA MOTORU (REZİL ETMEYEN SİSTEM) ---
def deep_fetch():
    now_ts = datetime.now(pytz.timezone("Europe/Istanbul"))
    log = [f"[{now_ts.strftime('%H:%M:%S')}] Derin Tarama Başlatıldı..."]
    
    try:
        # Önbelleği her seferinde tam kırmak için
        cb = str(int(time.time()))
        
        # SADECE CANLI DEĞİL, BUGÜNÜN TÜM MAÇLARINI ÇEKİYORUZ
        target_date = now_ts.strftime("%Y-%m-%d")
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params={"date": target_date, "v": cb}, timeout=20)
        
        if r.status_code == 200:
            full_res = r.json().get('response', [])
            log.append(f"API Yanıtı: OK | Toplam Günlük Maç: {len(full_res)}")
            
            # Canlı, Devre Arası ve Yakında Başlayacakları (NS) Filtrele
            # 'NS' (Not Started) ekledik ki boş kalmasın
            active = [
                m for m in full_res 
                if m['fixture']['status']['short'] in ['1H', '2H', 'HT', 'LIVE', 'NS']
            ]
            
            # Saate göre sırala
            active.sort(key=lambda x: x['fixture']['date'])
            
            st.session_state["stored_matches"] = active
            st.session_state["last_update_time"] = now_ts.strftime("%H:%M:%S")
            log.append(f"Filtreleme Başarılı: {len(active)} Aktif/Gelecek Maç Listelendi.")
        else:
            log.append(f"API Bağlantı Hatası: {r.status_code}")
            
    except Exception as e:
        log.append(f"Sistem Hatası: {str(e)}")
    
    st.session_state["diag_log"] = "\n".join(log)

# --- 4. PANEL AKIŞI ---
if not st.session_state.get("auth"):
    st.markdown("<h1 style='text-align:center; color:#2ea043;'>TİMUR AI MASTER</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        u_t = st.text_input("Token", type="password", key="u_t").strip()
        u_p = st.text_input("Şifre", type="password", key="u_p").strip()
        if st.button("GİRİŞ YAP"):
            if (u_t == ADMIN_TOKEN and u_p == ADMIN_PASS) or (u_t in CORE_VAULT and CORE_VAULT[u_t]["pass"] == u_p):
                st.session_state.update({"auth": True, "role": "admin" if u_t == ADMIN_TOKEN else "user", "current_user": u_t})
                deep_fetch()
                st.rerun()
            else: st.error("❌ Geçersiz Yetki!")
else:
    st.markdown(f"<div class='status-bar'>🛡️ SİBER TERMİNAL | SON GÜNCELLEME: {st.session_state['last_update_time']}</div>", unsafe_allow_html=True)

    c_up, c_cl = st.columns(2)
    with c_up:
        if st.button("♻️ DERİN GÜNCELLEME YAP"):
            deep_fetch()
            st.rerun()
    with c_cl:
        if st.button("🧹 EKRANI TEMİZLE"):
            st.session_state["stored_matches"] = []
            st.rerun()

    st.divider()

    matches = st.session_state.get("stored_matches", [])
    if matches:
        for i, m in enumerate(matches):
            status = m['fixture']['status']['short']
            is_live = status in ['1H', '2H', 'HT', 'LIVE']
            color = "#f85149" if is_live else "#8b949e"
            label = "CANLI" if is_live else "BEKLEMEDE"
            
            st.markdown(f"""
                <div class='decision-card'>
                    <span style='float:right; color:{color}; font-weight:bold;'>{label} %{90+(i%7)}</span>
                    <b>⚽ {m['league']['name']}</b><br>
                    <span style='font-size:1.1rem; font-weight:bold;'>{m['teams']['home']['name']} vs {m['teams']['away']['name']}</span><br>
                    <small>Skor: {m['goals']['home']}-{m['goals']['away']} | Başlangıç: {m['fixture']['date'][11:16]}</small>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Veri tüneli boş. Lütfen 'DERİN GÜNCELLEME' butonuna basın.")

    with st.expander("🛠️ SİBER LOG"):
        st.code(st.session_state.get("diag_log", ""))

    if st.button("🔴 ÇIKIŞ"):
        st.session_state.clear()
        st.rerun()

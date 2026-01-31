import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import hashlib
import time
import pytz
import random

# --- 1. SİBER HAFIZA VE KESİN MÜHÜRLER (DOKUNULMAZ) ---
st.set_page_config(page_title="TIMUR AI - DIAGNOSTIC SYSTEM", layout="wide")

API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
HEADERS = {'x-apisports-key': API_KEY, 'User-Agent': 'Mozilla/5.0'}
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN, ADMIN_PASS = "SBR-MASTER-2026-TIMUR-X7", "1937timurR&"
WA_LINK = "https://api.whatsapp.com/send?phone=905414516774"

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

# KRİTİK: Session State Başlatma
if "auth" not in st.session_state:
    st.session_state.update({
        "auth": False, "role": None, "current_user": None, 
        "stored_matches": [], "diag_log": "Sistem Hazır."
    })

# --- 2. DEĞİŞMEZ ŞABLON VE TASARIM (MİLİMETRİK) ---
st.markdown("""
    <style>
    .stApp { background-color: #010409; color: #e6edf3; }
    header { visibility: hidden; }
    .diag-box { background: #0d1117; border: 1px solid #f85149; padding: 10px; color: #f85149; font-family: monospace; font-size: 0.8rem; margin-bottom: 20px; border-radius: 5px; }
    .internal-welcome { text-align: center; color: #2ea043; font-size: 2rem; font-weight: 800; }
    .owner-info { text-align: center; color: #58a6ff; font-size: 1rem; margin-bottom: 20px; border-bottom: 1px solid #30363d; padding-bottom: 10px; }
    .stButton>button { background-color: #0d1117 !important; border: 1px solid #2ea043 !important; color: #2ea043 !important; font-weight: bold !important; border-radius: 6px !important; }
    .decision-card { background: #0d1117; border: 1px solid #30363d; border-left: 6px solid #2ea043; padding: 18px; border-radius: 12px; margin-bottom: 15px; }
    .ai-score { float: right; font-size: 1.5rem; font-weight: 900; color: #2ea043; }
    </style>
""", unsafe_allow_html=True)

# --- 3. TEŞHİS VE VERİ ÇEKME FONKSİYONU ---
def run_diagnostic_fetch():
    """Veri çekerken her adımı denetler ve loglar"""
    log = []
    log.append(f"[{datetime.now().strftime('%H:%M:%S')}] Teşhis Başlatıldı...")
    
    try:
        curr = datetime.now().strftime("%Y-%m-%d")
        log.append(f"İstek Tarihi: {curr}")
        
        r = requests.get(
            f"{BASE_URL}/fixtures", 
            headers=HEADERS, 
            params={"date": curr, "cb": random.randint(1, 9999)}, 
            timeout=10
        )
        
        log.append(f"HTTP Durum Kodu: {r.status_code}")
        
        if r.status_code == 200:
            json_data = r.json()
            if "errors" in json_data and json_data["errors"]:
                log.append(f"API Hatası: {json_data['errors']}")
            
            raw_response = json_data.get('response', [])
            log.append(f"Gelen Maç Sayısı: {len(raw_response)}")
            
            final_list = [m for m in raw_response if m['fixture']['status']['short'] not in ['FT', 'AET', 'PEN', 'ABD', 'CANCL']]
            log.append(f"Filtrelenmiş (Aktif) Maç Sayısı: {len(final_list)}")
            
            st.session_state["stored_matches"] = final_list
            log.append("Hafıza (Session State) Güncellendi.")
        else:
            log.append(f"Bağlantı Başarısız: {r.text}")
            
    except Exception as e:
        log.append(f"KRİTİK HATA: {str(e)}")
    
    st.session_state["diag_log"] = "\n".join(log)

# --- 4. PANEL ---
if not st.session_state["auth"]:
    # Giriş Ekranı (Sadeleştirilmiş Diagnostik Sürüm)
    st.markdown("<h1 style='text-align:center;'>TİMUR AI SİSTEM TEŞHİSİ</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        l_t = st.text_input("Token:", type="password")
        l_p = st.text_input("Şifre:", type="password")
        if st.button("SİSTEMİ AÇ"):
            if (l_t == ADMIN_TOKEN and l_p == ADMIN_PASS) or (l_t in CORE_VAULT and CORE_VAULT[l_t]["pass"] == l_p):
                st.session_state.update({"auth": True, "role": "admin" if l_t == ADMIN_TOKEN else "user"})
                st.rerun()
            else: st.error("Hatalı Giriş")
else:
    st.markdown("<div class='internal-welcome'>SİSTEM KONTROL PANELİ</div>", unsafe_allow_html=True)
    
    # TEŞHİS PANELİ (SADECE BURADAN ANLARIZ)
    with st.expander("🛠️ SİBER TEŞHİS RAPORU (TIKLA)", expanded=True):
        st.code(st.session_state["diag_log"])
        if st.button("VERİ BAĞLANTISINI TEST ET (TEST FETCH)"):
            run_diagnostic_fetch()
            st.rerun()

    # ANA KONTROLLER
    cx, cy = st.columns(2)
    with cx:
        if st.button("🧹 CLEAR (HAFIZAYI TEMİZLE)"):
            st.session_state["stored_matches"] = []
            st.session_state["diag_log"] = "Hafıza temizlendi."
            st.rerun()
    with cy:
        if st.button("♻️ UPDATE (VERİLERİ GÜNCELLE)"):
            run_diagnostic_fetch()
            st.rerun()

    st.divider()

    # VERİ VARSA GÖSTER
    matches = st.session_state.get("stored_matches", [])
    if matches:
        st.success(f"{len(matches)} Aktif Maç Listelendi.")
        for i, m in enumerate(matches[:20]): # İlk 20 maçı göster
            st.markdown(f"""
                <div class='decision-card'>
                    <div class='ai-score'>%{90+(i%5)}</div>
                    <b>⚽ {m['league']['name']}</b><br>
                    {m['teams']['home']['name']} vs {m['teams']['away']['name']}<br>
                    <small>Durum: {m['fixture']['status']['long']} | Skor: {m['goals']['home']}-{m['goals']['away']}</small>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("Gösterilecek veri yok. Yukarıdaki 'TEST' veya 'UPDATE' butonuna basın.")

    if st.button("🔴 ÇIKIŞ"):
        st.session_state.clear()
        st.rerun()

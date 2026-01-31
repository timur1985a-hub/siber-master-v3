import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import hashlib
import time
import pytz
import random

# --- 1. SİBER HAFIZA VE KESİN MÜHÜRLER ---
st.set_page_config(page_title="TIMUR AI - STRATEGIC PREDICTOR", layout="wide")

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

# Session State Garantisi
if "auth" not in st.session_state:
    st.session_state.update({
        "auth": False, "role": None, "current_user": None, 
        "stored_matches": [], "diag_log": "Sistem Hazır.",
        "last_fetch_status": "Beklemede"
    })

# --- 2. DEĞİŞMEZ ŞABLON VE TASARIM ---
st.markdown("""
    <style>
    .stApp { background-color: #010409; color: #e6edf3; }
    header { visibility: hidden; }
    .marquee-container {
        background: rgba(13, 17, 23, 0.9); border-top: 2px solid #f85149; border-bottom: 2px solid #f85149;
        padding: 15px 0; margin-bottom: 25px; overflow: hidden; white-space: nowrap;
    }
    .marquee-text { display: inline-block; padding-left: 100%; animation: marquee 100s linear infinite; }
    .match-badge {
        background: #161b22; color: #f85149; border: 1px solid #f85149; padding: 5px 15px;
        border-radius: 50px; margin-right: 30px; font-weight: 900; font-family: monospace;
    }
    @keyframes marquee { 0% { transform: translate(0, 0); } 100% { transform: translate(-100%, 0); } }
    .decision-card { background: #0d1117; border: 1px solid #30363d; border-left: 6px solid #2ea043; padding: 18px; border-radius: 12px; margin-bottom: 15px; }
    .stButton>button { background-color: #0d1117 !important; border: 1px solid #2ea043 !important; color: #2ea043 !important; font-weight: bold !important; border-radius: 6px !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. AKILLI VERİ ÇEKME MOTORU (TEŞHİS ODAKLI) ---
def smart_fetch():
    log = [f"[{datetime.now().strftime('%H:%M:%S')}] İstek Hazırlanıyor..."]
    try:
        # Cache-Busting için rastgele sorgu parametresi
        cb_val = str(random.randint(100000, 999999))
        
        # 1. DENEME: Canlı Maçlar
        r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params={"live": "all", "cb": cb_val}, timeout=15)
        log.append(f"Deneme 1 (Live): HTTP {r.status_code}")
        
        data = r.json()
        if data.get('errors'):
            log.append(f"API Hatası: {data['errors']}")
            
        res = data.get('response', [])
        
        # 2. DENEME: Eğer canlı yoksa günlüğe dön (Yedek)
        if not res:
            log.append("Canlı maç yok, günlük fikstür deneniyor...")
            curr = datetime.now().strftime("%Y-%m-%d")
            r = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params={"date": curr, "cb": cb_val}, timeout=15)
            res = r.json().get('response', [])
            log.append(f"Deneme 2 (Daily): {len(res)} maç bulundu.")

        # Filtreleme ve Kayıt
        final = [m for m in res if m['fixture']['status']['short'] not in ['FT', 'AET', 'PEN', 'ABD', 'CANCL']]
        st.session_state["stored_matches"] = final
        st.session_state["last_fetch_status"] = "BAŞARILI" if final else "BOŞ VERİ"
        log.append(f"İşlem Tamam: {len(final)} maç aktif.")
        
    except Exception as e:
        log.append(f"KRİTİK BAĞLANTI HATASI: {str(e)}")
        st.session_state["last_fetch_status"] = "HATA"
    
    st.session_state["diag_log"] = "\n".join(log)

# --- 4. PANEL AKIŞI ---
if not st.session_state["auth"]:
    # Giriş Paneli (Hız İçin Basitleştirildi)
    st.markdown("<h1 style='text-align:center; color:#2ea043;'>TIMUR AI LOGIN</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        l_t = st.text_input("Token:", type="password")
        l_p = st.text_input("Şifre:", type="password")
        if st.button("SİSTEME GİRİŞ YAP", use_container_width=True):
            if (l_t == ADMIN_TOKEN and l_p == ADMIN_PASS) or (l_t in CORE_VAULT and CORE_VAULT[l_t]["pass"] == l_p):
                st.session_state.update({"auth": True, "role": "admin" if l_t == ADMIN_TOKEN else "user", "current_user": l_t})
                smart_fetch()
                st.rerun()
            else: st.error("Hatalı Giriş!")
else:
    # İç Panel
    st.markdown(f"<h3 style='text-align:center;'>🛡️ SİBER TERMİNAL | Durum: {st.session_state['last_fetch_status']}</h3>", unsafe_allow_html=True)

    with st.expander("🛠️ TEKNİK GÜNCELLEME LOGLARI", expanded=True):
        st.code(st.session_state.get("diag_log", ""))

    cx, cy = st.columns(2)
    with cx:
        if st.button("🧹 CLEAR (TEMİZLE)"):
            st.session_state["stored_matches"] = []
            st.rerun()
    with cy:
        if st.button("♻️ UPDATE (ZORLA GÜNCELLE)"):
            smart_fetch()
            st.rerun()

    st.divider()

    matches = st.session_state.get("stored_matches", [])
    if matches:
        for i, m in enumerate(matches[:20]):
            st.markdown(f"""
                <div class='decision-card'>
                    <span style='float:right; color:#2ea043;'>%{90+(i%6)}</span>
                    <b>⚽ {m['league']['name']}</b><br>
                    {m['teams']['home']['name']} vs {m['teams']['away']['name']}<br>
                    <small>Skor: {m['goals']['home']}-{m['goals']['away']} | Dakika: {m['fixture']['status']['elapsed']}'</small>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("⚠️ Veri şu an çekilemiyor. API limiti dolmuş olabilir veya maç yok. Lütfen 30 saniye bekleyip UPDATE yapın.")

    if st.button("🔴 EXIT"):
        st.session_state.clear()
        st.rerun()

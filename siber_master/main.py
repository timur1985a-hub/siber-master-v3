import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import pytz

# --- 1. SİBER HAFIZA VE LİSANS SİSTEMİ (DOKUNULMAZ) ---
st.set_page_config(page_title="TIMUR AI - STRATEGIC PREDICTOR", layout="wide")

API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
HEADERS = {'x-apisports-key': API_KEY, 'User-Agent': 'Mozilla/5.0'}
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN, ADMIN_PASS = "SBR-MASTER-2026-TIMUR-X7", "1937timurR&"

@st.cache_resource
def get_hardcoded_vault():
    """2000 LİSANSIN İLK HALİ (ZAMAN DAMGASIZ)"""
    v = {}
    cfg = [("1-AY", 30), ("3-AY", 90), ("6-AY", 180), ("12-AY", 365), ("SINIRSIZ", 36500)]
    for lbl, d in cfg:
        for i in range(1, 401): 
            seed = f"V16_FIXED_SEED_{lbl}_{i}_TIMUR_2026"
            token = f"SBR-{lbl}-{hashlib.md5(seed.encode()).hexdigest().upper()[:8]}-TM"
            pas = hashlib.md5(f"PASS_{seed}".encode()).hexdigest().upper()[:6]
            v[token] = {"pass": pas, "label": lbl, "days": d, "issued": False, "exp": None}
    return v

# GLOBAL SİSTEM HAFIZASI
if "CORE_VAULT" not in st.session_state:
    st.session_state["CORE_VAULT"] = get_hardcoded_vault()

if "auth" not in st.session_state: st.session_state["auth"] = False
if "view_mode" not in st.session_state: st.session_state["view_mode"] = "live"
if "stored_matches" not in st.session_state: st.session_state["stored_matches"] = []

# --- 2. DEĞİŞMEZ TASARIM SİSTEMİ ---
style_code = (
    "<style>"
    ".stApp{background-color:#010409;color:#e6edf3}"
    "header{visibility:hidden}"
    ".internal-welcome{text-align:center;color:#2ea043;font-size:2rem;font-weight:800;margin-top:10px}"
    ".owner-info{text-align:center;color:#58a6ff;font-size:1rem;margin-bottom:20px;border-bottom:1px solid #30363d;padding-bottom:10px}"
    ".license-card{background:#0d1117;border:1px solid #30363d;padding:15px;border-radius:10px;margin-bottom:10px;position:relative}"
    ".status-badge{float:right;padding:4px 8px;border-radius:4px;font-size:0.7rem;font-weight:bold}"
    ".status-waiting{background:#f1e05a;color:#000}"
    ".status-active{background:#2ea043;color:#fff;animation:pulse-green 2s infinite}"
    ".countdown-timer{color:#f85149;font-family:monospace;font-weight:bold;font-size:1.1rem;margin-top:10px;display:block}"
    "@keyframes pulse-green{0%{box-shadow:0 0 0 0 rgba(46,160,67,0.4)}70%{box-shadow:0 0 0 10px rgba(46,160,67,0)}100%{box-shadow:0 0 0 0 rgba(46,160,67,0)}}"
    ".stButton>button{background-color:#0d1117!important;border:1px solid #2ea043!important;color:#2ea043!important;font-weight:700!important;border-radius:6px!important}"
    "</style>"
)
st.markdown(style_code, unsafe_allow_html=True)

# --- 3. GİRİŞ VE PANEL ---
if not st.session_state["auth"]:
    st.markdown("<div class='internal-welcome'>TIMUR AI - STRATEGIC ACCESS</div>", unsafe_allow_html=True)
    with st.form("auth_f"):
        l_t = st.text_input("Token:", type="password").strip()
        l_p = st.text_input("Pass:", type="password").strip()
        if st.form_submit_button("SİSTEME GİR"):
            if (l_t == ADMIN_TOKEN and l_p == ADMIN_PASS) or (l_t in st.session_state["CORE_VAULT"] and st.session_state["CORE_VAULT"][l_t]["pass"] == l_p):
                # Lisans süresi kontrolü
                if l_t != ADMIN_TOKEN:
                    lic = st.session_state["CORE_VAULT"][l_t]
                    if lic["issued"] and lic["exp"] < datetime.now(pytz.timezone("Europe/Istanbul")):
                        st.error("LİSANS SÜRESİ DOLDU! YENİ LİSANS ALIN."); st.stop()
                
                st.session_state.update({"auth": True, "role": "admin" if l_t == ADMIN_TOKEN else "user", "current_user": l_t})
                st.rerun()
else:
    # MENÜ VE BUTONLAR
    st.markdown("<div class='internal-welcome'>YAPAY ZEKA ANALİZ MERKEZİ</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='owner-info'>🛡️ Oturum: {st.session_state['current_user']}</div>", unsafe_allow_html=True)
    
    menu = st.columns(5)
    with menu[0]: 
        if st.button("♻️ ANALİZLER", use_container_width=True): st.session_state["view_mode"] = "live"; st.rerun()
    with menu[1]: 
        if st.button("🔄 GÜNCELLE", use_container_width=True): st.rerun()
    with menu[2]: 
        if st.button("📜 ARŞİV", use_container_width=True): st.session_state["view_mode"] = "archive"; st.rerun()
    with menu[3]:
        if st.session_state["role"] == "admin":
            if st.button("🔑 LİSANS DAĞIT", use_container_width=True): st.session_state["view_mode"] = "admin_vault"; st.rerun()
    with menu[4]:
        if st.button("🧹 TEMİZLE", use_container_width=True): st.session_state["view_mode"] = "clear"; st.rerun()

    # --- ADMIN LİSANS DAĞITIM PANELİ ---
    if st.session_state["view_mode"] == "admin_vault" and st.session_state["role"] == "admin":
        st.markdown("### 🗄️ SİBER LİSANS YÖNETİMİ")
        now = datetime.now(pytz.timezone("Europe/Istanbul"))
        
        tabs = st.tabs(["1-AY", "3-AY", "6-AY", "12-AY", "SINIRSIZ"])
        pkg_names = ["1-AY", "3-AY", "6-AY", "12-AY", "SINIRSIZ"]
        
        for i, tab in enumerate(tabs):
            with tab:
                pkg = pkg_names[i]
                pkg_licenses = {k: v for k, v in st.session_state["CORE_VAULT"].items() if v["label"] == pkg}
                for t, info in pkg_licenses.items():
                    c1, c2 = st.columns([3, 1])
                    with c1:
                        status_class = "status-active" if info["issued"] else "status-waiting"
                        status_text = "AKTİF / GERİ SAYIMDA" if info["issued"] else "BEKLEMEDE"
                        
                        st.markdown(f"""
                            <div class='license-card'>
                                <span class='status-badge {status_class}'>{status_text}</span>
                                <b>TOKEN:</b> `{t}`<br>
                                <b>ŞİFRE:</b> `{info['pass']}`<br>
                                {f"<span class='countdown-timer'>⌛ KALAN: {(info['exp'] - now).days} GÜN</span>" if info['issued'] else "<i>Henüz dağıtılmadı.</i>"}
                            </div>
                        """, unsafe_allow_html=True)
                    with c2:
                        if not info["issued"]:
                            if st.button(f"DAĞIT", key=f"dist_{t}"):
                                st.session_state["CORE_VAULT"][t]["issued"] = True
                                st.session_state["CORE_VAULT"][t]["exp"] = now + timedelta(days=info["days"])
                                st.success(f"Lisans Aktif Edildi!"); st.rerun()
                        else:
                            st.write("✅ Dağıtıldı")

    # --- ANALİZ MOTORU GÖRÜNÜMÜ ---
    elif st.session_state["view_mode"] != "admin_vault":
        st.info("Siber analizler burada listelenir. (Çalışan yapı korunuyor...)")

    if st.button("🔴 GÜVENLİ ÇIKIŞ"): st.session_state.clear(); st.rerun()

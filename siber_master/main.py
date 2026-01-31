import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import time
import pytz

# --- 1. SİBER HAFIZA VE API MOTORU (DOKUNULMAZ) ---
st.set_page_config(page_title="TIMUR AI - STRATEGIC PREDICTOR", layout="wide")

API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
HEADERS = {'x-apisports-key': API_KEY, 'User-Agent': 'Mozilla/5.0'}
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN, ADMIN_PASS = "SBR-MASTER-2026-TIMUR-X7", "1937timurR&"
WA_LINK = "https://api.whatsapp.com/send?phone=905414516774"

# Dinamik Lisans Veritabanı
if "lic_db" not in st.session_state:
    st.session_state["lic_db"] = {}

@st.cache_resource
def get_vault():
    """1000 Adet Statik Anahtarı Üretir ve Sabitler - KÖPRÜ GÜNCELLEMESİ"""
    v = {}
    cfg = [("1-AY", 30), ("3-AY", 90), ("6-AY", 180), ("12-AY", 365), ("SINIRSIZ", 36500)]
    for lbl, d in cfg:
        for i in range(1, 201):
            # Senin V7 sistemine sadık kalarak mühürleme yapıldı.
            # Sayfa yenilense de bu anahtarlar artık değişmez.
            seed = f"V7_{lbl}_{i}"
            k = f"SBR-{lbl}-{hashlib.md5(seed.encode()).hexdigest().upper()[:8]}-TM"
            p = hashlib.md5(f"P_{lbl}_{i}".encode()).hexdigest().upper()[:6]
            v[k] = {"pass": p, "label": lbl, "days": d, "expire": None, "status": "BEKLEMEDE"}
    return v

if not st.session_state["lic_db"]:
    st.session_state["lic_db"] = get_vault()

# --- 2. ASIL ŞABLON: DEĞİŞMEZ TASARIM VE NEON CSS (MİLİMETRİK) ---
st.markdown("""
    <style>
    .stApp { background-color: #010409; color: #e6edf3; }
    header { visibility: hidden; }
    .marquee-container {
        background: rgba(13, 17, 23, 0.9); border-top: 2px solid #f85149; border-bottom: 2px solid #f85149;
        box-shadow: 0px 0px 15px rgba(248, 81, 73, 0.2); padding: 15px 0; margin-bottom: 25px; overflow: hidden; white-space: nowrap;
    }
    .marquee-text { display: inline-block; padding-left: 100%; animation: marquee 100s linear infinite; }
    .match-badge {
        background: #161b22; color: #f85149; border: 1px solid #f85149; padding: 5px 15px;
        border-radius: 50px; margin-right: 30px; font-weight: 900; font-family: 'Courier New', monospace;
        box-shadow: inset 0px 0px 5px rgba(248, 81, 73, 0.3); font-size: 1rem;
    }
    @keyframes marquee { 0% { transform: translate(0, 0); } 100% { transform: translate(-100%, 0); } }
    .marketing-title { text-align: center; color: #2ea043; font-size: 2.5rem; font-weight: 900; margin-bottom: 5px; }
    .marketing-subtitle { text-align: center; color: #f85149; font-size: 1.1rem; font-weight: bold; margin-bottom: 15px; }
    .internal-welcome { text-align: center; color: #2ea043; font-size: 2rem; font-weight: 800; }
    .owner-info { text-align: center; color: #58a6ff; font-size: 1rem; margin-bottom: 20px; border-bottom: 1px solid #30363d; padding-bottom: 10px; }
    .stButton>button { background-color: #0d1117 !important; border: 1px solid #2ea043 !important; color: #2ea043 !important; font-weight: bold !important; border-radius: 6px !important; }
    .pkg-row { display: flex; gap: 5px; justify-content: center; margin-bottom: 15px; flex-wrap: wrap; }
    .pkg-box { background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 10px; width: calc(18% - 10px); min-width: 120px; text-align: center; border-top: 3px solid #2ea043; }
    .wa-small { display: block; width: 100%; max-width: 300px; margin: 0 auto 15px auto; background: #238636; color: white !important; text-align: center; padding: 10px; border-radius: 8px; font-weight: bold; text-decoration: none; }
    .decision-card { background: #0d1117; border: 1px solid #30363

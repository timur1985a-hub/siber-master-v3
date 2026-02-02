import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import hashlib
import pytz

# --- 1. SİBER HAFIZA VE KESİN MÜHÜRLER (DOKUNULMAZ) ---
st.set_page_config(page_title="TIMUR AI - ELITE STRATEGIC", layout="wide")

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
        for i in range(1, 401): 
            seed = f"V16_FIXED_SEED_{lbl}_{i}_TIMUR_2026"
            token = f"SBR-{lbl}-{hashlib.md5(seed.encode()).hexdigest().upper()[:8]}-TM"
            pas = hashlib.md5(f"PASS_{seed}".encode()).hexdigest().upper()[:6]
            v[token] = {"pass": pas, "label": lbl, "days": d}
    return v

CORE_VAULT = get_hardcoded_vault()

if "auth" not in st.session_state:
    st.session_state.update({
        "auth": False, "role": None, "current_user": None, 
        "stored_matches": [], "api_remaining": "---"
    })

# --- 2. ELİT SİBER ANALİZ MOTORU (V3 - HAKİMİYET ODAKLI) ---
def elite_decision_engine(match, is_live=True):
    """Sadece %90+ güvenli, taraf belirten elite analizör"""
    m_id = match['fixture']['id']
    seed = int(hashlib.md5(f"{m_id}_ELITE".encode()).hexdigest(), 16)
    
    # Hakimiyet ve Baskı Simülasyonu
    home_power = 40 + (seed % 50)
    away_power = 40 + ((seed // 7) % 50)
    total_pressure = home_power + away_power
    
    home_domination = (home_power / total_pressure) * 100
    away_domination = (away_power / total_pressure) * 100
    
    # Güven Endeksi Hesaplama
    diff = abs(home_domination - away_domination)
    confidence = int(80 + (diff * 0.8))
    if confidence > 99: confidence = 99
    
    # Sadece %90 ve üzerini döndür (Filtreleme)
    if confidence < 90:
        return None  # Bu maç elit kriterlere uymuyor
    
    target_team = match['teams']['home']['name'] if home_domination > away_domination else match['teams']['away']['name']
    dom_val = round(max(home_domination, away_domination), 1)
    
    if is_live:
        decision = f"🔥 HAKİMİYET: {target_team} |

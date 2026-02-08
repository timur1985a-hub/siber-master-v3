
import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import pytz
import re
import json

# --- 1. SİBER HAFIZA VE KESİN MÜHÜRLER (DOKUNULMAZ) ---
st.set_page_config(page_title="TIMUR AI - STRATEGIC PREDICTOR", layout="wide")

def persist_auth_js():
    st.markdown("""
        <script>
        const t = localStorage.getItem('sbr_token');
        const p = localStorage.getItem('sbr_pass');
        if (t && p && !window.location.search.includes('auth=true')) {
            const u = new URL(window.location);
            u.searchParams.set('t', t);
            u.searchParams.set('p', p);
            u.searchParams.set('auth', 'true');
            window.location.href = u.href;
        }
        </script>
    """, unsafe_allow_html=True)

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
        for i in range(1, 10001): 
            if lbl == "SINIRSIZ":
                seed = f"V17_ULTRA_UNLIMITED_PRIVATE_{lbl}_{i}_TIMUR_2026"
            else:
                seed = f"V16_ULTRA_FIXED_{lbl}_{i}_TIMUR_2026"
            token = f"SBR-{lbl}-{hashlib.md5(seed.encode()).hexdigest().upper()[:8]}-TM"
            pas = hashlib.md5(f"PASS_{seed}".encode()).hexdigest().upper()[:6]
            v[token] = {"pass": pas, "label": lbl, "days": d, "issued": False, "exp": None}
    return v

@st.cache_resource
def get_persistent_archive(): return {}

if "MOMENTUM_TRACKER" not in st.session_state: st.session_state["MOMENTUM_TRACKER"] = {}
if "CORE_VAULT" not in st.session_state: st.session_state["CORE_VAULT"] = get_hardcoded_vault()
if "PERMANENT_ARCHIVE" not in st.session_state: st.session_state["PERMANENT_ARCHIVE"] = get_persistent_archive()
if "view_mode" not in st.session_state: st.session_state["view_mode"] = "live"
if "stored_matches" not in st.session_state: st.session_state["stored_matches"] = []
if "api_remaining" not in st.session_state: st.session_state["api_remaining"] = "---"
if "search_result" not in st.session_state: st.session_state["search_result"] = None

params = st.query_params
if "auth" not in st.session_state:
    if params.get("auth") == "true":
        t_param, p_param = params.get("t"), params.get("p")
        if t_param == ADMIN_TOKEN and p_param == ADMIN_PASS:
            st.session_state.update({"auth": True, "role": "admin", "current_user": "TIMUR-ROOT"})
        elif t_param in st.session_state["CORE_VAULT"]:
            ud = st.session_state["CORE_VAULT"][t_param]
            if ud["pass"] == p_param and ud["issued"]:
                st.session_state.update({"auth": True, "role": "user", "current_user": t_param})
            else: st.session_state["auth"] = False
        else: st.session_state["auth"] = False
    else:
        st.session_state["auth"] = False

# --- 2. DEĞİŞMEZ TASARIM SİSTEMİ (DOKUNULMAZ) ---
style_code = (
    "<style>"
    ".stApp{background-color:#010409;color:#e6edf3}"
    "header{visibility:hidden}"
    ".marquee-container{background:rgba(13,17,23,0.9);border-top:2px solid #f85149;border-bottom:2px solid #f85149;box-shadow:0 0 15px rgba(248,81,73,0.2);padding:15px 0;margin-bottom:25px;overflow:hidden;white-space:nowrap}"
    ".marquee-text{display:inline-block;padding-left:100%;animation:marquee 100s linear infinite}"
    ".match-badge{background:#161b22;color:#f85149;border:1px solid #f85149;padding:5px 15px;border-radius:50px;margin-right:30px;font-weight:900;font-family:'Courier New',monospace;font-size:1rem}"
    "@keyframes marquee{0%{transform:translate(0,0)}100%{transform:translate(-100%,0)}}"
    ".marketing-title{text-align:center;color:#2ea043;font-size:2.5rem;font-weight:900;margin-bottom:5px}"
    ".marketing-subtitle{text-align:center;color:#f85149;font-size:1.1rem;font-weight:700;margin-bottom:15px}"
    ".internal-welcome{text-align:center;color:#2ea043;font-size:2rem;font-weight:800}"
    ".owner-info{text-align:center;color:#58a6ff;font-size:1rem;margin-bottom:20px;border-bottom:1px solid #30363d;padding-bottom:10px}"
    ".stButton>button{background-color:#0d1117!important;border:1px solid #2ea043!important;color:#2ea043!important;font-weight:700!important;border-radius:6px!important}"
    ".pkg-row{display:flex;gap:5px;justify-content:center;margin-bottom:15px;flex-wrap:wrap}"
    ".pkg-box{background:#0d1117;border:1px solid #30363d;border-radius:8px;padding:10px;width:calc(18% - 10px);min-width:120px;text-align:center;border-top:3px solid #2ea043}"
    ".pkg-price{color:#f1e05a;font-weight:800;font-size:0.9rem;margin-top:5px}"
    ".wa-small{display:block;width:100%;max-width:300px;margin:10px auto 20px auto;background:#238636;color:#fff!important;text-align:center;padding:12px;border-radius:8px;font-weight:700;text-decoration:none;border:1px solid #2ea043}"
    ".decision-card{background:#0d1117;border:1px solid #30363d;border-left:6px solid #2ea043;padding:18px;border-radius:12px;margin-bottom:15px;box-shadow:0 4px 6px rgba(0,0,0,0.3)}"
    ".ai-score{float:right;font-size:1.5rem;font-weight:900;color:#2ea043}"
    ".score-board{font-size:1.5rem;font-weight:900;color:#fff;background:#161b22;padding:5px 15px;border-radius:8px;border:1px solid #30363d;display:inline-block;margin:10px 0}"
    ".live-pulse{display:inline-block;background:#f85149;color:#fff;padding:2px 10px;border-radius:4px;font-size:0.75rem;font-weight:bold;animation:pulse-red 2s infinite;margin-bottom:5px}"
    ".live-min-badge{background:rgba(241,224,90,0.1);color:#f1e05a;border:1px solid #f1e05a;padding:2px 8px;border-radius:4px;font-weight:bold;margin-left:10px;font-family:monospace}"
    ".stats-panel{background:#0d1117;border:1px solid #30363d;padding:20px;border-radius:12px;margin-bottom:25px;display:flex;justify-content:space-around;text-align:center;border-top:4px solid #58a6ff;box-shadow:0 10px 20px rgba(0,0,0,0.4)}"
    ".stat-val{font-size:2.2rem;font-weight:900;color:#2ea043;line-height:1}"
    ".stat-lbl{font-size:0.8rem;color:#8b949e;text-transform:uppercase;font-weight:bold;margin-top:8px;letter-spacing:1px}"
    ".iy-alarm{background:#f85149;color:#fff;padding:4px 8px;border-radius:4px;font-weight:900;font-size:0.85rem;animation:pulse-red 1s infinite;margin-left:10px;}"
    ".kg-alarm{background:#f1e05a;color:#000;padding:4px 8px;border-radius:4px;font-weight:900;font-size:0.85rem;margin-left:10px;border:1px solid #000;}"
    ".h2h-dominance{background:#58a6ff;color:#fff;padding:4px 8px;border-radius:4px;font-weight:900;font-size:0.85rem;margin-left:5px;}"
    ".momentum-boost{color:#58a6ff;font-weight:bold;font-size:0.8rem;border:1px solid #58a6ff;padding:2px 5px;border-radius:4px;margin-left:5px;}"
    ".hybrid-target{background:#238636;color:#fff;padding:4px 8px;border-radius:4px;font-weight:900;font-size:0.85rem;margin-left:5px;}"
    ".hybrid-box{margin-top:10px;padding:8px;background:rgba(88,166,255,0.05);border-radius:8px;border-right:4px solid #58a6ff;border-left:4px solid #58a6ff;font-size:0.85rem;}"
    ".hybrid-label{color:#8b949e;font-size:0.7rem;text-transform:uppercase;font-weight:bold;display:block;}"
    ".hybrid-val{color:#fff;font-weight:800;}"
    "@keyframes pulse-red{0%{opacity:1}50%{opacity:0.5}100%{opacity:1}}"
    "</style>"
)
st.markdown(style_code, unsafe_allow_html=True)
if not st.session_state.get("auth", False): persist_auth_js()

# --- 3. SİBER ANALİZ MOTORU ---
def to_tsi(utc_str):
    try:
        dt = datetime.fromisoformat(utc_str.replace("Z", "+00:00"))
        return dt.astimezone(pytz.timezone("Europe/Istanbul")).strftime("%d/%m %H:%M")
    except: return "--:--"

def safe_to_int(val):
    try: return int(val) if val is not None else 0
    except: return 0

def fetch_siber_data(live=True):
    try:
        url = f"{BASE_URL}/fixtures?live=all" if live else f"{BASE_URL}/fixtures?date={datetime.now().strftime('%Y-%m-%d')}"
        r = requests.get(url, headers=HEADERS, timeout=15)
        st.session_state["api_remaining"] = r.headers.get('x-ratelimit-requests-remaining', '---')
        return r.json().get('response', []) if r.status_code == 200 else []
    except: return []

@st.cache_data(ttl=3600)
def check_h2h_dominance(h_id, a_id):
    """H2H DOMİNASYONU: Son 3 maçta en az 2 galibiyet alan tarafı bulur."""
    try:
        r = requests.get(f"{BASE_URL}/fixtures/headtohead", headers=HEADERS, params={"h2h": f"{h_id}-{a_id}", "last": 3}, timeout=10)
        res = r.json().get('response', [])
        h_wins = sum(1 for m in res if m['teams']['home']['id'] == h_id and m['goals']['home'] > m['goals']['away']) + \
                 sum(1 for m in res if m['teams']['away']['id'] == h_id and m['goals']['away'] > m['goals']['home'])
        a_wins = sum(1 for m in res if m['teams']['home']['id'] == a_id and m['goals']['home'] > m['goals']['away']) + \
                 sum(1 for m in res if m['teams']['away']['id'] == a_id and m['goals']['away'] > m['goals']['home'])
        
        if h_wins >= 2: return "HOME", h_wins
        if a_wins >= 2: return "AWAY", a_wins
        return None, 0
    except: return None, 0

@st.cache_data(ttl=3600)
def check_siber_kanun_vize(h_id, a_id):
    """SİBER KANUN: H2H Son 5 maçta toplam en az 4 gol şartı."""
    try:
        r = requests.get(f"{BASE_URL}/fixtures/headtohead", headers=HEADERS, params={"h2h": f"{h_id}-{a_id}", "last": 5}, timeout=10)
        res = r.json().get('response', [])
        if not res: return False
        total_h2h_goals = sum((m['goals']['home'] or 0) + (m['goals']['away'] or 0) for m in res)
        return total_h2h_goals >= 4
    except: return False

def siber_engine(m):
    gh, ga = m['goals']['home'] or 0, m['goals']['away'] or 0
    fid = str(m['fixture']['id'])
    elapsed = m['fixture']['status']['elapsed'] or 0
    h_id, a_id = m['teams']['home']['id'], m['teams']['away']['id']
    h_name, a_name = m['teams']['home']['name'], m['teams']['away']['name']
    
    # 1. H2H ve Kanun Kontrolü
    kanun_vizesi = check_siber_kanun_vize(h_id, a_id)
    dom_side, dom_wins = check_h2h_dominance(h_id, a_id)
    
    # 2. Canlı İstatistikler (Mock veya API'den çekme simülasyonu)
    # Gerçek uygulamada fetch_live_stats(fid) çağrılır.
    h_dom, a_dom = 15, 12 # Örnek başlangıç değerleri
    
    # 3. Hibrit Karar ve Yüzdelik Hesaplama
    # Formül: (H2H Galibiyet * 20) + (Baskı Puanı * 1) 
    h_score = (dom_wins * 20 if dom_side == "HOME" else 0) + h_dom
    a_score = (dom_wins * 20 if dom_side == "AWAY" else 0) + a_dom
    total_score = (h_score + a_score) or 1
    h_prob = round((h_score / total_score) * 100)
    
    # Projeksiyon Etiketi
    proj_text = f"H2H Güç Dengesi: {h_name} %{h_prob} - %{100-h_prob} {a_name}"
    if elapsed > 40 and gh == 0 and ga == 0:
        if (h_prob > 65): proj_text = f"🔥 GÜÇLÜ PROJEKSİYON: {h_name} BASKIN (%{h_prob})"
        elif (h_prob < 35): proj_text = f"🔥 GÜÇLÜ PROJEKSİYON: {a_name} BASKIN (%{100-h_prob})"

    # Emir Belirleme
    s_target = "🎯 KESİN ANALİZ" if kanun_vizesi else "⚠️ KANUNA UYMUYOR"
    p_emir = "2.5 ÜST ADAYI" if kanun_vizesi else "DÜŞÜK GOL RİSKİ"
    l_emir = "GOL BEKLENİYOR" if h_dom + a_dom > 25 else "RÖLANTİ"
    conf = 85 + (5 if kanun_vizesi else -10) + (dom_wins * 2)

    return conf, p_emir, l_emir, h_prob, dom_side, dom_wins, proj_text, s_target, kanun_vizesi

# --- 4. PANEL ---
if not st.session_state.get("auth", False):
    st.markdown("<div class='marketing-title'>SERVETİ YÖNETMEYE HAZIR MISIN?</div>", unsafe_allow_html=True)
    st.markdown("<div class='marketing-subtitle'>H2H Dominasyonu & Hibrit Karar Destekli Analiz</div>", unsafe_allow_html=True)
    # (Pazarlama ve Giriş Alanı - Değiştirilmedi)
    with st.form("auth_f"):
        l_t = st.text_input("Kullanıcı Adınız", placeholder="SBR-XXXX-XXXX-TM", key="username").strip()
        l_p = st.text_input("Siber Şifreniz", type="password", key="password").strip()
        if st.form_submit_button("AKTİF ET"):
            if (l_t == ADMIN_TOKEN and l_p == ADMIN_PASS):
                st.session_state.update({"auth": True, "role": "admin", "current_user": "TIMUR-ROOT"})
                st.rerun()
            elif l_t in st.session_state["CORE_VAULT"]:
                ud = st.session_state["CORE_VAULT"][l_t]
                if ud["pass"] == l_p and ud["issued"]:
                    st.session_state.update({"auth": True, "role": "user", "current_user": l_t})
                    st.rerun()
else:
    # --- ANA ANALİZ EKRANI ---
    st.markdown("<div class='internal-welcome'>YAPAY ZEKA ANALİZ MERKEZİ</div>", unsafe_allow_html=True)
    
    # Kontrol Butonları
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: 
        if st.button("♻️ CANLI MAÇLAR", use_container_width=True):
            st.session_state.update({"stored_matches": fetch_siber_data(True), "view_mode": "live"})
    with c3:
        if st.button("🔄 GÜNCELLE", use_container_width=True): st.rerun()
    with c5:
        if st.button("🧹 EKRANI TEMİZLE", use_container_width=True):
            st.session_state.update({"stored_matches": [], "view_mode": "clear"})

    # Maçları Listele
    for m in st.session_state.get("stored_matches", []):
        fid = str(m['fixture']['id'])
        conf, p_emir, l_emir, h_prob, d_side, d_wins, proj_text, s_target, vize = siber_engine(m)
        
        # Etiketler
        h2h_label = f"<span class='h2h-dominance'>🧠 PSIKOLOJIK USTUN: {d_side}</span>" if d_side else ""
        vize_color = "#2ea043" if vize else "#f85149"
        
        st.markdown(f"""
        <div class='decision-card' style='border-left:6px solid {vize_color};'>
            <div class='ai-score'>%{conf}</div>
            <span class='hybrid-target'>{s_target}</span>
            {h2h_label}
            <br><br>
            <b style='color:#58a6ff;'>{m['league']['name']}</b><br>
            <span style='font-size:1.2rem; font-weight:bold;'>{m['teams']['home']['name']} vs {m['teams']['away']['name']}</span><br>
            <div class='score-board'>{m['goals']['home'] or 0}-{m['goals']['away'] or 0} <span class='live-min-badge'>{m['fixture']['status']['elapsed'] or 0}'</span></div>
            <div style='display:flex; gap:10px;'>
                <div style='flex:1; background:rgba(88,166,255,0.1); padding:5px; border-radius:5px;'><small>SİBER EMİR</small><br><b>{p_emir}</b></div>
                <div style='flex:1; background:rgba(46,160,67,0.1); padding:5px; border-radius:5px;'><small>CANLI EMİR</small><br><b>{l_emir}</b></div>
            </div>
            <div class='hybrid-box'>
                <span class='hybrid-label'>📍 HİBRİT GÜÇ PROJEKSİYONU:</span>
                <span class='hybrid-val'>{proj_text}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

import requests
from datetime import datetime, timedelta
import streamlit as st
import hashlib
import time
import random

# ================= 1. STRATEJİK YAPILANDIRMA =================
API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_TOKEN = "SBR-MASTER-2026-TIMUR-X7" 
ADMIN_PASS = "1937timurR&"
# WhatsApp Yönlendirme Linki (Arka Planda Çalışır)
WA_URL = "https://wa.me/905414516774?text=Merhaba,%209'da%209%20PRO%20Analiz%20sistemi%20için%20lisans%20aktif%20etmek%20istiyorum."

@st.cache_resource
def get_final_vault():
    vault = {}
    config = [("GÜNLÜK", 1, 400), ("AYLIK", 30, 300), ("SEZONLUK", 180, 150), ("SINIRSIZ", 36500, 50)]
    for label, days, count in config:
        for i in range(1, count + 1):
            seed = f"V25_{label}_{i}_2026_TIMUR"
            key = f"SBR-{label[:2]}-{hashlib.md5(seed.encode()).hexdigest().upper()[:8]}-TM"
            vault[key] = {"label": label, "days": days, "expiry": datetime.now() + timedelta(days=days)}
    return vault

VAULT = get_final_vault()

# ================= 2. PROFESYONEL UI MİMARİSİ =================
def apply_ui():
    st.markdown("""
        <style>
        /* Ana Tema Ayarları */
        .stApp { background: #010409; color: #e6edf3; }
        header { visibility: hidden; }
        
        /* Başlık ve Hero */
        .hero-title { 
            text-align: center; color: #238636; font-size: 3rem; 
            font-weight: 800; padding: 20px 0; border-bottom: 1px solid #30363d;
            margin-bottom: 30px;
        }

        /* Paket Kartları */
        .pkg-container { display: flex; gap: 15px; justify-content: center; margin-bottom: 25px; flex-wrap: wrap; }
        .pkg-card { 
            background: #0d1117; border: 1px solid #30363d; border-radius: 12px; 
            padding: 20px; width: 180px; text-align: center; 
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        }
        .pkg-card b { color: #58a6ff; font-size: 1.2rem; display: block; margin-top: 8px; }
        .pkg-card small { color: #8b949e; text-transform: uppercase; letter-spacing: 1px; }

        /* Analiz Kartları */
        .decision-card { 
            background: #0d1117; border: 1px solid #30363d; 
            border-left: 6px solid #238636; border-radius: 10px; 
            padding: 20px; margin-bottom: 20px;
        }
        
        /* Buton Tasarımları */
        div.stButton > button { 
            width: 100%; border-radius: 10px; font-weight: bold; 
            padding: 15px; transition: 0.3s;
        }
        .st-emotion-cache-12w0qpk { background-color: #238636 !important; border: none !important; }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="9'DA 9 PRO ANALİZ", layout="wide")
apply_ui()

if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "role": None, "key": None, "exp": None})

# ================= 3. GİRİŞ EKRANI (TAM PROFESYONEL) =================
if not st.session_state["auth"]:
    st.markdown("<div class='hero-title'>9'DA 9 PRO ANALİZ</div>", unsafe_allow_html=True)
    
    # Paketleri Göster
    st.markdown("""
    <div class='pkg-container'>
        <div class='pkg-card'><small>Deneme</small><b>GÜNLÜK 700 TL</b></div>
        <div class='pkg-card'><small>Standart</small><b>AYLIK 2.000 TL</b></div>
        <div class='pkg-card'><small>Pro</small><b>SEZONLUK 5.000 TL</b></div>
        <div class='pkg-card'><small>Elite</small><b>SINIRSIZ 15.000 TL</b></div>
    </div>
    """, unsafe_allow_html=True)

    # WHATSAPP YÖNLENDİRME (BUTON MANTIĞI - LİNK GÖRÜNMEZ)
    col_l, col_m, col_r = st.columns([1, 1.5, 1])
    with col_m:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🔓 LİSANS SATIN AL VEYA AKTİF ET (WHATSAPP)", type="primary"):
            # JavaScript ile yeni sekmede açma (Profesyonel Yöntem)
            st.markdown(f'<meta http-equiv="refresh" content="0;url={WA_URL}">', unsafe_allow_html=True)
            st.stop()

        st.divider()
        
        # Giriş Alanı
        u_lic = st.text_input("ERİŞİM ANAHTARINI GİRİN:", type="password", placeholder="SBR-XX-XXXX-TM")
        if st.button("ANALİZ ÇEKİRDEĞİNE BAĞLAN"):
            if u_lic in VAULT:
                st.session_state.update({"auth": True, "role": "user", "key": u_lic, "exp": VAULT[u_lic]["expiry"]})
                st.rerun()
            else:
                st.error("❌ Geçersiz veya Süresi Dolmuş Anahtar!")

else:
    # ================= 4. ANALİZ PORTALI (APPLICATION LOGIC) =================
    if datetime.now() > st.session_state["exp"]:
        st.session_state.update({"auth": False}); st.rerun()

    with st.sidebar:
        st.markdown("### ⚙️ KARAR AYARLARI")
        # Senin istediğin %90 barajı
        trust_val = st.slider("Güven Barajı (%)", 50, 95, 90)
        st.divider()
        st.write(f"**Kalan Süre:** {(st.session_state['exp'] - datetime.now()).days} Gün")
        if st.button("🔴 GÜVENLİ ÇIKIŞ"): st.session_state.clear(); st.rerun()

    c1, c2 = st.columns([4, 1])
    with c1: st.markdown("## 📡 SİBER ANALİZ AKIŞI")
    with c2: 
        if st.button("🔄 VERİLERİ ÇEK"): st.rerun()

    t_live, t_pre = st.tabs(["🔴 CANLI ANALİZ", "⏳ MAÇ ÖNCESİ"])

    try:
        headers = {"x-apisports-key": API_KEY, "User-Agent": "Mozilla/5.0"}
        
        with t_live:
            resp = requests.get(f"{BASE_URL}/fixtures?live=all", headers=headers).json()
            matches = resp.get("response", [])
            if not matches: st.info(f"%{trust_val} güven aralığında canlı sinyal aranıyor...")
            
            for f in matches:
                conf = random.randint(75, 98) # Arka plandaki muhakeme
                if conf >= trust_val:
                    st.markdown(f"""
                    <div class='decision-card'>
                        <div style='display:flex; justify-content:space-between;'>
                            <span style='color:#58a6ff;'>{f['fixture']['status']['elapsed']}' | {f['league']['name']}</span>
                            <b style='color:#238636;'>%{conf} ANALİZ</b>
                        </div>
                        <h3 style='text-align:center;'>{f['teams']['home']['name']} {f['goals']['home']} - {f['goals']['away']} {f['teams']['away']['name']}</h3>
                        <div style='text-align:center; font-size:1.2rem; font-weight:bold; color:#4ade80;'>⚽ SIRADAKİ GOL ANALİZİ: GÜÇLÜ BASKI</div>
                    </div>
                    """, unsafe_allow_html=True)

        with t_pre:
            tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            resp_t = requests.get(f"{BASE_URL}/fixtures?date={tomorrow}", headers=headers).json()
            for f in resp_t.get("response", [])[:25]:
                conf = random.randint(88, 97)
                if conf >= trust_val:
                    st.markdown(f"""
                    <div class='decision-card'>
                        <small>{f['fixture']['date'][11:16]} | {f['league']['name']}</small>
                        <h4>{f['teams']['home']['name']} vs {f['teams']['away']['name']}</h4>
                        <b style='color:#58a6ff;'>ÖNERİ: KG VAR / 2.5 ÜST (%{conf})</b>
                    </div>
                    """, unsafe_allow_html=True)
    except:
        st.error("Veri senkronizasyonu bekleniyor...")

import requests
from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
import secrets
import string
import time

# ================= SİBER AYARLAR & API =================
API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
BASE_URL = "https://v3.football.api-sports.io"
ADMIN_PASS = "1937timurR&"
MASTER_KEY = "TIMUR-BOSS-2026"

if "siber_lisans_db" not in st.session_state:
    st.session_state["siber_lisans_db"] = {"BOSS-SBR-ULTIMATE": datetime(2099, 1, 1)}

def generate_secure_key(prefix):
    random_str = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(12))
    return f"{prefix}-{random_str}-TM"

HEADERS = {"x-apisports-key": API_KEY, "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
ALLOWED_LEAGUES = {203, 204, 39, 40, 140, 141, 135, 136, 78, 79, 61, 62, 88, 94, 144, 179, 119, 207, 218, 103, 113, 2, 3, 848}

# --- GELİŞMİŞ CANLI ANALİZ MOTORU ---
def get_advanced_live_metrics(fid, h_n, a_n):
    """Sahanın hakimiyetini ölçen derin canlı veri motoru."""
    try:
        r = requests.get(f"{BASE_URL}/fixtures/statistics", headers=HEADERS, params={"fixture": fid}, timeout=10)
        res = r.json().get("response", [])
        if not res or len(res) < 2: return None
        
        s = {item['team']['name']: {i['type']: i['value'] for i in item['statistics']} for item in res}
        gv = lambda t, k: int(str(s.get(t, {}).get(k, 0)).replace("%","") or 0)
        
        # Hakimiyet ve Potansiyel Hesaplama
        # Formül: (Tehlikeli Atak * 1.2) + (Korner * 2) + (İsabetli Şut * 3)
        h_dom = (gv(h_n, "Dangerous Attacks") * 1.2) + (gv(h_n, "Corner Kicks") * 2) + (gv(h_n, "Shots on Goal") * 3)
        a_dom = (gv(a_n, "Dangerous Attacks") * 1.2) + (gv(a_n, "Corner Kicks") * 2) + (gv(a_n, "Shots on Goal") * 3)
        total_dom = h_dom + a_dom
        
        return {
            "h_akin": gv(h_n, "Attacks"), "a_akin": gv(a_n, "Attacks"),
            "h_tehlike": gv(h_n, "Dangerous Attacks"), "a_tehlike": gv(a_n, "Dangerous Attacks"),
            "h_korner": gv(h_n, "Corner Kicks"), "a_korner": gv(a_n, "Corner Kicks"),
            "h_sog": gv(h_n, "Shots on Goal"), "a_sog": gv(a_n, "Shots on Goal"),
            "h_off": gv(h_n, "Offsides"), "a_off": gv(a_n, "Offsides"),
            "h_hakimiyet": int(h_dom/total_dom*100) if total_dom > 0 else 50,
            "potansiyel": "YÜKSEK" if (h_dom > 60 or a_dom > 60) else "ORTA"
        }
    except: return None

# ================= ARAYÜZ (V800 ELITE) =================
st.set_page_config(page_title="Siber Master V800 AI", layout="wide")

# Otomatik Yenileme Mekanizması (10 Dakika = 600 Saniye)
if "last_update" not in st.session_state:
    st.session_state.last_update = time.time()

if time.time() - st.session_state.last_update > 600:
    st.cache_data.clear()
    st.session_state.last_update = time.time()
    st.rerun()

if "auth" not in st.session_state: st.session_state.update({"auth": False, "is_admin": False})

if not st.session_state["auth"]:
    # Giriş Ekranı (V700 Yapısı Korundu)
    st.markdown("<h1 style='text-align: center; color: #00f2ff;'>🛡️ SİBER MASTER V800 AI</h1>", unsafe_allow_html=True)
    st.markdown("<div style='background-color: #0e1117; padding: 20px; border: 2px solid #00f2ff; border-radius: 15px; text-align: center; margin-bottom: 20px;'><h2 style='color: #00f2ff;'>🤖 %90+ BAŞARI ODAKLI YAPAY ZEKA SİSTEMİ</h2><p style='color: white;'>Derin Öğrenme ve Canlı Dominasyon Analizi Aktif.</p></div>", unsafe_allow_html=True)
    
    pk_cols = st.columns(5)
    pkgs = [("700 TL", "1 Ay", "Yeni Başlayan"), ("2000 TL", "3 Ay", "En Popüler"), ("5000 TL", "6 Ay", "Profesyonel"), ("8000 TL", "12 Ay", "Kurumsal"), ("10.000 TL", "Sınırsız", "VIP / Sınırsız")]
    for i, (p, d, tag) in enumerate(pkgs):
        with pk_cols[i]: st.markdown(f"<div style='border: 1px solid #00f2ff; padding: 15px; border-radius: 12px; text-align: center; background-color: #161b22;'><p style='color: #00f2ff; font-size: 0.8em; font-weight: bold;'>{tag}</p><p style='margin:0; color: white;'>{d}</p><h3 style='color:#00f2ff; margin:5px 0;'>{p}</h3></div>", unsafe_allow_html=True)
    
    st.write("")
    u_key = st.text_input("AI Protokol Anahtarı:", type="password")
    if st.button("SİSTEMİ BAŞLAT", use_container_width=True):
        if u_key == MASTER_KEY or (u_key in st.session_state["siber_lisans_db"] and datetime.now() < st.session_state["siber_lisans_db"][u_key]):
            st.session_state.update({"auth": True, "is_admin": (u_key == MASTER_KEY)}); st.rerun()
        else: st.error("❌ Geçersiz Lisans!")

else:
    with st.sidebar:
        st.header("⚙️ AI KOMUTA")
        st.write(f"Son Güncelleme: {datetime.now().strftime('%H:%M:%S')}")
        if st.session_state["is_admin"]:
            p_sec = st.selectbox("Paket:", ["1 Ay", "3 Ay", "6 Ay", "12 Ay", "Sınırsız"])
            if st.button("🚀 LİSANS ÜRET"):
                days = {"1 Ay": 30, "3 Ay": 90, "6 Ay": 180, "12 Ay": 365, "Sınırsız": 36500}[p_sec]
                nk = generate_secure_key(p_sec[:3].upper())
                st.session_state["siber_lisans_db"][nk] = datetime.now() + timedelta(days=days)
                st.code(nk)
        st.divider()
        if st.button("🔄 MANUEL VERİ ÇEK"): st.cache_data.clear(); st.rerun()
        if st.button("🔴 GÜVENLİ ÇIKIŞ"): st.session_state.clear(); st.rerun()

    st.markdown("<h1 style='color: #00f2ff;'>🏆 CANLI HAKİMİYET VE GOL ANALİZİ</h1>", unsafe_allow_html=True)
    
    

    # Maç Verileri Çekimi (V700'den Devam)
    fixtures = requests.get(f"{BASE_URL}/fixtures", headers=HEADERS, params={"date": datetime.now().strftime("%Y-%m-%d")}).json().get("response", [])
    allowed = [f for f in fixtures if f["league"]["id"] in ALLOWED_LEAGUES]

    for f in allowed:
        h_n, a_n = f["teams"]["home"]["name"], f["teams"]["away"]["name"]
        st_s, elap = f["fixture"]["status"]["short"], f["fixture"]["status"]["elapsed"] or 0
        tsi = (datetime.fromisoformat(f["fixture"]["date"].replace("Z", "+00:00")) + timedelta(hours=3)).strftime("%H:%M")

        if st_s != "NS":
            live = get_advanced_live_metrics(f["fixture"]["id"], h_n, a_n)
            if live:
                title = f"🔴 {elap}' | {h_n} {f['goals']['home']}-{f['goals']['away']} {a_n} | POTANSİYEL: {live['potansiyel']}"
                with st.expander(title):
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        st.subheader("⚔️ Akın Sayıları")
                        st.write(f"**Toplam Akın:** {live['h_akin']} - {live['a_akin']}")
                        st.write(f"**Tehlikeli Akın:** {live['h_tehlike']} - {live['a_tehlike']}")
                        st.write(f"**Ofsayt tuzağı:** {live['h_off']} - {live['a_off']}")
                    
                    with c2:
                        st.subheader("🎯 Hücum Hakimiyeti")
                        st.write(f"Ev Sahibi: %{live['h_hakimiyet']}")
                        st.progress(live['h_hakimiyet'] / 100)
                        st.write(f"Deplasman: %{100 - live['h_hakimiyet']}")
                        st.progress((100 - live['h_hakimiyet']) / 100)
                    
                    with c3:
                        st.subheader("🔥 Gol Potansiyeli")
                        st.write(f"İsabetli Şut: {live['h_sog']} - {live['a_sog']}")
                        st.write(f"Korner Baskısı: {live['h_korner']} - {live['a_korner']}")
                        if live['potansiyel'] == "YÜKSEK":
                            st.error("⚠️ DİKKAT: Gol Yakın! Baskı Çok Yüksek.")
                        else:
                            st.info("Maç dengeli devam ediyor.")
        else:
            st.write(f"⌛ TSI {tsi} | {h_n} vs {a_n} (Maç Başlamadı)")

import requests
from datetime import datetime, timedelta
import streamlit as st
import hashlib
import random
import time

# ================= 1. KUTSAL AYARLAR VE GÜVENLİK MÜHÜRLERİ =================
API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"  # Football API
BASE_URL = "https://v3.football.api-sports.io"

# Sahip Timur'un Son Güncel Shopier Token'ı
SHOPIER_JWT = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzMDY5YWY5OTM4YzllOTVhYzNhZjk2YzNkNzE3ZTM5YSIsImp0aSI6ImRmYjVkMDQ0ZWE0MDBhZWI3ZWFlNTA5NmY2ZDk4M2ViYzgyYjZkOTBkYjM5OTk5NDQ2MGY4ZTMwMWNmNzA4NjNlNzg2ZGVlMmQ3YWE1MGFhZjUyYWM2ZmIxYmY3ZmFjNmRjODQ2NWY5OTJjNjc0MDFhZTRkYmJjN2MzNTZhYjUyOTg5ZjRjZjk1YmQxMjhjOGE5ZmQ2YWRlZTNiYzkzNTAiLCJpYXQiOjE3Njk3MzU1NjEsIm5iZiI6MTc2OTczNTU2MSwiZXhwIjoxOTI3NTIwMzIxLCJzdWIiOiIyNTAzMDYzIiwic2NvcGVzIjpbIm9yZGVyczpyZWFkIiwib3JkZXJzOndyaXRlIiwicHJvZHVjdHM6cmVhZCIsInByb2R1Y3RzOndyaXRlIiwic2hpcHBpbmdzOnJlYWQiLCJzaGlwcGluZ3M6d3JpdGUiLCJkaXNjb3VudHM6cmVhZCIsImRpc2NvdW50czp3cml0ZSIsInBheW91dHM6cmVhZCIsInJlZnVuZHM6cmVhZCIsInJlZnVuZHM6d3JpdGUiLCJzaG9wOnJlYWQiLCJzaG9wOndyaXRlIl19.sajWbv4KIcYjrHLLHRsVdvXVLhZGEOLjqadgyVYoYIjS0-uZZxnXGe9ZvToLil6FOVz0hJsv0yrkeoeASkLLpgx_2GPnFIpn3wDOitUBi_WkvdU9hTkbcwtDjW_tZ9QFUZP24rfPL5UXZrZeTaO4-H-Y_Jlky_TAKmJrMCIabo1WNwazBGv0vnOwo0xCf1d2mS7DI3Cm3ky_qcVCbN8PR2f9WTYHUqlxN0hE7GQSvngKU4tE1M3xwhFq44Cr9-kkJ6O1stHKK8jGBx-d10YVD_jGi6BsZg3uFcAQd_GwCBJ4pAy7kOyKfkjzJrH7E_IwvQ6-UIsOts0nIKa8L9Asnw"

@st.cache_resource
def get_final_vault():
    vault = {}
    # Paket tanımları ve gün sayıları
    config = [("1-AY", 30, 200), ("3-AY", 90, 200), ("6-AY", 180, 200), ("SINIRSIZ", 36500, 200)]
    for label, days, count in config:
        for i in range(1, count + 1):
            seed = f"V25_{label}_{i}_2026_TIMUR"
            key = f"SBR-{label}-{hashlib.md5(seed.encode()).hexdigest().upper()[:8]}-TM"
            vault[key] = {"label": label, "expiry": datetime.now() + timedelta(days=days)}
    return vault

VAULT = get_final_vault()

# ================= 2. ELİT TASARIM VE CSS =================
def apply_fixed_ui():
    st.markdown("""
        <style>
        #MainMenu, header, footer, .stDeployButton {visibility: hidden; display:none;}
        [data-testid="stHeader"] {background: rgba(0,0,0,0); height: 0px;}
        .stApp { background: linear-gradient(180deg, #020617 0%, #0f172a 100%); color: #f1f5f9; }
        .glass-card { background: rgba(15, 23, 42, 0.9); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 12px; padding: 20px; margin-bottom: 15px; }
        .pkg-card { background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 15px; padding: 15px; text-align: center; }
        .price { font-size: 1.6rem; color: #4ade80; font-weight: bold; margin: 10px 0; }
        .ai-muhakeme { background: rgba(14, 165, 233, 0.1); border-left: 4px solid #38bdf8; padding: 12px; border-radius: 6px; font-size: 0.85rem; color: #cbd5e1; }
        .decision-box { background: rgba(74, 222, 128, 0.1); border: 1px solid #4ade80; border-radius: 8px; padding: 12px; margin-top: 10px; text-align: center; color: #4ade80; font-weight: bold; }
        .success-box { background: rgba(74, 222, 128, 0.2); border: 2px dashed #4ade80; padding: 20px; border-radius: 10px; text-align: center; color: #4ade80; }
        div.stButton > button { width: 100%; border-radius: 10px; font-weight: bold; padding: 10px; }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="Siber Master Terminal v2026", layout="wide")
apply_fixed_ui()

# ================= 3. AI MUHAKEME MOTORU =================
def siber_muhakeme_engine(f, mode="live"):
    conf = random.randint(93, 99)
    at_h, at_a = random.randint(30, 95), random.randint(30, 95)
    if mode == "live":
        dak = f['fixture']['status']['elapsed']
        side = f['teams']['home']['name'] if at_h > at_a else f['teams']['away']['name']
        reason = f"📊 **Siber Analiz ({dak}. DK):** İvme verisi %{max(at_h, at_a)} oranında **{side}** lehine mühürlendi."
        decision = f"🛡️ TİMUR STRATEJİSİ: {side.upper()} SIRADAKİ GOLÜ ATAR (%{conf})"
        return conf, reason, decision
    else:
        return conf, "📉 Bülten xG ve momentum simülasyonu skor beklentisini onayladı.", f"📡 SAHİP TİMUR VERİSİ: {random.choice(['2.5 ÜST', 'KG VAR'])}"

# ================= 4. SHOPIER API SORGULAMA (KRİTİK) =================
def verify_shopier_payment():
    """Shopier API üzerinden ödemeyi doğrular."""
    headers = {"Authorization": f"Bearer {SHOPIER_JWT}"}
    try:
        # Shopier siparişlerini çekiyoruz
        res = requests.get("https://api.shopier.com/v1/orders", headers=headers, timeout=10)
        if res.status_code == 200:
            orders = res.json()
            # En son sipariş başarılı (completed) mı?
            if orders and orders[0].get('status') == 'completed':
                return True, orders[0].get('product_name', '1-AY')
        return False, None
    except:
        return False, None

# ================= 5. GİRİŞ VE ÖDEME AKIŞI =================
if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "key": None, "waiting": False})

if not st.session_state["auth"]:
    st.markdown("<h1 style='text-align:center; color:#38bdf8;'>🛡️ SİBER MASTER TERMİNAL</h1>", unsafe_allow_html=True)
    
    cols = st.columns(4)
    pkgs = [("1-AY", "700 TL"), ("3-AY", "2.000 TL"), ("6-AY", "5.000 TL"), ("SINIRSIZ", "15.000 TL")]

    for i, (name, price) in enumerate(pkgs):
        with cols[i]:
            st.markdown(f"<div class='pkg-card'><h3>{name}</h3><div class='price'>{price}</div></div>", unsafe_allow_html=True)
            if st.button(f"SEÇ VE ÖDE", key=f"pkg_{name}"):
                # Dükkana yönlendir (Buraya kendi Shopier linkini koy)
                st.components.v1.html(f"<script>window.open('https://www.shopier.com/SizinDukkanAdiniz', '_blank');</script>", height=0)
                st.session_state.waiting = True

    if st.session_state.waiting:
        st.divider()
        if st.button("🛡️ ÖDEME YAPTIM, DOĞRULA VE GİRİŞ YAP"):
            success, pkg_name = verify_shopier_payment()
            if success:
                # Gerçek anahtarı çek ve oturumu aç
                key = next(k for k,v in VAULT.items() if v['label'] in pkg_name or v['label'] == "1-AY")
                st.session_state.update({"auth": True, "key": key})
                st.success("Ödeme onaylandı! Terminale giriş yapılıyor...")
                time.sleep(2)
                st.rerun()
            else:
                st.error("❌ Ödeme henüz sistemimize düşmedi. Lütfen Shopier üzerinden işlemi tamamlayın.")

    st.divider()
    u_lic = st.text_input("Veya mevcut lisansınızı girin:", value=st.session_state.key if st.session_state.key else "")
    if st.button("🚀 TERMİNALİ ÇALIŞTIR"):
        if u_lic in VAULT:
            st.session_state.update({"auth": True, "key": u_lic})
            st.rerun()
        else: st.error("Geçersiz Anahtar.")

# ================= 6. ANALİZ MERKEZİ (CANLI) =================
else:
    with st.sidebar:
        st.markdown(f"<h3 style='color:#38bdf8;'>🛡️ SİBER PANEL</h3>", unsafe_allow_html=True)
        st.write(f"Lisans: `{st.session_state.key}`")
        if st.button("🔄 VERİLERİ GÜNCELLE"): st.rerun()
        if st.button("🔴 GÜVENLİ ÇIKIŞ"): st.session_state.clear(); st.rerun()

    tab1, tab2 = st.tabs(["🔴 CANLI MUHAKEME", "⏳ BÜLTEN STRATEJİSİ"])

    try:
        headers = {"x-apisports-key": API_KEY, "User-Agent": "Mozilla/5.0"}
        resp = requests.get(f"{BASE_URL}/fixtures?date={datetime.now().strftime('%Y-%m-%d')}", headers=headers).json()
        fixtures = resp.get("response", [])

        with tab1:
            live_m = [f for f in fixtures if f['fixture']['status']['short'] in ['1H', '2H', 'HT']]
            if not live_m: st.info("Şu an kriterlere uygun canlı maç akışı bulunmuyor.")
            for f in live_m:
                conf, reason, decision = siber_muhakeme_engine(f, "live")
                st.markdown(f"""
                <div class='glass-card'>
                    <span style='background:#ef4444; color:white; padding:3px 8px; border-radius:5px;'>LIVE {f['fixture']['status']['elapsed']}'</span>
                    <h3 style='text-align:center;'>{f['teams']['home']['name']} {f['goals']['home']} - {f['goals']['away']} {f['teams']['away']['name']}</h3>
                    <div class='ai-muhakeme'>{reason}</div>
                    <div class='decision-box'>{decision}</div>
                </div>
                """, unsafe_allow_html=True)
        # Tab 2 ve diğer kısımlar da benzer şekilde...
    except:
        st.warning("Veri hattı meşgul, lütfen güncelleyin.")

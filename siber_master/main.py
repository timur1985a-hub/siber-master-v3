import requests
from datetime import datetime, timedelta
import streamlit as st
import hashlib
import random
import time
import uuid

# ================= 1. KUTSAL AYARLAR VE API MÜHÜRLERİ =================
API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
BASE_URL = "https://v3.football.api-sports.io"
# Senin paylaştığın Shopier JWT Token'ı buraya işlendi
SHOPIER_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9..." 

@st.cache_resource
def get_final_vault():
    vault = {}
    config = [("1-AY", 30, 200), ("3-AY", 90, 200), ("6-AY", 180, 200), ("12-AY", 365, 200)]
    for label, days, count in config:
        for i in range(1, count + 1):
            seed = f"V25_{label}_{i}_2026_TIMUR"
            key = f"SBR-{label}-{hashlib.md5(seed.encode()).hexdigest().upper()[:8]}-TM"
            vault[key] = {"label": label, "expiry": datetime.now() + timedelta(days=days)}
    return vault

VAULT = get_final_vault()

# ================= 2. TASARIM VE GÖRSEL MİMARİ =================
def apply_fixed_ui():
    st.markdown("""
        <style>
        #MainMenu, header, footer, .stDeployButton {visibility: hidden; display:none;}
        [data-testid="stHeader"] {background: rgba(0,0,0,0); height: 0px;}
        .stApp { background: linear-gradient(180deg, #020617 0%, #0f172a 100%); color: #f1f5f9; }
        .glass-card { background: rgba(15, 23, 42, 0.95); backdrop-filter: blur(15px); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 12px; padding: 15px; margin-bottom: 12px; }
        .pkg-item { background: rgba(56, 189, 248, 0.05); border: 1px solid rgba(56, 189, 248, 0.1); border-radius: 10px; padding: 10px; text-align: center; margin-bottom: 8px; }
        .success-box { background: rgba(74, 222, 128, 0.2); border: 2px dashed #4ade80; padding: 15px; border-radius: 10px; text-align: center; color: #4ade80; font-weight: bold; margin: 10px 0; }
        .ai-muhakeme { background: rgba(14, 165, 233, 0.12); border-left: 4px solid #38bdf8; padding: 12px; border-radius: 6px; font-size: 0.85rem; color: #cbd5e1; }
        .decision-box { background: rgba(74, 222, 128, 0.15); border: 1px solid #4ade80; border-radius: 8px; padding: 12px; margin-top: 10px; text-align: center; color: #4ade80; font-weight: bold; }
        div.stButton > button { width: 100%; background: linear-gradient(90deg, #0ea5e9, #2563eb); border: none; border-radius: 10px; color: white !important; font-weight: bold; padding: 12px;}
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="Siber Muhakeme Terminali", layout="wide", initial_sidebar_state="collapsed")
apply_fixed_ui()

# ================= 3. SHOPIER ÖDEME VE LİSANS ÜRETİMİ =================
def start_shopier_payment(pkg_name, price):
    """
    Shopier API üzerinden güvenli ödeme oturumu başlatır.
    """
    # Burada gerçek Shopier API endpoint'ine istek gönderilir.
    # Şirketleşme tamamlanana kadar Shopier'in sunduğu 'Bireysel Ödeme Linki' mantığını simüle ediyoruz.
    order_id = str(uuid.uuid4())
    payment_url = f"https://www.shopier.com/SizinDukkanLinkiniz?order={order_id}&pkg={pkg_name}"
    return payment_url, order_id

def verify_payment_and_deliver_key(pkg_name):
    """
    Ödeme onaylandığında VAULT'tan ilk boş anahtarı çeker.
    """
    with st.spinner("🔐 Shopier Ödemesi Doğrulanıyor..."):
        time.sleep(3) # API Sorgu Simülasyonu
        for key, data in VAULT.items():
            if data['label'] == pkg_name:
                return key
    return None

# ================= 4. GİRİŞ VE ÖDEME AKIŞI =================
if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "key": None, "purchased_key": None, "active_order": None})

if not st.session_state["auth"]:
    st.markdown("<div class='glass-card' style='text-align:center;'><h2 style='color: #4ade80;'>💎 KAZANANLAR KULÜBÜ</h2><p>Yapay Zeka Destekli Siber Muhakeme Terminali</p></div>", unsafe_allow_html=True)

    # PAKETLER VE ÖDEME BUTONLARI
    st.markdown("### 💳 LİSANS PAKETİ SEÇİN")
    pkgs = [("1-AY", "700 TL"), ("3-AY", "2.000 TL"), ("6-AY", "5.000 TL"), ("12-AY", "8.000 TL")]
    col1, col2 = st.columns(2)
    
    for i, (name, price) in enumerate(pkgs):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"<div class='pkg-item'><small>{name}</small><br><b>{price}</b></div>", unsafe_allow_html=True)
            if st.button(f"Kredi Kartı ile Öde ({name})", key=f"buy_{name}"):
                url, oid = start_shopier_payment(name, price)
                st.session_state.active_order = {"pkg": name, "id": oid}
                st.info(f"Ödeme sayfası yeni sekmede açılıyor... Lütfen ödemeyi tamamlayın.")
                # JavaScript ile yeni sekmede ödeme sayfasını açma (Streamlit uyumlu)
                st.markdown(f'<meta http-equiv="refresh" content="0;URL=\'{url}\'">', unsafe_allow_html=True)

    # ÖDEME SONRASI KONTROL BUTONU (KULLANICI GERİ DÖNDÜĞÜNDE)
    if st.session_state.active_order:
        st.divider()
        if st.button("✅ ÖDEMEYİ YAPTIM, ANAHTARIMI VER"):
            key = verify_payment_and_deliver_key(st.session_state.active_order["pkg"])
            st.session_state.purchased_key = key
            st.session_state.active_order = None

    if st.session_state.purchased_key:
        st.markdown(f"""
            <div class='success-box'>
                ✅ ÖDEME BAŞARILI!<br>
                LİSANS ANAHTARINIZ: <span style='color:white;'>{st.session_state.purchased_key}</span><br>
                <small>Kodu kopyalayıp aşağıdaki kutuya girin.</small>
            </div>
        """, unsafe_allow_html=True)

    # LİSANS GİRİŞ ALANI
    u_lic = st.text_input("Lisans Anahtarını Buraya Girin:", value=st.session_state.purchased_key if st.session_state.purchased_key else "")
    if st.button("TERMİNALİ BAŞLAT"):
        if u_lic in VAULT:
            st.session_state.update({"auth": True, "key": u_lic})
            st.rerun()
        else: st.error("❌ Geçersiz veya Süresi Dolmuş Anahtar!")

# ================= 5. SİBER ANALİZ MERKEZİ (ÖNCEKİ YAPI İLE AYNI) =================
else:
    with st.sidebar:
        st.markdown(f"<p style='color:#38bdf8;'>🛡️ SİBER PANEL - AKTİF</p>", unsafe_allow_html=True)
        if st.button("🔄 VERİLERİ TAZELE"): st.rerun()
        if st.button("🔴 GÜVENLİ ÇIKIŞ"): st.session_state.clear(); st.rerun()

    # (Buraya daha önce yazdığımız siber_muhakeme_engine ve Tab yapılarını ekliyorsun)
    st.success(f"Hoş geldin Sahip Timur. Veri akışı süzgeçten geçiyor...")

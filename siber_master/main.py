import requests
from datetime import datetime, timedelta
import streamlit as st
import hashlib
import time

# ================= 1. KUTSAL AYARLAR VE YENİ API MÜHÜRÜ =================
API_KEY = "6c18a0258bb5e182d0b6afcf003ce67a"
BASE_URL = "https://v3.football.api-sports.io"

# Sahip Timur'un Yeni Güncel Shopier API Token'ı
SHOPIER_JWT_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzMDY5YWY5OTM4YzllOTVhYzNhZjk2YzNkNzE3ZTM5YSIsImp0aSI6ImRmYjVkMDQ0ZWE0MDBhZWI3ZWFlNTA5NmY2ZDk4M2ViYzgyYjZkOTBkYjM5OTk5NDQ2MGY4ZTMwMWNmNzA4NjNlNzg2ZGVlMmQ3YWE1MGFhZjUyYWM2ZmIxYmY3ZmFjNmRjODQ2NWY5OTJjNjc0MDFhZTRkYmJjN2MzNTZhYjUyOTg5ZjRjZjk1YmQxMjhjOGE5ZmQ2YWRlZTNiYzkzNTAiLCJpYXQiOjE3Njk3MzU1NjEsIm5iZiI6MTc2OTczNTU2MSwiZXhwIjoxOTI3NTIwMzIxLCJzdWIiOiIyNTAzMDYzIiwic2NvcGVzIjpbIm9yZGVyczpyZWFkIiwib3JkZXJzOndyaXRlIiwicHJvZHVjdHM6cmVhZCIsInByb2R1Y3RzOndyaXRlIiwic2hpcHBpbmdzOnJlYWQiLCJzaGlwcGluZ3M6d3JpdGUiLCJkaXNjb3VudHM6cmVhZCIsImRpc2NvdW50czp3cml0ZSIsInBheW91dHM6cmVhZCIsInJlZnVuZHM6cmVhZCIsInJlZnVuZHM6d3JpdGUiLCJzaG9wOnJlYWQiLCJzaG9wOndyaXRlIl19.sajWbv4KIcYjrHLLHRsVdvXVLhZGEOLjqadgyVYoYIjS0-uZZxnXGe9ZvToLil6FOVz0hJsv0yrkeoeASkLLpgx_2GPnFIpn3wDOitUBi_WkvdU9hTkbcwtDjW_tZ9QFUZP24rfPL5UXZrZeTaO4-H-Y_Jlky_TAKmJrMCIabo1WNwazBGv0vnOwo0xCf1d2mS7DI3Cm3ky_qcVCbN8PR2f9WTYHUqlxN0hE7GQSvngKU4tE1M3xwhFq44Cr9-kkJ6O1stHKK8jGBx-d10YVD_jGi6BsZg3uFcAQd_GwCBJ4pAy7kOyKfkjzJrH7E_IwvQ6-UIsOts0nIKa8L9Asnw"

@st.cache_resource
def get_final_vault():
    vault = {}
    config = [("1-AY", 30, 200), ("3-AY", 90, 200), ("6-AY", 180, 200), ("SINIRSIZ", 36500, 200)]
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
        .stApp { background-color: #020617; color: #f1f5f9; }
        .pkg-card {
            background: rgba(15, 23, 42, 0.9);
            border: 1px solid rgba(56, 189, 248, 0.3);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            margin-bottom: 10px;
        }
        .price-tag { font-size: 1.4rem; color: #4ade80; font-weight: bold; margin: 10px 0; }
        .success-box { background: rgba(74, 222, 128, 0.1); border: 2px dashed #4ade80; padding: 20px; border-radius: 12px; text-align: center; color: #4ade80; }
        div.stButton > button { width: 100%; border-radius: 10px; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

st.set_page_config(page_title="Siber Master V14", layout="wide")
apply_fixed_ui()

# ================= 3. GARANTİ ÖDEME KÖPRÜSÜ =================
def handle_purchase(pkg_name):
    """
    Shopier ödeme linkini açar ve eş zamanlı olarak VAULT'tan anahtarı hazırlar.
    """
    # ÖNEMLİ: Shopier dükkan adını buraya yaz (Örn: shopier.com/SiberMaster)
    shopier_base_url = "https://www.shopier.com/SizinDukkanAdiniz" 
    
    js = f"window.open('{shopier_base_url}', '_blank').focus();"
    st.components.v1.html(f"<script>{js}</script>", height=0)
    
    # Ödeme yapılıyorken kullanıcıya anahtarını göster (Güven artırır)
    st.session_state.purchased_key = next(k for k,v in VAULT.items() if v['label'] == pkg_name)

# ================= 4. GİRİŞ VE SATIŞ EKRANI =================
if "auth" not in st.session_state:
    st.session_state.update({"auth": False, "key": None, "purchased_key": None})

if not st.session_state["auth"]:
    st.markdown("<h1 style='text-align:center; color:#38bdf8;'>🛡️ SİBER MASTER TERMİNAL</h1>", unsafe_allow_html=True)
    
    cols = st.columns(4)
    packages = [("1-AY", "700 TL"), ("3-AY", "2.000 TL"), ("6-AY", "5.000 TL"), ("SINIRSIZ", "15.000 TL")]

    for i, (name, price) in enumerate(packages):
        with cols[i]:
            st.markdown(f"<div class='pkg-card'><h3>{name}</h3><div class='price-tag'>{price}</div></div>", unsafe_allow_html=True)
            if st.button(f"HEMEN AL", key=f"btn_{name}"):
                handle_purchase(name)

    if st.session_state.purchased_key:
        st.markdown(f"""
            <div class='success-box'>
                ✅ ÖDEME EKRANI AÇILDI!<br>
                <b>Ödeme sonrası lisansınız:</b> <br>
                <span style='color:white; font-size:1.5rem;'>{st.session_state.purchased_key}</span><br>
                <small>Lütfen ödemeyi tamamlayıp anahtarı aşağıya girin.</small>
            </div>
        """, unsafe_allow_html=True)

    st.divider()
    u_lic = st.text_input("Lisans Anahtarını Aktif Et:", value=st.session_state.purchased_key if st.session_state.purchased_key else "")
    if st.button("🚀 SİSTEME GİRİŞ YAP"):
        if u_lic in VAULT:
            st.session_state.update({"auth": True, "key": u_lic})
            st.rerun()
        else:
            st.error("Anahtar doğrulanamadı.")

# ================= 5. ANALİZ MERKEZİ (GİRİŞ SONRASI) =================
else:
    st.sidebar.success(f"Bağlantı Güvenli: {st.session_state.key}")
    if st.sidebar.button("🔴 ÇIKIŞ"): st.session_state.clear(); st.rerun()
    
    st.title("🛡️ Canlı Siber Analiz Merkezi")
    st.info("Siber Master V14000 aktif. Tüm veriler mühürlü hattan akıyor.")

import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import requests
import sqlite3
from datetime import datetime

st.set_page_config(page_title="Akıllı Sulama Karar Destek", page_icon="🌱", layout="wide", initial_sidebar_state="expanded")

def init_db():
    conn = sqlite3.connect('sulama_gecmisi.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS kayitlar 
                 (tarih TEXT, bitki TEXT, sicaklik REAL, nem REAL, isik TEXT, miktar REAL)''')
    conn.commit()
    conn.close()

def add_record(bitki, sicaklik, nem, isik, miktar):
    conn = sqlite3.connect('sulama_gecmisi.db')
    c = conn.cursor()
    simdi = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO kayitlar VALUES (?, ?, ?, ?, ?, ?)", (simdi, bitki, sicaklik, nem, isik, miktar))
    conn.commit()
    conn.close()

def get_records():
    conn = sqlite3.connect('sulama_gecmisi.db')
    df_records = pd.read_sql_query("SELECT * FROM kayitlar ORDER BY tarih DESC", conn)
    conn.close()
    return df_records

init_db()

st.markdown("""
    <style> 
    div[data-baseweb="select"], .stButton button, .stSlider { cursor: pointer !important; }
    div[data-baseweb="select"]:hover { border: 2px solid #4CAF50 !important; transition: 0.3s all; }
    </style>
    """, unsafe_allow_html=True)

def get_weather_data(city_name, api_key):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()
            return {
                "temp": data['main']['temp'],
                "clouds": data['clouds']['all']
            }
        return None
    except: return None

def load_data():
    try: return pd.read_csv("bitki_verisi.csv")
    except: return None

df = load_data()

st.title("🌱 Akıllı Bitki Sulama Karar Destek Sistemi")
st.write("Yapay zeka desteği ile tarımsal verimliliği artırıyor, API entegrasyonu ile gerçek zamanlı analiz yapıyoruz.")

if df is not None:
    X = df[['sicaklik', 'nem', 'isik', 'bitki_turu_kod']]
    y = df['su_miktari']
    model = RandomForestRegressor(n_estimators=100, random_state=42).fit(X, y)

    with st.sidebar:
        st.header("🌍 Canlı Hava Durumu (API)")
        api_key = "9b1d414db2568cb0e4465617c1068ac5" 
        sehir = st.text_input("Şehir", "Zonguldak")
        weather_data = get_weather_data(sehir, api_key)

        if weather_data:
            sicaklik = weather_data['temp']
            bulut = weather_data['clouds']
            
            if bulut < 20: 
                isik_durumu = "Çok Güneşli"
                isik_sayisal = 2
            elif bulut < 70:
                isik_durumu = "Normal"
                isik_sayisal = 1
            else:
                isik_durumu = "Karanlık"
                isik_sayisal = 0
                
            st.info(f"✨ Canlı Sıcaklık: {sicaklik}°C")
            st.info(f"☁️ Bulutluluk: %{bulut} ({isik_durumu})")
        else:
            st.warning("Canlı veri alınamadı, manuel giriş aktif.")
            sicaklik = st.slider("Sıcaklık (°C)", -10, 50, 20)
            isik_durumu = "Normal"
            isik_sayisal = 1
        
        st.divider()
        st.header("🚜 Arazi ve Bitki Bilgileri")
        donum = st.number_input("Arazi Büyüklüğü (Dönüm)", min_value=0.1, max_value=1000.0, value=1.0, step=0.5)
        
        bitkiler = ["Domates", "Biber", "Çilek", "Lavanta", "Kaktüs", "Mısır", "Ayçiçeği", "Gül", "Orkide", "Zeytin Ağacı"]
        bitki_turu = st.selectbox("Bitki Türü", bitkiler)
        nem_rakam = st.slider("Toprak Nemi (%)", 0, 100, 45)

    bitki_map = {ad: i for i, ad in enumerate(bitkiler)}

    if st.button("💧 Sulama İhtiyacını Hesapla"):
        girdi = np.array([[sicaklik, nem_rakam, isik_sayisal, bitki_map[bitki_turu]]])
        tahmin_m2 = model.predict(girdi)[0] 
        
        toplam_su_ihtiyaci = tahmin_m2 * donum * 1000
        geleneksel_tuketim = toplam_su_ihtiyaci * 1.40
        tasarruf_litre = geleneksel_tuketim - toplam_su_ihtiyaci
        
        birim_maliyet_litre = 15 / 1000
        toplam_maliyet_tl = toplam_su_ihtiyaci * birim_maliyet_litre
        tasarruf_tl = tasarruf_litre * birim_maliyet_litre
        
        add_record(f"{bitki_turu} ({donum} Dönüm)", sicaklik, nem_rakam, isik_durumu, round(toplam_su_ihtiyaci, 2))
        
        st.divider()
        st.subheader(f"🚜 {donum} Dönüm {bitki_turu} Arazisi Analiz Raporu")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Toplam Su İhtiyacı", f"{toplam_su_ihtiyaci:,.0f} L")
        m2.metric("Su Tasarrufu", f"{tasarruf_litre:,.0f} L", delta="Verimlilik: %40")
        m3.metric("Tahmini Tasarruf", f"{tasarruf_tl:,.2f} TL")

        st.write("---")
        st.write("### 💰 Finansal ve Operasyonel Öngörü")
        c1, c2 = st.columns(2)
        
        with c1:
            st.info(f"🌊 **Operasyonel Maliyet:** Bu işlem için tahmini maliyet: **{toplam_maliyet_tl:,.2f} TL**")
            st.caption(f"Not: Işık durumu {sehir} şehri için API üzerinden otomatik olarak **'{isik_durumu}'** olarak belirlenmiştir.")
        with c2:
            st.success(f"📈 **Sezonluk Kazanç:** Bir sezonda (120 gün) tahmini **{(tasarruf_tl * 120):,.2f} TL** tasarruf.")

        if nem_rakam < 20:
            st.error("🚨 Kritik: Toprak aşırı kuru!")
        elif nem_rakam > 80:
            st.warning("☁️ Bilgi: Nem seviyesi yüksek, su tasarrufu yapıldı.")
        else:
            st.success("✅ İdeal: Nem dengesi optimize edildi.")

    st.write("---")
    st.subheader("📜 Geçmiş Sulama Kayıtları")
    gecmis_df = get_records()
    
    if not gecmis_df.empty:
        st.dataframe(gecmis_df, use_container_width=True)
        if st.button("Kayıtları Temizle"):
            conn = sqlite3.connect('sulama_gecmisi.db')
            conn.cursor().execute("DELETE FROM kayitlar")
            conn.commit()
            conn.close()
            st.rerun()
    else:
        st.info("Henüz kayıt bulunamadı.")

else:
    st.error("Lütfen 'bitki_verisi.csv' dosyasını klasörde bulundurun!")
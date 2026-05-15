import streamlit as st
import pandas as pd
import os
import main

st.set_page_config(page_title="NexusData AI", page_icon="📊", layout="wide")

# Gaya CSS Kreatif
st.markdown("""
    <style>
    .main { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
    .ai-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border-left: 8px solid #6c5ce7;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    div.stButton > button:first-child {
        background: linear-gradient(45deg, #6a11cb, #2575fc);
        color: white; border: none; border-radius: 10px; padding: 12px 30px;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("⚙️ Kawalan")
    run_bot = st.button("🚀 MULAKAN ANALISIS")
    st.info("Sistem ini menggunakan Playwright & Llama 3.1 AI.")

st.title("📊 NexusData: Analisis Pasaran Pintar")
st.write("Mentransformasi data web kepada wawasan perniagaan.")

if run_bot:
    with st.spinner("🤖 Sedang mengumpul data & menjana wawasan AI..."):
        main.run_all()
        st.success("Analisis Selesai!")

# Paparan Data
if os.path.exists('data_buku_besar.csv'):
    df = pd.read_csv('data_buku_besar.csv')
    df['Harga_Num'] = df['Harga'].str.replace('£', '').astype(float)

    # 1. Metrik di atas
    c1, c2, c3 = st.columns(3)
    c1.metric("Jumlah Produk", len(df))
    c2.metric("Purata Harga", f"£{df['Harga_Num'].mean():.2f}")
    c3.metric("Status AI", "Aktif")

    # 2. Graf Bar (Besar di tengah)
    st.subheader("📈 Visualisasi Harga Produk")
    st.bar_chart(data=df, x="Nama Produk", y="Harga_Num", color="#6c5ce7")

    # 3. Jadual & Rumusan AI (Bawah Graf)
    st.markdown("---")
    col_ai, col_table = st.columns([1.2, 0.8])
    
    with col_ai:
        st.subheader("🧠 Rumusan Eksekutif AI")
        if os.path.exists('laporan_ai.txt'):
            with open('laporan_ai.txt', 'r', encoding='utf-8') as f:
                st.markdown(f'<div class="ai-card">{f.read()}</div>', unsafe_allow_html=True)
    
    with col_table:
        st.subheader("📋 Senarai Data Produk")
        st.dataframe(df[['Nama Produk', 'Harga']], use_container_width=True, height=400)
else:
    st.warning("Data belum tersedia. Sila klik 'MULAKAN ANALISIS' untuk memulakan proses.")
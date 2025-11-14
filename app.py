# Import library yang dibutuhkan
import streamlit as st
import pandas as pd
import altair as alt

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="Laporan Penjualan Karpet Aladdin Test V.1",
    page_icon=" carpet ",
    layout="wide" 
)

# --- Judul Aplikasi ---
st.title('  Aplikasi Laporan Penjualan Aladdin Karpet Test V.1  ')
st.write("Unggah file CSV penjualan Anda untuk melihat grafik omset secara otomatis.")

# --- 1. Widget Upload File ---
uploaded_file = st.file_uploader("Pilih file CSV Anda", type=["csv"])

# --- 2. Proses Jika File Sudah Diunggah ---
if uploaded_file is not None:
    try:
        # Baca file CSV (dengan pemisah titik koma)
        df = pd.read_csv(uploaded_file, delimiter=';')
        
        st.success("File berhasil diunggah dan dibaca!")
        st.write("Data (5 baris pertama):", df.head())
        
        # --- 3. Buat dan Tampilkan Grafik ---
        if 'CABANG' in df.columns and 'OMSET REAL' in df.columns and 'CLOSING REAL' in df.columns:
            
            # --- GRAFIK 1: BATANG OMSET REAL ---
            st.header('Grafik Omset Real per Cabang (Batang)')
            st.write("Direkomendasikan untuk membandingkan nilai antar cabang.")
            
            chart_omset_bar = alt.Chart(df).mark_bar().encode(
                x=alt.X('CABANG', sort='-y', title='Cabang'),
                y=alt.Y('OMSET REAL', title='Omset Real'),
                tooltip=['CABANG', 'OMSET REAL']
            ).properties(
                title='Grafik Omset Real per Cabang'
            ).interactive()
            
            # Tampilkan grafik
            st.altair_chart(chart_omset_bar, use_container_width=True)
            
            # --- GRAFIK 2: GARIS OMSET REAL ---
            st.header('Grafik Omset Real per Cabang (Garis)')
            st.write("Ini adalah diagram garis yang Anda minta.")
            
            chart_omset_line = alt.Chart(df).mark_line(point=True).encode(
                x=alt.X('CABANG', sort=None, title='Cabang'),
                y=alt.Y('OMSET REAL', title='Omset Real'),
                tooltip=['CABANG', 'OMSET REAL']
            ).properties(
                title='Grafik Omset Real per Cabang (Bentuk Garis)'
            ).interactive()
            
            # Tampilkan grafik
            st.altair_chart(chart_omset_line, use_container_width=True)

            # --- GRAFIK 3: BATANG CLOSING REAL ---
            st.header('Grafik Closing Real per Cabang (Batang)')
            st.write("Grafik ini menunjukkan jumlah closing (transaksi) per cabang.")
            
            chart_closing_bar = alt.Chart(df).mark_bar().encode(
                x=alt.X('CABANG', sort='-y', title='Cabang'),
                y=alt.Y('CLOSING REAL', title='Jumlah Closing'),
                tooltip=['CABANG', 'CLOSING REAL']
            ).properties(
                title='Grafik Closing Real per Cabang'
            ).interactive()
            
            # Tampilkan grafik
            st.altair_chart(chart_closing_bar, use_container_width=True)
            
            #  TOMBOL DOWNLOAD GABUNGAN ---
            st.header("Download Laporan")
            st.write("Tombol ini akan mengunduh satu file HTML yang berisi ketiga grafik di atas.")

            # 1. Gabungkan ketiga grafik secara vertikal
            combined_chart = alt.vconcat(
                chart_omset_bar,
                chart_omset_line,
                chart_closing_bar
            )
            
            # 2. Ubah grafik gabungan menjadi string HTML
            html_combined = combined_chart.to_html()
            
            # 3. Buat satu tombol download
            st.download_button(
                label=" Download SEMUA Grafik (HTML)",
                data=html_combined,
                file_name="laporan_grafik_gabungan.html",
                mime="text/html"
            )

        else:
            st.error("Error: File CSV Anda tidak memiliki kolom 'CABANG', 'OMSET REAL', atau 'CLOSING REAL'.")

    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file: {e}")

else:
    st.info("Silakan unggah file CSV untuk memulai.")
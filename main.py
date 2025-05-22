import pickle
import streamlit as st
import os
from streamlit_option_menu import option_menu

# Fungsi untuk memuat model
@st.cache_resource
def load_model():
    model_path = os.path.join("model", "random_forest10.pkl")
    with open(model_path, "rb") as f:
        return pickle.load(f)

# Halaman beranda
def show_home():
    st.title("Prediksi Penyakit Ginjal Kronis")

    # Layout 2 kolom: kiri untuk teks, kanan untuk gambar besar
    col1, col2 = st.columns([2, 1])  # Lebih besar untuk teks, kecil untuk gambar

    with col1:
        st.header("Tentang Aplikasi")
        st.write("Aplikasi ini menggunakan model machine learning (Random Forest) untuk memprediksi risiko penyakit ginjal kronis berdasarkan parameter klinis pasien.")
        
        st.header("Fitur Penting")
        st.write("5 fitur utama yang paling berpengaruh dalam prediksi:")
        st.write("- Hemoglobin")
        st.write("- Volume Sel Darah Merah (PCV)")
        st.write("- Kreatinin Serum")
        st.write("- Gravitasi Spesifik")
        st.write("- Jumlah Sel Darah Merah")
        
        st.header("Akurasi Model")
        st.write("Model mencapai akurasi 97.5% dengan skor F1 96.55% pada data uji")
        st.markdown("""
        | Metrik    | Nilai   |
        |-----------|---------|
        | Akurasi   | 97.5%   |
        | Presisi   | 100%    |
        | Recall    | 93.33%  |
        | F1-Score  | 96.55%  |
        """)

    with col2:
        try:
            image_path = os.path.join("img", "Ginjal.png")
            st.image(image_path, use_container_width=True)
        except FileNotFoundError:
            st.warning("Gambar ginjal tidak ditemukan!")



# Halaman prediksi
def show_prediction():
    st.title("Prediksi Penyakit Ginjal Kronis")
    st.write("Masukkan data pasien untuk memprediksi risiko penyakit ginjal kronis.")
    
    try:
        rf_model = load_model()
    except FileNotFoundError:
        st.error("Model tidak ditemukan!")
        return

    # Input data
    col1, col2 = st.columns(2)
    with col1:
        hemo = st.number_input('Hemoglobin (g/dL)', min_value=3.0, max_value=20.0, value=12.5)
        pcv = st.number_input('Packed Cell Volume (%)', min_value=10, max_value=60, value=40)
        sg = st.selectbox('Specific Gravity', options=[1.005, 1.010, 1.015, 1.020, 1.025], index=2)
        rc = st.number_input('Red Blood Cell Count (juta sel/µL)', min_value=2.0, max_value=8.0, value=4.5)
        al = st.number_input('Albumin (skala 0-4)', min_value=0, max_value=5, value=0)

    with col2:
        bgr = st.number_input('Blood Glucose Random (mg/dL)', min_value=40, max_value=500, value=100)
        bu = st.number_input('Blood Urea (mg/dL)', min_value=1.0, max_value=300.0, value=50.0)
        sod = st.number_input('Sodium (mEq/L)', min_value=100.0, max_value=160.0, value=135.0)
        su = st.number_input('Sugar (skala 0-5)', min_value=0, max_value=5, value=0)
        sc = st.number_input('Serum Creatinine (mg/dL)', min_value=0.4, max_value=20.0, value=1.2)

    

    
    # Tombol prediksi
    if st.button('Prediksi', type="primary"):
        input_data = [[hemo, pcv, sg, rc, al, bgr, bu, sod, su, sc]]
        
        try:
            prediction = rf_model.predict(input_data)
            proba = rf_model.predict_proba(input_data)[0][0] * 100
            
            st.subheader("Hasil Prediksi")
            if prediction[0] == 0:
                st.error("🛑 Hasil Positif: Terdeteksi Penyakit Ginjal Kronis")
                st.write(f"Tingkat Keyakinan Model: {proba:.1f}%")

            else:
                st.success("✅ Hasil Negatif: Tidak Tertedekti Penyakit Ginjal Kronis")
                st.write(f"Tingkat Keyakinan Model: {proba:.1f}%")

        except Exception as e:
            st.error(f"Terjadi kesalahan dalam prediksi: {str(e)}")

# Fungsi utama aplikasi
def main():
    st.set_page_config(
        page_title="Prediksi Ginjal Kronis",
        page_icon="⚕️",
        layout="wide"
    )
    
    try:
        image_path = os.path.join("img", "gambar_ginjal.png")
        st.image(image_path, width=100)
    except FileNotFoundError:
        st.warning("Gambar tidak ditemukan!")
    
    with st.sidebar:
        page = option_menu(
            "Menu Utama", 
            ["Beranda", "Prediksi"], 
            icons=["house", "clipboard-pulse"], 
            default_index=0
        )
    
    if page == "Beranda":
        show_home()
    elif page == "Prediksi":
        show_prediction()

if __name__ == "__main__":
    main()
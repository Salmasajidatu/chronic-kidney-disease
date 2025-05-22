import pickle
import streamlit as st
import os
from streamlit_option_menu import option_menu

# Fungsi untuk memuat model
@st.cache_resource
def load_model():
    model_path = os.path.join("model", "random_forest.pkl")
    with open(model_path, "rb") as f:
        return pickle.load(f)

# Halaman beranda
def show_home():
    st.title("Prediksi Penyakit Ginjal Kronis")
    
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

# Halaman prediksi
def show_prediction():
    st.title("Prediksi Penyakit Ginjal Kronis")
    
    st.header("Masukkan Data Pasien")


    try:
        rf_model = load_model()
    except FileNotFoundError:
        st.error("Model tidak ditemukan!")
        return

    # Input data
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input('Usia', min_value=1, max_value=100, value=50)
        bp = st.number_input('Tekanan Darah (mmHg)', min_value=50, max_value=200, value=80)
        sg = st.number_input('Gravitasi Spesifik', min_value=1.000, max_value=1.050, value=1.015)
        al = st.number_input('Albumin (0-4)', min_value=0, max_value=4, value=0)
        su = st.number_input('Gula (0-5)', min_value=0, max_value=5, value=0)
        rbc = st.selectbox('Sel Darah Merah', ['Normal', 'Tidak Normal'])
        pc = st.selectbox('Sel Nanah', ['Normal', 'Tidak Normal'])
        pcc = st.selectbox('Gumpalan Sel Nanah', ['Ada', 'Tidak'])
        ba = st.selectbox('Bakteri', ['Ada', 'Tidak'])
        bgr = st.number_input('Gula Darah Acak (mg/dL)', min_value=40, max_value=500, value=100)
        bu = st.number_input('Urea (mg/dL)', min_value=1.0, max_value=300.0, value=40.0)
        sc = st.number_input('Kreatinin Serum (mg/dL)', min_value=0.4, max_value=20.0, value=1.2)

    with col2:
        sod = st.number_input('Sodium (mEq/L)', min_value=100.0, max_value=160.0, value=135.0)
        pot = st.number_input('Kalium (mEq/L)', min_value=2.0, max_value=10.0, value=4.5)
        hemo = st.number_input('Hemoglobin (g/dL)', min_value=3.0, max_value=20.0, value=12.0)
        pcv = st.number_input('Packed Cell Volume (%)', min_value=10, max_value=60, value=40)
        wbcc = st.number_input('Jumlah Sel Darah Putih (per µL)', min_value=4000, max_value=20000, value=8000)
        rbcc = st.number_input('Jumlah Sel Darah Merah (juta/µL)', min_value=2.0, max_value=8.0, value=4.5)
        htn = st.selectbox('Hipertensi', ['Ya', 'Tidak'])
        dm = st.selectbox('Diabetes', ['Ya', 'Tidak'])
        cad = st.selectbox('Penyakit Jantung Koroner', ['Ya', 'Tidak'])
        appet = st.selectbox('Nafsu Makan', ['Baik', 'Buruk'])
        pe = st.selectbox('Edema Kaki', ['Ya', 'Tidak'])
        ane = st.selectbox('Anemia', ['Ya', 'Tidak'])
    
    # Preprocessing input
    rbc = 1 if rbc == 'Normal' else 0
    pc = 1 if pc == 'Normal' else 0
    pcc = 1 if pcc == 'Ada' else 0
    ba = 1 if ba == 'Ada' else 0
    htn = 1 if htn == 'Ya' else 0
    dm = 1 if dm == 'Ya' else 0
    cad = 1 if cad == 'Ya' else 0
    appet = 1 if appet == 'Baik' else 0
    pe = 1 if pe == 'Ya' else 0
    ane = 1 if ane == 'Ya' else 0

    
    # Tombol prediksi
    if st.button('Prediksi Sekarang', type="primary"):
        input_data = [[age, bp, sg, al, su,
                    rbc, pc, pcc, ba,
                    bgr, bu, sc, sod, pot,
                    hemo, pcv, wbcc, rbcc,
                    htn, dm, cad, appet, pe, ane
                ]]
        
        try:
            prediction = rf_model.predict(input_data)
            proba = rf_model.predict_proba(input_data)[0][0] * 100
            
            st.subheader("Hasil Prediksi")
            if prediction[0] == 0:
                st.error("🛑 Resiko Tinggi: Kemungkinan gangguan ginjal terdeteksi")
                st.write(f"Tingkat Keyakinan Model: {proba:.1f}%")
                st.write("Rekomendasi: Segera konsultasi dengan dokter spesialis ginjal")
            else:
                st.success("✅ Hasil Normal: Tidak terdeteksi masalah ginjal")
                st.write(f"Tingkat Keyakinan Model: {proba:.1f}%")
                st.write("Saran: Pertahankan pola hidup sehat dan cek rutin")
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
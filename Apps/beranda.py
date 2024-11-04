import streamlit as st
import pandas as pd
pd.set_option('colheader_justify', 'center')
import mysql.connector as mysql
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import time
from PIL import Image
from streamlit_extras.stylable_container import stylable_container

def app():
    st.title("KBLI Corrector AI")

    with stylable_container(
			key="container_with_border",
			css_styles="""
				{
					border: 1px solid rgba(49, 51, 63, 0.2);
					border-radius: 0.5rem;
					padding: calc(1em - 1px);
					background-color: #d7b06d;
				}
				""",
		):
			
        st.markdown(f'''
            ### Apa itu **KBLI Corrector AI**?
            
            
            **KBLI Corrector AI** adalah sistem atau alat berbasis kecerdasan buatan yang dirancang untuk membantu pengguna **memastikan bahwa kode KBLI (Klasifikasi Baku Lapangan Usaha Indonesia) yang mereka gunakan sudah benar dan relevan dengan jenis usaha atau kegiatan tertentu**. KBLI Corrector AI dapat memeriksa keakuratan kode KBLI, merekomendasikan perbaikan jika terjadi ketidaksesuaian, dan memberikan saran kode yang lebih tepat berdasarkan deskripsi atau informasi terkait bidang usaha yang diinput pengguna.
            
            Dalam konteks konsultasi atau pemetaan kode, KBLI Corrector AI membantu:
            1. **Memastikan Konsistensi Kode**: Menilai apakah kode yang digunakan sesuai dengan kegiatan usaha yang diuraikan.
            2. **Menyarankan Koreksi atau Alternatif**: Memberikan rekomendasi untuk kode KBLI yang lebih akurat.
            3. **Mempermudah Penelusuran Kode**: Mengotomatiskan pencarian KBLI yang tepat, sehingga pengguna tidak perlu mencari secara manual.

           Kami berharap *tools* ini akan bermanfaat bagi bisnis, konsultan, dan lembaga pemerintah yang memerlukan klasifikasi usaha yang tepat untuk keperluan administratif, pajak, dan perizinan.
        ''')

import pandas as pd
import streamlit as st
import sqlalchemy
from sqlalchemy.pool import NullPool
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
import io
from Apps import upload
from streamlit_option_menu import option_menu
from Apps import dashboard, beranda, chatbot
from PIL import Image
import streamlit as st

logo = Image.open('Media\logo.png')

st.set_page_config(
    page_title="KBLI CorrectorAI",
    page_icon=logo,
    layout="wide",
    initial_sidebar_state="expanded",
)

# Remove Whitespace
st.markdown(
    """
  <style>
    div.block-container{
        padding-top:2rem;
    }
  </style>
""",
    unsafe_allow_html=True,
)

# MENU
with st.sidebar:

    cc1, cc2 = st.columns(2)

    cc1.image("Media\logo.png", use_column_width=True)
    cc2.image("Media\logo_kemenkeu.png", use_column_width=True)

    selected = option_menu(
                menu_title=None,
                # menu_icon='file-earmark-medical',
                default_index=0,
                # orientation='horizontal',
                options = ['Beranda', 'Konsultan CorrectorAI', 'Koreksi KBLI dan Harga Pengadaan', 'Dashboard'],
                icons = ['house', 'chat-dots', 'bounding-box', 'clipboard-data']
            )
    
    video_file = open('Media/abu2.mp4', 'rb')
    video_bytes = video_file.read()

    st.video(video_bytes, autoplay=True, muted=False, loop=False, )

    # st.image('media/BPJS_nobg.png', use_column_width=True)

if selected == 'Dashboard':
    dashboard.app()
if selected == 'Beranda':
    beranda.app()
if selected == 'Konsultan CorrectorAI':
    chatbot.app()
if selected == 'Koreksi KBLI dan Harga Pengadaan':
    upload.app()

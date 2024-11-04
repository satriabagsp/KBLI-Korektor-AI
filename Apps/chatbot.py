import streamlit as st
import pandas as pd
pd.set_option('colheader_justify', 'center')
import mysql.connector as mysql
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from openai import OpenAI
import streamlit_pills as stp
from streamlit_pills import pills

def app():
	st.title("Konsultan Corrector AI")

	st.info('''

            Pada halaman ini, Anda dapat berinteraksi dengan Chatbot AI kami untuk mempermudah pencarian kode KBLI dan KBKI. Cukup masukkan bidang usaha atau barang yang ingin Anda ketahui, dan kami akan membantu menemukan kode yang sesuai. Selain itu, chatbot ini juga siap memberikan perkiraan harga pasar sebagai referensi dalam menetapkan Harga Standar Penetapan Kegiatan (HSPK) untuk kebutuhan pengadaan.


            Mulailah percakapan untuk mendapatkan informasi yang cepat, akurat, dan relevan dengan kebutuhan Anda dalam proses pengadaan!
        ''')

	# Set OpenAI API key from Streamlit secrets
	client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

	if "openai_model" not in st.session_state:
		st.session_state["openai_model"] = "gpt-4"

	if "messages" not in st.session_state:
		st.session_state.messages = []

	for message in st.session_state.messages:
		with st.chat_message(message["role"]):
			st.markdown(message["content"].replace('ICD-10 Coding Expert: ',''))

	if prompt := st.chat_input("Apa yang ingin anda tanyakan terkait pencarian kode KBLI dan KBKI?", ):
		st.session_state.messages.append({"role": "user", "content": f"klasifikator KBLI dan KBKI expert: {prompt}"})
		with st.chat_message("user"):
			st.markdown(prompt)

		with st.chat_message("assistant"):
			stream = client.chat.completions.create(
				model=st.session_state["openai_model"],
				messages=[
					{"role": m["role"], "content": m["content"]}
					for m in st.session_state.messages
				],
				stream=True,
				# max_tokens=200
			)
			response = st.write_stream(stream)
		st.session_state.messages.append({"role": "assistant", "content": response})
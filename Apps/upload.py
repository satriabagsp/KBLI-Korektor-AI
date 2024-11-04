import streamlit as st
import pandas as pd
import numpy as np
# import requests
import time
from stqdm import stqdm
import json
import re
# from langflow.load import run_flow_from_json
# import pysqlite3
from PIL import Image

def call_langflow_api(csv_string):
	TWEAKS = {
		"ChatInput-7ylKj": {
			"files": "",
			"sender": "User",
			"sender_name": "User",
			"session_id": "",
			"should_store_message": True
		},
		"ChatOutput-mLw2g": {
			"data_template": "{text}",
			"input_value": "",
			"sender": "Machine",
			"sender_name": "AI",
			"session_id": "",
			"should_store_message": True
		},
		"Prompt-kfKaN": {
			"template": "Context:\n{konteks}\n\nTugas Anda adalah mengambil input yang terdiri dari ID, diagnosis, dan gejala, kemudian melakukan pencarian pada dokumen referensi untuk menemukan kode ICD-10 dan ICD-9 yang relevan. Jika terdapat lebih dari satu kemungkinan, berikan semua hasil yang mungkin. fokus pencarian dengan melihat diagnosis terlebih dahulu, setelah itu ke symptom. jika tidak sesuai dengan diagnosis, abaikan hasil. berikan probabilitas berdasarkan kecocokan pencarian. pastikan kolom Probability ada meskipun hasil tidak ditemukan. probabilitas merupakan angka 0 sampai 1, dan 2 digit dibelakang koma.\n\nGunakan format JSON berikut untuk setiap baris:\n\n  \"ICD-10\": \"<ICD-10 code>\",\n  \"ICD-9\": \"<ICD-9 code>\",\n  \"Procedure\": \"<Procedure>\",\n  \"Probability\": \"<Probability>\"\n\nPastikan informasinya sesuai konteks. jangan menambahkan atau mengurangi. Jika diluar konteks, kosongkan saja isiannya. Gunakan format di atas untuk memproses data berikut:\n{pertanyaan}",
			"pertanyaan": "",
			"konteks": ""
		},
		"Chroma-UKvLk": {
			"allow_duplicates": False,
			"chroma_server_cors_allow_origins": "",
			"chroma_server_grpc_port": None,
			"chroma_server_host": "",
			"chroma_server_http_port": None,
			"chroma_server_ssl_enabled": False,
			"collection_name": "ICD10",
			"limit": None,
			"number_of_results": 10,
			"persist_directory": "database/chroma-gpt",
			"search_query": "",
			"search_type": "Similarity"
		},
		"ParseData-EmU6G": {
			"sep": "\n",
			"template": "{text}"
		},
		"OpenAIModel-hgB7u": {
			"api_key": "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",
			"input_value": "",
			"json_mode": False,
			"max_tokens": None,
			"model_kwargs": {},
			"model_name": "gpt-4o-mini",
			"openai_api_base": "",
			"output_schema": {},
			"seed": 1,
			"stream": False,
			"system_message": "",
			"temperature": 0
		},
		"OpenAIEmbeddings-Eqx4O": {
			"chunk_size": 1000,
			"client": "",
			"default_headers": {},
			"default_query": {},
			"deployment": "",
			"dimensions": None,
			"embedding_ctx_length": 1536,
			"max_retries": 3,
			"model": "text-embedding-3-small",
			"model_kwargs": {},
			"openai_api_base": "",
			"openai_api_key": "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",
			"openai_api_type": "",
			"openai_api_version": "",
			"openai_organization": "",
			"openai_proxy": "",
			"request_timeout": None,
			"show_progress_bar": False,
			"skip_empty": False,
			"tiktoken_enable": True,
			"tiktoken_model_name": ""
		}
	}
	
	result = run_flow_from_json(flow="ChatGPT-File-Upload.json",
								input_value=csv_string,
								session_id="", # provide a session id if you want to use session state
								fallback_to_env_vars=True, # False by default
								tweaks=TWEAKS)

	return result

def ekstrak(langflow_result):
		
	res = langflow_result[0].outputs[0].results['message'].data['text']
	
	teks = res.replace("`", "")
	teks = teks.replace("json", "")
	teks = teks.replace("\n", "")
	teks = re.sub(' +', ' ', teks)
	
	teks = json.loads(teks)
	teks = pd.DataFrame(teks)
	
	teks['Probability'] = teks['Probability'].astype('float16')
	
	teks = teks.iloc[np.argmax(teks.Probability),:]
	return teks


def app():
	st.title("Koreksi KBLI dan Harga Pengadaan")

	st.info('''

            Di halaman ini, Anda dapat mengunggah file yang berisi informasi mengenai bidang usaha atau barang yang diperlukan untuk memudahkan proses pencarian kode KBLI dan KBKI.
			Cukup unggah file dalam format yang sesuai, dan sistem kami akan membantu mengidentifikasi kode KBLI atau KBKI yang relevan berdasarkan data yang Anda berikan. Selain itu, kami dapat memberikan perkiraan harga pasar sebagai referensi dalam menetapkan Harga Standar Penetapan Kegiatan (HSPK) untuk kebutuhan pengadaan Anda.
	 
        ''')
	
	uploaded_file = st.file_uploader("Unggah file ***xlsx**:", type=["xlsx"])

	if uploaded_file:
		# Membaca file XLSX yang diunggah
		df = pd.read_excel(uploaded_file)
		
		st.write(f"Data yang anda unggah ({len(df)} baris data):")
		st.dataframe(df, use_container_width=True, hide_index=True)

		# Memilih kolom untuk diagnosis dan symptom
		columns = df.columns.tolist()

		c1, c2 = st.columns(2)
		diagnosis_column = c1.selectbox("Pilih data berisi informasi **Kegiatan Usaha**:", columns)
		symptom_column = c2.selectbox("Pilih data berisi informasi **Produk Usaha**:", columns)

		df['idx'] = range(0, len(df))

		# Menampilkan data berdasarkan kolom yang dipilih
		if diagnosis_column and symptom_column:
			selected_data = df[[diagnosis_column, symptom_column]]
			selected_data.columns = ["kegiatan usaha", "produk usaha"]
			st.write("Data dengan kolom Diagnosis dan Symptom:")
			st.dataframe(selected_data, use_container_width=True, hide_index=True)

			if st.button("Gunakan AI"):
				output = []

				row_data = stqdm(selected_data.itertuples(), total=len(selected_data))
				
				for baris in row_data:
					row_data.set_description(f"Analisis {baris.diagnosis}")
					teks = f"""Diagnosis:\n {baris.diagnosis} \n Symptom:\n {baris.symptom}"""
					result = call_langflow_api(teks)
					output.append(ekstrak(result)) 

				output = pd.DataFrame(output)
				output['idx'] = range(0, len(output))
				final_output = pd.merge(df, output, on='idx', how='inner')
				final_output.to_excel('output/result.xlsx')
				st.dataframe(final_output)
				st.write("output telah tersimpan di ./output/result.xlsx")
							
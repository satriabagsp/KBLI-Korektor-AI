import streamlit as st
import pandas as pd
pd.set_option('colheader_justify', 'center')
import mysql.connector as mysql
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import matplotlib.pyplot as plt
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import geopandas as gpd
from shapely.geometry import box
import numpy as np
from shapely.geometry import Point

def app():
    st.title("Analisis Kesesuaian Klasifikasi")

    # DF 
    df = pd.read_excel('Data\data_dashboard_kemenkeu.xlsx')
    # df = df.fillna(0)

    # GDF
    gdf = gpd.read_file('Data/Provinsi Indonesia/provinsi.shp')
    gdf['kdprov'] = gdf['kdprov'] + '00'
    gdf = gdf[['kdprov', 'geometry']]

    # st.write(df.columns)

    # Pilihan kategori dan subkategori
    pil_1, pil_2, pil_3, pil_4 = st.columns(4)

    # Pilih wilayah
    list_provinsi = ['NASIONAL'] + df.nmprov.drop_duplicates().to_list()
    with pil_1:
        wilayah = st.selectbox(
            'Pilih Wilayah',
            list_provinsi)
        
        if wilayah != 'NASIONAL':
            df = df[df.nmprov == wilayah].reset_index(drop=True)

    # Pilih Jenis Pengadaan
    list_pengadaan = ['Semua Jenis'] + df['Jenis Pengadaan'].drop_duplicates().to_list()
    with pil_2:
        jenis_pengadaan = st.selectbox(
            'Pilih Jenis Pengadaan',
            list_pengadaan)
        
        if jenis_pengadaan != 'Semua Jenis':
            df = df[df['Jenis Pengadaan'] == jenis_pengadaan].reset_index(drop=True)

    # Pilih Mekanisme
    list_mekanisme = ['Semua Mekanisme'] + df['Mekanisme Pengadaan'].drop_duplicates().to_list()
    with pil_3:
        mekanisme = st.selectbox(
            'Pilih Mekanisme Pengadaan',
            list_mekanisme)
        
        if mekanisme != 'Semua Mekanisme':
            df = df[df['Mekanisme Pengadaan'] == mekanisme].reset_index(drop=True)

    # Pilih Potensi Kerugian
    list_potensi = ['Semua Potensi Kerugian'] + df['Potensi Kerugian Negara'].drop_duplicates().to_list()
    with pil_4:
        potensi = st.selectbox(
            'Pilih Potensi Kerugian',
            list_potensi)
        
        if potensi != 'Semua Potensi Kerugian':
            df = df[df['Potensi Kerugian Negara'] == potensi].reset_index(drop=True)

    
    # st.dataframe(df)


    grf_1, grf_2 = st.columns([1.2,2.8])

    with grf_1:
        # KBLI
        jml_kbli_sesuai = df['KBLI Sesuai'].sum()
        jml_kbli_tidak_sesuai = df['KBLI Tidak Sesuai'].sum()

        # st.write(jml_10_tidak_sesuai)
        fig_kbli = px.pie(
                        values=[jml_kbli_sesuai,jml_kbli_tidak_sesuai], 
                        names=['Sesuai','Tidak Sesuai'],
                        color_discrete_sequence=px.colors.qualitative.Antique,
                    )

        fig_kbli.update_traces(textposition='inside', textinfo='percent+label')
        
        fig_kbli.update_layout(showlegend=False)
        # fig_pie.update_layout(legend_traceorder="alphabetical")

        fig_kbli.update_layout(
            autosize=True,
            width=300,
            height=250,
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0,
                pad=0
            ),
            paper_bgcolor="#f0f0f5",
        )

        st.write(f'**Persentase Kesesuaian KBLI**')
        st.plotly_chart(fig_kbli, use_container_width=True)

        st.write('')
        # KBKI
        jml_kbki_sesuai = df['KBKI Sesuai'].sum()
        jml_kbki_tidak_sesuai = df['KBKI Tidak Sesuai'].sum()

        # st.write(jml_10_tidak_sesuai)
        fig_kbki = px.pie(
                        values=[jml_kbki_sesuai,jml_kbki_tidak_sesuai], 
                        names=['Sesuai','Tidak Sesuai'],
                        color_discrete_sequence=px.colors.qualitative.Antique,)

        fig_kbki.update_traces(textposition='inside', textinfo='percent+label')
        
        fig_kbki.update_layout(showlegend=False)
        # fig_pie.update_layout(legend_traceorder="alphabetical")

        fig_kbki.update_layout(
            autosize=True,
            width=300,
            height=250,
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0,
                pad=0
            ),
            paper_bgcolor="#f0f0f5",
        )

        st.write(f'**Persentase Kesesuaian Kode KBKI**')
        st.plotly_chart(fig_kbki, use_container_width=True)


    with grf_2:
        # DF Provinsi
        df['idkab'] = df['idkab'].astype(str)
        df['kdprov'] = df['idkab'].str[0:2] + '00'

        df_prov = df.groupby(by=['kdprov','nmprov'], as_index=False).agg(jumlah_sesuai=('KBLI Sesuai','sum'), jumlah_tidak_sesuai=('KBLI Tidak Sesuai','sum'), selisih=('Selisih Biaya Pengadaan','sum'))
        df_prov['Persentase KBLI'] = df_prov['jumlah_sesuai'] / (df_prov['jumlah_sesuai'] + df_prov['jumlah_tidak_sesuai']) *100
        df_prov = df_prov.drop(columns=['jumlah_sesuai','jumlah_tidak_sesuai'])

        df_prov = df_prov.merge(gdf, on='kdprov', how='left')
        df_prov = gpd.GeoDataFrame(df_prov, geometry="geometry")
        # .drop_duplicates(subset=['kdprov'], keep='first').reset_index(drop=True)

        # st.write(df_prov)

       # Get center
        bounds = df_prov.total_bounds 
        polygon = box(*bounds)

        lat = polygon.centroid.y
        lon = polygon.centroid.x
        max_bound = max(abs(bounds[2] - bounds[0]), abs(bounds[3] - bounds[1])) * 111
        zoom = 12.3 - np.log(max_bound)

        fig2 = px.choropleth_mapbox(
			df_prov,
			geojson = df_prov.geometry, 
			locations = df_prov.index,
			color = df_prov['Persentase KBLI'],
            color_continuous_scale = 'Brwnyl',
			mapbox_style="carto-positron",
			# mapbox_style="open-street-map",
            # color_discrete_sequence=px.colors.qualitative.Antique,
			center={"lat": lat, "lon": lon},
			zoom=zoom,
			opacity=0.8,
			hover_name="nmprov",
			height=300,
			# hover_data={'Persentase ICD-10':True, 'nmprov':True},
			# labels={'nmkab':'Kabupaten/kota', 'vul_idx':'Vulnerability Index', 'adap_index':'Adaptive Index', 'expo_index':'Exposure Index', 'sensi_inde':'Sensitivity Index'}
		)

        fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        fig2.update(layout_coloraxis_showscale=False)
        
        st.write(f'**Sebaran Persentase Kesesuaian KBLI**')
        st.plotly_chart(fig2, use_container_width=True)

        # st.write(df_prov)

        # BAR
        df_prov = df_prov.rename(columns={'nmprov':'Provinsi','selisih':'Selisih Biaya Pengadaan'})
        bar = px.bar(df_prov, 
                        x = 'Provinsi', 
                        y = 'Selisih Biaya Pengadaan',
                        
                        color_discrete_sequence=px.colors.qualitative.Antique 
                    #  orientation='h', 
                        # text = periode,
                        # color='nmprov',   # if values in column z = 'some_group' and 'some_other_group'
                        # color_discrete_sequence=color_discrete_sequence,
                    )

        bar.update_traces(textposition='outside')

        bar.update_layout(
            autosize=True,
            # width=500,
            height=300,
            margin=dict(
                l=0,
                r=10,
                b=20,
                t=10,
                pad=2
            ),
            # paper_bgcolor="#e0e0ef",
        )
        # # fig.update_layout(hovermode="x unified")
        bar.update_layout(showlegend=False)

        st.write(f'**Selisih Ketidaksesuaian Biaya Pengadaan menurut Provinsi**')
        st.plotly_chart(bar, use_container_width=True)

        

    #     # st.dataframe(df_prov)

    
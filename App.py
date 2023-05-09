import streamlit as st
import pandas as pd
import base64
from io import StringIO

def process_file(file, pesos=False):
    df = pd.read_excel(file, engine='openpyxl')
    output = StringIO()

    for _, fila in df.iterrows():
        cbu = str(fila['CBU'])
        cuit = str(int(fila['CUIT']))
        nombre = str(fila['NOMBRE'])
        importe = str(fila['IMPORTE'])

        if pesos:
            registro = f'DL2;300100000000468;{cbu};;{cuit};{nombre};{importe};VAR;N;N;TRANSF COHEN;\r\n'
        else:
            registro = f'DR2;900100000102553;{cbu};;{cuit};{nombre};{importe};VAR;N;N;TRANSF COHEN;\r\n'

        output.write(registro)

    output.seek(0)
    return output.getvalue()

def get_download_link(text, filename):
    b64 = base64.b64encode(text.encode()).decode()
    return f'<a href="data:text/plain;base64,{b64}" download="{filename}">Descargar archivo TXT</a>'

st.title('Generador de archivos de reinversión para tesorería')
uploaded_file = st.file_uploader("Sube tu archivo Excel", type=['xlsx'])

if uploaded_file is not None:
    st.subheader('Generador de archivo de reinversion DÓLARES para tesorería')
    processed_file = process_file(uploaded_file, pesos=False)
    download_link = get_download_link(processed_file, 'salida_dolares.txt')
    st.markdown(download_link, unsafe_allow_html=True)

    st.subheader('Generador de archivo de reinversion PESOS para tesorería')
    processed_file_pesos = process_file(uploaded_file, pesos=True)
    download_link_pesos = get_download_link(processed_file_pesos, 'salida_pesos.txt')
    st.markdown(download_link_pesos, unsafe_allow_html=True)

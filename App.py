import streamlit as st
import pandas as pd
import base64
from io import StringIO

def process_file(file):
    df = pd.read_excel(file, engine='openpyxl')
    output = StringIO()

    for _, fila in df.iterrows():
        cbu = str(int(fila['CBU']))
        cuit = str(int(fila['CUIT']))
        nombre = str(fila['NOMBRE'])
        importe = str(fila['IMPORTE'])

        registro = f'DR2;900100000102553;{cbu};;{cuit};{nombre};{importe};VAR;N;N;TRANSF COHEN;\r\n'
        output.write(registro)

    output.seek(0)
    return output.getvalue()

def get_download_link(text, filename):
    b64 = base64.b64encode(text.encode()).decode()
    return f'<a href="data:text/plain;base64,{b64}" download="{filename}">Descargar archivo TXT</a>'

st.title('Generador de archivo de reinversion DOLARES para tesoreria')
uploaded_file = st.file_uploader("Sube tu archivo Excel", type=['xlsx'])

if uploaded_file is not None:
    processed_file = process_file(uploaded_file)
    download_link = get_download_link(processed_file, 'salida.txt')
    st.markdown(download_link, unsafe_allow_html=True)

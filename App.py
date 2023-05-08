import streamlit as st
import pandas as pd
from io import StringIO

def process_file(file):
    df = pd.read_excel(file, engine='openpyxl')
    output = StringIO()

    for _, fila in df.iterrows():
        cbu = str(int(fila['CBU']))
        cuit = str(int(fila['CUIT']))
        nombre = str(fila['NOMBRE'])
        importe = str(fila['IMPORTE'])

        registro = f'DR2;900100000102553;{cbu};;{cuit};{nombre};{importe};VAR;N;N;TRANSF COHEN;\n'
        output.write(registro)

    output.seek(0)
    return output

st.title('Generador de Archivo TXT desde Excel')
uploaded_file = st.file_uploader("Sube tu archivo Excel", type=['xlsx'])

if uploaded_file is not None:
    processed_file = process_file(uploaded_file)
    st.download_button(
        label="Descargar archivo TXT",
        data=processed_file,
        file_name="salida.txt",
        mime="text/plain",
    )

import streamlit as st
import pandas as pd
import base64
from io import StringIO
from datetime import datetime
from pandas import ExcelWriter
import uuid
import re


def process_file(file, pesos=False):
    # ...
    # (El contenido de la función process_file no ha cambiado)


def get_download_link(text, filename):
    # ...
    # (El contenido de la función get_download_link no ha cambiado)


def download_button(object_to_download, download_filename, button_text, pickle_it=False):
    # ...
    # (El contenido de la función download_button no ha cambiado)


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

    # Nueva sección: Reinversión Títulos
    st.subheader("Reinversión Títulos")
    reinv = st.file_uploader("Sube tu archivo Excel para Reinversión Títulos", type=['xlsx'])

    if reinv:
        # El código adicional proporcionado empieza aquí
        columnas = ['Comitente Número','Moneda','Importe']
        # ...
        # (El resto del código adicional se mantiene sin cambios)

        ################################ EXCEL PREPARACION #############################

        # ...
        # (Continúa con el código adicional proporcionado sin cambios)

        # ...
        # (El resto del código adicional se mantiene sin cambios)

        ################################ EXCEL PREPARACION #############################
        
        # ...
        # (Continúa con el código adicional proporcionado sin cambios)

        tablero = pd.read_excel(reinv, usecols=columnas, engine='openpyxl')
        tablero_xls = pd.read_excel(reinv,engine='openpyxl')
        comit = tablero['Comitente Número']
        # st.text(comit)

        st.dataframe(tablero)
        # st.table(tablero)
    
        ################################ EXCEL PREPARACION #############################
        
        def crearSheet(archivo):
            archivo = archivo
            # print(archivo)

            sheet = {'Fecha Concertacion':[],
                      'Fecha Vencimiento':[],
                      'Cuenta':[],
                      'Concepto':[],
                      'Debe':[],
                      'Haber':[],
                      'Contraparte - Custodia':[],
                      'Contraparte - Depositante':[],
                      'Contraparte - Cuenta':[]}
    
            for num in archivo.index:
                # print(num)
                
                fecha = datetime.now()
                fecha = fecha.strftime("%d/%m/%Y")

                sheet['Fecha Concertacion'].append(fecha)         
                sheet['Fecha Vencimiento'].append(fecha)         
                sheet['Cuenta'].append(archivo['Comitente Número'][num])         
                sheet['Concepto'].append(archivo['Tipo'][num])        
                sheet['Debe'].append('0,00')         
                sheet['Haber'].append(archivo['Importe'][num])
                sheet['Contraparte - Custodia'].append('CAJAVAL')
                sheet['Contraparte - Depositante'].append('0046')
                sheet['Contraparte - Cuenta'].append(archivo['Comitente Número'][num])

            sheet = pd.DataFrame(sheet)
            return sheet            

        moneda_7000 = tablero_xls['Moneda'] == 'Dolar Renta Exterior - 7.000' 
        moneda_10000 = tablero_xls['Moneda'] == 'Dolar Renta Local - 10.000'
        moneda_8000 = tablero_xls['Moneda'] == 'Pesos Renta - 8.000'
        nuevo7000 = tablero_xls[moneda_7000]
        nuevo10000 = tablero_xls[moneda_10000]
        nuevo8000 = tablero_xls[moneda_8000]

        reinversion_xls = nuevo7000.append(nuevo10000)
        reinversion_xls = reinversion_xls.append(nuevo8000)
      
        reinversion_xls = reinversion_xls.reindex(columns=['Número','Comitente Descripción','Fecha','Moneda','Comitente Número',
            'Importe','Tipo','Banco','Tipo de Cuenta','Sucursal','Cuenta','CBU','Tipo de identificador impositivo','Número de identificador impositivo',
            'Titular','Estado'])

        sheet_7000 = crearSheet(nuevo7000.set_index('Número'))
        sheet_10000 = crearSheet(nuevo10000.set_index('Número'))
        sheet_8000 = crearSheet(nuevo8000.set_index('Número'))

        with ExcelWriter('REINVERSION_FECHA.xlsx') as writer:
            reinversion_xls.to_excel(writer,sheet_name='Sheet1',index=False)
            sheet_7000.to_excel(writer,sheet_name='7000',index=False)  
            sheet_10000.to_excel(writer,sheet_name='10000',index=False)  
            sheet_8000.to_excel(writer,sheet_name='8000',index=False)  
        
        control_file = 'REINVERSION_FECHA.xlsx'
        with open(control_file, 'rb') as f:
            s = f.read()

        download_button_str = download_button(s, control_file, f'EXCEL LISTO {control_file}')
        st.markdown(download_button_str, unsafe_allow_html=True)
        # ...
        # (El resto del código adicional se mantiene sin cambios)

        ################################ EXCEL PREPARACION #############################
        
        # ...
        # (Continúa con el código adicional proporcionado sin cambios)

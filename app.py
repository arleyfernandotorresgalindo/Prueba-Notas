import streamlit as st
import pandas as pd
import requests
from io import BytesIO

# OneDrive public link (replace with your actual link)
#EXCEL_URL = "https://uexternadoedu-my.sharepoint.com/personal/arley_torres_uexternado_edu_co/EWLkjJhxRxBBrJaydePdva4Bnz4Z8JyRwg65IqooLIWu3A?download=1"
EXCEL_URL = 'output1.xlsx'

#response = requests.get(EXCEL_URL)
#file_bytes = BytesIO(response.content)

@st.cache_data
def load_data(url):
    try:
        df1 = pd.read_excel(url, sheet_name=None, engine="openpyxl")
        return df1
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Load data
df1 = load_data(EXCEL_URL)

st.title("Consulta De Calificaciones 2025-01")

# User inputs
materia = st.selectbox('Elegir su materia', ['Precálculo', 'Programación 2', 'Estructura de datos'])
email = st.text_input("Ingrese su correo electrónico:")
student_id = st.text_input("Ingrese su número de documento:")
df = df1[materia]

if st.button("Consultar"):
    if not email or not student_id:
        st.warning("Por favor, ingrese ambos valores.")
    else:
        student_data = df[(df["Correo"].str.contains(email, case = False)) & (df["Nro.Documento"] == int(student_id))]

        if not student_data.empty:
            st.success("Calificaciones encontradas:")
            st.write(student_data)
        else:
            st.error("No se encontraron calificaciones con estos datos.")

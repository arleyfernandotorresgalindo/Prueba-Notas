import streamlit as st
import pandas as pd

# OneDrive public link (replace with your actual link)
EXCEL_URL = "https://uexternadoedu-my.sharepoint.com/:x:/g/personal/arley_torres_uexternado_edu_co/EWLkjJhxRxBBrJaydePdva4Bnz4Z8JyRwg65IqooLIWu3A?e=xe0H7o"

@st.cache_data
def load_data(url):
    try:
        df = pd.read_excel(url, engine="openpyxl")
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Load data
df = load_data(EXCEL_URL)

st.title("Consulta de Calificaciones")

# User inputs
email = st.text_input("Ingrese su correo electrónico:")
student_id = st.text_input("Ingrese su número de documento:")

if st.button("Consultar"):
    if not email or not student_id:
        st.warning("Por favor, ingrese ambos valores.")
    else:
        student_data = df[(df["Correo"] == email) & (df["Nro.Documento"] == int(student_id))]

        if not student_data.empty:
            st.success("Calificaciones encontradas:")
            st.write(student_data)
        else:
            st.error("No se encontraron calificaciones con estos datos.")

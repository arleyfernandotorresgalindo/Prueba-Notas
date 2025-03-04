import streamlit as st
import pandas as pd
import requests
from io import BytesIO
from googleapiclient.discovery import build
from google.oauth2 import service_account
import os

EXCEL_URL = 'output.xlsx'

def read_all_sheets_as_dataframes(service_account_file, spreadsheet_id):
    """Reads all sheets from a Google Spreadsheet and returns them as a dictionary of pandas DataFrames."""

    try:
        creds = service_account.Credentials.from_service_account_file(
            service_account_file, scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
        service = build('sheets', 'v4', credentials=creds)
        sheet_metadata = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        sheets = sheet_metadata.get('sheets', [])

        all_dfs = {}  # Dictionary to store DataFrames for each sheet

        for sheet in sheets:
            sheet_name = sheet['properties']['title']
            range_name = sheet_name  # Read the entire sheet

            result = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
            values = result.get('values', [])

            if not values:
                print(f'No data found in sheet: {sheet_name}')
                all_dfs[sheet_name] = None  # Store None to indicate an empty sheet
                continue

            header = values[0]
            data = values[1:]
            df = pd.DataFrame(data, columns=header)
            all_dfs[sheet_name] = df

        return all_dfs

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

SERVICE_ACCOUNT_FILE = os.environ.get("GOOGLE_SHEETS_CREDENTIALS")
SPREADSHEET_ID = '1ypOrL9AQPhFCpEUF9WFGltFwFB6lhKxeqzdYKdPOjwo'

all_dataframes = read_all_sheets_as_dataframes(SERVICE_ACCOUNT_FILE, SPREADSHEET_ID)

st.title("Consulta De Calificaciones 2025-01")

# User inputs
materia = st.selectbox('Elegir su materia', ['Precálculo', 'Programación 2', 'Estructura de datos'])
email = st.text_input("Ingrese su correo electrónico:")
student_id = st.text_input("Ingrese su número de documento:")
df = all_dataframes[materia]

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

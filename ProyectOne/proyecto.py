import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()


db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

engine = create_engine(f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}')

def cargar_excel(archivo):
    df = pd.read_excel(archivo)
    return df

def mostrar_datos(df):
    st.write("Vista previa de los datos:")
    st.dataframe(df)

def escribir_a_base_de_datos(df, tabla):
    try:
        df.to_sql(tabla, con=engine, if_exists='replace', index=False)
        st.success(f"Datos guardados en la tabla {tabla} de la base de datos.")
    except Exception as e:
        st.error(f"Error al escribir en la base de datos: {e}")

def recuperar_datos(tabla):
    query = f"SELECT * FROM {tabla} LIMIT 10"
    try:
        df = pd.read_sql(query, con=engine)
        return df
    except Exception as e:
        st.error(f"Error al recuperar datos: {e}")
        return None

def insercion_masiva(df, tabla):
    try:
        df.to_sql(tabla, con=engine, if_exists='append', index=False, chunksize=500)
        st.success(f"Inserción masiva exitosa en la tabla {tabla}.")
    except Exception as e:
        st.error(f"Error en la inserción masiva: {e}")

st.title("Gestión de archivos Excel y base de datos MySQL")

archivo = st.file_uploader("Sube un archivo de Excel", type="xlsx")

if archivo:
    df = cargar_excel(archivo)
    mostrar_datos(df)

    
    tabla = st.text_input("Nombre de la tabla en la base de datos:", "mi_tabla")

    
    if st.button("Escribir en la base de datos"):
        escribir_a_base_de_datos(df, tabla)

    
    if st.button("Realizar inserción masiva"):
        insercion_masiva(df, tabla)


if st.button("Recuperar datos de la base de datos"):
    tabla_a_recuperar = st.text_input("Nombre de la tabla para recuperar datos:", "mi_tabla")
    datos_recuperados = recuperar_datos(tabla_a_recuperar)
    if datos_recuperados is not None:
        mostrar_datos(datos_recuperados)

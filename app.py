import streamlit as st
import pandas as pd
import time
from io import BytesIO

# Título de la app
st.title("Consulta de Infracciones SIMIT")
st.write("Sube un archivo con cédulas para verificar si tienen infracciones.")

# Subir archivo
archivo = st.file_uploader("Subir archivo CSV con columna 'cedula'", type=["csv"])

if archivo is not None:
    df = pd.read_csv(archivo)

    if "cedula" not in df.columns:
        st.error("❌ El archivo debe contener una columna llamada 'cedula'.")
    else:
        st.success("✅ Archivo cargado correctamente.")
        st.write("Primeras filas del archivo:")
        st.dataframe(df.head())

        if st.button("Consultar SIMIT (simulado)"):
            resultados = []

            with st.spinner("Consultando infracciones..."):
                for cedula in df["cedula"]:
                    time.sleep(0.5)  # Simula tiempo de respuesta

                    # --- Simulación de lógica de respuesta ---
                    if int(str(cedula)[-1]) % 2 == 0:  # Cedulas pares tienen infracciones
                        resultados.append({
                            "cedula": cedula,
                            "estado": "Tiene infracciones",
                            "tipo_multa": "Comparendo por velocidad",
                            "valor": "$350.000",
                            "pagada": "No"
                        })
                    else:
                        resultados.append({
                            "cedula": cedula,
                            "estado": "No tiene infracciones a la fecha",
                            "tipo_multa": "",
                            "valor": "",
                            "pagada": ""
                        })

            resultados_df = pd.DataFrame(resultados)
            st.success("✅ Consulta completada.")
            st.dataframe(resultados_df)

            # Descargar archivo
            def convertir_excel(df):
                output = BytesIO()
                with pd.ExcelWriter(output, engine="openpyxl") as writer:
                    df.to_excel(writer, index=False)
                return output.getvalue()

            excel_data = convertir_excel(resultados_df)
            st.download_button(
                label="📥 Descargar resultados en Excel",
                data=excel_data,
                file_name="resultados_infracciones.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

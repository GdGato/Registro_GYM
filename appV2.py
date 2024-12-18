import streamlit as st
import json
import pandas as pd
from datetime import datetime, timedelta
import os

# Ejercicios por tipo de entrenamiento
ejercicios_ppl = {
    "Empuje": {
        "Pecho": ["Press de banca", "Press inclinado con mancuernas", "Fondos en paralelas", "Aperturas con mancuernas"],
        "Hombros": ["Press militar", "Elevaciones laterales", "Press Arnold", "Pájaros"],
        "Tríceps": ["Extensión de tríceps con cuerda", "Press cerrado", "Patada de tríceps", "Rompecráneos"]
    },
    "Jalón": {
        "Espalda": ["Dominadas", "Remo con barra", "Pull-over con mancuerna", "Remo en máquina"],
        "Bíceps": ["Curl con barra", "Curl martillo", "Curl concentrado", "Curl en predicador"],
        "Trapecio": ["Encogimientos con mancuernas", "Remo al mentón", "Face pulls", "Remo con barra a un brazo"]
    },
    "Pierna": {
        "Cuádriceps": ["Sentadilla con barra", "Prensa de pierna", "Zancadas", "Extensiones de pierna"],
        "Isquiotibiales": ["Peso muerto rumano", "Curl femoral", "Buenos días", "Hip thrust"],
        "Glúteos": ["Hip thrust", "Patada trasera", "Puente de glúteos", "Sentadillas búlgaras"]
    }
}

# Función para cargar los datos de entrenamientos desde un archivo JSON
def cargar_datos():
    try:
        with open("entrenamientos.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        st.error("Error al leer el archivo de entrenamientos. El formato podría ser incorrecto.")
        return []

# Función para guardar los datos de entrenamientos en un archivo JSON
def guardar_datos(entrenamientos):
    try:
        with open("entrenamientos.json", "w") as f:
            json.dump(entrenamientos, f, indent=4)
    except Exception as e:
        st.error(f"Error al guardar los datos: {e}")

# Función para calcular la repetición máxima estimada (1RM) usando la fórmula de Epley
def calcular_1rm(peso, repeticiones):
    return peso * (1 + 0.0333 * repeticiones)

# Función para generar un plan de entrenamiento en CSV con repeticiones y RPE libres
def generar_plan_csv(tipo_entrenamiento):
    fecha_inicio = datetime.now()
    plan = []
    
    for grupo_muscular, ejercicios in ejercicios_ppl[tipo_entrenamiento].items():
        num_ejercicios = 4 if grupo_muscular in ['Pecho', 'Espalda', 'Pierna'] else 3  # Grupos grandes: 4, pequeños: 3
        selected_ejercicios = ejercicios[:num_ejercicios]  # Seleccionar los ejercicios necesarios

        for ejercicio in selected_ejercicios:
            # Generar el número de series basadas en principios científicos (dependiendo del tipo de entrenamiento)
            num_series = 4  # Un ejemplo, este número podría ajustarse según el entrenamiento de volumen o fuerza

            # Agregar las series al plan (sin pedir repeticiones)
            for i in range(num_series):
                plan.append({
                    "Fecha": fecha_inicio.strftime('%Y-%m-%d'),
                    "Tipo": tipo_entrenamiento,
                    "Grupo Muscular": grupo_muscular,
                    "Ejercicio": ejercicio,
                    "Serie": i + 1,
                    "Repeticiones": "Libre",  # Aquí el usuario lo llenará
                    "RPE": "Libre",  # Aquí el usuario lo llenará
                    "Peso (kg)": "Libre",  # Aquí el usuario lo llenará
                    "RM Estimado": "Calculable",  # Basado en la entrada del usuario
                })
                fecha_inicio += timedelta(days=1)  # Avanzar un día para el siguiente ejercicio

    df = pd.DataFrame(plan)
    csv_filename = f"plan_{tipo_entrenamiento}.csv"
    df.to_csv(csv_filename, index=False)
    return csv_filename

# Función para cargar el CSV y agregarlo al registro
def cargar_csv_y_guardar(csv_file, entrenamientos):
    df = pd.read_csv(csv_file)
    for _, row in df.iterrows():
        nuevo_entrenamiento = {
            "tipo": row["Tipo"],
            "grupo_muscular": row["Grupo Muscular"],
            "ejercicio": row["Ejercicio"],
            "fecha": row["Fecha"],
            "serie": row["Serie"],
            "repeticiones": row["Repeticiones"],
            "rpe": row["RPE"],
            "peso": row["Peso (kg)"],
            "rm_estimado": row["RM Estimado"],
        }
        entrenamientos.append(nuevo_entrenamiento)
    guardar_datos(entrenamientos)
    st.success("¡Entrenamientos cargados exitosamente desde el CSV!")

# Función principal de Streamlit
def main():
    st.title("Registro de Entrenamientos PPL")
    entrenamientos = cargar_datos()
    menu = ["Registrar Entrenamiento", "Mostrar Registro", "Generar Plan PPL", "Cargar Plan desde CSV"]
    opcion = st.sidebar.selectbox("Selecciona una opción", menu)

    if opcion == "Registrar Entrenamiento":
        st.subheader("Registrar un nuevo entrenamiento")
        tipo_entrenamiento = st.selectbox("Selecciona el tipo de entrenamiento", ["Empuje", "Jalón", "Pierna"])
        grupo_muscular = st.selectbox("Selecciona el grupo muscular", list(ejercicios_ppl[tipo_entrenamiento].keys()))
        ejercicio = st.selectbox("Selecciona el ejercicio", ejercicios_ppl[tipo_entrenamiento][grupo_muscular])
        num_series = st.number_input("¿Cuántas series deseas agregar?", min_value=1, max_value=5, step=1)
        series = []
        for i in range(num_series):
            st.write(f"### Serie {i + 1}")
            repeticiones = st.number_input(f"Repeticiones para serie {i + 1}", min_value=1, step=1)
            esfuerzo = st.slider(f"Percepción de esfuerzo (RPE) para serie {i + 1}", 1, 10, 7)
            peso = st.number_input(f"Peso (kg) para serie {i + 1}", min_value=1, step=1)
            series.append({"repeticiones": repeticiones, "rpe": esfuerzo, "peso": peso})
        if st.button("Registrar Entrenamiento"):
            nuevo_entrenamiento = {
                "tipo": tipo_entrenamiento,
                "grupo_muscular": grupo_muscular,
                "ejercicio": ejercicio,
                "fecha": datetime.now().strftime('%Y-%m-%d'),
                "series": series
            }
            entrenamientos.append(nuevo_entrenamiento)
            guardar_datos(entrenamientos)
            st.success("¡Entrenamiento registrado exitosamente!")

    elif opcion == "Generar Plan PPL":
        tipo_entrenamiento = st.selectbox("Selecciona el tipo de entrenamiento", ["Empuje", "Jalón", "Pierna"])
        if st.button("Generar Plan en CSV"):
            csv_filename = generar_plan_csv(tipo_entrenamiento)
            st.success(f"Plan de entrenamiento para {tipo_entrenamiento} generado en el archivo CSV.")
            st.download_button(label="Descargar CSV", data=open(csv_filename, "rb"), file_name=csv_filename, mime="text/csv")

    elif opcion == "Mostrar Registro":
        st.subheader("Registro de Entrenamientos")
        if entrenamientos:
            df = pd.DataFrame(entrenamientos)
            st.write(df)
        else:
            st.warning("No se han registrado entrenamientos aún.")

    elif opcion == "Cargar Plan desde CSV":
        uploaded_file = st.file_uploader("Sube tu archivo CSV", type=["csv"])
        if uploaded_file is not None:
            try:
                csv_file = uploaded_file.read()
                entrenamientos = []
                cargar_csv_y_guardar(csv_file, entrenamientos)
                st.success("¡Plan cargado exitosamente!")
            except Exception as e:
                st.error(f"Error al cargar el archivo CSV: {e}")

if __name__ == "__main__":
    main()

import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from ejercicios import ejercicios_ppl

# Función para cargar los datos de entrenamientos desde un archivo JSON
def cargar_datos():
    """Carga los entrenamientos registrados desde un archivo JSON"""
    try:
        with open("entrenamientos.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # Si el archivo no existe, devuelve una lista vacía
        return []
    except json.JSONDecodeError:
        # Si el archivo tiene un formato incorrecto, muestra un mensaje de error
        st.error("Error al leer el archivo de entrenamientos. El formato podría ser incorrecto.")
        return []

# Función para guardar los datos de entrenamientos en un archivo JSON
def guardar_datos(entrenamientos):
    """Guarda los entrenamientos registrados en un archivo JSON"""
    try:
        with open("entrenamientos.json", "w") as f:
            json.dump(entrenamientos, f, indent=4)
    except Exception as e:
        # Si ocurre un error al guardar, muestra el mensaje de error
        st.error(f"Error al guardar los datos: {e}")

# Función para graficar el progreso de un ejercicio
def graficar_progreso(entrenamientos, ejercicio_seleccionado):
    """Genera un gráfico con el progreso de un ejercicio específico"""
    # Filtrar los entrenamientos por el ejercicio seleccionado
    datos_ejercicio = []
    
    for entrenamiento in entrenamientos:
        if entrenamiento["ejercicio"] == ejercicio_seleccionado:
            for serie in entrenamiento["series"]:
                datos_ejercicio.append({
                    "Fecha": entrenamiento["fecha"],
                    "Peso": serie["peso"]
                })
    
    if datos_ejercicio:
        # Convertir los datos a un DataFrame de pandas para el gráfico
        df = pd.DataFrame(datos_ejercicio)
        df["Fecha"] = pd.to_datetime(df["Fecha"])

        # Graficar el progreso
        plt.figure(figsize=(10, 6))
        plt.plot(df["Fecha"], df["Peso"], marker='o', linestyle='-', color='b')
        plt.title(f"Progreso de {ejercicio_seleccionado}", fontsize=16)
        plt.xlabel("Fecha", fontsize=12)
        plt.ylabel("Peso (kg)", fontsize=12)
        plt.grid(True)
        st.pyplot(plt)
    else:
        # Si no hay datos para ese ejercicio, muestra una advertencia
        st.warning("No hay datos disponibles para este ejercicio.")

# Función principal de Streamlit
def main():
    """Función principal que controla la interfaz de usuario y el flujo del programa"""
    st.title("Registro de Entrenamientos PPL")

    # Cargar los entrenamientos registrados
    entrenamientos = cargar_datos()

    # Menú de opciones de Streamlit
    menu = ["Registrar Entrenamiento", "Mostrar Registro", "Ver Progreso"]
    opcion = st.sidebar.selectbox("Selecciona una opción", menu)

    if opcion == "Registrar Entrenamiento":
        # Sección para registrar un nuevo entrenamiento
        st.subheader("Registrar un nuevo entrenamiento")

        # Selección de tipo de entrenamiento (Empuje, Jalón, Pierna)
        tipo_entrenamiento = st.selectbox("Selecciona el tipo de entrenamiento", ["Empuje", "Jalón", "Pierna"])

        # Selección del grupo muscular basado en el tipo de entrenamiento
        grupo_muscular = st.selectbox("Selecciona el grupo muscular", list(ejercicios_ppl[tipo_entrenamiento].keys()))

        # Selección de ejercicio basado en el grupo muscular
        ejercicio = st.selectbox("Selecciona el ejercicio", ejercicios_ppl[tipo_entrenamiento][grupo_muscular])

        # Número de series que el usuario quiere agregar
        num_series = st.number_input("¿Cuántas series deseas agregar?", min_value=1, max_value=10, step=1)

        # Lista para almacenar las series del entrenamiento
        series = []

        for i in range(num_series):
            st.write(f"### Serie {i + 1}")
            # Introducción de detalles de cada serie
            peso = st.number_input(f"Peso (kg) para serie {i + 1}", min_value=1, step=1)
            repeticiones = st.number_input(f"Repeticiones para serie {i + 1}", min_value=1, step=1)
            esfuerzo = st.slider(f"Percepción de esfuerzo (RPE) para serie {i + 1}", 1, 10, 7)

            # Guardar cada serie en la lista de series
            series.append({
                "peso": peso,
                "repeticiones": repeticiones,
                "esfuerzo": esfuerzo
            })

        if st.button("Registrar Entrenamiento"):
            # Crear un nuevo registro de entrenamiento con la fecha actual
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

    elif opcion == "Mostrar Registro":
        # Mostrar el historial de entrenamientos registrados
        st.subheader("Historial de entrenamientos")
        
        if entrenamientos:
            for i, entrenamiento in enumerate(entrenamientos, 1):
                st.write(f"### Entrenamiento {i}")
                st.write(f"**Tipo**: {entrenamiento['tipo']}")
                st.write(f"**Grupo Muscular**: {entrenamiento['grupo_muscular']}")
                st.write(f"**Ejercicio**: {entrenamiento['ejercicio']}")
                
                # Mostrar las series de cada entrenamiento
                for j, serie in enumerate(entrenamiento["series"], 1):
                    st.write(f"  - **Serie {j}:**")
                    st.write(f"    - **Peso**: {serie['peso']} kg")
                    st.write(f"    - **Repeticiones**: {serie['repeticiones']}")
                    st.write(f"    - **Percepción de Esfuerzo (RPE)**: {serie['esfuerzo']}")
                st.write("---")
        else:
            st.warning("No hay entrenamientos registrados.")
    
    elif opcion == "Ver Progreso":
        # Mostrar el progreso de un ejercicio específico
        st.subheader("Ver Progreso de un Ejercicio")

        # Selección de ejercicio para ver el progreso
        ejercicio_seleccionado = st.selectbox("Selecciona el ejercicio para ver el progreso", [
            ejercicio for tipo in ejercicios_ppl.values() for grupo in tipo.values() for ejercicio in grupo
        ])

        if ejercicio_seleccionado:
            graficar_progreso(entrenamientos, ejercicio_seleccionado)

# Ejecutar la función principal si este archivo es ejecutado
if __name__ == "__main__":
    main()

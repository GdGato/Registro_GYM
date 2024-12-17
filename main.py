import json
from ejercicios import ejercicios_ppl

# Nombre del archivo JSON
ARCHIVO_JSON = "registro_entrenamiento_ppl.json"

# Cargar los datos del archivo JSON
def cargar_datos():
    try:
        with open(ARCHIVO_JSON, "r") as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}  # Si no existe el archivo o está vacío, inicia con un diccionario vacío

# Guardar los datos en el archivo JSON
def guardar_datos():
    with open(ARCHIVO_JSON, "w") as archivo:
        json.dump(registro_entrenamiento, archivo, indent=4)
    print("Datos guardados correctamente.\n")

# Mostrar el registro completo
def mostrar_registro():
    if not registro_entrenamiento:
        print("No hay datos registrados aún.\n")
        return
    print("\n--- Registro Completo de Entrenamientos ---")
    for tipo, musculos in registro_entrenamiento.items():
        print(f"\nEntrenamiento: {tipo}")
        for musculo, ejercicios in musculos.items():
            print(f"  {musculo}:")
            for ej in ejercicios:
                print(f"    {ej['nombre']}:")
                for serie in ej['series']:
                    print(f"      Serie {serie['serie']}: Peso: {serie['peso']}kg | Reps: {serie['repeticiones']} | Esfuerzo: {serie['percepcion']}/10")
    print("\n--- Fin del Registro ---\n")

# Inicializar el registro de entrenamiento
registro_entrenamiento = cargar_datos()

# Función para agregar un ejercicio
def agregar_ejercicio():
    while True:
        print("\n¿Qué tipo de entrenamiento es hoy?")
        print("0. Empuje\n1. Jalón\n2. Pierna\n3. Mostrar registro\n4. Guardar y salir")
        
        try:
            tipo_opcion = int(input("Elige el número del tipo de entrenamiento: "))
            if tipo_opcion == 3:  # Mostrar el registro
                mostrar_registro()
                continue
            elif tipo_opcion == 4:  # Guardar y salir
                guardar_datos()
                exit("Programa finalizado.")
            
            tipos = list(ejercicios_ppl.keys())
            tipo = tipos[tipo_opcion]
        except (ValueError, IndexError):
            print("Opción no válida. Intenta de nuevo.")
            continue
        
        while True:
            musculos = list(ejercicios_ppl[tipo].keys())
            print(f"\nMúsculos trabajados en {tipo}:")
            for i, musculo in enumerate(musculos):
                print(f"{i}. {musculo}")
            print(f"{len(musculos)}. Mostrar registro")
            print(f"{len(musculos)+1}. Regresar")

            try:
                musculo_opcion = int(input("Elige el número del músculo: "))
                if musculo_opcion == len(musculos):  # Mostrar el registro
                    mostrar_registro()
                    continue
                elif musculo_opcion == len(musculos) + 1:  # Regresar al menú anterior
                    break
                musculo = musculos[musculo_opcion]
            except (ValueError, IndexError):
                print("Opción no válida. Intenta de nuevo.")
                continue

            while True:
                ejercicios = ejercicios_ppl[tipo][musculo]
                print(f"\nEjercicios disponibles para {musculo}:")
                for i, ej in enumerate(ejercicios):
                    print(f"{i}. {ej}")
                print(f"{len(ejercicios)}. Mostrar registro")
                print(f"{len(ejercicios)+1}. Regresar")

                try:
                    ejercicio_opcion = int(input("Elige el número del ejercicio: "))
                    if ejercicio_opcion == len(ejercicios):  # Mostrar el registro
                        mostrar_registro()
                        continue
                    elif ejercicio_opcion == len(ejercicios) + 1:  # Opción para regresar
                        break
                    ejercicio = ejercicios[ejercicio_opcion]
                except (ValueError, IndexError):
                    print("Opción no válida. Intenta de nuevo.")
                    continue

                # Capturar datos por serie
                print(f"\nDetalles del ejercicio: {ejercicio}")
                series_data = []
                while len(series_data) < 3 or len(series_data) > 5:
                    try:
                        num_series = int(input("¿Cuántas series hiciste? (3-5): "))
                        if 3 <= num_series <= 5:
                            for i in range(num_series):
                                print(f"\nSerie {i+1}:")
                                peso = float(input("Peso (kg): "))
                                repeticiones = int(input("Repeticiones: "))
                                percepcion = int(input("Percepción de esfuerzo (1-10): "))
                                series_data.append({
                                    "serie": i+1,
                                    "peso": peso,
                                    "repeticiones": repeticiones,
                                    "percepcion": percepcion
                                })
                        else:
                            print("Debes ingresar entre 3 y 5 series.")
                    except ValueError:
                        print("Entrada inválida. Introduce valores numéricos válidos.")

                # Guardar los datos
                if tipo not in registro_entrenamiento:
                    registro_entrenamiento[tipo] = {}
                if musculo not in registro_entrenamiento[tipo]:
                    registro_entrenamiento[tipo][musculo] = []

                registro_entrenamiento[tipo][musculo].append({
                    "nombre": ejercicio,
                    "series": series_data
                })
                guardar_datos()  # Guardar automáticamente después de cada ejercicio
                print(f"\nEjercicio '{ejercicio}' agregado correctamente con {len(series_data)} series.\n")

# Ejecutar el programa
if __name__ == "__main__":
    print("\n=== Registro de Entrenamiento PPL ===")
    agregar_ejercicio()

# Registro de Entrenamiento PPL

Este proyecto es una aplicación para registrar entrenamientos de tipo **Push/Pull/Legs (PPL)**. 
Permite agregar ejercicios, registrar series con sus respectivos pesos, repeticiones y percepción de esfuerzo, 
y visualizar el registro completo de entrenamientos en cualquier momento.
    
### Funcionalidades

- **Registro de entrenamientos**: Permite registrar entrenamientos organizados en tres tipos de sesiones: Empuje (Push), Jalón (Pull), y Pierna (Legs).
- **Ejercicios por músculo**: Para cada tipo de entrenamiento, puedes seleccionar ejercicios dirigidos a trabajar músculos específicos.
- **Registro de series**: Guarda los detalles de cada serie, como el peso, las repeticiones y la percepción de esfuerzo (RPE).
- **Visualización del registro**: Puedes consultar el historial completo de tus entrenamientos en cualquier momento.
- **Guardar y cargar datos**: Los datos se almacenan automáticamente en un archivo JSON para facilitar su carga y recuperación en futuras ejecuciones.
    
## Instalación
### Requisitos
Asegúrate de tener Python 3.x instalado en tu sistema.
### Pasos de instalación

1. **Clona este repositorio**:
    
```bash
git clone https://github.com/tu_usuario/registro_entrenamiento_ppl.git
cd registro_entrenamiento_ppl
```

2. **Instala las dependencias necesarias** (si es necesario):
    
```bash
pip install -r requirements.txt
```
### Uso

1. Ejecuta el archivo principal para iniciar la aplicación:
    
```bash
python main.py
```

2. Sigue las instrucciones del menú para agregar ejercicios y registrar tus entrenamientos.
3. Para guardar y salir, selecciona la opción correspondiente en el menú.
4. Para ver el registro de entrenamientos, selecciona la opción **"Mostrar registro"** en el menú.
    
## Contribución

Si deseas contribuir al proyecto, sigue estos pasos:
    

1. Haz un **fork** de este repositorio.
2. Crea una nueva rama para tu funcionalidad:
    
```bash
git checkout -b feature-nueva-funcionalidad
```

3. Realiza tus cambios y haz commit:
    
```bash
git commit -am 'Añadí nueva funcionalidad'
```

4. Realiza un **push** de tu rama:
    
```bash
git push origin feature-nueva-funcionalidad
```

5. Abre un **Pull Request** describiendo los cambios realizados.
    
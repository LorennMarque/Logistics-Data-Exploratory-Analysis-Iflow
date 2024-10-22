import pandas as pd
import matplotlib.pyplot as plt
import os
import ffmpeg

# Cargar los datos
datos = pd.read_csv('iflow_clean.csv')  # Ajusta con tu dataset
datos['fin_visita'] = pd.to_datetime(datos['fin_visita'], format='mixed', errors='coerce')
datos = datos.sort_values('fin_visita').head(10)

# Crear una carpeta temporal para guardar los fotogramas
os.makedirs('frames', exist_ok=True)

# Parámetros para graficar
fig, ax = plt.subplots(figsize=(8, 6))

# Generar un gráfico por cada fila del dataset
for i, row in datos.iterrows():
    ax.clear()
    ax.scatter(row['longitud'], row['latitud'], color='red', s=10)
    ax.set_xlim(datos['longitud'].min(), datos['longitud'].max())
    ax.set_ylim(datos['latitud'].min(), datos['latitud'].max())
    ax.set_title(f"Visita: {row['fin_visita']}")
    
    # Guardar cada gráfico como un fotograma
    plt.savefig(f"frames/frame_{i:05d}.png")

plt.close()

# Crear el video con ffmpeg
(
    ffmpeg
    .input('frames/frame_%05d.png', framerate=30)
    .output('animacion.mp4', crf=25, pix_fmt='yuv420p')
    .run()
)

# Eliminar los fotogramas temporales
import shutil
shutil.rmtree('frames')

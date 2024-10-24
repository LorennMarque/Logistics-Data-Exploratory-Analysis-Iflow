import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from math import radians, sin, cos, sqrt, asin
from itertools import combinations

# Función para calcular la distancia Haversine entre dos puntos geográficos
def haversine(lon1, lat1, lon2, lat2):
    # Convertir grados decimales a radianes
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    # Fórmula de Haversine
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    r = 6371  # Radio de la Tierra en kilómetros
    return c * r

# Leer los datos del archivo CSV
df = pd.read_csv('data/clean_iflow_data.csv')

# Mantener una copia de las fechas originales
df['fin_visita_original'] = df['fin_visita']

# Convertir 'fin_visita' a formato datetime, manejando formatos mixtos
df['fin_visita'] = pd.to_datetime(df['fin_visita'], format='mixed', errors='coerce')

# Verificar si hay fechas no parseadas
num_nulos = df['fin_visita'].isnull().sum()
print(f"Número de fechas no parseadas: {num_nulos}")

if num_nulos > 0:
    fechas_no_parseadas = df[df['fin_visita'].isnull()]['fin_visita_original']
    print("Fechas no parseadas:")
    print(fechas_no_parseadas)

# Filtrar las entregas del día 2024-05-23
fecha_objetivo = pd.to_datetime('2024-05-23')
df_dia = df[df['fin_visita'].dt.date == fecha_objetivo.date()]

# Ordenar las entregas cronológicamente
df_dia = df_dia.sort_values('fin_visita')

# Seleccionar las primeras 20 entregas
df_muestra = df_dia.head(100).reset_index(drop=True)

# Suponer una velocidad promedio de desplazamiento (km/h)
velocidad_promedio = 40.0  # Ajusta este valor según sea necesario

# Diccionario para asignaciones de repartidores
asignaciones_repartidores = {}

# Procesar entregas por cada cliente en df_muestra
for cliente, grupo in df_muestra.groupby('cliente'):
    entregas = grupo.reset_index(drop=True)
    n = len(entregas)
    G = nx.Graph()
    
    # Añadir nodos al grafo
    for idx in entregas.index:
        G.add_node(idx)
    
    # Construir el grafo de conflictos
    for i, j in combinations(entregas.index, 2):
        d1 = entregas.loc[i]
        d2 = entregas.loc[j]
        
        # Calcular diferencia de tiempo en horas
        diferencia_tiempo = abs((d2['fin_visita'] - d1['fin_visita']).total_seconds()) / 3600.0
        
        # Calcular distancia entre entregas
        distancia = haversine(d1['longitud'], d1['latitud'], d2['longitud'], d2['latitud'])
        
        # Calcular tiempo mínimo de viaje en horas
        tiempo_viaje = distancia / velocidad_promedio
        
        # Verificar si hay conflicto
        if diferencia_tiempo == 0:
            # No agregamos una arista; entregas con la misma marca de tiempo se asignarán al mismo repartidor
            pass
        elif diferencia_tiempo < tiempo_viaje:
            # No pueden ser realizadas por el mismo repartidor
            G.add_edge(i, j)
    
    # Aplicar algoritmo de coloreo de grafos
    coloreo = nx.coloring.greedy_color(G, strategy='largest_first')
    
    # Asignar entregas a repartidores
    for idx, color in coloreo.items():
        id_repartidor = f'{cliente}_{color}'
        if id_repartidor not in asignaciones_repartidores:
            asignaciones_repartidores[id_repartidor] = []
        asignaciones_repartidores[id_repartidor].append(entregas.loc[idx])

# Visualizar los resultados
colores = list(mcolors.TABLEAU_COLORS.keys())

plt.figure(figsize=(10, 8))

for idx, (repartidor, entregas_repartidor) in enumerate(asignaciones_repartidores.items()):
    entregas_df = pd.DataFrame(entregas_repartidor)
    latitudes = entregas_df['latitud']
    longitudes = entregas_df['longitud']
    color = colores[idx % len(colores)]
    plt.scatter(longitudes, latitudes, c=color, label=repartidor)

plt.xlabel('Longitud')
plt.ylabel('Latitud')
plt.title('Asignación de Entregas a Repartidores')
plt.legend()
plt.grid(True)
plt.show()

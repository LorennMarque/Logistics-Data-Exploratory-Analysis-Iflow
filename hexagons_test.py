import pandas as pd
import h3
import folium

# Cargar el dataset
df = pd.read_csv('iflow_clean.csv')

# Verificar que las columnas requeridas estén presentes
if not {'latitud', 'longitud', 'fin_visita'}.issubset(df.columns):
    raise ValueError("El dataset debe contener las columnas 'latitud', 'longitud', y 'fin_visita'.")

# Convertir 'fin_visita' a datetime con control de errores
df['fin_visita'] = pd.to_datetime(df['fin_visita'], errors='coerce')

# Filtrar por la fecha específica y eliminar filas con NaN
df_filtrado = df[df['fin_visita'].dt.date == pd.to_datetime('2024-05-23').date()]
df_filtrado = df_filtrado.dropna(subset=['latitud', 'longitud'])

# Ordenar por 'fin_visita' y seleccionar las primeras 20 entregas
df_filtrado = df_filtrado.sort_values(by='fin_visita').head(60)

# Generar IDs de hexágonos H3
resolution = 6
df_filtrado['hex_id'] = df_filtrado.apply(
    lambda row: h3.latlng_to_cell(row['latitud'], row['longitud'], resolution), axis=1
)

# Asignar colores a los hexágonos por grupo
colores = ['red', 'blue', 'green', 'purple', 'orange']
df_filtrado['color'] = df_filtrado['hex_id'].apply(lambda x: colores[hash(x) % len(colores)])

# Crear un mapa centrado en el promedio de las coordenadas
lat_centro = df_filtrado['latitud'].mean()
lon_centro = df_filtrado['longitud'].mean()
mapa = folium.Map(location=[lat_centro, lon_centro], zoom_start=12)

# Agregar marcadores al mapa con colores asignados
for _, row in df_filtrado.iterrows():
    folium.Marker(
        location=[row['latitud'], row['longitud']],
        popup=f"<b>Hex ID:</b> {row['hex_id']}<br><b>Fin Visita:</b> {row['fin_visita']}",
        icon=folium.Icon(color=row['color'], icon='info-sign')
    ).add_to(mapa)

# Guardar el mapa como archivo HTML
mapa.save('mapa_entregas.html')
print("Mapa guardado como 'mapa_entregas.html'")

# Mostrar los primeros resultados filtrados
print(df_filtrado.head())

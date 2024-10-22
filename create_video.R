install.packages("gganimate")
install.packages("gifski")  # Para exportar la animación
install.packages("transformr")  # Para transformaciones suaves en la animación

# Cargar las bibliotecas
library(ggplot2)
library(gganimate)
library(gifski)
library(dplyr)



# Cargar tu dataset
# Supongamos que tu dataset se llama 'datos' y tiene las columnas 'latitud', 'longitud' y 'fin_visita'
# Ejemplo: 

datos <- read.csv('iflow_clean.csv')
# Asegúrate de que 'fin_visita' esté en formato datetime
datos$fin_visita <- as.POSIXct(datos$fin_visita)

# Ordenar los datos por 'fin_visita'
datos <- datos[order(datos$fin_visita), ] %>% head(10)

# Crear el gráfico de dispersión con ggplot2
plot <- ggplot(datos, aes(x = longitud, y = latitud)) +
  geom_point(color = "red", size = 2) +  # Personaliza el color y el tamaño de los puntos
  labs(title = 'Tiempo: {frame_time}') +  # Mostrará el tiempo (fin_visita) en cada fotograma
  theme_minimal() +
  transition_time(fin_visita) +  # Esto animará en función del tiempo
  ease_aes('linear')  # Aplicar transición lineal entre fotogramas

# Generar la animación
animacion <- animate(plot, nframes = 30, fps = 30, duration = 10)  # 900 segundos (15 minutos)

anim_save("animacion.mp4", animation = animacion)  # Guardar como video (MP4)
# anim_save("animacion.gif", animation = animacion)  # Guardar como GIF
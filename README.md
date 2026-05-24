# 📖 Practica final Python

Dashboard interactivo con Streamlit que nos permite explorar y compartir la visualización de la información de un conjunto de datos real para el cliente.

La aplicación se ha desarrollado en Python utilizando Streamlit para la creación del dashboard, y Pandas para el tratamiento de datasets además de Numpy para el cálculo de datos.

##### Enlace a dashboard de streamlit desplegado
https://eda-maria-jorge.streamlit.app/

# La aplicación se divide en los siguientes apartados:

## 1. Clientes por estado y ciudad
Se ofrecen a primera vista cuatro métricas con filtrado de resultados dinámico en función de la fecha:
- Clientes únicos activos en el periodo seleccionado
- Media diaria de clientes activos durante el periodo de días seleccionado
- Clientes nuevos únicos del periodo seleccionado
- Media diaria de clientes nuevos del periodo seleccionado

También podemos ver los datos en una representación de tabla y en un mapa de distribución de clientes por ciudad, en la que se puede filtrar el número de ciudades a mostrar.  

**Análisis de datos** - estos datos no reflejan muchos cambios si comparamos clientes únicos con clientes nuevos, con lo que se puede concluir que no hay mucha recurrencia de compra.

### Enfoque técnico
- Implementación de carga de dataset en caché para optimizar tiempos de carga. Procesamiento y carga gestionado con Pandas.
- Cálculo de coordenadas y guardado de datos en un archivo CSV para optimizar recursos a la hora de representar los datos de clientes en un mapa.
- Filtrado de datos por fecha a través de la creación de un DataFrame que se actualiza según los valores introducidos en el ``st.datetime_input()``
- Librería ***Folium*** para construcción de mapa que representa la distribución de clientes por ciudad sobre un mapa interactivo.



# 2. Pedidos por ciudad
Se realiza un análisis y cálculo de:
- Número de pedidos por ciudad
- Porcentaje que representan esos pedidos por ciudad con respecto al total de pedidos
- Ratio de pedidos por cliente en esa ciudad

Para este filtrado de datos se ha tenido en cuenta que hay nombres de ciudades iguales en diferentes estados.

Los datos están representados mediante gráficos de barras donde se puede ver el porcentaje de pedidos por cliente en cada ciudad y el ratio.

También le acompañan la muestra de las siguientes métricas globales:
- Número total de pedidos
- Número total de clientes
- Ratio global de pedidos por cliente

**Análisis de datos** - Teniendo en cuenta que el ratio total entre clientes y pedidos es de 1.03, quiere decir que los clientes no piden una segunda vez pese a tener valoraciones muy positivas respecto a los productos, algunas ciudades tienen un porcentaje de pedidos retrasados alto con respecto al total de pedidos de la ciudad, esto puede deberse a múltiples factores como la accesibilidad a la zona geográfica, falta de logística propia (subcontratando el reparto a diversas empresa, dependiendo del estado o ciudad). La empresa no se enfoca en ninguna industria o producto concreto, lo que puede llegar a explicar su volumen de compra y la decisión de los clientes de no repetir su compra.

### Enfoque técnico
- Implementación de carga de datasets en caché para optimizar tiempos de carga. Procesamiento y carga gestionado con Pandas.
- Agrupación de datos por estado y ciudad.
- Uso conjunto de ``customer_state`` y ``customer_city`` para evitar confusión con el mismo nombre de ciudades en diferentes estados.
- Filtro dinámico con ``st.selectbox()`` para filtrar por estado y ciudad.
- Filtro dinámico con ``st.slider()`` para seleccionar el número de ciudades a mostrar en los gráficos de barras y así facilitar la visualización de datos.


## 3. Análisis de retrasos en pedidos
Se representa en dos gráficos de barras estáticos el top 15 de ciudades con mayor porcentaje de pedidos que llegan tarde con respecto al total de pedidos de esa ciudad, y el top 15 de ciudades con más días de retraso medio en la entrega.

A continuación, se puede filtrar por estado y ciudad otro gráfico en el que se muestra el porcentaje de pedidos con entrega tardía con respecto al total de pedidos de esa ciudad. Para identificar bien la comparación, se puede ver en amarillo el porcentaje de pedidos retrasados y en gris el total de pedidos. La cifra del número total de pedidos de cada ciudad se ha normalizado para poder representar ambos valores bajo la misma escala (sobre 100).

Se visualizan también las siguientes métricas dinámicas mediante el filtro de ciudades y estados:
- Número total de pedidos
- Número total de pedidos con entrega tardía
- Porcentaje de esos pedidos retrasados frente al total
- Retraso medio en días

Además, se muestran en formato tabla los mismos datos que en el gráfico de barras filtrado.

Por último, se sugiere un autodiagnóstico del posible problema del retraso en la entrega de esos pedidos que va en base a los datos de la tabla filtrada.

### Enfoque técnico
- Implementación de carga de dataset en caché para optimizar tiempos de carga. Procesamiento y carga gestionado con Pandas.
- Comparación de fechas de entrega estimada y real para detectar los pedidos con entrega tardía.
- Filtro dinámico de estado y ciudad con ``st.selectbox()``
- Librería ***Altair*** junto con componentes gráficos de Streamlit para construcción de gráficos.
- Normalización de datos para representación gráfica bajo la misma escala.
- Generación de autodiagnóstico bajo reglas de comparación de las métricas calculadas según volumen de pedidos y nivel de retrasos detectados.


## 4. Reviews y satisfacción del cliente
Se analiza la satisfacción del cliente a través de las reviews. Se calcula el número total de reviews y la puntuación media por estado, excluyendo los pedidos que llegaron con retraso para no sesgar el resultado. Esto permite identificar en qué estados los clientes están más satisfechos con sus compras, independientemente de la logística.

**Análisis de datos:** Permite identificar geográficamente dónde la experiencia de compra (sin contar la entrega) es mejor o peor, ayudando a enfocar mejoras en la calidad del producto o la atención del vendedor.

### Enfoque técnico
- Se combinan los datasets de pedidos y reviews.
- Se filtran los datos para excluir los pedidos que llegaron con retraso y así no sesgar la puntuación de satisfacción.
- Se agrupan los resultados por estado para calcular el número total de reviews y la puntuación media.

## 5. Análisis de puntualidad en pedidos
Esta sección se centra en la eficiencia de las entregas. Muestra la media de días de adelanto con la que se entregan los pedidos en cada ciudad. Es un indicador clave para evaluar el rendimiento logístico y la fiabilidad de las fechas de entrega estimadas.

**Análisis de datos:** Un valor alto indica una logística eficiente y una buena experiencia para el cliente. Un valor bajo o negativo en ciertas ciudades puede señalar problemas con los transportistas locales o una mala estimación de los tiempos de entrega.

### Enfoque técnico
- Se calcula la diferencia en días entre la fecha de entrega real y la estimada.
- Se filtran los resultados para considerar solo los pedidos con valores positivos (entregados antes de tiempo).
- Se agrupan los datos por ciudad para calcular la media de días de adelanto en la entrega.

## 6. Oferta y demanda por categoría
Se presenta un análisis de la oferta y la demanda por categoría de producto. La página muestra:
- Un resumen con las 3 categorías más y menos vendidas en todo el marketplace.
- Un selector para elegir una categoría específica.
- Para la categoría seleccionada, se muestra el número total de pedidos y dos gráficos: uno con el top 10 de ciudades con más compradores (demanda) y otro con el top 10 de ciudades con más vendedores (oferta).

**Análisis de datos:** Comparar la oferta y la demanda ayuda a identificar oportunidades de mercado. Una alta demanda con baja oferta local sugiere que nuevos vendedores de esa categoría podrían tener éxito en esa ciudad.

### Enfoque técnico
- Se combinan todos los datasets relevantes (pedidos, productos, clientes, vendedores) para crear una vista de datos unificada.
- Se realiza una agrupación inicial por categoría de producto para identificar y mostrar las 3 más y menos vendidas.
- Se implementa un filtro dinámico (`st.selectbox`) para que el usuario elija una categoría.
- Para la categoría seleccionada, se filtra el dataset y se realizan dos agrupaciones: por ciudad del comprador (demanda) y por ciudad del vendedor (oferta), mostrando el top 10 en gráficos de barras.
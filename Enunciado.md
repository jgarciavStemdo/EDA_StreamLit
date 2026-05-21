📖 Practica final Python
Nuestro objetivo es crear un dashboard interactivo con Streamlit que nos permita explorar y compartir la visualización de la información de un conjunto de datos real para nuestro cliente.

Lista de tareas principales:
1. Clientes por estado y ciudad
Representa una clasificación del número de clientes por estado. Crea una tabla en la que se muestren:

Estado
Ciudad
Número de clientes por ciudad
Tanto la tabla como los gráficos deberán ser dinámicos respecto a la fecha para permitir el análisis temporal de la evolución de clientes.

2. Pedidos por ciudad
A la tabla anterior añade las siguientes columnas:

Número de pedidos
Porcentaje que representan respecto al total de pedidos
Además, representa el ratio de pedidos por cliente, utilizando el tipo de gráfico que consideres más adecuado.

Tras este análisis, responde a las siguientes cuestiones:

¿Qué información o patrones se pueden identificar a partir de estos datos?
¿Qué acciones, como analista de datos, crees que debería tomar la empresa para mejorar sus ventas?
3. Análisis de retrasos en pedidos
Calcula y representa:

Número de pedidos que llegan tarde por ciudad
Porcentaje de pedidos retrasados respecto al total de pedidos de la ciudad
Tiempo medio de retraso en días
Además, al representar esta información, el dashboard deberá incluir un autodiagnóstico que indique la razón más probable del problema.

4. Reviews y satisfacción del cliente
Calcula y representa:

Número de reviews por estado
Score medio de las reviews en cada estado
Para este cálculo, se deberán excluir los pedidos con retraso, ya que se entiende que la valoración negativa podría deberse principalmente al retraso en la entrega del producto.

Esto serán las métricas que tendrá que tener en el ejercicio calculadas y representadas como mínimo, puedes añadir todas las que veas interesantes!

 

Recursos

Image

Entregables
App funcionando en local.
Código implementado.
Presentación breve del trabajo (5-10 minutos por equipo).






------------------------------------------------------------------------------------------------


# 1. clientes por estado y ciudad
``customers_dataset.csv``

- Estado
- Ciudad
- Número de clientes por ciudad

Filtrado por fechas dinámicamente en streamlit al dibujar.


# 2. Pedidos por ciudad
``order_items_dataset.csv``

- Número de pedidos
- Percoentaje que representan respecto al total de pedidos


# 3. Análisis de retrasos en pedidos
Shipping_limit_date - ``order_items_dataset.csv``

``orders_dataset.csv``

- Número de pedidos que llegan tarde por ciudad
- Porcentaje de pedidos retrasados respecto al total de pedidos de la ciudad
- Tiempo medio de retraso en días


# 4. Reviews y satisfacción del cliente
``order_reviews_dataset.csv``

- Número de reviews por estado
- Score medio de las reviews en cada estado




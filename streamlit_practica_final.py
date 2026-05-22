#Ejemplo para desplegar en streamlit
# Se despliega así: `streamlit run main.py` dentro de la ruta del archivo sstreamlit


#Este archivo es una prueba para mostrar como se puede montar una pagina web con streamlit
# Streamlit es una libreria de python que permite crear aplicaciones web de manera sencilla y rapida

# Para instalar streamlit, puedes usar el siguiente comando:
# pip install streamlit

# Para ejecutar este archivo, puedes usar el siguiente comando:
# streamlit run <nombredelarchivo>.py

# Importar librerías



# ====================================================================================================
# 1. CLIENTES POR ESTADO Y CIUDAD ====================================================================
# ====================================================================================================



import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
# librería para geolocalización 
# instalar en environment con pip install streamlit pandas geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

import matplotlib.pyplot as plt
import numpy as np

#titulo
st.title("📊 CLIENTES POR ESTADO Y CIUDAD")
st.subheader("Filtrado dinámico por fechas de todos los pedidos")


# CARGA DE DATOS CACHEADA
@st.cache_data
def load_data():
    # Carga del dataset
    csv_customers_dataset = pd.read_csv('resources/customers_dataset.csv')
    csv_orders_dataset = pd.read_csv('resources/orders_dataset.csv')
    # Comprobación de nulos en fecha antes del casting
    csv_orders_dataset['order_purchase_timestamp'].isna().any()
    
    # Casting a fecha
    csv_orders_dataset['order_purchase_timestamp'] = csv_orders_dataset['order_purchase_timestamp'].apply(pd.to_datetime)
    
    merge_data_to_compare = pd.merge(csv_orders_dataset,csv_customers_dataset, on='customer_id')
    
    # '''
    # Para realizar el filtro tomamos la fecha de compra desde orders_dataset, para compararlo con la fecha actual.
    # '''
    

    # delivered_orders = merge_data_to_compare[merge_data_to_compare['order_status'] == 'delivered']
    
    # customers_by_city_state = csv_customers_dataset.groupby(
    #     ['customer_state', 'customer_city']
    # )['customer_id'].nunique().reset_index()
    
    # customers_by_city_state.sort_values('customer_unique_id',ascending=False)
    # dfcustomer = customers_by_city_state.sort_values('customer_unique_id',ascending=False)


    return csv_customers_dataset, csv_orders_dataset, merge_data_to_compare
csv_customers_dataset, csv_orders_dataset, merge_data_to_compare = load_data()
    

# SLIDE CON RANGO DE FECHAS
minima = merge_data_to_compare['order_purchase_timestamp'].min().to_pydatetime()
maxima = merge_data_to_compare['order_purchase_timestamp'].max().to_pydatetime()

# Filtrar por rango de fechas (1 semana)-----------------------------------------
# Crea un control deslizante de fecha y hora con un rango de una semana (7 días)
# https://docs.kanaries.net/es/topics/Python/streamlit-datetime-slider

# selected_date = st.slider(
#     "Selecciona un rango de fechas",
#     min_value=minima,
#     max_value=maxima,
#     value=(minima, maxima),
#     step=timedelta(days=7),
# )

# fecha_inicio, fecha_fin = selected_date


# # FILTRO POR FECHAS SLIDE
# df_filtrado = merge_data_to_compare[
#     (merge_data_to_compare['order_purchase_timestamp'] >= fecha_inicio) &
#     (merge_data_to_compare['order_purchase_timestamp'] <= fecha_fin)
# ]



# FILTRO DECHAS DATETIME INPUT (seleccionador de fechas mostrado en dos columnas)
import datetime

col1, col2 = st.columns(2)

with col1:
    min_date = st.datetime_input(
        "Selecciona fecha inicio",
        value=minima,
        min_value=minima,
        max_value=maxima
    )


with col2:
    max_date = st.datetime_input(
        "Selecciona fecha fin",
        value=maxima,
        min_value=minima,
        max_value=maxima
    )


st.write("Desde: ", min_date)
st.write("Hasta: ", max_date)

# filtro por fechas datetime input
df_filtrado = merge_data_to_compare[
    (merge_data_to_compare['order_purchase_timestamp'] >= min_date) &
    (merge_data_to_compare['order_purchase_timestamp'] <= max_date)
]



# AGRUPACIÓN Y FILTRADO
dfcustomer_filtrado = df_filtrado.groupby(
    ['customer_state', 'customer_city']
)['customer_id'].nunique().reset_index().sort_values('customer_id', ascending=False)

st.table(dfcustomer_filtrado, height=300)



# minima
# maxima

# Filtrar por rango de fechas (1 semana)-----------------------------------------
# Crea un control deslizante de fecha y hora con un rango de una semana

#datetime(2020, 1, 1)
#campo a splitear order_purchase_timestamp


# start_date = datetime(2020, 1, 1)
# end_date = datetime(maxima)







# ====================================================================================================
# 2. PEDIDOS POR CIUDAD ==============================================================================
# ====================================================================================================

# A la tabla anterior añade las siguientes columnas:
#    - Número de pedidos
#    - Porcentaje que representan respecto al total de pedidos
# Además, representa el ratio de pedidos por cliente, utilizando el tipo de gráfico que consideres más adecuado.

# Tras este análisis, responde a las siguientes cuestiones:
# ¿Qué información o patrones se pueden identificar a partir de estos datos?
# ¿Qué acciones, como analista de datos, crees que debería tomar la empresa para mejorar sus ventas?


# agrupar por estado y ciudad del ciente
orders_by_city = merge_data_to_compare.groupby(
    ['customer_state', 'customer_city']
)['order_id'].nunique().reset_index()


#total de pedidos únicos en el dataset
total_orders = merge_data_to_compare['order_id'].nunique()

# añadir columna para represetnar porcentaje de pedidos por ciudad respecto al total
orders_by_city['order_percentage'] = (
    orders_by_city['order_id'] / total_orders
) * 100

# calcular número de clientes únicos
customers_by_city = merge_data_to_compare.groupby(
    ['customer_state', 'customer_city']
)['customer_id'].nunique().reset_index()

#nuevo dataframe con la fusión
city_stats = pd.merge(
    customers_by_city,
    orders_by_city,
    on=['customer_state', 'customer_city']
)
# ordenar resultados
city_stats = city_stats.sort_values('customer_id', ascending=False)

# REPRESENTACIÓN EN GRÁFICO DE BARRAS
#número de pedidos
#    - Número de pedidos
#    - Porcentaje que representan respecto al total de pedidos

st.title("📊 RATIO DE PEDIDOS POR CIUDAD")
# dibujar tabla completa
#st.table(city_stats, height=300)

# dibujar gráfico de barras -----------------------------------------------------------------------

# calcular ratio
city_stats['orders_per_customer'] = city_stats['order_id'] / city_stats['customer_id']

# selector para filtrar
col1, col2 = st.columns(2)

with col1:
    # selector de estado (customer_state)
    selected_state = st.selectbox("Selecciona un estado", options=["Todos"] + sorted(city_stats['customer_state'].unique()))

#filtrar por estado
if selected_state != "Todos":
    filtered = city_stats[city_stats['customer_state'] == selected_state]
else:
    filtered = city_stats.copy()

with col2:
    # selector de ciudad (customer_city) que depende del estado seleccionado
    selected_city = st.selectbox("Selecciona una ciudad", options=["Todas"] + sorted(filtered['customer_city'].unique()))

#filtrar por ciudad
if selected_city != "Todas":
    filtered = filtered[filtered['customer_city'] == selected_city]

#st.bar_chart(data = city_stats.set_index('customer_city')['order_percentage'])

# mostrar gráfico de barras filtrado
st.subheader("Ratio de pedidos por cliente")
#st.bar_chart(data=filtered.set_index('customer_city')['orders_per_customer'])


# ordenar por ratio
filtered = filtered.sort_values('order_percentage', ascending=False)
top_n = st.slider("Número de ciudades a mostrar", 5, 100, 15)
top_filtered = filtered.head(top_n)
st.bar_chart(top_filtered.set_index('customer_city')['order_percentage'])



# tabla filtrada
st.subheader("Datos filtrados (tabla)")
st.dataframe(filtered[['customer_state', 'customer_city', 'customer_id', 'order_id', 'order_percentage', 'orders_per_customer']])




# ====================================================================================================
# 3. ANÁLISIS DE RETRASOS EN PEDIDOS =================================================================
# ====================================================================================================





# ====================================================================================================
# 4. REVIEWS Y SATISFACCIÓN DEL CLIENTE ==============================================================
# ====================================================================================================




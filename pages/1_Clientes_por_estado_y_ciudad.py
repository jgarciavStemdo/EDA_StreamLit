import streamlit as st
import pandas as pd

import datetime
from datetime import datetime, timedelta
# librería para geolocalización
# instalar en environment con pip install streamlit pandas geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

import matplotlib.pyplot as plt
import numpy as np

# INSTALAR FOLIUM EN ENTORNO VIRTUAL: pip install folium streamlit-folium
import folium
from streamlit_folium import st_folium


# ====================================================================================================
# 1. CLIENTES POR ESTADO Y CIUDAD ====================================================================
# ====================================================================================================
# Representa una clasificación del número de clientes por estado. Crea una tabla en la que se muestren:
#    - Estado
#    - Ciudad
#    - Número de clientes por ciudad
# Tanto la tabla como los gráficos deberán ser dinámicos respecto a la fecha para permitir el
# análisis temporal de la evolución de clientes.


# ====================================================================================================
# CARGA DE DATASET EN CACHÉ
# ====================================================================================================

@st.cache_data
def load_data():
    # Carga del dataset
    csv_customers_dataset = pd.read_csv('streamlit_resources/customers_dataset.csv')
    #st.write(csv_customers_dataset.columns)
    csv_orders_dataset = pd.read_csv('streamlit_resources/orders_dataset.csv')
    # Comprobación de nulos en fecha antes del casting
    csv_orders_dataset['order_purchase_timestamp'].isna().any()

    # Casting a fecha
    csv_orders_dataset['order_purchase_timestamp'] = csv_orders_dataset['order_purchase_timestamp'].apply(pd.to_datetime)

    merge_data_to_compare = pd.merge(csv_orders_dataset,csv_customers_dataset, on='customer_id')

    return csv_customers_dataset, csv_orders_dataset, merge_data_to_compare
csv_customers_dataset, csv_orders_dataset, merge_data_to_compare = load_data()

# Título
st.markdown("""
<div style="
    background-color: #ffffff;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin-top: 25px;
    margin-bottom: 25px;">
    <h2 style="margin-top: 0;">📊 CLIENTES POR ESTADO Y CIUDAD</h2>
</div>
""", unsafe_allow_html=True)

# ====================================================================================================
# SELECTORES DE RANGO DE FECHA
# ====================================================================================================

st.subheader("Filtrado dinámico por fechas de todos los pedidos")

# Obtener fecha máxima y mínima del dataset
minima = merge_data_to_compare['order_purchase_timestamp'].min().to_pydatetime()
maxima = merge_data_to_compare['order_purchase_timestamp'].max().to_pydatetime()

# Seleccionador de fechas mostrado en dos columnas
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


# st.write("Desde: ", min_date)
# st.write("Hasta: ", max_date)

# filtro por fechas datetime input
df_filtrado = merge_data_to_compare[
    (merge_data_to_compare['order_purchase_timestamp'] >= min_date) &
    (merge_data_to_compare['order_purchase_timestamp'] <= max_date)
]


# ====================================================================================================
# CLIENTES TOTALES HASTA FECHA FILTRADA
# ====================================================================================================

clientes_totales_filtrado = df_filtrado['customer_unique_id'].nunique()


# ====================================================================================================
# MEDIA DE CLIENTES POR MES
# ====================================================================================================

clientes_mensuales = df_filtrado.groupby(
    df_filtrado['order_purchase_timestamp'].dt.to_period('M')
)['customer_unique_id'].nunique()

media_clientes_mensual = clientes_mensuales.mean()


# REPRESENTACIÓN DE MÉTRICAS EN COLUMNAS
mt1, mt2 = st.columns(2)

with mt1:
    st.metric(
        label=f"Clientes totales hasta {max_date.date()}",
        value=clientes_totales_filtrado
    )
    
with mt2:
    st.metric(
        label="Media de clientes mensuales",
        value=round(media_clientes_mensual, 2)
    )

# ====================================================================================================
# AGRUPACIÓN Y FILTRADO DE DATOS
# ====================================================================================================
dfcustomer_filtrado = df_filtrado.groupby(
    ['customer_state', 'customer_city']
)['customer_id'].nunique().reset_index().sort_values('customer_id', ascending=False)

st.table(dfcustomer_filtrado, height=300)


# ====================================================================================================
# GEOLOCALIZACIÓN CACHE
# ====================================================================================================

@st.cache_data
def geocodificar_ciudades(ciudades_estados):
    geolocator = Nominatim(user_agent="streamlit_dashboard")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    coords = {}
    for ciudad, estado in ciudades_estados:
        try:
            location = geocode(f"{ciudad}, Brazil")
            if location:
                coords[(ciudad, estado)] = (location.latitude, location.longitude)
        except Exception:
            pass
    return coords

# ====================================================================================================
# AGRUPACIÓN Y FILTRADO DE CLIENTES
# ====================================================================================================

dfcustomer_filtrado = df_filtrado.groupby(
    ['customer_state', 'customer_city']
)['customer_id'].nunique().reset_index().sort_values('customer_id', ascending=False)
dfcustomer_filtrado = dfcustomer_filtrado.rename(columns={'customer_id': 'num_clientes'})

# ====================================================================================================
# CONSTRUCCIÓN DE MAPA
# ====================================================================================================
# https://www.youtube.com/watch?v=gWV1gbeB-IM
# https://github.com/clint-kristopher-morris/Tutorials/blob/main/streamlit-part-1/app.py

def construir_mapa(ciudades_estados, max_clientes, filas):
    # Selector del tipo de mapa a pintar
    tipo_mapa = st.selectbox( "Tipo de mapa", ["cartodbpositron", "cartodbdark_matter", "OpenStreetMap"] )
    
    m = folium.Map(location=[-14.235, -51.925], zoom_start=4, tiles=tipo_mapa)
    coords = geocodificar_ciudades(ciudades_estados)

    for ciudad, estado, num in filas:
        key = (ciudad, estado)
        if key not in coords:
            continue

        lat, lon = coords[key]
        radio = 5 + (num / max_clientes) * 25

        if num > max_clientes * 0.5:
            color = '#E24B4A'
        elif num > max_clientes * 0.2:
            color = '#ED8E2F'
        else:
            color = '#378ADD'

        folium.CircleMarker(
            location=[lat, lon],
            radius=radio,
            color=color,
            stroke=False,
            fill=True,
            fill_color=color,
            fill_opacity=0.6,
            tooltip=f"{ciudad.title()} ({estado}): {num} clientes"
        ).add_to(m)

    return m

st.subheader("Mapa de distribución de clientes por ciudad (top 100)")

# Filtrado de mapa para ver n ciudades top por número de clientes
#top_n = st.slider("Número de ciudades con más clientes a mostrar", 5, 400, 100)
top_ciudades = dfcustomer_filtrado.head(100)
max_clientes = dfcustomer_filtrado['num_clientes'].max()
# con tuple se cachea el resultado 
pares_ciudad_estado = tuple(zip(top_ciudades['customer_city'], top_ciudades['customer_state']))
with st.spinner("Cargando mapa..."):
    coords = geocodificar_ciudades(pares_ciudad_estado)

filas = tuple(zip(top_ciudades['customer_city'], top_ciudades['customer_state'], top_ciudades['num_clientes']))

m = construir_mapa(pares_ciudad_estado, max_clientes, filas)

map_data = st_folium(m, height=500, use_container_width=True)



import streamlit as st
import pandas as pd

import datetime
from datetime import datetime, timedelta

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

# ====================================================================================================
# FILTRADO DE DATOS POR FECHAS
# ====================================================================================================

df_filtrado = merge_data_to_compare[
    (merge_data_to_compare['order_purchase_timestamp'] >= min_date) &
    (merge_data_to_compare['order_purchase_timestamp'] <= max_date)
]


# ====================================================================================================
# CLIENTES TOTALES HASTA FECHA FILTRADA
# ====================================================================================================

clientes_totales_filtrado = df_filtrado['customer_unique_id'].nunique()



# ====================================================================================================
# CLIENTES ACTIVOS POR DÍA EN EL RANGO SELECCIONADO
# ====================================================================================================

clientes_diarios = df_filtrado.groupby(df_filtrado['order_purchase_timestamp'].dt.date)['customer_unique_id'].nunique()

media_clientes_diaria = clientes_diarios.mean()

rango_dias = (max_date - min_date).days + 1


# ====================================================================================================
# CLIENTES NUEVOS EN EL PERIODO SELECCIONADO
# ====================================================================================================

cliente_primer_pedido = (merge_data_to_compare.groupby('customer_unique_id')['order_purchase_timestamp'].min().reset_index())

# Clientes nuevos en el rango de fecha filtrado
clientes_nuevos = cliente_primer_pedido[
    (cliente_primer_pedido['order_purchase_timestamp'] >= min_date) &
    (cliente_primer_pedido['order_purchase_timestamp'] <= max_date)
]

# total de clientes nuevos en el periodo
total_clientes_nuevos = clientes_nuevos['customer_unique_id'].nunique()


# ====================================================================================================
# MEDIA DIARIA DE CLIENTES NUEVOS EN EL PERIODO SELECCIONADO
# ====================================================================================================

clientes_nuevos_diarios = clientes_nuevos.groupby(clientes_nuevos['order_purchase_timestamp'].dt.date)['customer_unique_id'].nunique()

# media mensual de clientes nuevos
media_clientes_nuevos = clientes_nuevos_diarios.mean()


# ====================================================================================================
# REPRESENTACIÓN DE MÉTRICAS EN COLUMNAS
# ====================================================================================================
mt1, mt2 = st.columns(2)

with mt1:
    st.metric(
        label=f"Clientes únicos activos de {min_date.date()} a {max_date.date()}",
        value=clientes_totales_filtrado
    )
    
with mt2:
    st.metric(
        label=f"Media diaria de clientes ativos ({rango_dias} días)",
        value=round(media_clientes_diaria, 2)
    )
    

mt3, mt4 = st.columns(2)
  
with mt3:
    st.metric(
        label=f"Clientes nuevos de {min_date.date()} a {max_date.date()}",
        value=total_clientes_nuevos
    )
    
with mt4:
    st.metric(
        label=f"Media diaria de clientes nuevos ({rango_dias} días)",
        value=round(media_clientes_nuevos, 2)
    )

# ====================================================================================================
# AGRUPACIÓN Y FILTRADO DE DATOS
# ====================================================================================================
dfcustomer_filtrado = df_filtrado.groupby(
    ['customer_state', 'customer_city']
)['customer_id'].nunique().reset_index().sort_values('customer_id', ascending=False)

st.table(dfcustomer_filtrado, height=300)


# ====================================================================================================
# CARGA DE COORDENADAS DESDE CSV GENERADO EN generar_coordenadas.py
# ====================================================================================================

@st.cache_data
def load_coords():
    df = pd.read_csv('streamlit_resources/cities_coords.csv').dropna(subset=['lat', 'lon'])
    return {
        (row['customer_city'], row['customer_state']): (row['lat'], row['lon'])
        for _, row in df.iterrows()
    }

coords_globales = load_coords()

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

def construir_mapa(max_clientes, filas):
    # Selector del tipo de mapa a pintar
    tipo_mapa = st.selectbox( "Tipo de mapa", ["cartodbpositron", "cartodbdark_matter", "OpenStreetMap"] )
    
    m = folium.Map(location=[-14.235, -51.925], zoom_start=4, tiles=tipo_mapa)

    for ciudad, estado, num in filas:
        key = (ciudad, estado)
        if key not in coords_globales:
            continue

        lat, lon = coords_globales[key]
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

st.subheader("Mapa de distribución de clientes por ciudad")

# Filtrado de mapa para ver n ciudades top por número de clientes
top_n = st.slider("Número de ciudades con más clientes a mostrar", 5, 4500, 100)
top_ciudades = dfcustomer_filtrado.head(top_n)
max_clientes = dfcustomer_filtrado['num_clientes'].max()

filas = tuple(zip(top_ciudades['customer_city'], top_ciudades['customer_state'], top_ciudades['num_clientes']))

m = construir_mapa(max_clientes, filas)
map_data = st_folium(m, height=500, use_container_width=True)



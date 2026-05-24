import streamlit as st
import pandas as pd

import folium
from streamlit_folium import st_folium

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter


# ====================================================================================================
# CARGA DE DATASET EN CACHÉ
# ====================================================================================================

@st.cache_data
def load_data():

    csv_customers_dataset = pd.read_csv('streamlit_resources/customers_dataset.csv')
    csv_orders_dataset = pd.read_csv('streamlit_resources/orders_dataset.csv')
    csv_order_items_dataset = pd.read_csv('streamlit_resources/order_items_dataset.csv')
    csv_sellers_dataset = pd.read_csv('streamlit_resources/sellers_dataset.csv')

    csv_orders_dataset['order_purchase_timestamp'] = pd.to_datetime(
        csv_orders_dataset['order_purchase_timestamp']
    )

    return csv_customers_dataset, csv_orders_dataset, csv_order_items_dataset, csv_sellers_dataset


csv_customers_dataset, csv_orders_dataset, csv_order_items_dataset, csv_sellers_dataset = load_data()


# ====================================================================================================
# MERGE BASE
# ====================================================================================================

merge_sellers_customer_order = csv_orders_dataset.merge(csv_customers_dataset,on='customer_id').merge(csv_order_items_dataset,on='order_id').merge(csv_sellers_dataset,on='seller_id')

# ====================================================================================================
# RUTAS COMERCIALES
# ====================================================================================================

seller_customer_flow = merge_sellers_customer_order.groupby(['seller_city','customer_city'])['order_id'].nunique().reset_index()

seller_customer_flow = seller_customer_flow.rename(columns={'order_id': 'Número de pedidos'})

seller_customer_flow = seller_customer_flow.sort_values('Número de pedidos',ascending=False)

# ====================================================================================================
# GEOLOCALIZACIÓN CACHE
# ====================================================================================================

@st.cache_data
def geocodificar(ciudades):

    geolocator = Nominatim(user_agent="streamlit_routes")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

    coords = {}

    for ciudad in ciudades:
        try:
            location = geocode(f"{ciudad}, Brazil")
            if location:
                coords[ciudad] = (location.latitude, location.longitude)
        except:
            pass

    return coords


# ====================================================================================================
# MAPA
# ====================================================================================================

# Título
st.markdown("""
<div style="
    background-color: #ffffff;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin-top: 25px;
    margin-bottom: 25px;">
    <h2 style="margin-top: 0;">🌍 FLUJOS DE COMPRA ENTRE CIUDADES</h2>
</div>
""", unsafe_allow_html=True)

# Top 150 rutas
top_routes = seller_customer_flow.head(150)

ciudades = tuple(
    set(top_routes['seller_city']).union(set(top_routes['customer_city']))
)

with st.spinner("Cargando mapa..."):
    coords = geocodificar(ciudades)


def construir_mapa(df, coords):

    tipo_mapa = st.selectbox(
        "Tipo de mapa",
        ["cartodbpositron", "cartodbdark_matter", "OpenStreetMap"]
    )

    m = folium.Map(location=[-14.235, -51.925], zoom_start=4, tiles=tipo_mapa)

    max_pedidos = df['Número de pedidos'].max()

    for _, row in df.iterrows():

        origen = row['seller_city']
        destino = row['customer_city']
        peso = row['Número de pedidos']

        if origen not in coords or destino not in coords:
            continue

        lat1, lon1 = coords[origen]
        lat2, lon2 = coords[destino]

        folium.PolyLine(
            locations=[(lat1, lon1), (lat2, lon2)],
            weight=1,
            color="blue",
            opacity=0.5
        ).add_to(m)

        folium.CircleMarker(
            location=[lat1, lon1],
            radius=4,
            color="red",
            fill=True,
            fill_opacity=0.8,
            tooltip=f"Vendedor: {origen}"
        ).add_to(m)

        folium.CircleMarker(
            location=[lat2, lon2],
            radius=4,
            color="green",
            fill=True,
            fill_opacity=0.8,
            tooltip=f"Cliente: {destino}"
        ).add_to(m)

    return m


m = construir_mapa(top_routes, coords)

st.markdown("""
### Leyenda
- 🔴 Vendedor
- 🟢 Cliente
""")

st_folium(m, height=600, use_container_width=True)
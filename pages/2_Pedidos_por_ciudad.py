import streamlit as st
import pandas as pd


# cargar datos 
@st.cache_data
def load_data():
    csv_customers_dataset = pd.read_csv('resources/customers_dataset.csv')
    csv_orders_dataset = pd.read_csv('resources/orders_dataset.csv')
    csv_orders_dataset['order_purchase_timestamp'] = pd.to_datetime(csv_orders_dataset['order_purchase_timestamp'])
    merge_data_to_compare = pd.merge(csv_orders_dataset, csv_customers_dataset, on='customer_id')
    return csv_customers_dataset, csv_orders_dataset, merge_data_to_compare

csv_customers_dataset, csv_orders_dataset, merge_data_to_compare = load_data()



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



orders_by_city = merge_data_to_compare.groupby(
    ['customer_state', 'customer_city']
)['order_id'].count().reset_index()

total_orders = merge_data_to_compare['order_id'].nunique()

orders_by_city['order_percentage'] = (
    orders_by_city['order_id'] / total_orders
) * 100

customers_by_city = merge_data_to_compare.groupby(
    ['customer_state', 'customer_city']
)['customer_unique_id'].nunique().reset_index()

city_stats = pd.merge(
    customers_by_city,
    orders_by_city,
    on=['customer_state', 'customer_city']
)

# customer_unique_id identifica al cliente REAL (siempre el mismo aunque haga varios pedidos)
# customer_id cambia en cada pedido, por eso sirve para contar pedidos, no clientes
# order_id es el identificador del pedido
city_stats['orders_per_customer'] = (
    city_stats['order_id'] / city_stats['customer_unique_id']
).round(2)

city_stats = city_stats.rename(columns={
    'order_id': 'Número de pedidos',
    'order_percentage': 'Porcentaje de pedidos',
    'customer_unique_id': 'Número de clientes',
    'orders_per_customer':'Ratio de pedidos por cliente'
})

city_stats.sort_values('Número de clientes', ascending=False)




# REPRESENTACIÓN GRÁFICA --------------------------------------------------------------------------------
#número de pedidos
#    - Número de pedidos
#    - Porcentaje que representan respecto al total de pedidos


#titulo
st.markdown("""
<div style="
    background-color: #ffffff;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin-top: 25px;
    margin-bottom: 25px;">
    <h2 style="margin-top: 0;">📊 RATIO DE PEDIDOS POR CIUDAD</h2>
</div>
""", unsafe_allow_html=True)



# dibujar tabla completa
#st.table(city_stats, height=300)

# dibujar gráfico de barras -----------------------------------------------------------------------

# calcular ratio
#city_stats['orders_per_customer'] = city_stats['order_id'] / city_stats['customer_id']

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
filtered = filtered.sort_values('Porcentaje de pedidos', ascending=False)
top_n = st.slider("Número de ciudades a mostrar", 5, 100, 15)
top_filtered = filtered.head(top_n)
st.bar_chart(top_filtered.set_index('customer_city')['Porcentaje de pedidos'])


# tabla filtrada
st.subheader("Datos filtrados (tabla)")
st.dataframe(filtered[['customer_state', 
                       'customer_city', 
                       'Número de clientes', 
                       'Número de pedidos', 
                       'Porcentaje de pedidos', 
                       'Ratio de pedidos por cliente']])


# Preguntas
st.subheader("Cuestiones")

with st.expander("¿Qué información o patrones se pueden identificar a partir de estos datos?"):
    st.write('''
        The chart above shows some numbers I picked for you.
        I rolled actual dice for these, so they're *guaranteed* to
        be random.
    ''')
with st.expander("¿Qué acciones, como analista de datos, crees que debería tomar la empresa para **mejorar sus ventas**?"):
    st.write('''
        The chart above shows some numbers I picked for you.
        I rolled actual dice for these, so they're *guaranteed* to
        be random.
    ''')

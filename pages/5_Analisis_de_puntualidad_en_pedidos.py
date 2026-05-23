import streamlit as st
import pandas as pd
#importar librería altair
import altair as alt


# cargar datos
@st.cache_data
def load_data():
    csv_customers_dataset = pd.read_csv('streamlit_resources/customers_dataset.csv')
    csv_orders_dataset = pd.read_csv('streamlit_resources/orders_dataset.csv')
    csv_orders_dataset['order_purchase_timestamp'] = pd.to_datetime(csv_orders_dataset['order_purchase_timestamp'])
    merge_data_to_compare = pd.merge(csv_orders_dataset, csv_customers_dataset, on='customer_id')
    return csv_customers_dataset, csv_orders_dataset, merge_data_to_compare

csv_customers_dataset, csv_orders_dataset, merge_data_to_compare = load_data()

delivered_orders = merge_data_to_compare[merge_data_to_compare['order_status'] == 'delivered']



# ====================================================================================================
# 5. ANÁLISIS DE RETRASOS PUNTUALES =================================================================
# ====================================================================================================
# Calcula y representa:
#     - Número de pedidos que llegan antes por ciudad
#     - Porcentaje de pedidos anticipados respecto al total de pedidos de la ciudad
#     - Tiempo medio de anticipación en días



st.markdown("""
<div style="
    background-color: #ffffff;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin-top: 25px;
    margin-bottom: 25px;">
    <h2 style="margin-top: 0;">⏱️ ANÁLISIS DE PEDIDOS PUNTUALES</h2>
</div>
""", unsafe_allow_html=True)



# Convertir columnas a fecha
delivered_orders['order_delivered_customer_date'] = pd.to_datetime(delivered_orders['order_delivered_customer_date'])
delivered_orders['order_estimated_delivery_date'] = pd.to_datetime(delivered_orders['order_estimated_delivery_date'])

# Pedidos retrasados
delivered_orders['is_earlier'] = (delivered_orders['order_delivered_customer_date'].dt.date < delivered_orders['order_estimated_delivery_date'].dt.date)

# Número de pedidos retrasados por ciudad
earlier_by_city = delivered_orders.groupby(
    ['customer_state', 'customer_city']
)['is_earlier'].sum().reset_index()

# Total de pedidos por ciudad
total_by_city = delivered_orders.groupby(
    ['customer_state', 'customer_city']
)['order_id'].count().reset_index()

advance_all_stats = total_by_city.merge(earlier_by_city, on=["customer_state","customer_city"])

advance_all_stats['Porcentaje anticipados'] = (
    advance_all_stats['is_earlier'] / advance_all_stats['order_id'] * 100
).round(2)

# Días de retraso
delivered_orders['advance_days'] = (delivered_orders['order_estimated_delivery_date'] - delivered_orders['order_delivered_customer_date']).dt.days

# Retraso medio por ciudad
avg_advance_by_city = delivered_orders[delivered_orders['is_earlier']].groupby(
    ['customer_state', 'customer_city']
)['advance_days'].mean().reset_index()

advance_all_stats = advance_all_stats.merge(
    avg_advance_by_city,
    on=['customer_state', 'customer_city'],
)

advance_all_stats = advance_all_stats.rename(columns={
    'order_id': 'Total pedidos',
    'is_earlier': 'Pedidos anticipados',
    'advance_days':'Anticipación media en días'
})

advance_all_stats.sort_values(by='Total pedidos',ascending=False)




# REPRESENTACIÓN GRÁFICA --------------------------------------------------------------------------------

st.subheader("Evolución temporal de anticipos por ciudad")


# gráfico 1 ___________________________________________________________________
#     - Número de pedidos que llegan antes por ciudad
# top 15 ciudades con más pedidos
top_cities = (advance_all_stats.sort_values('Total pedidos', ascending=False).head(15).sort_values('Porcentaje anticipados', ascending=False))

bar_pct = alt.Chart(top_cities).mark_bar().encode(
    x=alt.X('Porcentaje anticipados:Q', title='% pedidos anticipados'),
    y=alt.Y('customer_city:N', sort='-x', title='Ciudad'),
    color=alt.value("#12DB62"),
    tooltip=[
        alt.Tooltip('customer_city:N', title='Ciudad'),
        alt.Tooltip('Porcentaje anticipados:Q', title='% anticipados', format='.1f'),
        alt.Tooltip('Total pedidos:Q', title='Total pedidos'),
    ]
)

# gráfico 2 ___________________________________________________________________
#     - Tiempo medio de anticipación en días
bar_days = alt.Chart(top_cities).mark_bar().encode(
    x=alt.X('Anticipación media en días:Q', title='Días de anticipo medio'),
    y=alt.Y('customer_city:N', sort='-x', title='Ciudad'),
    color=alt.value("#ED9A00"),
    tooltip=[
        alt.Tooltip('customer_city:N', title='Ciudad'),
        alt.Tooltip('Anticipación media en días:Q', title='Días de anticipación', format='.1f'),
        alt.Tooltip('Porcentaje anticipados:Q', title='% anticipados', format='.1f'),
    ]
)



# pintar gráficos
topporcentaje, topdias = st.columns(2)

with topporcentaje:
    st.subheader("Top ciudades con mayor % de pedidos anticipados")
    st.altair_chart(bar_pct, use_container_width=True)

with topdias:
    st.subheader("Top ciudades con más días de anticipación media")
    st.altair_chart(bar_days, use_container_width=True)




st.subheader("Porcentaje de pedidos anticipados respecto al total de pedidos de la ciudad")

# selector para filtrar
col1, col2 = st.columns(2)

with col1:
    # selector de estado (customer_state)
    city_stats = sorted(delivered_orders['customer_state'].unique())
    selected_state = st.selectbox("Selecciona un estado", options=["Todos"] + city_stats)

#filtrar por estado
if selected_state != "Todos":
    filtered = delivered_orders[delivered_orders['customer_state'] == selected_state]
else:
    filtered = delivered_orders.copy()

with col2:
    # selector de ciudad (customer_city) que depende del estado seleccionado
    selected_city = st.selectbox("Selecciona una ciudad", options=["Todas"] + sorted(filtered['customer_city'].unique()))

#filtrar por ciudad
if selected_city != "Todas":
    df_city = filtered[filtered['customer_city'] == selected_city]
else:
    df_city = filtered.copy()

    
    

# gráfico 3 ___________________________________________________________________
#     - Porcentaje de pedidos retrasados respecto al total de pedidos de la ciudad
#usar Altair con doble eje Y (para total de pedidos y para porcentaje sobre esos pedidos)

if selected_state != "Todos":
    chart_data = advance_all_stats[advance_all_stats['customer_state'] == selected_state]
else:
    chart_data = advance_all_stats.copy()
    

if selected_city != "Todas":
    chart_data = chart_data[chart_data['customer_city'] == selected_city]
else:
    chart_data = chart_data.copy()
    
chart_data = chart_data.sort_values('Total pedidos', ascending=False).head(30).copy()


# normalizar total de pedidos a escala 100 para comparar con porcentaje
chart_data['Total pedidos normalizado'] = (chart_data['Total pedidos'] / chart_data['Total pedidos'].max() * 100).round(2)

if df_city['is_earlier'].sum() != 0:
    
    # KPIs
    kpi_total = len(df_city)
    kpi_earlier = df_city['is_earlier'].sum()
    kpi_pct = round((kpi_earlier / kpi_total) * 100, 2) if kpi_total > 0 else 0
    kpi_advance = round(df_city[df_city['is_earlier']]['advance_days'].mean(), 2) if kpi_earlier > 0 else 0

    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.metric("Total pedidos", kpi_total)
    with k2:
        st.metric("Pedidos anticipados", kpi_earlier)
    with k3:
        st.metric("Porcentaje sobre el total", f"{kpi_pct}%")
    with k4:
        st.metric("Anticipación media (días)", kpi_advance)
        
    #dibujar gráfico
    st.bar_chart(chart_data,
        x='customer_city',
        y=['Porcentaje anticipados', 'Total pedidos normalizado'],
        color=["#AFDB12", "#586D5C"],
        horizontal=True,
        x_label='Ciudad',
        y_label='*Se muestran las 30 ciudades con mayor número de pedidos. Cifra normalizada a escala 0-100'
    )
    #dibujar tabla
    chart_data['Anticipación media en días'] = chart_data['Anticipación media en días'].round(2)
    st.dataframe(chart_data[['customer_state', 
                       'customer_city', 
                       'Total pedidos', 
                       'Pedidos anticipados', 
                       'Porcentaje anticipados', 
                       'Anticipación media en días']])
    
else:
    st.info(f"No hay pedidos anticipados registrados en {selected_city}")
    




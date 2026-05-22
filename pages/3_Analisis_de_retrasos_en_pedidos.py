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
# 3. ANÁLISIS DE RETRASOS EN PEDIDOS =================================================================
# ====================================================================================================
# Calcula y representa:
#     - Número de pedidos que llegan tarde por ciudad
#     - Porcentaje de pedidos retrasados respecto al total de pedidos de la ciudad
#     - Tiempo medio de retraso en días
# Además, al representar esta información, el dashboard deberá incluir un autodiagnóstico que indique 
# la razón más probable del problema.


st.markdown("""
<div style="
    background-color: #ffffff;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin-top: 25px;
    margin-bottom: 25px;">
    <h2 style="margin-top: 0;">⏱️ Análisis de retrasos en pedidos</h2>
</div>
""", unsafe_allow_html=True)




# Pedidos retrasados
delivered_orders['is_late'] = delivered_orders['order_delivered_customer_date'] > delivered_orders['order_estimated_delivery_date']

# Número de pedidos retrasados por ciudad
late_by_city = delivered_orders.groupby(
    ['customer_state', 'customer_city']
)['is_late'].sum().reset_index()

# Total de pedidos por ciudad
total_by_city = delivered_orders.groupby(
    ['customer_state', 'customer_city']
)['order_id'].count().reset_index()

delay_all_stats = total_by_city.merge(late_by_city, on=["customer_state","customer_city"])

delay_all_stats['Porcentaje retrasados'] = (
    delay_all_stats['is_late'] / delay_all_stats['order_id'] * 100
).round(2)

delay_all_stats = delay_all_stats.rename(columns={
    'order_id': 'Total pedidos',
    'is_late': 'Pedidos retrasados'
})

delay_all_stats.sort_values(by='Total pedidos',ascending=False)


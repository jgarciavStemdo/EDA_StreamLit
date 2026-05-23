import streamlit as st
import pandas as pd
import altair as alt

# cargar datos 
@st.cache_data
def load_data():
    csv_customers_dataset = pd.read_csv('streamlit_resources/customers_dataset.csv')
    csv_orders_dataset = pd.read_csv('streamlit_resources/orders_dataset.csv')
    csv_reviews_dataset = pd.read_csv('streamlit_resources/order_reviews_dataset.csv')
    csv_orders_dataset['order_purchase_timestamp'] = pd.to_datetime(csv_orders_dataset['order_purchase_timestamp'])
    merge_data_to_compare = pd.merge(csv_orders_dataset, csv_customers_dataset, on='customer_id')
    return csv_customers_dataset, csv_orders_dataset, csv_reviews_dataset, merge_data_to_compare

csv_customers_dataset, csv_orders_dataset, csv_reviews_dataset, merge_data_to_compare = load_data()

delivered_orders = merge_data_to_compare[merge_data_to_compare['order_status'] == 'delivered'].copy()
delivered_orders['order_delivered_customer_date'] = pd.to_datetime(delivered_orders['order_delivered_customer_date'])
delivered_orders['order_estimated_delivery_date'] = pd.to_datetime(delivered_orders['order_estimated_delivery_date'])
delivered_orders['delay_days'] = (
    delivered_orders['order_delivered_customer_date'] - delivered_orders['order_estimated_delivery_date']
).dt.days
delivered_orders['is_late'] = delivered_orders['delay_days'] > 0


# ====================================================================================================
# 4. REVIEWS Y SATISFACCIÓN DEL CLIENTE ==============================================================
# ====================================================================================================
# Calcula y representa:
#     - Número de reviews por estado
#     - Score medio de las reviews en cada estado
#
# Para este cálculo, se deberán excluir los pedidos con retraso, 
# ya que se entiende que la valoración negativa podría deberse principalmente 
# al retraso en la entrega del producto.

# Esto serán las métricas que tendrá que tener en el ejercicio calculadas 
# y representadas como mínimo, puedes añadir todas las que veas interesantes!

st.markdown("""
<div style="
    background-color: #ffffff;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin-top: 25px;
    margin-bottom: 25px;">
    <h2 style="margin-top: 0;">⭐ REVIEWS POR ESTADO (SIN RETRASOS)</h2>
</div>
""", unsafe_allow_html=True)


# ============================
# CÁLCULO DE MÉTRICAS
# ============================

reviews_products_delivered = delivered_orders.merge(
    csv_reviews_dataset[['order_id', 'review_score']],
    on='order_id'
)

# Filtrar solo pedidos entregados a tiempo
on_time_reviews = reviews_products_delivered[
    reviews_products_delivered['is_late'] == False
]

# Número de reviews por estado
reviews_by_state = on_time_reviews.groupby('customer_state')['review_score'].count().reset_index()

reviews_by_state = reviews_by_state.rename(columns={
    'review_score': 'Número de reviews totales'
})

# Score medio por estado
avg_score_by_state = on_time_reviews.groupby('customer_state')['review_score'].mean().round(2).reset_index()

avg_score_by_state = avg_score_by_state.rename(columns={
    'review_score':'Media de puntuación'
})

# Unir métricas
reviews_stats = reviews_by_state.merge(avg_score_by_state, on='customer_state').sort_values(by='Media de puntuación', ascending=False)


# ============================
# REPRESENTACIÓN STREAMLIT
# ============================

st.subheader("Tabla resumen de reviews por estado")
st.table(reviews_stats)


st.subheader("Número de reviews por estado")
st.bar_chart(
    data=reviews_stats,
    x='customer_state',
    y='num_reviews'
)


st.subheader("Score medio de reviews por estado")
st.bar_chart(
    data=reviews_stats,
    x='customer_state',
    y='score_medio'
)
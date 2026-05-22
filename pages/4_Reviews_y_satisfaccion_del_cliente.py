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








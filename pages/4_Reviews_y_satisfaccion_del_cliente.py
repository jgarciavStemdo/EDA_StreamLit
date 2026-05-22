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
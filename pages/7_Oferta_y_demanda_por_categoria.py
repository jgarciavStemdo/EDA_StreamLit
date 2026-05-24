import streamlit as st
import pandas as pd
import plotly.express as px

# ====================================================================================================
# Título
# ====================================================================================================
st.markdown("""
<div style="
    background-color: #ffffff;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    margin-top: 25px;
    margin-bottom: 25px;">
    <h2 style="margin-top: 0;">📊 Análisis de oferta y demanda por Categoría</h2>
</div>
""", unsafe_allow_html=True)

# ====================================================================================================
# Carga de datos
# ====================================================================================================
@st.cache_data
def load_data():
    df_customers = pd.read_csv('streamlit_resources/customers_dataset.csv')
    df_orders = pd.read_csv('streamlit_resources/orders_dataset.csv')
    df_items = pd.read_csv('streamlit_resources/order_items_dataset.csv')
    df_products = pd.read_csv('streamlit_resources/products_dataset.csv')
    df_translation = pd.read_csv('streamlit_resources/product_category_name_translation.csv')
    df_sellers = pd.read_csv('streamlit_resources/sellers_dataset.csv')
    
    df = df_orders.merge(df_customers, on='customer_id')
    df = df.merge(df_items, on='order_id')
    df = df.merge(df_products, on='product_id')
    df = df.merge(df_translation, on='product_category_name')
    df = df.merge(df_sellers, on='seller_id')
    
    # Crear columnas combinadas para ubicación
    df['customer_location'] = df['customer_city'] + ", " + df['customer_state']
    df['seller_location'] = df['seller_city'] + ", " + df['seller_state']
    
    return df

df = load_data()

# ====================================================================================================
# Top 3 mejores y peores categorías
# ====================================================================================================
st.markdown("#### Resumen General de Ventas por Categoría")

pedidos_por_categoria = df.groupby('product_category_name_english')['order_id'].nunique().sort_values(ascending=False)

top_3_categorias = pedidos_por_categoria.head(3)
bottom_3_categorias = pedidos_por_categoria.tail(3)

col1, col2 = st.columns(2)

with col1:
    st.markdown("##### 3 Categorías más compradas")
    for categoria, n_pedidos in top_3_categorias.items():
        nombre_limpio = categoria.replace('_', ' ').title()
        st.markdown(f"- **{nombre_limpio}:** {n_pedidos:,} pedidos")

with col2:
    st.markdown("##### 3 Categorías menos compradas")
    for categoria, n_pedidos in bottom_3_categorias.sort_values(ascending=True).items():
        nombre_limpio = categoria.replace('_', ' ')
        st.markdown(f"- **{nombre_limpio}:** {n_pedidos:,} pedidos")


# ====================================================================================================
# Selector de Categoría para análisis detallado
# ====================================================================================================
st.header("Selecciona una categoría para un análisis detallado")

lista_categorias = df['product_category_name_english'].unique()

categoria_seleccionada = st.selectbox(
    "Elige una categoría de producto:",
    lista_categorias
)


# ====================================================================================================
# Análisis para la categoría seleccionada
# ====================================================================================================
if categoria_seleccionada:
    
    st.subheader(f"Análisis para: **{categoria_seleccionada.replace('_', ' ')}**")
    
    # Filtrar el dataframe por la categoría seleccionada
    df_categoria = df[df['product_category_name_english'] == categoria_seleccionada]

    # Métrica Global de Pedidos
    total_orders = df_categoria['order_id'].nunique()
    
    st.metric(label="Número Total de Pedidos en esta Categoría", value=f"{total_orders:,}")

    col_graf1, col_graf2 = st.columns(2)

    # Compradores
    with col_graf1:
        st.markdown("#### 🛍️ Demanda: Top 10 Ciudades Compradoras")
        
        top_ciudades_compradoras = df_categoria.groupby('customer_location')['order_id'].nunique().nlargest(10).reset_index()
        top_ciudades_compradoras.rename(columns={'order_id': 'Numero de Pedidos'}, inplace=True)

        if not top_ciudades_compradoras.empty:
            fig_compradores = px.bar(
                top_ciudades_compradoras,
                x='Numero de Pedidos',
                y='customer_location',
                orientation='h',
                text='Numero de Pedidos'
            )
            fig_compradores.update_layout(
                yaxis_title="Ubicación del Comprador",
                xaxis_title="Número de Pedidos",
                yaxis={'categoryorder':'total ascending'}
            )
            st.plotly_chart(fig_compradores, use_container_width=True)
        else:
            st.info("No hay datos de demanda para esta categoría.")

    # Vendedores
    with col_graf2:
        st.markdown("#### 📈 Oferta: Top 10 Ciudades Vendedoras")
        
        top_ciudades_vendedoras = df_categoria.groupby('seller_location')['seller_id'].nunique().nlargest(10).reset_index()
        top_ciudades_vendedoras.rename(columns={'seller_id': 'Numero de Vendedores'}, inplace=True)

        if not top_ciudades_vendedoras.empty:
            fig_vendedores = px.bar(
                top_ciudades_vendedoras,
                x='Numero de Vendedores',
                y='seller_location',
                orientation='h',
                text='Numero de Vendedores'
            )
            fig_vendedores.update_layout(
                yaxis_title="Ubicación del Vendedor",
                xaxis_title="Número de Vendedores Únicos",
                yaxis={'categoryorder':'total ascending'}
            )
            st.plotly_chart(fig_vendedores, use_container_width=True)
        else:
            st.info("No hay datos de oferta para esta categoría.")
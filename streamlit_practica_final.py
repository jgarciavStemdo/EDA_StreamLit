import streamlit as st

st.set_page_config(
    page_title="Dashboard",
    page_icon="📦"
    #layout="wide"
)

st.title("📖 Practica final Python")

st.sidebar.success("Selecciona una opción")

st.markdown("""
Índice de contenidos:

1. **Clientes por estado y ciudad**  
2. **Pedidos por ciudad**  
3. **Análisis de retrasos en pedidos**  
4. **Reviews y satisfacción del cliente**

Usa el menú lateral para navegar entre las secciones.
""")



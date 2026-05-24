import pandas as pd
import unicodedata
import re

def normalizar(texto):
    """Normalizar texto"""
    if pd.isna(texto):
        return ""
    texto = str(texto).lower().strip()
    # Eliminar tildes y diacríticos
    texto = unicodedata.normalize('NFKD', texto)
    texto = ''.join(c for c in texto if not unicodedata.combining(c))
    # Eliminar caracteres especiales
    texto = re.sub(r'[^a-z0-9\s]', '', texto)
    texto = re.sub(r'\s+', ' ', texto).strip()
    return texto

customers = pd.read_csv('streamlit_resources/customers_dataset.csv')

url = "https://raw.githubusercontent.com/kelvins/municipios-brasileiros/main/csv/municipios.csv"
municipios = pd.read_csv(url)

# Normalizar ambos lados
municipios['nome_norm'] = municipios['nome'].apply(normalizar)
ciudades = customers[['customer_city', 'customer_state']].drop_duplicates()
ciudades['city_norm'] = ciudades['customer_city'].apply(normalizar)

merged = ciudades.merge(
    municipios[['nome_norm', 'latitude', 'longitude']],
    left_on='city_norm',
    right_on='nome_norm',
    how='left'
).drop(columns=['city_norm', 'nome_norm'])

merged = merged.rename(columns={'latitude': 'lat', 'longitude': 'lon'})
merged.to_csv('streamlit_resources/cities_coords.csv', index=False)

encontradas = merged['lat'].notna().sum()
total = len(merged)
print(f"{encontradas}/{total} ciudades geocodificadas ({round(encontradas/total*100)}%)")
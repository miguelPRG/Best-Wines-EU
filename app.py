import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Melhores Vinhos da UE", layout="wide")
st.title("🍷 Melhores Vinhos da União Europeia")

# Carregar dados
@st.cache_data
def load_data():
    df = pd.read_csv('./data/winemag-data-130k-v2.csv')
    eu = ['Portugal', 'France', 'Italy', 'Spain', 'Germany', 'Austria', 'Greece', 
          'Hungary', 'Romania', 'Bulgaria', 'Croatia', 'Slovenia', 'Slovakia', 
          'Czech Republic', 'Poland', 'Cyprus', 'Malta', 'Belgium', 'Netherlands', 
          'Luxembourg', 'Ireland', 'Denmark', 'Sweden', 'Finland', 'Estonia', 
          'Latvia', 'Lithuania']
    df_eu = df[df['country'].isin(eu)].copy()
    # Imputar preço por mediana por país (como no notebook)
    df_eu['price'] = df_eu.groupby('country')['price'].transform(lambda x: x.fillna(x.median()))
    df_eu['price'].fillna(df_eu['price'].median(), inplace=True)
    # Evitar divisão por zero
    df_eu = df_eu[df_eu['price'] > 0].copy()
    # Calcular pontos por euro uma vez
    df_eu['points_per_euro'] = df_eu['points'] / df_eu['price']
    return df_eu

df_eu = load_data()

# Métricas topo (refactor para evitar recomputos)
col1, col2, col3 = st.columns(3)
ranking = df_eu.groupby('country')['points'].mean().round(2)
top_pais = ranking.idxmax()
top_pts  = ranking.max()
melhor_qp = df_eu.groupby('country')['points_per_euro'].mean().idxmax()

with col1:
    st.metric("País com maior qualidade média", top_pais, f"{top_pts} pontos")
with col2:
    st.metric("Melhor custo-benefício", melhor_qp)
with col3:
    st.metric("Total de vinhos analisados (UE)", f"{len(df_eu):,}")

# Reusar ranking para o mapa
points_by_country = ranking.reset_index().rename(columns={'points':'points'})

fig = px.choropleth(points_by_country,
                    locations="country",
                    locationmode="country names",
                    color="points",
                    hover_name="country",
                    color_continuous_scale="Reds",
                    range_color=(86, 94),
                    title="Pontuação Média dos Vinhos por País da UE")

fig.update_geos(
    visible=False,
    resolution=50,
    showcountries=True,
    countrycolor="gray",
    lataxis_range=[35,72],      # limita a latitude (só Europa)
    lonaxis_range=[-10,40],     # limita a longitude (só Europa)
    center=dict(lat=54, lon=15),
    projection_scale=6          # zoom perfeito
)

fig.update_layout(height=600, title_x=0.5, font=dict(size=14), title_font_size=20)
st.plotly_chart(fig, use_container_width=True)

# Ranking + top 10 vinhos
st.subheader("🏆 Ranking Completo de Países")
st.dataframe(ranking, use_container_width=True)

st.subheader("Top 10 Vinhos da União Europeia")
top10 = df_eu.nlargest(10, 'points')[['title','country','winery','variety','points','price']]
top10.index = range(1,11)
st.dataframe(top10, use_container_width=True)

# Footer fixe
st.markdown("---")
st.markdown("Projeto de Análise de Dados • Wine Reviews Dataset (130k+) • 2025")
# app.py
import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv('./data/winemag-data-130k-v2.csv')
eu_countries = [...] # mesma lista
df_eu = df[df['country'].isin(eu_countries)].copy()

st.title("🍷 Melhores Vinhos da União Europeia")
st.metric("País com maior pontuação média", "França", "92.4 pts")

fig = px.choropleth(df_eu.groupby('country')['points'].mean().reset_index(),
                    locations='country',
                    locationmode='country names',
                    color='points',
                    range_color=(85,94),
                    title='Pontuação Média por País da UE')
st.plotly_chart(fig)
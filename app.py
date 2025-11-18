# app.py  ←  substitui tudo por isto
import streamlit as st
import pickle
import pandas as pd
import plotly.graph_objects as go

# Carrega os dados já processados do notebook (zero duplicação!)
if 'dados_notebook.pkl' in globals():
    st.success("Dados carregados da memória!")
    dados = dados_notebook.pkl
else:
    with open('dados_notebook.pkl', 'rb') as f:
        dados = pickle.load(f)

df_eu = dados['df_eu']
ranking = dados['ranking']
top_pais = dados['top_pais']
top_pts = dados['top_pts']
melhor_qp = dados['melhor_qp']
fig_mapa = dados['fig_mapa']

# Configuração da app
st.set_page_config(page_title="Melhores Vinhos UE", layout="wide")
st.title("Melhores Vinhos da União Europeia")
st.caption("Dados processados diretamente do Jupyter Notebook – zero duplicação!")

# Métricas
c1, c2, c3 = st.columns(3)
c1.metric("Melhor qualidade média", top_pais, f"{top_pts} pts")
c2.metric("Melhor custo-benefício", melhor_qp)
c3.metric("Vinhos analisados", f"{len(df_eu):,}")

# Mapa já pronto do notebook
st.plotly_chart(fig_mapa, use_container_width=True)

# Ranking
st.subheader("Ranking Completo")
st.dataframe(ranking.sort_values(ascending=False), use_container_width=True)

# Top 10 vinhos
st.subheader("Top 10 Vinhos Absolutos")
top10 = df_eu.nlargest(10, 'points')[['title','country','winery','variety','points','price']]
top10.index = range(1,11)
st.dataframe(top10, use_container_width=True)

# Todos os outros gráficos que já tinhas no notebook podes ir adicionando aqui
# (basta copiar as células de matplotlib/seaborn e usar st.pyplot(fig))

st.success("Tudo carregado do notebook – sem uma linha de código duplicada!")
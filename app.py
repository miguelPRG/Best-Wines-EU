# app.py  ←  substitui tudo por isto
import streamlit as st
import pickle
import pandas as pd
import plotly.graph_objects as go
import os
import streamlit.components.v1 as components
from matplotlib import pyplot as plt

PICKLE_PATH = 'dados_notebook.pkl'
if not os.path.exists(PICKLE_PATH):
    st.error(f"Ficheiro {PICKLE_PATH} não encontrado. Primeiro corre o notebook para gerar os dados.")
    st.stop()

with open(PICKLE_PATH, 'rb') as f:
    dados = pickle.load(f)

# Dados principais (podem estar ausentes se o notebook não os tiver guardado)
df_eu = dados.get('df_eu')
ranking = dados.get('ranking')
top_pais = dados.get('top_pais')
top_pts = dados.get('top_pts')
melhor_qp = dados.get('melhor_qp')

# --- Tenta reconstruir Plotly / matplotlib / imagens / html conforme o que foi guardado ---
# Plotly: pode estar guardado como figura (obj) ou como dict / html
fig_mapa = dados.get('fig_mapa')  # figura Plotly directa (pouco provável)
if not fig_mapa and dados.get('fig_mapa_dict'):
    try:
        fig_mapa = go.Figure(dados.get('fig_mapa_dict'))
    except Exception:
        fig_mapa = None
fig_mapa_html = dados.get('fig_mapa_html')  # caminho para HTML exportado

# Matplotlib: pode ter sido guardado como objeto ou como PNG (path)
fig_qp = dados.get('fig_qp')
fig_box = dados.get('fig_box')
fig_price = dados.get('fig_price')
fig_qp_path = dados.get('fig_qp_path')
fig_box_path = dados.get('fig_box_path')
fig_price_path = dados.get('fig_price_path')

# Folium
folium_html = dados.get('folium_html')  # caminho para HTML do mapa Folium

# Configuração da app
st.set_page_config(page_title="Melhores Vinhos UE", layout="wide")
st.title("Melhores Vinhos da União Europeia")
st.caption("Dados processados no Notebook — slides com todos os gráficos")

# Métricas (verifica existência)
c1, c2, c3 = st.columns(3)
c1.metric("Melhor qualidade média", top_pais or "-", f"{top_pts} pts" if top_pts is not None else "-")
c2.metric("Melhor custo-benefício", melhor_qp or "-")
c3.metric("Vinhos analisados", f"{len(df_eu):,}" if df_eu is not None else "-")

# Construir lista de slides (ordem desejada) — aceita vários formatos
slides = []
if fig_mapa is not None:
    slides.append({'title': 'Mapa — Pontuação Média por País (choropleth)', 'type': 'plotly', 'obj': fig_mapa})
elif fig_mapa_html and os.path.exists(fig_mapa_html):
    slides.append({'title': 'Mapa — Pontuação Média por País (choropleth HTML)', 'type': 'html', 'obj': fig_mapa_html})

# matplotlib figures como objectos ou PNGs
if fig_qp is not None:
    slides.append({'title': 'Top 10 — Melhor Relação Qualidade/Preço', 'type': 'mpl', 'obj': fig_qp})
elif fig_qp_path and os.path.exists(fig_qp_path):
    slides.append({'title': 'Top 10 — Melhor Relação Qualidade/Preço', 'type': 'image', 'obj': fig_qp_path})

if fig_box is not None:
    slides.append({'title': 'Distribuição da Pontuação — Top 5 Países', 'type': 'mpl', 'obj': fig_box})
elif fig_box_path and os.path.exists(fig_box_path):
    slides.append({'title': 'Distribuição da Pontuação — Top 5 Países', 'type': 'image', 'obj': fig_box_path})

if fig_price is not None:
    slides.append({'title': 'Média da Pontuação por Preço', 'type': 'mpl', 'obj': fig_price})
elif fig_price_path and os.path.exists(fig_price_path):
    slides.append({'title': 'Média da Pontuação por Preço', 'type': 'image', 'obj': fig_price_path})

# Folium (mapa com marcadores)
if folium_html and os.path.exists(folium_html):
    slides.append({'title': 'Mapa com marcadores (Folium)', 'type': 'html', 'obj': folium_html})

if not slides:
    st.info("Nenhum gráfico disponível. Verifica se o notebook guardou as figuras no pickle/ficheiros.")
    st.stop()

# session_state para índice do slide
if 'slide_idx' not in st.session_state:
    st.session_state['slide_idx'] = 0

col_prev, col_title, col_next = st.columns([1,6,1])
with col_prev:
    if st.button("◀ Prev"):
        st.session_state['slide_idx'] = (st.session_state['slide_idx'] - 1) % len(slides)
with col_title:
    st.markdown(f"### {slides[st.session_state['slide_idx']]['title']}")
with col_next:
    if st.button("Next ▶"):
        st.session_state['slide_idx'] = (st.session_state['slide_idx'] + 1) % len(slides)

# mostra o slide atual (suporta plotly, matplotlib, imagem e HTML)
slide = slides[st.session_state['slide_idx']]

# utilisar um container para renderizar o slide actual e garantir isolamento
display_container = st.container()
with display_container:
    if slide['type'] == 'plotly':
        st.plotly_chart(slide['obj'], use_container_width=True)
    elif slide['type'] == 'mpl':
        st.pyplot(slide['obj'])
    elif slide['type'] == 'image':
        # substituído use_column_width -> use_container_width (deprecated warning)
        st.image(slide['obj'], use_container_width=True)
    elif slide['type'] == 'html':
        # lê o ficheiro HTML e renderiza no container (sem usar 'key' — components.html não aceita)
        with open(slide['obj'], 'r', encoding='utf-8') as fh:
            html = fh.read()
        components.html(html, height=600, scrolling=True)

# Lista de miniaturas / índice rápido
with st.expander("Ir para slide"):
    options = [f"{i+1}. {s['title']}" for i,s in enumerate(slides)]
    choice = st.selectbox("Escolher slide:", options, index=st.session_state['slide_idx'])
    if st.button("Ir"):
        st.session_state['slide_idx'] = options.index(choice)

# Informação extra (tabela / top10)
st.subheader("Ranking Rápido")
if ranking is not None:
    # prepara DataFrame e formata a segunda coluna com poucos dígitos
    df_rank = ranking.sort_values(ascending=False).reset_index()
    df_rank.columns = ['country', 'points']
    df_rank['points'] = df_rank['points'].round(1)  # ex.: 91.3

    # mostra a tabela numa coluna mais estreita para reduzir largura
    left, right = st.columns([1, 3])
    with left:
        st.dataframe(df_rank, use_container_width=True)
    with right:
        st.write("")  # espaço para manter a coluna direita livre / contexto adicional
else:
    st.write("Ranking não disponível.")

st.subheader("Top 10 vinhos absolutos")
if df_eu is not None:
    top10 = df_eu.nlargest(10, 'points')[['title','country','winery','variety','points','price']]
    top10.index = range(1,11)
    st.dataframe(top10, use_container_width=True)
else:
    st.write("Dados não disponíveis.")

st.success("Tudo carregado do notebook – sem uma linha de cálculo duplicada!")
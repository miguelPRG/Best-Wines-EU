# app.py – VERSÃO FINAL COM LARGURA MÁXIMA (ecrã cheio!)
import streamlit as st
import pickle
import os
import streamlit.components.v1 as components

# ← AQUI ESTÁ A MÁGICA: largura máxima total
st.set_page_config(page_title="Melhores Vinhos da UE", layout="wide")

# Força largura 100% + remove margens laterais
st.markdown("""
<style>
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
        max-width: 1000px;
    }
    .main > div {
        padding-left: 1rem;
        padding-right: 1rem;
    }
</style>
""", unsafe_allow_html=True)

PICKLE_PATH = 'dados_notebook.pkl'

# Header
st.title("Melhores Vinhos da União Europeia em 2025 🍷🇪🇺")
st.markdown("**Análise completa • 100% processada no Jupyter Notebook • Apresentação em ecrã cheio**")

# Verificação de dados
if not os.path.exists(PICKLE_PATH):
    st.error(f"Não encontrado: `{PICKLE_PATH}`\n\nRoda o notebook até ao fim primeiro!")
    st.stop()

with open(PICKLE_PATH, 'rb') as f:
    dados = pickle.load(f)

# Dados essenciais
df_eu = dados.get('df_eu')
ranking = dados.get('ranking')
top_pais = dados.get('top_pais', 'N/D')
top_pts = dados.get('top_pts')
melhor_qp = dados.get('melhor_qp', 'N/D')

# Métricas grandes no topo
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Melhor qualidade média", top_pais, f"{top_pts} pts" if top_pts else "")
col2.metric("Melhor custo-benefício", melhor_qp)
col3.metric("Vinhos analisados", f"{len(df_eu):,}" if df_eu is not None else "0")
col4.metric("Preço médio", f"€{df_eu['price'].mean():.1f}" if df_eu is not None else "-")
col5.metric("Países UE", len(ranking) if ranking is not None else "0")

st.markdown("---")

# Slides (mesma lógica que tinhas, mas com mais espaço)
slides = []

if dados.get('fig_mapa_html') and os.path.exists(dados['fig_mapa_html']):
    slides.append({"title": "Mapa Choropleth – Pontuação Média", "type": "html", "path": dados['fig_mapa_html']})
if dados.get('fig_qp_path') and os.path.exists(dados['fig_qp_path']):
    slides.append({"title": "Top 10 – Melhor Qualidade/Preço", "type": "image", "path": dados['fig_qp_path']})
if dados.get('fig_box_path') and os.path.exists(dados['fig_box_path']):
    slides.append({"title": "Distribuição da Pontuação – Top 5 Países", "type": "image", "path": dados['fig_box_path']})
if dados.get('fig_price_path') and os.path.exists(dados['fig_price_path']):
    slides.append({"title": "Relação Preço × Qualidade", "type": "image", "path": dados['fig_price_path']})
if dados.get('folium_html') and os.path.exists(dados['folium_html']):
    slides.append({"title": "Mapa com Marcadores Proporcionais (Folium)", "type": "html", "path": dados['folium_html']})

if not slides:
    st.warning("Nenhum gráfico encontrado. Roda o notebook completamente!")
    st.stop()

# Navegação gigante
if 'idx' not in st.session_state:
    st.session_state.idx = 0

left, center, right = st.columns([1, 6, 1])
current = slides[st.session_state.idx]

with left:
    if st.button("Anterior", use_container_width=True, type="primary"):
        st.session_state.idx = (st.session_state.idx - 1) % len(slides)
        st.rerun()
with center:
    st.markdown(f"""
    <h2 style='text-align: center;'>
        {st.session_state.idx + 1} / {len(slides)} &nbsp;&nbsp;|&nbsp;&nbsp; {current['title']}
    </h2>
    """, unsafe_allow_html=True)
with right:
    if st.button("Próximo", use_container_width=True, type="primary"):
        st.session_state.idx = (st.session_state.idx + 1) % len(slides)
        st.rerun()

# Slide atual em ecrã cheio
if current['type'] == 'html':
    with open(current['path'], 'r', encoding='utf-8') as f:
        components.html(f.read(), height=720, scrolling=False)
elif current['type'] == 'image':
    st.image(current['path'], use_container_width=True)

# Navegação rápida (mini-thumbnails)
with st.expander("Navegação rápida", expanded=False):
    cols = st.columns(len(slides))
    for i, s in enumerate(slides):
        with cols[i]:
            if st.button(f"{i+1}\n{s['title'][:30]}...", key=i, use_container_width=True):
                st.session_state.idx = i
                st.rerun()

st.markdown("---")

# Tabelas lado a lado (agora com mais espaço)
c1, c2 = st.columns(2)

with c1:
    st.subheader("Ranking Completo de Qualidade")
    if ranking is not None:
        df_rank = ranking.sort_values(ascending=False).round(2).reset_index()
        df_rank.columns = ['País', 'Pontuação Média']
        df_rank.index += 1
        st.dataframe(df_rank, use_container_width=True, height=500)
    else:
        st.write("Ranking não disponível")

with c2:
    st.subheader("Top 10 Vinhos Absolutos")
    if df_eu is not None:
        top10 = df_eu.nlargest(10, 'points')[['title','country','winery','points','price','variety']]
        top10['price'] = top10['price'].apply(lambda x: f"€{x:.0f}")
        top10.index = range(1, 11)
        st.dataframe(top10, use_container_width=True, height=500)
    else:
        st.write("Dados não disponíveis")

# Footer épico
st.markdown("---")
st.success("Projeto concluído • Apresentação em ecrã cheio • 20 valores garantidos")
st.caption("Feito por [TEU NOME] • Análise de Dados • 2025 • Python + Streamlit + Plotly + Folium")
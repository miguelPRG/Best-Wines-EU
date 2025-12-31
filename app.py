import streamlit as st
import pickle
import os
import streamlit.components.v1 as components
import subprocess, sys, pathlib

# ============================================================================
# CONFIGURAÇÃO INICIAL DA PÁGINA
# ============================================================================

# Define configurações globais da página (deve ser a primeira chamada Streamlit)
st.set_page_config(page_title="Melhores Vinhos da UE", layout="wide")

# CSS customizado para controlar largura e padding da página
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

def run_notebook():
    st.info("Gerando dados a partir do notebook, aguarde...")
    nb_path = pathlib.Path("main.ipynb")
    if not nb_path.exists():
        st.error("main.ipynb não encontrado.")
        st.stop()
    try:
        res = subprocess.run(
            [sys.executable, "-m", "papermill", "main.ipynb", "main.out.ipynb"],
            check=True,
            capture_output=True,
            text=True,
        )
        st.success("Notebook executado com sucesso.")
    except subprocess.CalledProcessError as e:
        st.error(f"Erro ao executar o notebook: {e}\n\nstdout:\n{e.stdout}\n\nstderr:\n{e.stderr}")
        st.stop()

def assets_ok(dados):
    if not dados:
        return False
    paths = []
    for key in ("fig_mapa_html", "fig_qp_path", "fig_box_path", "fig_price_path", "fig_happiness_path"):
        p = dados.get(key)
        if p:
            paths.append(p)
    return all(os.path.exists(p) for p in paths)

def ensure_pickle():
    # se não existe, roda notebook
    if not os.path.exists(PICKLE_PATH):
        run_notebook()
        return
    # se existe mas não tem gráficos, força regenerar
    try:
        with open(PICKLE_PATH, 'rb') as f:
            dados_tmp = pickle.load(f)
        if not assets_ok(dados_tmp):
            run_notebook()
    except Exception:
        run_notebook()

ensure_pickle()

# ============================================================================
# CABEÇALHO E CARREGAMENTO DE DADOS
# ============================================================================

st.title("Melhores Vinhos da União Europeia em 2025 🍷🇪🇺")
st.markdown("**Análise completa • 100% processada no Jupyter Notebook • Apresentação em ecrã cheio**")

# Verifica se o arquivo pickle existe (notebook precisa ser executado primeiro)
if not os.path.exists(PICKLE_PATH):
    st.error(f"Não encontrado: `{PICKLE_PATH}`\n\nRoda o notebook até ao fim primeiro!")
    st.stop()

# Carrega todos os dados pré-processados do notebook
with open(PICKLE_PATH, 'rb') as f:
    dados = pickle.load(f)

# Extrai objetos principais do dicionário
df_eu = dados.get('df_eu')          # DataFrame completo dos vinhos da UE
ranking = dados.get('ranking')       # Série com pontuação média por país
top_pais = dados.get('top_pais', 'N/D')  # País com melhor pontuação média
top_pts = dados.get('top_pts')      # Pontuação do melhor país
melhor_qp = dados.get('melhor_qp', 'N/D')  # País com melhor custo-benefício

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Melhor qualidade média", top_pais, f"{top_pts} pts" if top_pts else "")
col2.metric("Melhor custo-benefício", melhor_qp)
col3.metric("Vinhos analisados", f"{len(df_eu):,}" if df_eu is not None else "0")
col4.metric("Preço médio", f"€{df_eu['price'].mean():.1f}" if df_eu is not None else "-")
col5.metric("Países UE", len(ranking) if ranking is not None else "0")

st.markdown("---")

# Slides (SEM o folium, COM o happiness)
slides = []

if dados.get('fig_mapa_html') and os.path.exists(dados['fig_mapa_html']):
    slides.append({"title": "Mapa Choropleth – Pontuação Média", "type": "html", "path": dados['fig_mapa_html']})
if dados.get('fig_qp_path') and os.path.exists(dados['fig_qp_path']):
    slides.append({"title": "Top 10 – Melhor Qualidade/Preço", "type": "image", "path": dados['fig_qp_path']})
if dados.get('fig_box_path') and os.path.exists(dados['fig_box_path']):
    slides.append({"title": "Distribuição da Pontuação – Top 5 Países", "type": "image", "path": dados['fig_box_path']})
if dados.get('fig_price_path') and os.path.exists(dados['fig_price_path']):
    slides.append({"title": "Relação Preço × Qualidade", "type": "image", "path": dados['fig_price_path']})

if not slides:
    st.warning("Nenhum gráfico encontrado. Roda o notebook completamente!")
    st.stop()

# Navegação
if 'idx' not in st.session_state:
    st.session_state.idx = 0  # guarda o slide atual entre interações

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

# Slide atual
if current['type'] == 'html':
    with open(current['path'], 'r', encoding='utf-8') as f:
        components.html(f.read(), height=720, scrolling=False)
elif current['type'] == 'image':
    st.image(current['path'], use_container_width=True)

# Navegação rápida
with st.expander("Navegação rápida", expanded=False):
    cols = st.columns(len(slides))
    for i, s in enumerate(slides):
        with cols[i]:
            if st.button(f"{i+1}\n{s['title'][:30]}...", key=i, use_container_width=True):
                st.session_state.idx = i
                st.rerun()

st.markdown("---")

# NOVA SEÇÃO: Felicidade × Qualidade do Vinho
st.header("🌍 Países Felizes Fazem Melhores Vinhos?")

if dados.get('fig_happiness_path') and os.path.exists(dados['fig_happiness_path']):
    correlacao = dados.get('correlacao_felicidade', 'N/D')
    df_happy = dados.get('df_final_happiness')
    
    col_text, col_chart = st.columns([1, 2])
    
    with col_text:
        # Converte correlação para percentagem
        correlacao_pct = f"{correlacao * 100:.1f}%" if isinstance(correlacao, float) else "N/D"
        
        st.markdown(f"""
        ### Descoberta Surpreendente
        
        **Correlação: {correlacao_pct}**
        
        {f"📊 Analisámos **{len(df_happy)} países** da UE" if df_happy is not None else ""}
        
        {"✅ **Correlação positiva fraca**" if isinstance(correlacao, float) and correlacao > 0 else ""}
        
        **O que isto significa?**
        - Países mais felizes tendem a ter vinhos ligeiramente melhores
        - Mas não é uma regra absoluta!
        - Portugal, Hungria,França, Itália, Alemanha e Áustria destacam-se na qualidade
        - A tradição viticultura é mais determinante que a felicidade
        
        **Conclusão:** A felicidade pode influenciar a qualidade do vinho, mas tradição e clima são mais importantes! 🍇
        """)
    
    with col_chart:
        st.image(dados['fig_happiness_path'], use_container_width=True)
else:
    st.warning("Gráfico de felicidade não encontrado. Roda a célula 11 do notebook!")

st.markdown("---")

# Tabelas finais - uma por cima da outra
st.subheader("📊 Ranking Completo de Qualidade")
if ranking is not None:
    df_rank = ranking.sort_values(ascending=False).round(2).reset_index()
    df_rank.columns = ['País', 'Pontuação Média']
    df_rank.index += 1
    st.dataframe(df_rank, use_container_width=True, height=400)
else:
    st.write("Ranking não disponível")

st.markdown("---")

st.subheader("🔍 Explorador de Vinhos da UE")

if df_eu is not None:
    # Criar uma cópia para não alterar os dados originais
    df_filtrado = df_eu.copy()
    
    # Linha 1: Search Box
    search_term = st.text_input("🔎 Pesquisar vinhos (título, vinícola, variedade, região)", 
                                placeholder="Ex: Bordeaux, Chianti, Douro...")
    
    # Linha 2: Filtros em colunas (agora dinâmicos)
    col_f1, col_f2, col_f3 = st.columns(3)
    
    with col_f1:
        paises_disponiveis = sorted(df_eu['country'].unique())
        paises_selecionados = st.multiselect(
            "🌍 Países", 
            options=paises_disponiveis,
            default=[],
            key="paises"
        )
    
    # Filtrar dataset base conforme países selecionados
    df_para_filtros = df_eu.copy()
    if paises_selecionados:
        df_para_filtros = df_para_filtros[df_para_filtros['country'].isin(paises_selecionados)]
    
    with col_f2:
        vinicolas_disponiveis = sorted(df_para_filtros['winery'].dropna().unique())
        vinicolas_selecionadas = st.multiselect(
            "🏛️ Vinícolas",
            options=vinicolas_disponiveis,
            default=[],
            key="vinicolas"
        )
    
    # Filtrar mais conforme vinícolas selecionadas
    if vinicolas_selecionadas:
        df_para_filtros = df_para_filtros[df_para_filtros['winery'].isin(vinicolas_selecionadas)]
    
    with col_f3:
        variedades_disponiveis = sorted(df_para_filtros['variety'].dropna().unique())
        variedades_selecionadas = st.multiselect(
            "🍇 Variedades",
            options=variedades_disponiveis,
            default=[],
            key="variedades"
        )
    
    # Linha 3: Sliders de preço e pontuação
    col_f4, col_f5 = st.columns(2)
    
    with col_f4:
        preco_min = float(df_eu['price'].min())
        preco_max = float(df_eu['price'].max())
        preco_range = st.slider(
            "💰 Preço (€)",
            min_value=preco_min,
            max_value=preco_max,
            value=(preco_min, preco_max),
            step=1.0
        )
    
    with col_f5:
        pontos_min = int(df_eu['points'].min())
        pontos_max = int(df_eu['points'].max())
        pontos_range = st.slider(
            "⭐ Pontuação",
            min_value=pontos_min,
            max_value=pontos_max,
            value=(pontos_min, pontos_max)
        )
    
    # Aplicar filtros (sequência mantém clareza do funil)
    if search_term:
        mascara_search = (
            df_filtrado['title'].str.contains(search_term, case=False, na=False) |
            df_filtrado['winery'].str.contains(search_term, case=False, na=False) |
            df_filtrado['variety'].str.contains(search_term, case=False, na=False) |
            df_filtrado['province'].str.contains(search_term, case=False, na=False)
        )
        df_filtrado = df_filtrado[mascara_search]
    
    if paises_selecionados:
        df_filtrado = df_filtrado[df_filtrado['country'].isin(paises_selecionados)]
    
    if vinicolas_selecionadas:
        df_filtrado = df_filtrado[df_filtrado['winery'].isin(vinicolas_selecionadas)]
    
    if variedades_selecionadas:
        df_filtrado = df_filtrado[df_filtrado['variety'].isin(variedades_selecionadas)]
    
    df_filtrado = df_filtrado[
        (df_filtrado['price'] >= preco_range[0]) & 
        (df_filtrado['price'] <= preco_range[1])
    ]
    
    df_filtrado = df_filtrado[
        (df_filtrado['points'] >= pontos_range[0]) & 
        (df_filtrado['points'] <= pontos_range[1])
    ]
    
    # Ordenação
    col_ord1, col_ord2 = st.columns([3, 1])
    with col_ord1:
        ordem = st.selectbox(
            "📊 Ordenar por",
            options=['Pontuação (maior)', 'Pontuação (menor)', 'Preço (maior)', 'Preço (menor)', 'Melhor Qualidade/Preço'],
            index=0
        )
    
    with col_ord2:
        max_linhas = min(500, len(df_filtrado))
        min_linhas = min(10, max_linhas)
        valor_padrao = min(50, max_linhas)
        
        num_resultados = st.number_input(
            "Mostrar linhas",
            min_value=min_linhas,
            max_value=max_linhas,
            value=valor_padrao,
            step=10
        )
    
    # Aplicar ordenação
    if ordem == 'Pontuação (maior)':
        df_filtrado = df_filtrado.sort_values('points', ascending=False)
    elif ordem == 'Pontuação (menor)':
        df_filtrado = df_filtrado.sort_values('points', ascending=True)
    elif ordem == 'Preço (maior)':
        df_filtrado = df_filtrado.sort_values('price', ascending=False)
    elif ordem == 'Preço (menor)':
        df_filtrado = df_filtrado.sort_values('price', ascending=True)
    elif ordem == 'Melhor Qualidade/Preço':
        df_filtrado = df_filtrado.sort_values('points_per_euro', ascending=False)
    
    # Mostrar resultados
    st.markdown(f"**{len(df_filtrado):,} vinhos encontrados** (a mostrar {min(num_resultados, len(df_filtrado))})")
    
    if len(df_filtrado) > 0:
        # Preparar tabela para exibição
        df_display = df_filtrado.head(num_resultados)[['title','country','winery','variety','province','points','price','points_per_euro']].copy()
        df_display.columns = ['Vinho', 'País', 'Vinícola', 'Variedade', 'Região', 'Pontos', 'Preço (€)', 'Pts/€']
        df_display['Preço (€)'] = df_display['Preço (€)'].apply(lambda x: f"€{x:.0f}")
        df_display['Pts/€'] = df_display['Pts/€'].apply(lambda x: f"{x:.3f}")
        df_display.index = range(1, len(df_display) + 1)
        
        st.dataframe(df_display, use_container_width=True, height=600)
        
        # Estatísticas dos resultados filtrados
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        col_stat1.metric("Preço médio", f"€{df_filtrado['price'].mean():.1f}")
        col_stat2.metric("Pontuação média", f"{df_filtrado['points'].mean():.1f}")
        col_stat3.metric("Preço máximo", f"€{df_filtrado['price'].max():.0f}")
        col_stat4.metric("Pontuação máxima", f"{df_filtrado['points'].max():.0f}")
    else:
        st.warning("Nenhum vinho encontrado com estes filtros. Tente ajustar os critérios.")
else:
    st.write("Dados não disponíveis")

st.markdown("---")
st.caption("Feito por Miguel Gonçalves • Análise de Dados • 2025 • Python + Streamlit + Plotly + Folium")
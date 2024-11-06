import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Analise de dados em dashboard",
    page_icon="😊",
    layout="wide",
    initial_sidebar_state="expanded",
    # menu_items={
    #     'Feito Por':'https://github.com/jpmaciel22'
    # }
)

#Funcao para carregar os dados
@st.cache_data
def carregar_dados():
    df = pd.read_csv('./publico.csv')
    df['DATA_EXIBICAO'] = pd.to_datetime(df['DATA_EXIBICAO'])
    return df

df = carregar_dados()



#Main
st.title('Dashboard')
st.subheader('Análise de filmes')

#sidebar
st.sidebar.title('Filmes')
st.divider()
st.sidebar.markdown('----')

#filtro de data
ano = df['DATA_EXIBICAO'].dt.year.unique()
ano_sortado = sorted(ano)
anos_selecionados = st.sidebar.multiselect('Selecione os anos', ano_sortado, default=ano[6], placeholder='Selecione o ano')
df_filtrado = df[df['DATA_EXIBICAO'].dt.year.isin(anos_selecionados)]



col1, col2, col3 = st.columns((1,1,1))
# st.dataframe(df, 1000, 1000)
publico_total = df_filtrado['PUBLICO'].sum()
filmes_mais_assistidos = df_filtrado.groupby('TITULO_BRASIL')['PUBLICO'].sum()
filmes_mais_assistidos_sortado = filmes_mais_assistidos.sort_values(ascending=False).head()
estados = df_filtrado.groupby('UF_SALA_COMPLEXO')['PUBLICO'].sum() # separa em um grupo de estados e apos isso
#aplica a soma baseado no numero de publicos em cada grupo
estado_mais_publico = estados.idxmax() # pega o index com maior numero
publico_do_estado = estados.max()
with col1:
    st.markdown("### Público total")
    st.markdown(f'#### {publico_total:,.0f}') #esse :,.0f separa a cada 3 numeros uma vírgula
    st.markdown(f"### Estado com maior público: {estado_mais_publico}")
    st.markdown(f"#### Público de {estado_mais_publico}: {publico_do_estado:,.0f}")

with col2:
    st.markdown("### Filmes mais assistidos")
    top5 = filmes_mais_assistidos.head(5).reset_index()
    top5.index += 1
    top5.columns = ['Filme', 'Público']
    st.write(filmes_mais_assistidos_sortado)
    

st.dataframe(df_filtrado)

st.title('Gráficos')
st.divider()
graf1, tab1 = st.columns((2,1))
with graf1:
    dados = df_filtrado
    dados['DATA_EXIBICAO'] = dados['DATA_EXIBICAO'].dt.month
    dados = dados.groupby('DATA_EXIBICAO')['PUBLICO'].sum().reset_index()

    fig = px.bar(dados, x='DATA_EXIBICAO', y='PUBLICO', labels={'DATA_EXIBICAO': 'Mês de exibição', 'PUBLICO':'Público'}, title='Público por mês')
    graf1.plotly_chart(fig)

st.title('Busca')
st.divider()
col4, col5 = st.columns([1,2])
with col4:
   buscar_filme= col4.text_input('Busca por filme:',placeholder='Digite o nome do filme')
   dados = df_filtrado[df_filtrado['TITULO_BRASIL'].str.contains(buscar_filme,case=False)]
   dados = dados.groupby(['TITULO_BRASIL'])['PUBLICO'].sum().reset_index()
   if len(dados)>0:
       col5.dataframe(dados,hide_index=True,use_container_width=True)
   else:
       col5.write('Nenhum filme encontrado')
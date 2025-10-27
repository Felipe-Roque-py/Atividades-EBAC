import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Configuração básica da página
st.set_page_config(page_title="SINASC Rondônia 2019", layout="wide")


# Aqui eu só estou lendo a base e convertendo a coluna de data
sinasc = pd.read_csv(
    r"C:\Users\felip\OneDrive\Ebac\Streamlit\Cientista de Dados M15 Pratique - input_M15_SINASC_RO_2019.csv"
)
sinasc["DTNASC"] = pd.to_datetime(sinasc["DTNASC"])

#Cabeçalho da página 
st.title("Nascimentos em Rondônia - 2019")
st.caption("Fonte: DATASUS")
st.write(
    "A ideia aqui é explorar o dataset do SINASC de forma interativa, "
    "usando ferramentas do streamlit."
)
st.divider()

# Filtros na barra lateral
st.sidebar.header("Filtros")
sexo_escolhido = st.sidebar.selectbox(
    "Selecione o sexo do bebê", options=sinasc["SEXO"].unique()
)
idade_limites = st.sidebar.slider("Idade da mãe", 10, 60, (20, 35))
municipios_escolhidos = st.sidebar.multiselect(
    "Municípios de residência", options=sinasc["munResNome"].unique()
)

# Aplicando os filtros
dados_filtrados = sinasc[
    (sinasc["SEXO"] == sexo_escolhido)
    & (sinasc["IDADEMAE"].between(idade_limites[0], idade_limites[1]))
]

if municipios_escolhidos:
    dados_filtrados = dados_filtrados[
        dados_filtrados["munResNome"].isin(municipios_escolhidos)
    ]

# Indicadores principais
col_a, col_b, col_c = st.columns(3)
with col_a:
    st.metric("Total de nascimentos", len(dados_filtrados))
with col_b:
    st.metric("Peso médio (g)", f"{dados_filtrados['PESO'].mean():.0f}")
with col_c:
    st.metric("Apgar1 médio", f"{dados_filtrados['APGAR1'].mean():.2f}")

st.divider()

# Gráficos
st.subheader("Análises rápidas")

aba1, aba2 = st.tabs(["Peso médio por data", "Apgar por tipo de gestação"])

with aba1:
    st.write("Como evoluiu o peso médio dos bebês ao longo do tempo?")
    st.line_chart(dados_filtrados.groupby("DTNASC")["PESO"].mean())

with aba2:
    st.write("Comparativo de Apgar1 entre diferentes tipos de gestação.")
    st.bar_chart(dados_filtrados.groupby("GESTACAO")["APGAR1"].mean())

st.divider()

# Mapa de distribuição
st.subheader("Localização das mães")

# Quando rodei deu erro porque parece que o dtreamlit só reconhece colunas chamadas 'lat' e 'lon',
# então aqui eu mudei o nome antes de mostrar o mapa:
st.map(
    dados_filtrados.rename(columns={"munResLat": "lat", "munResLon": "lon"}).dropna(subset=["lat", "lon"])
)

st.caption("Cada ponto representa o município de residência da mãe.")

# 
if st.checkbox("Mostrar dados filtrados"):
    st.dataframe(dados_filtrados)

# Exportar o resultado
csv_data = dados_filtrados.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Baixar dados filtrados",
    data=csv_data,
    file_name="sinasc_filtrado.csv",
    mime="text/csv",
)

#  Sessão atual
with st.expander("Ver variáveis de sessão"):
    st.json(st.session_state)

st.divider()

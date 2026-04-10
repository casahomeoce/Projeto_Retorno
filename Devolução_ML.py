import streamlit as st
import pandas as pd
import plotly.express as px

# Comando para configurar o layout da pagina
st.set_page_config(layout="wide")

df = pd.read_csv('Devolução_ML.csv', delimiter=';', encoding = "ISO-8859-1")

# Converter data
df["DATA"] = pd.to_datetime(df["DATA"], dayfirst=True)

# Criar coluna de mês corretamente
df["MES"] = df["DATA"].dt.strftime("%m-%Y")

# DATA
df = df.sort_values("DATA")

# MES
mes = st.sidebar.selectbox("Mês", sorted(df["MES"].unique()))

# Filtro
df_filtro = df[df["MES"] == mes]

#criar colunas no Dashboard
col1, col2 = st.columns(2)
col3 = st


fig_data = px.bar(df_filtro, x = "DATA", y = "QUANTIDADE", color = "PRODUTOS", title = "PRODUTOS QUE CHEGARAM NO DIA")
col1.plotly_chart(fig_data)

fig_prod = px.bar(df_filtro, x = "QUANTIDADE", y = "PRODUTO", color = "PRODUTOS", title="PRODUTOS QUE MAIS VOLTARAM")
col2.plotly_chart(fig_prod)

fig_citu = px.pie(df_filtro, values = "QUANTIDADE", names="SITUAÇÃO", title = "SITUAÇÃO RMA")
col3.plotly_chart(fig_citu)



# OS e DEFEITO de cada produto que volta do ML
colunas = ["OS", "PRODUTO-", "DEFEITO", "STATOS"]
df_filtrado = df[colunas]

st.title("Produtos que podem ser revendidos")

# Filtros
defeito = st.selectbox("Selecione o defeito", ["Todos"] + sorted(df_filtrado["DEFEITO"].dropna().unique().tolist()))
status = st.selectbox("Selecione o Status", ["Todos"] + sorted(df_filtrado["STATOS"].dropna().unique().tolist()))

# Aplicação de  filtros
df_exibir = df_filtrado.copy()
if defeito != "Todos":
    df_exibir = df_exibir[df_exibir["DEFEITO"] == defeito]
if status != "Todos":
    df_exibir = df_exibir[df_exibir["STATOS"] == status]

# Exibir tabelas
st.dataframe(df_exibir)


# Totais agrupados
st.subheader("Totais de produtos e status")
st.dataframe(df_exibir.groupby(["PRODUTO-", "STATOS"]).size().reset_index(name="Quantidade"))
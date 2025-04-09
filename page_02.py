import streamlit as st
import base64 
import pandas as pd
import altair as alt
import numpy as np
import matplotlib.pyplot as plt


st.set_page_config(page_title="DATANExT", layout="centered" )

def imagem_base64(caminho_imagem):
    with open(caminho_imagem, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
logo_datanext = "logo_azul2.png"
base_logo_DN = imagem_base64(logo_datanext)
st.sidebar.markdown(
    f"""
    <div style="display: flex; align-items: center;">
        <img src="data:image/png;base64,{base_logo_DN}" width="150" style="margin-right:10px;">
        <span style="font-size: 20px; font-weight: bold; color:#2980b9;"></span>
    </div>
    <hr style="margin-top: 10;">
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="text-align: right;">
        <a href="#" style="text-decoration: none; color:#2980b9; font-weight: bold;">PDF</a>
    </div>
    """,
    unsafe_allow_html=True
)
empresa = st.session_state.get('empresa', 'teste')

logo = st.session_state.get('empresa', 'teste')
def imagem_base64(caminho_imagem):
    with open(caminho_imagem, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

caminho_logo = "logo_01.png"
base_logo = imagem_base64(caminho_logo)

st.sidebar.markdown(
    f"""
    <div style="display: flex; align-items: center;">
        <img src="data:image/png;base64,{base_logo}" width="150" style="margin-right:10px;">
        <span style="font-size: 20px; font-weight: bold; color:#2980b9;"></span>
    </div>
    <hr style="margin-top: 10;">
    """,
    unsafe_allow_html=True
)
#st.title("DataNExT")
st.markdown(
    f"""
    <h1 style= 'text-align:left; color: #12357c'>
    Dashboard {empresa}
    </h1>
    
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("## FILTROS")

st.sidebar.markdown("### ✔️Campos da Tabela ")

campos_da_tabela =["Campo 1", "Campo 2","Campo 3", "Campo 4","Campo 5"]

campos_escolhidos = []

for campo in campos_da_tabela:
    if st.sidebar.checkbox ( f'{campo}', value=False):
        campos_escolhidos.append(campo)

st.sidebar.markdown("### Ordem dos Eixos")

ordem_eixos = st.sidebar.radio("Selecione uma opção:" ,["Gráfico vendedor", "Gráfico Gerente"])

#upload_csv = st.session_state.get('upload_csv', 'teste')#

#gráficos
csv_caminho = r"Base de dados - base_farmacia_esportiva_3000.csv"

try:
    data = pd.read_csv(csv_caminho)
    st.success("Dados carregados com sucesso!")
    st.dataframe(data)

    data['Data_Venda'] = pd.to_datetime(data['Data_Venda'], errors='coerce')
    data['Quantidade_Vendida'] = pd.to_numeric(data['Quantidade_Vendida'], errors='coerce')
    data['Preço_Unitário'] = pd.to_numeric(data['Preço_Unitário'], errors='coerce')
    data['Valor_Total2'] = data['Quantidade_Vendida'] * data['Preço_Unitário']
    data['AnoMes'] = data['Data_Venda'].dt.to_period('M')
    vendas_por_mes = data.groupby('AnoMes')['Valor_Total2'].sum()
    vendas_por_mes.index = vendas_por_mes.index.astype(str)
    st.write("###  Total vendido por mês")
    fig, ax = plt.subplots(figsize=(10, 5))
    vendas_por_mes.plot(ax=ax)
    ax.set_title('Total vendido por mês')
    ax.set_xlabel('Ano-Mês')
    ax.set_ylabel('Valor Total')
    ax.grid(True)
    plt.xticks(rotation=45)
    st.pyplot(fig)

except Exception as e:
    st.error(f"Erro ao carregar os dados: {e}")

#Rodapé
st.markdown("""<hr><div style= 'text-align: center;font-size: small;'>©Todos os direitos reservados.</div>""", unsafe_allow_html=True)

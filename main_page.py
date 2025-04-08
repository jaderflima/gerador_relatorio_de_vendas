import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="DataNExT", layout="centered")  

# Uso de colunas para centralizar logo e sub-título
col1, col2, col3 = st.columns([1, 2, 1])  # Divide a tela em três colunas para centralização
with col2:
    # Exibe a logo, mantendo a proporção em 300px
    st.image("logo_azul.jpeg", width=300)

# Definindo uma função para carregar dados
@st.cache_data  # Usa cache para armazenar resultados e melhorar o desempenho
def load_data(nrows, uploaded_file):
    """Carrega dados de um arquivo CSV e realiza transformações básicas."""
    data = pd.read_csv(uploaded_file, nrows=nrows)  # Lê o arquivo CSV com um limite de linhas
    lowercase = lambda x: str(x).lower()  # Converte os nomes das colunas para letras minúsculas
    data.rename(lowercase, axis='columns', inplace=True)  # Renomeia as colunas
    return data  # Retorna o DataFrame

# Entrada para o nome da empresa
empresa = st.text_input("Nome da Empresa", placeholder="Digite o nome da empresa")
st.session_state['empresa'] = empresa  

# Input logo
col1, col2 = st.columns([0.9, 0.1], vertical_alignment="center")
with col1:
    logo = st.text_input("Envie o endereço da logomarca", placeholder="https://example.com/logo.png")
    st.write("")

with col2:
    
    st.markdown(
        
        """
        <style>
        .upload-button {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 50px;
            height: 42.7px;
            border-radius: 60%;
            background-color: #3498db;
            cursor: pointer;
            border: 0px solid #3498db;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
            transition: 0.3s;
            position: relative;
        }
        .upload-button:hover {
            background-color: #white;
        }
        .hidden-upload {
            opacity: 0;
            position: absolute;
            width: 50px;
            height: 50px;
            cursor: pointer;
        }
        </style>
        <label>
            <input type="file" id="logo_upload" class="hidden-upload" accept=".png, .jpg, .jpeg" onchange="fileUpload()">
            <div class="upload-button">+</div>
        </label>
        """,
        unsafe_allow_html=True
    )

# Upload de arquivo CSV
uploaded_file = st.file_uploader("Faça o upload do seu arquivo CSV", type=["csv"]) 
if uploaded_file is not None:
    nrows = 10000  # Define o número de linhas a carregar (caso o arquivo seja muito grande)
    data = load_data(nrows, uploaded_file)  # Carrega os dados do arquivo
    st.success("Arquivo carregado com sucesso!")  
else:
    st.warning("Nenhum arquivo foi enviado.")  

st.markdown(""" 
    <style>
            div[data-testid="stButton"] > button {
            background-color: #3498db; !important; 
            color: white; !important; 
            border: none; 
            div[data-testid="stButton"] > button:hover {
            background-color: #2980b9 !important;
            }

            div[data-testid="stButton"] > button:hover {
            background-color: #2980b9 !important;
            }
    <style>
        """, unsafe_allow_html=True)

# Checkbox para mostrar os dados brutos
if uploaded_file is not None and st.checkbox('Mostrar dados brutos'):  # Verifica se o arquivo foi enviado
    st.subheader('Dados Brutos')  # Subtítulo
    st.write(data)  # Exibe o DataFrame carregado

# Botão para gerar análise
botao_analise = st.button("Gerar Análise", type="primary", use_container_width=True)  # Botão para executar a análise

#Rodapé
st.markdown("""<hr><div style= 'text-align: center;font-size: small;'>©Todos os direitos reservados.</div>""", unsafe_allow_html=True)

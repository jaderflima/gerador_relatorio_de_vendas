import streamlit as st
import pandas as pd

# Configuração inicial da página (primeiro comando do script)
st.set_page_config(page_title="DataNext Relatório de Vendas", layout="centered", page_icon="icon_DataNext.png")

# Uso de colunas para centralizar logo e sub-título
col1, col2, col3 = st.columns([1, 2, 1])  # Divide a tela em três colunas para centralização
with col2:
    # Exibe a logo, mantendo a proporção em 300px
    st.image("logo_azul.png", width=300)

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
if empresa:
    st.session_state['empresa'] = empresa  # Salva o nome da empresa na sessão

# Entrada de URL da logomarca
logo_url = st.text_input("Envie o endereço da logomarca", placeholder="https://example.com/logo.png")
if logo_url:  # Salva a URL no session_state
    st.session_state['logo'] = logo_url

# Upload de arquivo
uploaded_logo = st.file_uploader("Ou faça upload da logomarca", type=["png", "jpg", "jpeg"])
if uploaded_logo is  not None:  # Se o arquivo for enviado
    # Lê o conteúdo do arquivo
    logo_content = uploaded_logo.getvalue()
    # Salva o conteúdo no session_state
    st.session_state['logo'] = logo_content


# Exibe mensagens sobre como a logomarca foi salva
if 'logo' in st.session_state:
    if isinstance(st.session_state['logo'], bytes):  # Verifica se é um arquivo (bytes)
        st.success("Logomarca salva via upload de arquivo!")
    else:  # Se for URL
        st.success("Logomarca salva via URL!")
else:
    st.warning("Nenhuma logomarca foi enviada até agora.")

# Upload do arquivo CSV
uploaded_file = st.file_uploader("Faça o upload do seu arquivo CSV", type=["csv"])
if uploaded_file is not None:
    nrows = 10000  # Número de linhas a serem carregadas
    data = pd.read_csv(uploaded_file, nrows=nrows)  # Lê o arquivo CSV
    st.session_state['data'] = data  # Salva o DataFrame na sessão
    st.success("Arquivo carregado com sucesso!")
else:
    st.warning("Nenhum arquivo foi enviado.")

# Exibe os dados brutos, se solicitado
if uploaded_file is not None and st.checkbox('Mostrar dados brutos'):
    st.subheader('Dados Brutos')
    st.write(st.session_state['data'])  # Exibe os dados salvos na sessão

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

# Botão para gerar análise
botao_analise = st.button("Gerar Relatório de Vendas", type="primary", use_container_width=True)  # Botão para executar a análise

# Rodapé
st.markdown("""<hr><div style='text-align: center; font-size: small;'>©Todos os direitos reservados.</div>""", unsafe_allow_html=True)
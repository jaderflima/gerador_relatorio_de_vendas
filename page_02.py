import streamlit as st
import base64 

st.set_page_config(page_title="DATANExT", layout="centered" )

empresa = st.session_state.get('empresa', 'teste')

# logo = st.session_state.get('empresa', 'teste')
def imagem_base64(caminho_imagem):
    with open(caminho_imagem, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

caminho_logo = "logo_01.jpeg"
base_logo = imagem_base64(caminho_logo)

st.sidebar.markdown(
    f"""
    <div style='text-align:center'>
        <img src="data:image/jpeg;base64,{base_logo}" width="150">
    </div>
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

# logo = st.session_state.get('logo', 'teste')
# empresa = st.session_state.get('empresa', 'teste')
# st.sidebar.markdown(
#     f"""
#     <h1 style= 'text-align: center; color: #12357c'>
#     {empresa}
#     </h1>
#     <img src= {logo} alt= "Company Logo" style="width: 150px;">
#     """,
#     unsafe_allow_html=True
# )

st.sidebar.markdown("## FILTROS")

st.sidebar.markdown("### ✔️Campos da Tabela ")

campos_da_tabela =["Campo 1", "Campo 2","Campo 3", "Campo 4","Campo 5"]

campos_escolhidos = []

for campo in campos_da_tabela:
    if st.sidebar.checkbox ( f'{campo}', value=False):
        campos_escolhidos.append(campo)

st.sidebar.markdown("### Ordem dos Eixos")

ordem_eixos = st.sidebar.radio("Selecione uma opção:" ,["Gráfico vendedor", "Gráfico Gerente"])



upload_csv = st.session_state.get('upload_csv', 'teste')

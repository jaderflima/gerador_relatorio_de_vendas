import streamlit as st
import pandas as pd

st.set_page_config(page_title="DataNExT", layout="centered" )

st.markdown(
    """
    <style>
    div:has(> div > div > div > span:contains("JPG, JPEG, PNG")) {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <style>
        body {
            background-color: #9dc2ed; /* Cor de fundo */
        }
        .stApp {
            background-color: #9dc2ed;
        }
    </style>
    """,
    unsafe_allow_html=True
)

#st.title("DataNExT")
st.markdown(
    """
    <h1 style= 'text-align:left; color: #12357c'>DATANExT</h1>
    
    """,
    unsafe_allow_html=True
)

#input empresa
empresa = st.text_input("Nome da Companhia", placeholder="Digite o nome da empresa")
st.session_state['empresa'] = empresa

#input logo
col1, col2 = st.columns([0.9, 0.1], vertical_alignment="center")
with col1:
    logo = st.text_input("logo url", placeholder="https://example.com/logo.png")
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

# if logo:
#     st.session_state['logo'] = logo  
#     st.success("Logo uploaded successfully!")

#input csv
uploaded_file = st.file_uploader("Carregue um arquivo CSV", type=["csv"])

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

if uploaded_file is not None:
     # Lendo o arquivo CSV
     df = pd.read_csv(uploaded_file)
     st.write("Dados carregados com sucesso!")
     st.dataframe(df)
else:
    st.warning("Por favor, carregue um arquivo para continuar.")

botao_analise = st.button("Gerar Análise", type="primary", use_container_width=True)

    # st.session_state['upload_csv'] = upload_csv  
    # st.success("csv uploaded successfully!")



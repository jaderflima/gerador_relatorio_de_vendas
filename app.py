import streamlit as st

st.set_page_config(page_title="DataNExT", layout="centered")

st.markdown(
    """
    <style>
        body {
            background-color: #C23B22; /* Cor de fundo */
        }
        .stApp {
            background-color: #C23B22;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("DataNExT")

empresa = st.text_input("Nome da Companhia", placeholder="Digite o nome da empresa", label_visibility="visible")

col1, col2 = st.columns([0.9, 0.1], vertical_alignment="bottom")
with col1:
    logo = st.text_input("Logo URL", placeholder="https://example.com/logo.png", label_visibility="visible")
with col2:
    upload_logo = st.button("", on_click=None, type="secondary", icon=":material/add_circle:", disabled=False, use_container_width=False)

upload_csv = st.file_uploader("Upload CSV", type="csv", on_change=None, args=None, kwargs=None, disabled=False, label_visibility="visible")

botao_analise = st.button("Gerar Análise", on_click=None, type="primary", disabled=True, use_container_width=True)
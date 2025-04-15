import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from fpdf import FPDF

# --- Funções Utilitárias ---
@st.cache_data
def load_data(nrows, uploaded_file):
    """Carrega dados de um arquivo CSV e realiza transformações básicas."""
    data = pd.read_csv(uploaded_file, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

def imagem_base64(caminho_imagem):
    with open(caminho_imagem, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def gerar_pdf(data_for_pdf, empresa_nome):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Dashboard DataNExT", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Nome da Empresa: {empresa_nome}", ln=True, align="L")
    pdf.cell(200, 10, txt="Relatório gerado a partir do dashboard.", ln=True, align="L")

    if data_for_pdf is not None:
        pdf.cell(200, 10, txt=f"Total de Vendas: R$ {data_for_pdf['valor_total'].sum():,.2f}".replace(",", "."), ln=True, align="L")
        # Adicione mais informações relevantes para o PDF

    pdf_output = BytesIO()
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    pdf_output.write(pdf_bytes)
    pdf_output.seek(0)
    return pdf_output

def borda(title, value):
    st.markdown(
    f"""
    <div style="
        border: 2px solid;
        border-radius: 10px;
        padding:10px;
        margin-bottom:8px;
        background-color: white;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
        text-align:center;
    ">
        <h4 style="margin-bottom: 8px; color: #333; font-size:20px;">{title} </h4>
        <p style="font-size: 25px; font-weight: bold; margin: 0; color: #000;">{value} </p>
    </div>
""",
unsafe_allow_html=True
)

#  Página Principal (Carregar Dados)
def main_page():
    st.set_page_config(page_title="DataNext - Carregar Dados", layout="centered", page_icon="icon_DataNext.png")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("logo_azul.png", width=300)

    empresa = st.text_input("Nome da Empresa", placeholder="Digite o nome da empresa")
    if empresa:
        st.session_state['empresa'] = empresa

    logo_url = st.text_input("Envie o endereço da logomarca", placeholder="https://example.com/logo.png")
    if logo_url:
        st.session_state['logo'] = logo_url

    uploaded_logo = st.file_uploader("Ou faça upload da logomarca", type=["png", "jpg", "jpeg"])
    if uploaded_logo is not None:
        st.session_state['logo'] = uploaded_logo.getvalue()

    if 'logo' in st.session_state:
        if isinstance(st.session_state['logo'], bytes):
            st.success("Logomarca salva via upload de arquivo!")
        else:
            st.success("Logomarca salva via URL!")
    else:
        st.warning("Nenhuma logomarca foi enviada até agora.")

    uploaded_file = st.file_uploader("Faça o upload do seu arquivo CSV", type=["csv"])
    if uploaded_file is not None:
        nrows = 10000
        data = load_data(nrows, uploaded_file)
        st.session_state['data'] = data
        st.success("Arquivo carregado com sucesso!")
    else:
        st.warning("Nenhum arquivo foi enviado.")

    if uploaded_file is not None and st.checkbox('Mostrar dados brutos'):
        st.subheader('Dados Brutos')
        st.write(st.session_state['data'])

    st.markdown("""
        <style>
            div[data-testid="stButton"] > button {
            background-color: #3498db !important;
            color: white !important;
            border: none !important;
            }
            div[data-testid="stButton"] > button:hover {
            background-color: #2980b9 !important;
            }
        <style>
            """, unsafe_allow_html=True)

    if st.button("Gerar Relatório de Vendas", type="primary", use_container_width=True):
        if 'data' in st.session_state:
            st.session_state['current_page'] = 'relatorio'
            st.rerun()
        else:
            st.warning("Por favor, carregue os dados antes de gerar o relatório.")

    st.markdown("""<hr><div style='text-align: center; font-size: small;'>©Todos os direitos reservados.</div>""", unsafe_allow_html=True)

# --- Página de Relatório ---
def relatorio_page():
    st.set_page_config(page_title="DATANExT", layout="wide")

    st.markdown("""
    <style>
    /* Estilos CSS para o multiselect e slider (mantidos do page_02.py) */
    section[data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] {
        background-color: #2980b9 !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 2px !important;
    }
    section[data-testid="stSidebar"] .stMultiSelect div[data-baseweb="select"] * {
        color: white !important;
    }
    section[data-testid="stSidebar"] .stMultiSelect span[data-baseweb="tag"] {
        background-color: #2980b9 !important;
        color: white !important;
        border: none !important;
        border-radius: 5px !important;
    }
    section[data-testid="stSidebar"] .stMultiSelect span[data-baseweb="tag"] svg {
        color: white !important;
    }
    section[data-testid="stSidebar"] .stMultiSelect div[role="listbox"] {
        background-color: #2980b9 !important;
        color: white !important;
    }
    section[data-testid="stSidebar"] .stMultiSelect div[role="option"] {
        background-color: #2980b9 !important;
        color: white !important;
    }
        section[data-testid="stSidebar"] .stMultiSelect div[role="option"]:hover {
        background-color: #2980b9 !important;
    }
    div[data-baseweb="slider"] > div > div:nth-child(1) {
        background: #2980b9 !important;
        height: 4px !important;
    }
    div[data-baseweb="slider"] [role="slider"] {
        background: #2980b9 !important;
        border: none !important;
    }
    div[data-baseweb="slider"] [data-testid="stTooltipLabel"] {
        background: #2980b9 !important;
        height: 4px !important;
    }
    div[data-baseweb="slider"] [data-testid="stTickBar"] span {
        font-weight: bold !important;
    }
    </style>
    """,
    unsafe_allow_html=True)

    empresa = st.session_state.get('empresa', 'Sem empresa definida')
    logo = st.session_state.get('logo', None)
    data = st.session_state.get('data', None)

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

    if data is not None:
        pdf_file = gerar_pdf(data.copy(), empresa)
        pdf_base64 = base64.b64encode(pdf_file.getvalue()).decode('latin1')
        logo_pdf = "pdf.png"
        base_logo_pdf = imagem_base64(logo_pdf)
        st.markdown(
            f"""
            <style>
            .pdf-icon-container {{
                display: flex;
                justify-content: flex-end; /* Alinha o ícone à direita */
                margin-top: 10px;
            }}
            .pdf-icon {{
                width: 40px; /* Tamanho do ícone */
                cursor: pointer; /* Estilo do cursor ao passar o mouse */
            }}
            </style>
            <div class="pdf-icon-container">
                <a download="dashboard.pdf" href="data:application/pdf;base64,{pdf_base64}">
                    <img src="data:image/png;base64,{base_logo_pdf}" class="pdf-icon" alt="PDF Icon">
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

    if logo:
        if isinstance(logo, bytes):
            st.sidebar.markdown(
                f"""
                <div style="display: flex; justify-content: center; align-items: center;">
                    <img src="data:image/png;base64,{base64.b64encode(logo).decode()}" width="150" alt="Logomarca">
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.sidebar.markdown(
                f"""
                <div style="display: flex; justify-content: center; align-items: center;">
                    <img src="{logo}" width="150" alt="Logomarca enviada por URL">
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        caminho_logo = "logo_01.png"
        base_logo = imagem_base64(caminho_logo)
        st.sidebar.markdown(
            f"""
            <div style="display: flex; justify-content: center; align-items: center;">
                <img src="data:image/png;base64,{base_logo}" width="150" alt="Logomarca local">
            </div>
            <hr style="margin-top: 10;">
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        f"""
        <h1 style= 'text-align:left; color: #12357c'>
        Dashboard {empresa}
        </h1>
        """,
        unsafe_allow_html=True
    )

    if data is not None:
        st.success("Análise Gerada com Sucesso!")

        data['data_venda'] = pd.to_datetime(data['data_venda'], errors='coerce')
        data['quantidade_vendida'] = pd.to_numeric(data['quantidade_vendida'], errors='coerce')
        data['preço_unitário'] = pd.to_numeric(data['preço_unitário'], errors='coerce')
        data['valor_total'] = data['quantidade_vendida'] * data['preço_unitário']
        data['AnoMes'] = data['data_venda'].dt.to_period('M')

        st.sidebar.markdown("#### FILTROS")

        categorias = st.sidebar.multiselect("Categoria do Produto", options=data['categoria_produto'].dropna().unique())
        if categorias:
            data = data[data['categoria_produto'].isin(categorias)]

        vendedores = st.sidebar.multiselect("Vendedores", options=data['vendedor'].dropna().unique())
        if vendedores:
            data = data[data['vendedor'].isin(vendedores)]

        canal = st.sidebar.multiselect("Canal de Venda", options=data['canal_venda'].dropna().unique())
        if canal:
            data = data[data['canal_venda'].isin(canal)]

        data_minima = data['data_venda'].min().date()
        data_maxima = data['data_venda'].max().date()

        intervalo_data =  st.sidebar.slider("Intervalo de Vendas",min_value=data_minima,max_value=data_maxima,value=(data_minima,data_maxima))
        data = data[(data['data_venda'].dt.date >= intervalo_data[0]) & (data['data_venda'].dt.date <=  intervalo_data[1])]

        vendas_por_mes = data.groupby('AnoMes')['valor_total'].sum()
        vendas_por_mes.index = vendas_por_mes.index.astype(str)

        vendas_categoria = data.groupby('categoria_produto')['valor_total'].sum().sort_values(ascending=False)

        vendas_vendedor = data.groupby('vendedor')['valor_total'].sum().sort_values(ascending=False)

        canal_vendas = data.groupby('canal_venda').size().sort_values(ascending=False)

        col1, col2, col3 = st.columns([0.5, 0.5, 0.3])
        with col1:
            st.write('#### Vendas por Mês')
            fig1, ax1 = plt.subplots(figsize=(6, 3))
            vendas_por_mes.plot(kind='barh', ax=ax1, color='#2980b9')
            ax1.set_xlabel('Ano / Mês')
            ax1.set_ylabel('Valor Total')
            ax1.grid(True)
            plt.xticks(rotation=0)
            for container in ax1.containers:
                rotulo1 = [f'R$ {v:,.2f}'.replace(",","x").replace(".",",").replace("x",".") for v in container.datavalues]
                ax1.bar_label(container,labels=rotulo1, padding=5, fontsize = 10)
            st.pyplot(fig1)

        with col2:
            st.write('###### Vendas por Categoria')
            fig2, ax2 = plt.subplots(figsize=(5, 3))
            cores = ['#2980b9', '#3498db', '#1f618d', '#2471a3','#12496e','#91c8ed']

            vendas_categoria.plot(
                kind='pie',
                ax=ax2,
                colors=cores,
                autopct='%1.1f%%',
                startangle=90,
                legend=False
            )

            ax2.set_ylabel('')
            ax2.set_xlabel('')
            ax2.axis('equal')
            st.pyplot(fig2)


        with col3:
            qtd_vendas = data.shape[0]
            faturamento_total = data['valor_total'].sum()
            ticket_medio = faturamento_total / qtd_vendas if qtd_vendas != 0 else 0

            borda("Quantidade de Vendas", f"{qtd_vendas:,}".replace(",", "."))
            borda("Faturamento Total", f"R$ {faturamento_total:,.2f}".replace(",", "."))
            borda("Ticket Médio", f"R$ {ticket_medio:,.2f}".replace(",", ".").replace(".", ","))

        col4, col5 = st.columns([0.5, 0.5])
        with col4:
            st.write('#### Vendas por Vendedor')
            fig4, ax4 = plt.subplots(figsize=(6, 3))
            ax4.plot(vendas_vendedor.index, vendas_vendedor.values, marker='o', linestyle='-', color='#2471a3')
            ax4.set_xlabel('Vendedor')
            ax4.set_ylabel('Valor Total')
            ax4.grid(True)
            plt.xticks(rotation=0, ha='right', fontsize=6)


            # Rótulos nos pontos
            for i, valor in enumerate(vendas_vendedor.values):
                valor_formatado = f'R$ {valor:,.0f}'.replace(',', '.')
                ax4.annotate(valor_formatado,
                            (vendas_vendedor.index[i], vendas_vendedor.values[i]),
                            textcoords="offset points",
                            xytext=(0, 8),
                            ha='center',
                            fontsize=8)

            st.pyplot(fig4)

        with col5:
            st.write('#### Canal de vendas')
            fig5, ax5 = plt.subplots(figsize=(6, 3))
            canal_vendas.plot(kind='bar', ax=ax5)
            ax5.set_xlabel('')
            ax5.set_ylabel('')
            ax5.grid(False)
            plt.xticks(rotation=0)
            for container in ax5.containers:
                ax5.bar_label(container, fmt="%.0f",  padding=0.8, fontsize = 7)
            st.pyplot(fig5)

    else:
        st.warning("Por favor, carregue os dados na página inicial.")

    st.markdown("""<hr><div style= 'text-align: center;font-size: small;'>©Todos os direitos reservados.</div>""", unsafe_allow_html=True)

# --- Controle de Página ---
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'main'

if st.session_state['current_page'] == 'main':
    main_page()
elif st.session_state['current_page'] == 'relatorio':
    relatorio_page()

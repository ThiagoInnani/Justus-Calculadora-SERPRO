import streamlit as st
import pandas as pd
from main import calcular_custo_integra, formatar_detalhes_faixa
import plotly.graph_objects as go

st.set_page_config(page_title="Calculadora SERPRO JUSTUS", page_icon="img/Logo Justus.png", layout="wide")

st.logo(
    image="img/LogoJustusExtended.png",
    size="large",
    link="https://justus.com.br",
    icon_image="img/Logo Justus.png",
)
st.sidebar.markdown("Bem-Vindo(a) a calculadora de Serpro da Justus!")


st.title("Calculadora SERPRO JUSTUS")

tab1, tab2 = st.tabs(["Simulador de Custos", "Tabela de Custos"])

with tab1:
    st.header("Simulador de Custos do Integra Contador")

    # Entradas do usuário
    num_empresas = st.number_input("Número de empresas clientes", min_value=1, value=1, step=1)
    consultas_por_empresa = st.number_input("Número de consultas por empresa/mês", min_value=0, value=0, step=1)
    emissoes_por_empresa = st.number_input("Número de emissões por empresa/mês", min_value=0, value=0, step=1)
    declaracoes_por_empresa = st.number_input("Número de declarações por empresa/mês", min_value=0, value=0, step=1)

    if st.button("Calcular Custos"):
        resultado = calcular_custo_integra(num_empresas, consultas_por_empresa, emissoes_por_empresa, declaracoes_por_empresa)
        
        #st.write(resultado)  # Adicionado para depuração

        st.subheader("Resultado da simulação")

        
        # Exibir custo total
        st.metric("Custo Total", f"R$ {resultado['Custo Total']:.2f}")
        
        # Criar tabela de custos detalhados
        detalhes = {
            "Tipo": ["Consultas", "Emissões", "Declarações"],
            "Custo": [
                f"R$ {resultado.get('Custo Consultas', 0):.2f}",
                f"R$ {resultado.get('Custo Emissões', 0):.2f}",
                f"R$ {resultado.get('Custo Declarações', 0):.2f}"
            ],
            "Detalhes": [
                formatar_detalhes_faixa(resultado.get('Faixas Consultas', [])),
                formatar_detalhes_faixa(resultado.get('Faixas Emissões', [])),
                formatar_detalhes_faixa(resultado.get('Faixas Declarações', []))
            ]
        }

        
        df = pd.DataFrame(detalhes)
        st.table(df)
        
        # Gráfico de pizza
        fig = go.Figure(data=[go.Pie(
            labels=["Consultas", "Emissões", "Declarações"],
            values=[
                resultado.get('Custo Consultas', 0),  # Usa 0 como valor padrão se a chave não existir
                resultado.get('Custo Emissões', 0),   # Usa 0 como valor padrão se a chave não existir
                resultado.get('Custo Declarações', 0) # Usa 0 como valor padrão se a chave não existir
            ]
        )])
        fig.update_layout(title="Distribuição de Custos")
        st.plotly_chart(fig)

        st.info("Este simulador ajuda a calcular os custos do Integra Contador com base no número de empresas e operações realizadas.")

with tab2:
    st.header("Tabela de Custos do Serpro")

    st.subheader("Como funciona o modelo de pagamento?")
    st.write("O pagamento é calculado direto na faixa do consumo total do mês.")
    st.write("Confira abaixo a tabela de preços e as faixas de consumo")

    # Dados para as tabelas
    dados_consulta = {
        "Faixa": range(1, 9),
        "Consumo": ["De 1 até 300", "De 301 até 1.000", "De 1.001 até 3.000", "De 3.001 até 7.000", 
                    "De 7.001 até 15.000", "De 15.001 até 23.000", "De 23.001 até 30.000", "Acima de 30.000"],
        "Preço": ["R$ 0,24", "R$ 0,21", "R$ 0,18", "R$ 0,16", "R$ 0,14", "R$ 0,11", "R$ 0,09", "R$ 0,06"]
    }

    dados_emissao = {
        "Faixa": range(1, 9),
        "Consumo": ["De 1 até 500", "De 501 até 5.000", "De 5.001 até 10.000", "De 10.001 até 15.000", 
                    "De 15.001 até 25.000", "De 25.001 até 35.000", "De 35.001 até 50.000", "Acima de 50.000"],
        "Preço": ["R$ 0,32", "R$ 0,29", "R$ 0,26", "R$ 0,22", "R$ 0,19", "R$ 0,16", "R$ 0,12", "R$ 0,08"]
    }

    dados_declaracao = {
        "Faixa": range(1, 9),
        "Consumo": ["De 1 até 100", "De 101 até 500", "De 501 até 1.000", "De 1.001 até 3.000", 
                    "De 3.001 até 5.000", "De 5.001 até 8.000", "De 8.001 até 10.000", "Acima de 10.000"],
        "Preço": ["R$ 0,40", "R$ 0,36", "R$ 0,32", "R$ 0,28", "R$ 0,24", "R$ 0,20", "R$ 0,16", "R$ 0,12"]
    }

    # Criar DataFrames
    df_consulta = pd.DataFrame(dados_consulta)
    df_emissao = pd.DataFrame(dados_emissao)
    df_declaracao = pd.DataFrame(dados_declaracao)

    # Exibir tabelas lado a lado
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Consulta")
        st.table(df_consulta)

    with col2:
        st.subheader("Emissão")
        st.table(df_emissao)

    with col3:
        st.subheader("Declaração")
        st.table(df_declaracao)

    st.markdown("Para mais informações sobre custos e detalhes do serviço, consulte a [página oficial do Integra Contador](https://loja.serpro.gov.br/integracontador).")

    st.warning("Nota: Os preços podem estar sujeitos a alterações. Consulte sempre a tabela mais recente para obter informações atualizadas.")

# Adicionar informações do criador com cor personalizada
st.markdown("---")
st.subheader("Justus Informática")
st.markdown(
    """
    **Endereço:** Rua Frederico Bahls, 666. Centro, Ponta Grossa - PR\n
    **E-mail:** justus@justus.com.br\n
    **Telefone:** (42) 2101 7700\n
    **Site:** https://justus.com.br
    """
)

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Configurar a página
st.set_page_config(page_title="Controle de Gastos", layout="centered")

# Título do aplicativo
st.title("Aplicativo de Controle de Gastos")

# Inicializar dados
if 'dados' not in st.session_state:
    st.session_state['dados'] = {
        'Dinheiro em Conta': 0.0,
        'Gastos Diários': [],
        'Gastos Fixos Mensais': [],
        'Historico Gastos': []
    }

# Funções para adicionar valores
def adicionar_dinheiro(valor):
    st.session_state['dados']['Dinheiro em Conta'] += valor

def adicionar_gasto_diario(descricao, valor):
    st.session_state['dados']['Gastos Diários'].append({'Descrição': descricao, 'Valor': valor})
    st.session_state['dados']['Historico Gastos'].append({'Descrição': descricao, 'Valor': valor})

def adicionar_gasto_fixo(descricao, valor):
    st.session_state['dados']['Gastos Fixos Mensais'].append({'Descrição': descricao, 'Valor': valor})
    st.session_state['dados']['Historico Gastos'].append({'Descrição': descricao, 'Valor': valor})

# Inputs para adicionar valores
st.header("Adicionar Dinheiro em Conta")
valor_dinheiro = st.number_input("Valor", min_value=0.0, format="%.2f")
if st.button("Adicionar Dinheiro"):
    adicionar_dinheiro(valor_dinheiro)
    st.success("Dinheiro adicionado com sucesso!")

st.header("Registrar Gastos Diários")
descricao_diaria = st.text_input("Descrição do Gasto Diário")
valor_diario = st.number_input("Valor Diário", min_value=0.0, format="%.2f", key="valor_diario")
if st.button("Adicionar Gasto Diário"):
    adicionar_gasto_diario(descricao_diaria, valor_diario)
    st.success("Gasto diário adicionado com sucesso!")

st.header("Registrar Gastos Fixos Mensais")
descricao_fixo = st.text_input("Descrição do Gasto Fixo")
valor_fixo = st.number_input("Valor Fixo", min_value=0.0, format="%.2f", key="valor_fixo")
if st.button("Adicionar Gasto Fixo"):
    adicionar_gasto_fixo(descricao_fixo, valor_fixo)
    st.success("Gasto fixo adicionado com sucesso!")

# Exibir os dados
st.header("Dados Atuais")
st.write(f"Dinheiro em Conta: R$ {st.session_state['dados']['Dinheiro em Conta']:.2f}")
if st.session_state['dados']['Gastos Diários']:
    st.write("Gastos Diários:")
    st.write(pd.DataFrame(st.session_state['dados']['Gastos Diários']))
if st.session_state['dados']['Gastos Fixos Mensais']:
    st.write("Gastos Fixos Mensais:")
    st.write(pd.DataFrame(st.session_state['dados']['Gastos Fixos Mensais']))

# Gerar gráficos
st.header("Gráficos")
if st.session_state['dados']['Historico Gastos']:
    df = pd.DataFrame(st.session_state['dados']['Historico Gastos'])
    
    # Gráfico de barra dos gastos
    st.subheader("Gastos Totais")
    fig, ax = plt.subplots()
    df.groupby('Descrição')['Valor'].sum().plot(kind='bar', ax=ax)
    st.pyplot(fig)
    
    # Gráfico de linha dos gastos ao longo do tempo
    st.subheader("Histórico de Gastos")
    fig, ax = plt.subplots()
    df['Valor'].plot(kind='line', ax=ax)
    st.pyplot(fig)

# Salvar os dados em um arquivo CSV
if st.button("Salvar Dados"):
    df.to_csv("gastos.csv", index=False)
    st.success("Dados salvos com sucesso!")

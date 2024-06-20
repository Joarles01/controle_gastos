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
        'Renda Mensal': 0.0,
        'Gastos Diários': [],
        'Gastos Fixos Mensais': [],
        'Historico Gastos': []
    }

# Funções para adicionar valores
def adicionar_dinheiro(valor):
    st.session_state['dados']['Dinheiro em Conta'] += valor

def adicionar_gasto(descricao, valor, categoria, motivo):
    gasto = {'Descrição': descricao, 'Valor': valor, 'Categoria': categoria, 'Motivo': motivo}
    st.session_state['dados']['Dinheiro em Conta'] -= valor
    if categoria == "Diário":
        st.session_state['dados']['Gastos Diários'].append(gasto)
    else:
        st.session_state['dados']['Gastos Fixos Mensais'].append(gasto)
    st.session_state['dados']['Historico Gastos'].append(gasto)

def adicionar_renda_mensal(valor):
    st.session_state['dados']['Renda Mensal'] = valor
    st.session_state['dados']['Dinheiro em Conta'] += valor

# Inputs para adicionar valores
st.header("Adicionar Dinheiro em Conta")
valor_dinheiro = st.number_input("Valor", min_value=0.0, format="%.2f")
if st.button("Adicionar Dinheiro"):
    adicionar_dinheiro(valor_dinheiro)
    st.success("Dinheiro adicionado com sucesso!")

st.header("Adicionar Renda Mensal")
valor_renda = st.number_input("Renda Mensal", min_value=0.0, format="%.2f", key="renda")
if st.button("Adicionar Renda Mensal"):
    adicionar_renda_mensal(valor_renda)
    st.success("Renda mensal adicionada com sucesso!")

st.header("Registrar Gastos")
descricao = st.text_input("Descrição do Gasto")
valor = st.number_input("Valor", min_value=0.0, format="%.2f", key="valor")
categoria = st.selectbox("Categoria", ["Diário", "Fixo Mensal"])
motivo = st.text_input("Motivo do Gasto")
if st.button("Adicionar Gasto"):
    adicionar_gasto(descricao, valor, categoria, motivo)
    st.success("Gasto adicionado com sucesso!")

# Exibir os dados
st.header("Dados Atuais")
st.write(f"Dinheiro em Conta: R$ {st.session_state['dados']['Dinheiro em Conta']:.2f}")
st.write(f"Renda Mensal: R$ {st.session_state['dados']['Renda Mensal']:.2f}")
if st.session_state['dados']['Gastos Diários']:
    st.write("Gastos Diários:")
    st.write(pd.DataFrame(st.session_state['dados']['Gastos Diários']))
if st.session_state['dados']['Gastos Fixos Mensais']:
    st.write("Gastos Fixos Mensais:")
    st.write(pd.DataFrame(st.session_state['dados']['Gastos Fixos Mensais']))

# Calcular o total gasto no mês
total_gastos_mes = sum(gasto['Valor'] for gasto in st.session_state['dados']['Historico Gastos'])

st.write(f"Total Gasto no Mês: R$ {total_gastos_mes:.2f}")

# Função para editar dados
def editar_dados():
    st.subheader("Editar Gastos")
    tipo_gasto = st.selectbox("Selecionar Tipo de Gasto", ["Diário", "Fixo Mensal"])
    if tipo_gasto == "Diário":
        gastos = st.session_state['dados']['Gastos Diários']
    else:
        gastos = st.session_state['dados']['Gastos Fixos Mensais']
    
    if gastos:
        gasto_selecionado = st.selectbox("Selecionar Gasto", [f"{g['Descrição']} - R$ {g['Valor']:.2f}" for g in gastos])
        gasto_index = [f"{g['Descrição']} - R$ {g['Valor']:.2f}" for g in gastos].index(gasto_selecionado)
        
        nova_descricao = st.text_input("Nova Descrição", value=gastos[gasto_index].get('Descrição', ''))
        novo_valor = st.number_input("Novo Valor", min_value=0.0, format="%.2f", value=gastos[gasto_index].get('Valor', 0.0))
        novo_motivo = st.text_input("Novo Motivo", value=gastos[gasto_index].get('Motivo', ''))
        
        if st.button("Salvar Alterações"):
            # Atualizar o dinheiro em conta com o valor antigo e novo
            valor_antigo = gastos[gasto_index]['Valor']
            st.session_state['dados']['Dinheiro em Conta'] += valor_antigo - novo_valor
            
            gastos[gasto_index]['Descrição'] = nova_descricao
            gastos[gasto_index]['Valor'] = novo_valor
            gastos[gasto_index]['Motivo'] = novo_motivo
            st.success("Gasto atualizado com sucesso!")
            
        if st.button("Excluir Gasto"):
            # Atualizar o dinheiro em conta ao excluir o gasto
            valor_antigo = gastos[gasto_index]['Valor']
            st.session_state['dados']['Dinheiro em Conta'] += valor_antigo
            
            gastos.pop(gasto_index)
            st.success("Gasto excluído com sucesso!")

editar_dados()

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

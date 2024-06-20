import streamlit as st
import pandas as pd

# Configurar a página
st.set_page_config(page_title="Controle de Gastos", layout="centered")

# Título do aplicativo
st.title("Aplicativo de Controle de Gastos")

# Inicializar uma lista para armazenar os gastos
if 'gastos' not in st.session_state:
    st.session_state['gastos'] = []

# Função para adicionar um gasto
def adicionar_gasto(descricao, valor, categoria):
    st.session_state['gastos'].append({
        'Descrição': descricao,
        'Valor': valor,
        'Categoria': categoria
    })

# Inputs para adicionar gastos
descricao = st.text_input("Descrição do Gasto")
valor = st.number_input("Valor", min_value=0.0, format="%.2f")
categoria = st.selectbox("Categoria", ["Alimentação", "Transporte", "Lazer", "Outros"])

# Botão para adicionar gasto
if st.button("Adicionar Gasto"):
    adicionar_gasto(descricao, valor, categoria)
    st.success("Gasto adicionado com sucesso!")

# Exibir a lista de gastos
if st.session_state['gastos']:
    df = pd.DataFrame(st.session_state['gastos'])
    st.write(df)

    # Exibir o total de gastos
    total = df['Valor'].sum()
    st.write(f"**Total de Gastos:** R$ {total:.2f}")
else:
    st.write("Nenhum gasto adicionado ainda.")

# Salvar os dados em um arquivo CSV
if st.button("Salvar Dados"):
    df.to_csv("gastos.csv", index=False)
    st.success("Dados salvos com sucesso!")

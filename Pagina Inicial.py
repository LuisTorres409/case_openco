import streamlit as st
from utils import load_data, create_bad_column, create_new_features
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Case OpenCo", layout="wide")

# Título principal
st.markdown("""
# Bem-vindo ao App do Case OpenCo

Este aplicativo é uma implementação do case do processo seletivo da OpenCo. Nele, realizamos uma análise detalhada de um dataset com informações sobre contratos, organizados por empresa, setor, valor, entre outros atributos.

Você pode navegar pelas respostas de cada pergunta utilizando a barra lateral.

Além disso, todas as análises realizadas estão disponíveis em um notebook, que pode ser encontrado na pasta **Notebooks** deste repositório.
""")

# Exemplo de pré-carregamento leve dos dados
df = load_data()

st.markdown("### Visualização rápida da base (primeiras linhas)")
st.dataframe(df.head())

# 📊 Case OpenCo – Análise de Crédito

Este repositório é a resposta ao **case do processo seletivo da OpenCo**. Ele está dividido em duas partes principais:

1. 📓 Análises exploratórias e modelagens em Jupyter Notebook
2. 🌐 Aplicativo interativo desenvolvido com Streamlit

---

## 1. 📓 Análises no Notebook

A análise completa dos dados foi feita em um notebook, disponível na pasta [`Notebooks/`](./Notebooks).  
Nele estão incluídas:

- Análises descritivas e estatísticas
- Criação de variáveis derivadas
- Identificação de padrões de inadimplência
- Visualizações dos dados

---

## 2. 🌐 Aplicativo Streamlit

O repositório principal também contém um **app interativo em Streamlit**, que permite ao usuário explorar as análises diretamente em uma interface visual, organizada por perguntas do case, acessíveis no menu lateral.

🔗 **Acesse o app online aqui:**  
[https://case-openco.streamlit.app/](https://case-openco.streamlit.app/)

---

## 🚀 Como executar localmente

Siga os passos abaixo para rodar o projeto localmente:

```bash
# 1. Clone o repositório
git clone https://github.com/LuisTorres409/case_openco.git
cd case_openco

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Execute o app
streamlit run "Página Inicial.py"

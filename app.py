# 1. Importações
import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import requests
from streamlit_lottie import st_lottie

# --- FUNÇÕES AUXILIARES ---
def load_lottieurl(url: str):
    """Carrega uma animação Lottie de um URL."""
    try:
        r = requests.get(url, timeout=10)
        if r.status_code != 200:
            return None
        return r.json()
    except requests.exceptions.RequestException:
        return None

@st.cache_data
def treinar_modelo():
    """Treina o modelo com os dados."""
    df = pd.read_csv("pizzas.csv")
    x = df[["diametro"]]
    y = df["preco"]
    modelo = LinearRegression()
    modelo.fit(x, y)
    return modelo, df

# --- CARREGAR ANIMAÇÃO (fatia de pizza) ---
lottie_pizza_slice = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_pizzapie.json")  # fatia de pizza animada

# --- EXECUÇÃO PRINCIPAL ---
model, df = treinar_modelo()

# --- INTERFACE ---
st.set_page_config(page_title="🍕 Previsor de Preços de Pizza", page_icon="🍕", layout="centered")

st.title("🍕 Previsão do Preço de Pizzas")
st.write("Este app usa **Regressão Linear** para prever o preço de uma pizza com base no diâmetro.")

# --- Gráfico ---
st.write("### 📊 Relação entre Diâmetro e Preço")
fig, ax = plt.subplots()
ax.scatter(df["diametro"], df["preco"], color="blue", label="Dados Reais")
ax.plot(df["diametro"], model.predict(df[["diametro"]]), color="red", linewidth=2, label="Linha de Regressão")
ax.set_xlabel("Diâmetro (cm)")
ax.set_ylabel("Preço (R$)")
ax.legend()
st.pyplot(fig)

# --- Formulário ---
st.write("### 🔮 Faça sua Previsão")
with st.form("prediction_form"):
    diametro_input = st.number_input(
        "Digite o diâmetro da pizza (em cm):",
        min_value=10, max_value=50, value=28, step=1
    )
    submitted = st.form_submit_button("Prever Preço")


# --- Resultado ---
if submitted:
    preco_previsto = model.predict([[diametro_input]])[0]
    st.metric("Preço Previsto", f"R$ {preco_previsto:.2f}")

# --- RODAPÉ ---
st.markdown("Desenvolvido por **Tatiana Kami**")





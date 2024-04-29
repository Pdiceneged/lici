import streamlit as st
import requests
import json
import base64
import datetime

st.set_page_config(
    page_title="Licitalert",
    page_icon="🤝"
)
@st.cache_data()
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_img_as_base64("fundocontrat.png")

page_bg_img = f"""
<style>
header, footer {{
    visibility: hidden !important;
}}

#MainMenu {{
    visibility: visible !important;
    color: #F44D00;
}}

[data-testid="stAppViewContainer"] > .main {{
    background-image: url("data:fundoesg4k/png;base64,{img}");
    background-size: cover; 
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

[data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
    right: 2rem;
}}

.stTextInput>div>div>input[type="text"] {{
    background-color: #E8C8BA; 
    color: #000; 
    border-radius: 7px; 
    border: 2px solid #000010; 
    padding: 5px; 
    width: 500; 
}}

@media (max-width: 360px) {{
    [data-testid="stAppViewContainer"] > .main, [data-testid="stSidebar"] > div:first-child {{
        background-size: auto;
    }}
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

def coletar_licitacoes(url, palavras_chave, pagina, token, data_maxima, licitacoes_por_pagina=100):
    palavras_chave_str = ",".join(palavras_chave)
    params = {
        'uf': '',
        'palavra_chave': palavras_chave_str,
        'pagina': pagina,
        'licitacoesPorPagina': licitacoes_por_pagina,
        'token': token
    }
    headers = {'Token': token}
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        try:
            data = response.json()
        except json.JSONDecodeError:
            st.error("Erro ao decodificar a resposta JSON.")
            return None

        licitacoes_info = ""
        for licitacao in data.get('licitacoes', []):
            try:
                data_abertura = datetime.datetime.strptime(licitacao['abertura'], "%d/%m/%Y")
                if data_abertura <= data_maxima:
                    licitacoes_info += f"Título: {licitacao['titulo']}\n\n"
                    licitacoes_info += f"Identificador desta licitação: {licitacao['id_licitacao']}\n\n"
                    licitacoes_info += f"Modalidade: {licitacao['tipo']}\n\n"
                    licitacoes_info += f"Órgão Responsável: {licitacao['orgao']}\n\n"
                    licitacoes_info += f"Data de Abertura: {licitacao['abertura']}\n\n"
                    licitacoes_info += f"Valor: {licitacao['valor']}\n\n"
                    licitacoes_info += f"Objeto: {licitacao['objeto']}\n\n"
                    licitacoes_info += f"Link: {licitacao['link']}\n\n"
                    licitacoes_info += "---\n\n"
            except ValueError as e:
                st.warning(f"Data de abertura inválida para a licitação com título {licitacao['titulo']}: {licitacao['abertura']}")
                continue  # Pula para a próxima licitação
        return licitacoes_info
    else:
        st.error(f"Erro na solicitação: {response.status_code}")
        return None

    st.markdown("---")

def imprimir_licitacoes(licitacoes_info):
    st.write("## Resultado da consulta de licitações")
    if licitacoes_info:
        licitacoes_split = licitacoes_info.split('---\n\n')
        for licitacao in licitacoes_split:
            if licitacao:
                st.write(licitacao)
                st.markdown("---")
    else:
        st.write("Nenhuma licitação encontrada.")

def main():
    st.image("kkk.png", width=270, use_column_width=False)
    st.title("Olá Contratos")
    token = st.text_input("Coloque o Token:", type='password')
    url_api = st.secrets["licitacao"]["url"]
    data_maxima_input = st.date_input("Data máxima para as licitações:", datetime.datetime.today())
    data_maxima = datetime.datetime.combine(data_maxima_input, datetime.datetime.min.time())

    buscar_button = st.button("Buscar Licitações")
    if buscar_button:
        st.info("Buscando licitações...")
        licitacoes_info = coletar_licitacoes(url_api, ["elétrica", "fotovoltaica", "subestação", "corte", "religa", "sigfi", "migdi"], 1, token, data_maxima)
        st.success("Licitações processadas com sucesso!")
        st.write("Número de licitações coletadas: {}".format(len(licitacoes_info.split('---\n\n')) - 1))
        imprimir_licitacoes(licitacoes_info)
        

if __name__ == "__main__":
    main()



st.markdown("---")
st.markdown("Desenvolvido por [PedroFS](https://linktr.ee/Pedrofsf)")

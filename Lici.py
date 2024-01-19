import streamlit as st
import requests
import json

def coletar_licitacoes(url, palavras_chave, pagina, token):
    palavras_chave_str = ",".join(palavras_chave)

    params = {
        'uf': '',
        'palavra_chave': palavras_chave_str,
        'pagina': pagina,
        'token': token
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        try:
            data = response.json()
        except json.JSONDecodeError:
            st.error("Erro ao decodificar a resposta JSON.")
            return ""

        licitacoes_info = ""

        for licitacao in data.get('licitacoes', []):
            licitacoes_info += f"Título: {licitacao['titulo']}\n\n"
            licitacoes_info += f"Identificador desta licitação: {licitacao['id_licitacao']}\n\n"
            licitacoes_info += f"Modalidade: {licitacao['tipo']}\n\n"
            licitacoes_info += f"Órgão Responsável: {licitacao['orgao']}\n\n"
            licitacoes_info += f"Data de Abertura: {licitacao['abertura']}\n\n"
            licitacoes_info += f"Valor: {licitacao['valor']}\n\n"
            licitacoes_info += f"Objeto: {licitacao['objeto']}\n\n"
            licitacoes_info += f"Link: {licitacao['link']}\n\n"
            licitacoes_info += "---\n\n"

        return licitacoes_info
    else:
        st.error(f"Erro na solicitação: {response.status_code}")
        st.error(response.text)
        return ""
    st.markdown("---")

def imprimir_licitacoes(licitacoes_info):
    st.write("## Resultado da consulta de solicitações")
    st.text("Bom dia, este é o boletim Ceneged de busca por solicitações.")

    if licitacoes_info:
        licitacoes_split = licitacoes_info.split('\n\n')
        for licitacao in licitacoes_split:
            if licitacao:
                st.write(licitacao)
    else:
        st.write("Nenhuma solicitação encontrada.")


def main():
    st.image("kkk.png", width=270, use_column_width=False)

    st.title("Olá Contratos")
    st.markdown("**Lembre-se de conferir se já foi requisitada a solicitação no dia de hoje, busque apenas 1 vez no dia!**")

    token = st.text_input("Coloque o Token:", type='password')
    url_api = st.secrets["licitacao"]["url"]

    buscar_button = st.button("Buscar Licitações")
    max_licitacoes = 97
    palavras_chave = ["elétrica", "fotovoltaica", "subestação", "corte", "religa", "sigfi", "migdi"]

    if buscar_button:
        st.info("Buscando licitações...")

        licitacoes_info = ""
        pagina_atual = 1
        while len(licitacoes_info.split('\n\n')) < max_licitacoes:
            licitacoes_info_pagina = coletar_licitacoes(url_api, palavras_chave, pagina_atual, token)
            if not licitacoes_info_pagina:
                break

            licitacoes_info += licitacoes_info_pagina
            pagina_atual += 1

        imprimir_licitacoes(licitacoes_info)

        st.success("Licitações processadas com sucesso!")
        st.write("Número de licitações coletadas: {}".format(len(licitacoes_info.split('\n\n')) - 1))

if __name__ == "__main__":
    main()

st.markdown("---")
st.markdown("Desenvolvido por [PedroFS](https://linktr.ee/Pedrofsf)")
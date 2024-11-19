# -*- coding: utf-8 -*-

!pip install requests beautifulsoup4 openai langchain-openai

import requests
from bs4 import BeautifulSoup

def fetch_clean_text_from_url(url):
    """
    Obtém e limpa o texto de uma URL.
    """
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove scripts e estilos
        for script_or_style in soup(['script', 'style']):
            script_or_style.decompose()

        raw_text = soup.get_text(separator=" ")

        # Limpa o texto
        lines = (line.strip() for line in raw_text.splitlines())
        parts = (phrase.strip() for line in lines for phrase in line.split(" "))
        clean_text = '\n'.join(part for part in parts if part)
        return clean_text
    else:
        print(f"Failed to fetch URL. Status code: {response.status_code}")
        return None

from langchain_openai.chat_models.azure import AzureChatOpenAI

def create_azure_chat_client():
    """
    Configura e retorna o cliente AzureChatOpenAI.
    """
    return AzureChatOpenAI(
        azure_endpoint="ENDPOINT_URL",
        api_key="API_KEY",
        api_version="2024-02-15-preview",
        deployment_name="gpt-4o-mini",
        max_retries=0
    )

def translate_text_to_language(text, target_language, client):
    """
    Traduz um texto para o idioma alvo usando AzureChatOpenAI.
    """
    messages = [
        ("system", "Você atua como tradutor de textos"),
        ("user", f"Traduza o seguinte texto para o idioma {target_language} e responda em markdown:\n\n{text}")
    ]
    response = client.invoke(messages)
    print(response.content)
    return response.content

# Exemplo de uso
if __name__ == "__main__":
    url = 'https://dev.to/nozibul_islam_113b1d5334f/dsa-heap-key-questions-and-challenges-3a55'
    azure_client = create_azure_chat_client()

    # Extrai e limpa o texto do artigo
    extracted_text = fetch_clean_text_from_url(url)

    if extracted_text:
        # Traduz o artigo para português
        translated_article = translate_text_to_language(extracted_text, "pt-br", azure_client)
        print(translated_article)

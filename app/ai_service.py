import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('HUGGINGFACE_API_KEY')
API_URL = "https://api-inference.huggingface.co/models/cardiffnlp/twitter-xlm-roberta-base-sentiment"
headers = {"Authorization": f"Bearer {API_KEY}"}

def query_huggingface(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def analyze_sentiment(text_to_analyze):
    if not API_KEY:
        print("ERRO: Chave da API da Hugging Face não encontrada.")
        return "Erro na IA"

    try:
        output = query_huggingface({"inputs": text_to_analyze})
        
        if isinstance(output, list) and output and isinstance(output[0], list):
            best_result = max(output[0], key=lambda x: x.get('score', 0))
            label = best_result.get('label', '').lower()

            sentiment_map = {
                'positive': 'Positivo', 'label_2': 'Positivo',
                'negative': 'Negativo', 'label_0': 'Negativo',
                'neutral': 'Neutro', 'label_1': 'Neutro'
            }
            return sentiment_map.get(label, 'Indefinido')
        else:
            print(f"ERRO: Formato de resposta inesperado da API: {output}")
            return "Erro na IA"
    except Exception as e:
        print(f"ERRO: Ocorreu um erro inesperado na análise: {e}")
        return "Erro na IA"
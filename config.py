import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Classe de configuração que carrega as variáveis sensíveis do .env
    """
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    HUGGINGFACE_API_KEY = os.environ.get('HUGGINGFACE_API_KEY')
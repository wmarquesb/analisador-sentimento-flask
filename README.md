# Analisador de Sentimento com IA

![Captura de tela do Dashboard](https://i.imgur.com/MEnOMQx.png)

### Sobre o Projeto

Esta é uma aplicação web Full Stack construída com Python e Flask, onde usuários podem se cadastrar, fazer login e submeter textos para receber uma análise de sentimento (Positivo, Negativo ou Neutro) em tempo real, fornecida por uma API de Inteligência Artificial.

### Principais Funcionalidades

- **Autenticação de Usuários:** Sistema completo de registro e login com senhas seguras (hash).
- **Análise de Sentimento:** Integração com a API da Hugging Face para classificar textos.
- **Dashboard de Estatísticas:** Visualização de dados agregados, como contagem total e um gráfico de pizza da distribuição de sentimentos.
- **Histórico Paginado:** O histórico de análises é dividido em páginas para uma navegação eficiente.
- **CRUD Completo:** Os usuários podem criar, reler, re-analisar (Update) e apagar seus próprios feedbacks.

### Tecnologias Utilizadas

- **Backend:** Python, Flask, SQLAlchemy, PostgreSQL
- **Frontend:** HTML, CSS, Bootstrap 5, JavaScript (Vanilla), Chart.js
- **APIs:** Hugging Face Inference API
- **Arquitetura:** Application Factory, Blueprints

### Minha Experiência Desenvolvendo Este Projeto

Este projeto foi um passo fundamental na minha jornada como desenvolvedor. O objetivo era ir além de um CRUD básico e construir uma aplicação mais robusta e escalável, aplicando padrões de arquitetura profissionais como o Application Factory.

O maior desafio e, ao mesmo tempo, o aprendizado mais valioso, foi a integração com a API de IA externa. Lidar com a autenticação, tratar as respostas e, principalmente, depurar os problemas de comunicação me deu uma experiência prática muito real. Outro ponto importante foi a implementação do dashboard de estatísticas, que me forçou a pensar em como agregar e visualizar dados de forma útil para o usuário.

Construir este analisador do zero solidificou meu conhecimento em todo o ecossistema Full Stack, desde a modelagem de dados com SQLAlchemy até a criação de uma interface de usuário interativa e responsiva.

### Como Executar Localmente

1.  Clone o repositório e navegue até a pasta.
2.  Crie e ative um ambiente virtual.
3.  Instale as dependências: `pip install -r requirements.txt`.
4.  Crie um arquivo `.env` na raiz e adicione suas chaves, seguindo o exemplo abaixo:
    ```
    SECRET_KEY="sua_chave_secreta_aqui"
    DATABASE_URL="sua_url_do_postgresql"
    HUGGINGFACE_API_KEY="sua_chave_da_huggingface"
    ```
5.  Inicie o servidor: `python run.py`.

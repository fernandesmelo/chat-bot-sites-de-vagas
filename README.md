# Chatbot Telegram baseado em regras (execução local)

Este projeto é um exemplo simples de chatbot do Telegram que responde com mensagens fixas usando Python. A integração é feita via polling, rodando localmente.

## Requisitos

- Python 3.7 ou superior
- Token de bot do Telegram (obtenha via [@BotFather](https://t.me/BotFather))

## Instalação

Clone o projeto ou extraia o `.zip`, depois:

```bash
cd chatbot_telegram_regras
python -m venv venv
source venv/bin/activate  # no Windows: venv\Scripts\activate

pip install -r requirements.txt

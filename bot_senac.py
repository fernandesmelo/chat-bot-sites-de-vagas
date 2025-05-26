import telebot
from telebot import types

CHAVE_API = "7951513268:AAGvzmxfbe5vtmaSVuDJ4idPwWzDeGwuiEo" 

bot = telebot.TeleBot(CHAVE_API, parse_mode="Markdown")

links_uteis = {
    "wellfound.com": "https://wellfound.com/",
    "arc.dev": "https://arc.dev/",
    "https://www.trampardecasa.com.br/": "https://www.trampardecasa.com.br/",
    "remotar.com.br": "https://remotar.com.br/",
    "remote.io": "https://www.remote.io/",
    "workingnomads.com": "https://www.workingnomads.com/jobs",
    "pangian.com": "https://pangian.com/remote/",
    "simplyhired.com.br": "https://www.simplyhired.com.br/",
    "Eureca": "https://eureca.me/",
    "Cia de Talentos": "https://www.ciadetalentos.com.br/pt/",
    "Companhia de Estágios": "https://www.ciadeestagios.com.br/",
    "Acroos.Jobs": "https://login.across.jobs/?pUrlRedirecionadaPortal=/",
    "Machtbox": "https://matchboxbrasil.com/",
    "Glassdoor": "https://www.glassdoor.com.br/index.htm",
    "LinkedIn": "https://br.linkedin.com/",
    "vagas.com": "https://www.vagas.com.br/",
    "gupy": "https://portal.gupy.io/",
    "abler": "https://abler.com.br/",
    "99jobs": "https://99jobs.com/",
    "Yellow.rec": "https://www.yellow.rec.br/",
    "Hays": "https://www.hays.com.br/",
    "Resch": "https://reschrh.com.br/",
    "Catho": "https://reschrh.com.br/",
    "Indeed": "https://br.indeed.com/",
    "Adecco": "https://www.adecco.com/pt-br"
}

def enviar_menu_principal(chat_id, message_id=None):
    """
    Cria e envia a mensagem do menu principal.
    Pode editar uma mensagem existente se message_id for fornecido.
    """
    nome_usuario = "Usuário" 
    try:
        nome_usuario = bot.get_chat(chat_id).first_name
    except Exception:
        pass

    texto = f"""Olá, {nome_usuario}!

Sou o **Assistente Virtual de Sites de Vagas**. 
Como posso te ajudar agora? Selecione uma opção:
"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_vagas = types.InlineKeyboardButton("Vagas.com", callback_data="vagas.com")
    btn_gupy = types.InlineKeyboardButton("Gupy", callback_data="gupy")
    btn_abler = types.InlineKeyboardButton("Abler", callback_data="abler")
    btn_99jobs = types.InlineKeyboardButton("99jobs", callback_data="99jobs")
    markup.add(btn_vagas, btn_gupy, btn_abler, btn_99jobs)

    if message_id:
        bot.edit_message_text(texto, chat_id, message_id, reply_markup=markup)
    else:
        bot.send_message(chat_id, texto, reply_markup=markup)

@bot.message_handler(commands=["start", "iniciar"])
def iniciar(mensagem):
    """
    Apenas chama a função que envia o menu principal.
    """
    enviar_menu_principal(mensagem.chat.id)

@bot.callback_query_handler(func=lambda call: True)
def responder_callback(call):
    """
    Processa todos os cliques nos botões inline.
    """
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    
    markup_voltar = types.InlineKeyboardMarkup()
    btn_voltar = types.InlineKeyboardButton("« Voltar ao Menu", callback_data="voltar_menu")
    markup_voltar.add(btn_voltar)

    if call.data == "voltar_menu":
        enviar_menu_principal(chat_id, message_id)
        bot.answer_callback_query(call.id)
        return

    elif call.data in ["vagas.com", "gupy", "abler", "99jobs"]:
        texto = f"Acesse o site de vagas: {links_uteis[call.data]}"
        bot.edit_message_text(texto, chat_id, message_id, reply_markup=markup_voltar)

    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda mensagem: True)
def responder_padrao(mensagem):
    """
    Responde a qualquer mensagem que não seja um comando conhecido.
    """
    texto = "Não compreendi sua mensagem. Por favor, utilize o comando /iniciar para ver as opções."
    bot.reply_to(mensagem, texto)


print("Bot em execução...")
bot.polling()
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

sites_por_tipo = {
    "estagio": {
        "Eureca": "https://eureca.me/",
        "Cia de Talentos": "https://www.ciadetalentos.com.br/pt/",
        "Companhia de Estágios": "https://www.ciadeestagios.com.br/",
        "Acroos.Jobs": "https://login.across.jobs/?pUrlRedirecionadaPortal=/",
        "Machtbox": "https://matchboxbrasil.com/",
    },
    "remoto": {
        "wellfound.com": "https://wellfound.com/",
        "arc.dev": "https://arc.dev/",
        "https://www.trampardecasa.com.br/": "https://www.trampardecasa.com.br/",
        "remotar.com.br": "https://remotar.com.br/",
        "remote.io": "https://www.remote.io/",
        "workingnomads.com": "https://www.workingnomads.com/jobs",
        "pangian.com": "https://pangian.com/remote/",
        "simplyhired.com.br": "https://www.simplyhired.com.br/",
    },
    "geral": {
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
}

def enviar_menu_tipo_site(chat_id, message_id=None):
    texto = "Qual tipo de site você deseja acessar?\nEscolha uma opção:"
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_estagio = types.InlineKeyboardButton("Estágio", callback_data="tipo_estagio")
    btn_remoto = types.InlineKeyboardButton("Remoto", callback_data="tipo_remoto")
    btn_geral = types.InlineKeyboardButton("Geral", callback_data="tipo_geral")
    markup.add(btn_estagio, btn_remoto, btn_geral)
    if message_id:
        bot.edit_message_text(texto, chat_id, message_id, reply_markup=markup)
    else:
        bot.send_message(chat_id, texto, reply_markup=markup)

def enviar_menu_sites(chat_id, tipo, message_id=None):
    texto = f"Selecione um site de {tipo.capitalize()}:"
    markup = types.InlineKeyboardMarkup(row_width=2)
    for nome, url in sites_por_tipo[tipo].items():
        markup.add(types.InlineKeyboardButton(nome, callback_data=f"site_{tipo}_{nome}"))
    btn_voltar = types.InlineKeyboardButton("« Voltar", callback_data="voltar_tipo")
    markup.add(btn_voltar)
    if message_id:
        bot.edit_message_text(texto, chat_id, message_id, reply_markup=markup)
    else:
        bot.send_message(chat_id, texto, reply_markup=markup)

@bot.message_handler(commands=["start", "iniciar"])
def iniciar(mensagem):
    enviar_menu_tipo_site(mensagem.chat.id)

@bot.callback_query_handler(func=lambda call: True)
def responder_callback(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    if call.data == "voltar_menu" or call.data == "voltar_tipo":
        enviar_menu_tipo_site(chat_id, message_id)
        bot.answer_callback_query(call.id)
        return

    if call.data.startswith("tipo_"):
        tipo = call.data.replace("tipo_", "")
        enviar_menu_sites(chat_id, tipo, message_id)
        bot.answer_callback_query(call.id)
        return

    if call.data.startswith("site_"):
        _, tipo, nome = call.data.split("_", 2)
        url = sites_por_tipo[tipo][nome]
        markup_voltar = types.InlineKeyboardMarkup()
        btn_voltar = types.InlineKeyboardButton("« Voltar", callback_data=f"tipo_{tipo}")
        markup_voltar.add(btn_voltar)
        texto = f"Acesse o site: {url}"
        bot.edit_message_text(texto, chat_id, message_id, reply_markup=markup_voltar)
        bot.answer_callback_query(call.id)
        return

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
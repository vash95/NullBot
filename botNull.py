import telegram
import re
import pickle
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from datetime import datetime, timedelta
from configparser import ConfigParser
from collections import OrderedDict
import json
import os
import sys
from threading import Thread
import logging
from random import randint
import postgre 

timeTexto = 0
canTalk = True
muchoTexto = 0
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

logger = logging.getLogger(__name__)

dataPath = os.getcwd() + '/data'



def ini_to_dict(path):
    config = ConfigParser()
    config.read(path)
    return_value = OrderedDict()
    for section in reversed(config.sections()):
        return_value[section] = OrderedDict()
        section_tuples = config.items(section)
        for itemTurple in reversed(section_tuples):
            return_value[section][itemTurple[0]] = itemTurple[1]
    return return_value

settings = ini_to_dict(os.path.join(os.path.dirname(__file__), "config.ini"))



updater = Updater(settings["main"]["token"])


def start(bot, update):
    update.message.reply_text('¿Ya ha acabado One Piece?', reply_to_message_id=update.message.message_id)


def help(bot, update):
    update.message.reply_text('pregunta a tu madre')




def echo(bot, update):

    global canTalk
    global muchoTexto 
    global timeTexto 

    mensaje = update.message
    mensajeLower = update.message.text.lower()

    #if (datetime.now() - timeTexto).total_seconds() < 60 and muchoTexto > 20:
    #   bot.sendDocument(chat_id=update.message.chat_id, document=open(dataPath + '/photo/texto.webp', 'rb'))

    #pajero
    if datetime.now().hour == 22 and datetime.now().minute == 35  and searchString(mensajeLower, 'hora patito')):
        update.message.reply_text('Felicidades')

    #basicos
    if update.message.text != None and "null stop" == update.message.text.lower():
        stop(bot, update)
    elif update.message.text != None and "null go" == update.message.text.lower():
        restart(bot, update)

    #null
    if searchString(mensajeLower, 'paja'):
        now = datetime.now()
        if now.hour < 18 and now.hour > 8  and datetime.today().weekday() <= 4  :
            update.message.reply_text('Deja de hacerte pajas ' + update.message.from_user.name + ' en el trabajo')
        else:
            update.message.reply_text('Deja de hacerte pajas ' + update.message.from_user.name)

    elif re.search(r'\bbuenos d[ií]as\b', update.message.text.lower()):
        bot.sendDocument(chat_id=update.message.chat_id, document=open(dataPath + '/photo/buenos.webp', 'rb'))

    elif searchString(update, 'top comentarios'):
        update.message.reply_text('''- Joe, no hay gow?
- Me siento engañado, pense k Joseph era el de la gorra 
- Donde Eren mate a Levi 
- LO HIZE! 
- ¿Para qué voy a chuparlo? si es para jugar
- Akainu se parece a Luis Augusto
         ''')   

    elif update.message.text.lower()[-3:] == 'ps5':
        update.message.reply_text('POR EL CULO TE LA HINCO')

    elif searchString(mensajeLower, xd') and randint(0,10) == 1 :
        bot.sendDocument(chat_id=update.message.chat_id, document=open(dataPath + '/gifs/salvame.mp4', 'rb'))

    elif re.search(r'\bnuevos cap[ií]tulos\b',update.message.text.lower()):
        rows = postgre.select("select * from new_cap order by id limit 5")
        for row in rows:
            bot.send_message(chat_id=update.message.chat_id, text='Titulo: '+row[0]+ ' Cap: '+ str(row[1])+' Url: '+row[2])

    elif searchString(mensajeLower, 'busca anime'):
        anime = update.message.text.lower().replace("busca anime", "").strip()
        rows = postgre.select("select * from anime where lower(titulo) like '"+anime+"%' limit 10")
        for row in rows:
            bot.send_message(chat_id=update.message.chat_id, text='Resultados: '+ row[0])

    elif searchString(mensajeLower, 'busca cap'):
        cap = update.message.text.lower().replace("busca cap", "").strip().split(" ", 1)
        rows = postgre.select("select * from capitulos where lower(anime) = '"+cap[1]+"' and episodio ="+cap[0])
        for row in rows:
            bot.send_message(chat_id=update.message.chat_id, text='Titulo: '+row[0]+ ' Cap: '+ str(row[1])+' Url: '+row[2])

# Devuelve true si msg contiene str
def searchString(msg, str):
    return re.search(r'\b{re.escape(str)}\b', msg)

# Imprime capis de anime nuevos
def animeCaps(bot, update, cantidad):
    capis = postgre.select("select * from new_cap order by id limit " + cantidad)
    for capi in capis:
        printAnime(bot, update, row[0], str(row[1]), row[2])

# Imprime un mensaje de un capi formateado
def printAnime(bot, update, titulo, capi, url):
    bot.send_message(chat_id=update.message.chat_id, parse_mode='HTML', text="""<b>titulo</b><br>capi<br>url""")

def isAdmin(bot, update):
    if str(update.message.from_user.id) == str(settings["main"]["admin"]) :
        return True
    else:
        return None

# COMANDO: imprime 5 capis nuevos
def cmd_capis(bot, update):
    animeCaps(bot, update, 5)
      
def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def stop(bot, update):
    if isAdmin(bot, update):
        global canTalk
        canTalk = None
    else:
        bot.send_photo(chat_id=update.message.chat_id, photo=open(dataPath + '/photo/skinner.jpg', 'rb'))
    #    bot.send_message(chat_id=update.message.chat_id, text="PATHETIC")")

def restart(bot, update):
    if isAdmin(bot, update):
        global canTalk
        canTalk = True
    else:
        bot.send_photo(chat_id=update.message.chat_id, photo=open(dataPath + '/photo/skinner.jpg', 'rb'))


def main():
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler('seguir', restart))
    dp.add_handler(CommandHandler('parar', stop))
    dp.add_handler(CommandHandler("Capis", cmd_capis))

    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()

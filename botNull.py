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

botGlobal = 0 
timeTexto = 0
canTalk = True
muchoTexto = 0
# holi desde develop
# holi
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
    global botGlobal

    botGlobal = bot

    mensajeLower = update.message.text.lower()
    now = datetime.now()

    #if (datetime.now() - timeTexto).total_seconds() < 60 and muchoTexto > 20:
    #   bot.sendDocument(chat_id=update.message.chat_id, document=open(dataPath + '/photo/texto.webp', 'rb'))

    
    #basicos
    if update.message.text != None and "null stop" == mensajeLower:
        stop(bot, update)
    elif update.message.text != None and "null go" == mensajeLower:
        restart(bot, update)

    #null
    if re.search(r'\bpaja\b', mensajeLower):
        if now.hour < 18 and now.hour > 8  and datetime.today().weekday() <= 4  :
            update.message.reply_text('Deja de hacerte pajas ' + update.message.from_user.name + ' en el trabajo')
        else:
            update.message.reply_text('Deja de hacerte pajas ' + update.message.from_user.name)

    elif re.search(r'\bbuenos d[ií]as\b', mensajeLower):
        bot.sendDocument(chat_id=update.message.chat_id, document=open(dataPath + '/photo/buenos.webp', 'rb'))

    elif re.search(r'\btop comentarios\b', mensajeLower):
        update.message.reply_text('''- Joe, no hay gow?
- Me siento engañado, pense k Joseph era el de la gorra 
- Donde Eren mate a Levi 
- LO HIZE! 
- ¿Para qué voy a chuparlo? si es para jugar
- Akainu se parece a Luis Augusto
         ''')   

    elif mensajeLower[-3:] == 'ps5':
        update.message.reply_text('POR EL CULO TE LA HINCO')

    elif re.search(r'\bxd\b', mensajeLower) and randint(0,10) == 1:
        bot.sendDocument(chat_id=update.message.chat_id, document=open(dataPath + '/gifs/salvame.mp4', 'rb'))

    elif re.search(r'\bnuevos cap[ií]tulos\b',mensajeLower):
        rows = postgre.select("select * from new_cap order by id limit 5")
        for row in rows:
            bot.send_message(chat_id=update.message.chat_id, text='Titulo: '+row[0]+ ' Cap: '+ str(row[1])+' Url: '+row[2])

    elif re.search(r'\bbusca anime\b', mensajeLower):
        anime = mensajeLower.replace("busca anime", "").strip()
        rows = postgre.select("select * from anime where lower(titulo) like '"+anime+"%' limit 10")
        for row in rows:
            bot.send_message(chat_id=update.message.chat_id, text='Resultados: '+ row[0])

    elif re.search(r'\bbusca cap\b', mensajeLower):
        cap = mensajeLower.replace("busca cap", "").strip().split(" ", 1)
        rows = postgre.select("select * from capitulos where lower(anime) = '"+cap[1]+"' and episodio ="+cap[0])
        for row in rows:
            bot.send_message(chat_id=update.message.chat_id, text='Titulo: '+row[0]+ ' Cap: '+ str(row[1])+' Url: '+row[2])
    elif re.search(r'\binformativo matinal\b', mensajeLower):
        rows = postgre.select("select * from informativo where fecha = '"+ str(datetime.today())+"'")
        if len(rows) == 0:
             bot.send_photo(chat_id=update.message.chat_id, photo=open(dataPath + '/photo/informativo.jpg', 'rb'))
        for row in rows:
            bot.send_message(chat_id=update.message.chat_id, text=row[1])
    
    #patito
    elif re.search(r'\bhora patito\b', mensajeLower):
        horaPatito(update,now)
    #palito
    elif re.search(r'\bhora palito\b', mensajeLower):
        horaPalito(update,now)
    #pi
    elif re.search(r'\bhora pi\b', mensajeLower):
        horaPi(update,now)
        
        



# Imprime capis de anime nuevos
def animeCaps(bot, update, cantidad):
    capis = postgre.select("select * from new_cap order by id limit " + str(cantidad))
    for capi in capis:
        printAnime(bot, update, capi[0], str(capi[1]), capi[2])

# Imprime un mensaje de un capi formateado
def printAnime(bot, update, titulo, capi, url):
    #bot.send_message(chat_id=update.message.chat_id, parse_mode='HTML', text="""<b>titulo</b><p>capi<p>url""")
    bot.send_message(chat_id=update.message.chat_id, text='Titulo: '+titulo+ ' Cap: '+ capi+' Url: '+ url)

def isAdmin(bot, update):
    if str(update.message.from_user.id) == str(settings["main"]["admin"]) :
        return True
    else:
        return None

# COMANDO: imprime 5 capis nuevos
def cmd_capis(bot, update):
    animeCaps(bot, update, 5)
 
def horaPatito(update, now):
    if now.hour == 22 and now.minute == 22:
        #TODO: ver si el usuario esta en la base de datos
        
        # si esta, sumar 1 al contador, actualizar dia de ultimo patito igual a hoy

        # else, crear registro en base de datos con su id, contador a 1, ultimo dia de patito igual a hoy

        # enviar imagen sticker
        botGlobal.sendDocument(chat_id=update.message.chat_id, document=open(dataPath + '/photo/paptito.webp', 'rb'))

        #contestar a mensaje
        update.message.reply_text('Enhorabuena ' + update.message.from_user.name + ' por la hora patito')


def horaPalitoHandler(update, now):

    if (now.hour == 23 or now.hour == 11) and now.minute == 11:
        horaPalito4(update)
    elif now.hour == 1 and now.minute == 11:
        horaPalito3(update)

def horaPalito4(update, now):
    #TODO: ver si el usuario esta en la base de datos

    # enviar imagen sticker
    botGlobal.sendDocument(chat_id=update.message.chat_id, document=open(dataPath + '/photo/horapalito4.webp', 'rb'))

    #contestar a mensaje
    update.message.reply_text('Hora palito!!!')

def horaPalito3(update, now):
    #TODO: ver si el usuario esta en la base de datos

    # enviar imagen sticker
    botGlobal.sendDocument(chat_id=update.message.chat_id, document=open(dataPath + '/photo/horapalito3.webp', 'rb'))

    #contestar a mensaje
    update.message.reply_text('Hora palito pero les falta uno :(')

def horaPi(update, now):
    if now.hour == 3 and now.minute == 14:
        #TODO: ver si el usuario esta en la base de datos

        # enviar imagen sticker
        botGlobal.sendDocument(chat_id=update.message.chat_id, document=open(dataPath + '/photo/horapi.webp', 'rb'))

        #contestar a mensaje
        update.message.reply_text('Muy bien ' + update.message.from_user.name + ' máquina ahora a dormir que es tarde')

def horaPorrito(update, now):
    if (now.hour == 4 or now.hour == 16) and now.minute == 20:
        #TODO: ver si el usuario esta en la base de datos

        # enviar imagen sticker
        botGlobal.sendDocument(chat_id=update.message.chat_id, document=open(dataPath + '/photo/horaporrito.webp', 'rb'))

        #contestar a mensaje
        update.message.reply_text(update.message.from_user.name + ' fúmatelo a mi salud crack')
        
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
    dp.add_handler(CommandHandler("capis", cmd_capis))

    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
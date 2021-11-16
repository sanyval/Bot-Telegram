import os
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
import Bot as bot

#Imporamos las Variables de entorno. En esta caso el TOKEN
load_dotenv()
TOKEN=os.environ.get("TOKEN")


def main():
    # Establecemos conexiòn entre el programa y el bot
    updater=Updater(TOKEN,use_context=True)
    dp=updater.dispatcher

    # Establecer comandos que escucha el bot
    dp.add_handler(CommandHandler("start",bot.start))
    dp.add_handler(CommandHandler("ayuda",bot.ayuda))
    dp.add_handler(CommandHandler("secuencia",bot.secuencia))
    dp.add_handler(CommandHandler("grafo", bot.grafo))

    # Establecer los callbacks de cada boton
    dp.add_handler(CallbackQueryHandler(bot.menu_ayuda,pattern="m1"))
    dp.add_handler(CallbackQueryHandler(bot.menu_ayuda, pattern="m2"))
    dp.add_handler(CallbackQueryHandler(bot.menu_ayuda, pattern="m3"))
    dp.add_handler(CallbackQueryHandler(bot.menu_ayuda, pattern="m4"))
    dp.add_handler(CallbackQueryHandler(bot.menu_ayuda, pattern="m5"))

    #Iniciar el bot
    updater.start_polling()

    #Mantener el bot
    updater.idle()


if __name__=='__main__':
    main()
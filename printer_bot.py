import os
import logging
from time import sleep
from tkinter import image_types
from urllib import response
from telegram import Update
from telegram.ext import Updater, CallbackContext, CommandHandler, MessageHandler, Filters
import win32api
import win32print
from im2pdf import convert


token = ""


updater = Updater(token=token, use_context=True)

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


def start(update: Update, context: CallbackContext):
    first_name = update.message.chat.first_name
    context.bot.send_message(chat_id=update.effective_chat.id, text="Selam {}, ben Yazdırgaç, dosyalarınızı yazdırıyorum \U0001F47E".format(first_name))

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def start(update: Update, context: CallbackContext):
    with open(__file__) as f:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f.read().replace(token, ''))

start_handler = CommandHandler('code', start)
dispatcher.add_handler(start_handler)


def echo(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)


def respond(response_text, update):
    updater.dispatcher.bot.sendMessage(chat_id=update.effective_chat.id, text=response_text)

def print_pdf(fp):
        GHOSTSCRIPT_PATH = "C:\\Program Files\\gs\\gs9.56.0\\bin\\gswin64.exe"
        GSPRINT_PATH = "C:\\Program Files\\Ghostgum\\gsview\\gsprint.exe"
        currentprinter = win32print.GetDefaultPrinter()
        win32api.ShellExecute(0, 'open', GSPRINT_PATH, '-ghostscript "'+GHOSTSCRIPT_PATH+'" -printer "'+currentprinter+'" "{}"'.format(fp), '.', 0)

def file_recieved(update, context):
    fp = context.bot.get_file(update.message.document).download()
    print("Download succesfull.")

    image_extensions = ['.pbm','.pgm','.ppm','.tiff','.rast','.xbm','.jpg','.jpeg','.bmp','.png','.webp','.exr']
    
    extension = os.path.splitext(fp)[1].lower()
    print('Extension: ', extension)
    
    if extension == '.pdf':
        print_pdf(fp)
    
    if extension in image_extensions:
        convert(fp, "out.pdf")
        print_pdf("out.pdf")
        fp = "out.pdf"

    else:
        os.startfile(fp, "print")
    

    sleep(3)
    os.remove(fp)
    
    respond("Dosya yazdırıldı \U00002705", update = update)


def photo_recieved(update, context):
    fp = context.bot.get_photo(update.message.photo).download()
    print("Photo download succesfull.")

    convert(fp, "out.pdf")
    print_pdf("out.pdf")
    fp = "out.pdf"

    sleep(3)
    os.remove(fp)
    
    respond("Resim yazdırıldı \U00002705", update = update)



photo_print_handler = MessageHandler(Filters.photo, photo_recieved)
dispatcher.add_handler(photo_print_handler)



updater.start_polling()
updater.idle()

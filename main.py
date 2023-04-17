import logging
import os
import requests
import traceback
import json
import urllib.request
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, ContextTypes, MessageHandler, filters

load_dotenv()

URL = os.environ.get('URL')
BOT_TOKEN = os.environ.get('BOT_TOKEN')


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def post_request(photo):
    try:
        urllib.request.urlretrieve(photo, 'temp.jpg')
        with open('temp.jpg', 'rb') as f:
            files = {'file': ('temp.jpg', f, 'image/jpeg')}
            response = requests.post(url = URL, files=files)
            response_json = json.loads(response.text)
            value = response_json['result']
        
        if os.path.exists("temp.jpg"):
            os.remove("temp.jpg")
        else:
            print("The file does not exist")
        return value
    except:
        traceback.print_exc()
        print(Exception)
    finally:
        print(response.json())

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Please upload a photo for ID here!")

async def uploadPhoto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = await context.bot.get_file(update.message.photo[-1].file_id)
    file_path = file.file_path
    print(file_path)
    try:
        await context.bot.send_message(chat_id=update.effective_chat.id, text= post_request(file_path))
    except Exception as e:
        print(e)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Try Again")


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def main() -> None:
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    upload_handler = MessageHandler(filters.PHOTO, uploadPhoto)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(start_handler)
    application.add_handler(upload_handler)
    application.add_handler(unknown_handler)

    # application.run_webhook(
    #     listen='0.0.0.0',
    #     port=8443,
    #     secret_token='awserdtfyuioxcfvgbhnjkmlrxdcfvgbhkjn',  #change this
    #     key='private.key',      #generate SSL cert using openssl
    #     cert='cert.pem',        #
    #     webhook_url='https://mltelebot.com:8443'      #enable domains in GCP
    #)
    application.run_polling()

if __name__ == '__main__':
    main()
import telebot
from config import *
from logicai import *
import base64
import os

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я искусственный интелект который преобразует твой текст в изображение напиши /generate, чтобы создать картинку.")

@bot.message_handler(commands=['generate'])
def addtask_command(message):
    bot.send_message(message.chat.id, "Введите описание картинки:")
    bot.register_next_step_handler(message, promt)
    
def promt(message):
    promt1 = message.text
    bot.send_message(message.chat.id, "Выберите стиль картинки, написав цифру выбранного стиля:\n1.KANDINSKY - стандартная генерация\n2.UHD- Детальное фото\n3.ANIME - аниме стиль")
    bot.register_next_step_handler(message, promt2,promt1=promt1)

def promt2(message,promt1):
    promt2 = message.text
    style = 'KANDINSKY'
    if str(promt2) == '2':
        style = 'UHD'
    elif str(promt2) == '3':
        style = 'ANIME'
    msg = bot.reply_to(message, "Ожидайте")
    bot.send_chat_action(message.chat.id, 'typing')
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', api_token, secret_key)
    model_id = api.get_model()
    uuid = api.generate(promt1, model_id,style)
    images = api.check_generation(uuid)
    image_base64 = images[0]
    image_data = base64.b64decode(image_base64)
    with open("image.jpg", "wb") as file:
        file.write(image_data)
    bot.delete_message(message.chat.id, msg.message_id)
    with open("image.jpg", "rb") as file:
        bot.send_photo(message.chat.id, file)
    os.remove('image.jpg')



if __name__=="__main__":
    bot.polling()
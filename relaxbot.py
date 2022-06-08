import os
import sys
import logging
import requests

from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler

from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)
formatter = logging.Formatter(
    '%(asctime)s [%(levelname)s] %(message)s'
)
handler.setFormatter(formatter)

URL_CATS = 'https://api.thecatapi.com/v1/images/search'
URL_DOGS = 'https://api.thedogapi.com/v1/images/search'


def get_new_image(url):
    """Получение ссылку на картинку."""
    try:
        response = requests.get(url)
        response = response.json()
        random_image = response[0].get('url')
        return random_image
    except Exception as error:
        logger.error(f'Ошибка при запросе к основному API: {error}')


def send_new_cat(update, context):
    """"Отправка картинки с котиком."""
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image(URL_CATS))


def send_new_dog(update, context):
    """"Отправка картинки с собачкой."""
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image(URL_DOGS))


def wake_up_bot(update, context):
    chat = update.effective_chat
    name = chat.first_name
    button = ReplyKeyboardMarkup([['/cat', '/dog']], resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text=f'Привет, {name}. Я релакс-бот. Помогу справится с плохим '
             f'настроением. Нажимай на кнопки Котик или Собачка и я '
             f'пришлю тебе картинку.',
        reply_markup=button
    )


def main():
    updater = Updater(token=token)

    updater.dispatcher.add_handler(CommandHandler('start', wake_up_bot))
    updater.dispatcher.add_handler(CommandHandler('cat', send_new_cat))
    updater.dispatcher.add_handler(CommandHandler('dog', send_new_dog))

    updater.start_polling(poll_interval=3.0)
    updater.idle()


if __name__ == '__main__':
    main()

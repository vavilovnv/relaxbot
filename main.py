import os
import sys
import logging
import requests

from random import randint
from dotenv import load_dotenv
from telegram.update import Update
from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          Filters, CallbackContext)

load_dotenv()

RETRY_TIME = 2.0

TOKEN = os.getenv('TOKEN')

URL_CATS = 'https://api.thecatapi.com/v1/images/search'
URL_DOGS = 'https://api.thedogapi.com/v1/images/search'
URL_FOXES = 'https://randomfox.ca/images/'

logger = logging.getLogger(__name__)


def get_new_image(url: str, url_type: int) -> str:
    """Getting a link to an image depending on the type of API."""
    if url_type == 1:
        try:
            response = requests.get(url)
            response = response.json()
            random_image = response[0].get('url')
            return random_image
        except Exception as error:
            logger.error(f'Ошибка при запросе {url} к основному API: {error}')
    elif url_type == 2:
        try:
            response = requests.get(url)
            return response.url
        except Exception as error:
            logger.error(f'Ошибка при запросе {url}: {error}')


def send_new_cat(update: Update, context: CallbackContext) -> None:
    """Sending a picture of a cat"""
    logger.info('Sending a picture with a cat')
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image(URL_CATS, 1))


def send_new_dog(update: Update, context: CallbackContext) -> None:
    """Sending a picture of a dog."""
    logger.info('Sending a picture with a dog')
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image(URL_DOGS, 1))


def send_new_fox(update: Update, context: CallbackContext) -> None:
    """Sending a picture of a fox."""
    logger.info('Sending a picture with a fox')
    chat = update.effective_chat
    url_foxes = f'{URL_FOXES}{randint(1, 121)}.jpg'
    context.bot.send_photo(chat.id, get_new_image(url_foxes, 2))


def send_text_message(update: Update, context: CallbackContext) -> None:
    """Sending basic instruction."""
    logger.info('Sending an instruction')
    chat = update.effective_chat
    text_message = (f'Нажимай скорее на кнопку c котиком, собачкой '
                    f'или лисичкой и я пришлю тебе картинку!')
    context.bot.send_message(chat_id=chat.id, text=text_message)


def change_content_to_send(update: Update, context: CallbackContext) -> None:
    """Select a picture to send."""
    message_text = update.message.text.strip()
    if message_text == 'Котик 🐱':
        send_new_cat(update, context)
    elif message_text == 'Собачка 🐶':
        send_new_dog(update, context)
    elif message_text == 'Лисичка 🦊':
        send_new_fox(update, context)
    else:
        send_text_message(update, context)


def wake_up_bot(update: Update, context: CallbackContext) -> None:
    """Bot initialization."""
    chat = update.effective_chat
    name = chat.first_name
    keyboard = [
        ['Котик 🐱', 'Собачка 🐶'],
        ['Лисичка 🦊', 'Инфо ℹ️'],
    ]
    hello_message = (f'Привет, {name}. Я релакс-бот. Помогу справится с '
                     f'плохим настроением. Нажимай на кнопку c котиком, '
                     f'собачкой или лисичкой и я пришлю тебе картинку.')
    logger.info('Bot initialization')
    context.bot.send_message(
        chat_id=chat.id,
        text=hello_message,
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )


def main():
    """The basis of the bot."""
    updater = Updater(token=TOKEN)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', wake_up_bot))
    dp.add_handler(MessageHandler(Filters.text, change_content_to_send))

    logger.info('Starting service...')
    updater.start_polling(poll_interval=RETRY_TIME)
    updater.idle()


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(stream=sys.stdout)
    logger.addHandler(handler)
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(message)s'
    )
    handler.setFormatter(formatter)

    main()

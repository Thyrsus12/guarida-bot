import json
import os
import re
from datetime import datetime, timedelta
import pytz

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from dotenv import load_dotenv

load_dotenv()
user_name = 'la_guarida_juegos_bot'
timetable = '*Martes a Sábado* \n 10:30\-14:00 \n 17:00\-20:30 \n *Domingo* \n 10:30\-14:00 \n 17:00\-20:30 \n *Lunes CERRADO*'
contact = '*Teléfono* 911825459 \n *Web* https://www\.laguaridajuegos\.com/'
token = os.getenv('BOT_TOKEN')

async def start(update: Update, context: ContextTypes):
    start_text = "Hola! Soy el bot de La Guarida. Escribe el comando /info para ver todo lo que puedo hacer 😁"
    await update.message.reply_text(f"{start_text}")


async def info(update: Update, context: ContextTypes):
    keyboard = [
        [
            InlineKeyboardButton("📋 Reservar mesa", callback_data=json.dumps({"name": "booking"}))
        ],
        [
            InlineKeyboardButton("🕘 Horario", callback_data=json.dumps({"name": "timetable"})),
            InlineKeyboardButton("📍 Ubicación", url="https://maps.app.goo.gl/qtjcJr9z6KRpGmgf9"),
            InlineKeyboardButton("📞 Contacto", callback_data=json.dumps({"name": "contact"}))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text('¿En que puedo ayudarte?', reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes):
    query = update.callback_query

    await query.answer()
    if json.loads(query.data)['name'] == 'timetable':
        await query.edit_message_text(text=f"{timetable}", parse_mode=ParseMode.MARKDOWN_V2)
    elif json.loads(query.data)['name'] == 'contact':
        await query.edit_message_text(text=f"{contact}", parse_mode=ParseMode.MARKDOWN_V2)
    elif json.loads(query.data)['name'] == 'booking':
        await query.edit_message_text(text='reserva')


def handle_response(text: str, context: ContextTypes, update: Update):
        return 'No te he entendido'


async def handle_message(update: Update, context: ContextTypes):
    message_type = update.message.chat.type
    text = update.message.text

    if message_type == 'group':
        if text.startswith(user_name):
            new_text = text.replace(user_name, '')
            response = handle_response(new_text, context, update)
        else:
            return
    else:
        response = handle_response(text, context, update)

    await update.message.reply_text(response)


async def error(update: Update, context: ContextTypes):
    print(context.error)
    await update.message.reply_text('Ha ocurrido un error')


if __name__ == '__main__':
    print('Iniciando...')
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('info', info))
    app.add_handler(CallbackQueryHandler(button))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_error_handler(error)

    print('Bot iniciado')
    app.run_polling(poll_interval=1, timeout=10)

import logging

from datetime import date, time, datetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler
from api import Api

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

country = 'IRN'
api_handler = Api()
keyboard = [
    [
        InlineKeyboardButton("تعداد فوتی ها", callback_data='1'),
        InlineKeyboardButton("تعداد مبتلایان", callback_data='2'),
    ],
    [
        InlineKeyboardButton(
            "تعداد واکسینه شده ها", callback_data='3'),
        InlineKeyboardButton(
            "تعداد بهبود یافته ها", callback_data='4'),
    ],
    [
        InlineKeyboardButton("درصد جمعیت فوت شده", callback_data='5'),
        InlineKeyboardButton(
            "درصد جمعیت واکسینه شده", callback_data='6'),
    ],
]


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                            text="Welcome to the covid-19 bot.\nEnter the name of the country you want to see the stats :")


def help(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="به ربات خوش آمدید ابتدا با دستور /start لیست کشور ها را مشاهده کنید و بعد از وارد کردن نام کشور های درون لیست یکی از دکمه ها را انتخاب کنید.")


def menu(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, 
                            text="Welcome to the covid-19 bot.\nEnter the name of the country you want to see the stats :")


def stop(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Subscription suspended thanks for using our bot!")

# main menu
def show_stats(update: Update, context: CallbackContext):
    global country
    country = update.message.text
    print(f"selected country : {country}")
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "Please Choose : ", reply_markup=reply_markup)

# handling inline keyboard callbacks
def button(update: Update, context: CallbackContext):
    now = datetime.now()
    now_str = now.strftime("%d/%m/%Y %H:%M:%S")
    query = update.callback_query
    data = int(query.data)
    result = ""
    if data == 1:
        result = f"{country} until {now_str} has {api_handler.get_data(name=country,record='deaths')} deaths"
    elif data == 2:
        result = f"{country} until {now_str} has {api_handler.get_data(name=country,record='confirmed')} cases with covid-19"
    elif data == 3:
        result = f"{country} until {now_str} has {api_handler.get_data(name=country,record='stringency')} vaccinated cases"
    elif data == 4:
        result = f"{country} until {now_str} has {api_handler.get_data(name=country,record='stringency_legacy')} cases cured from covid-19"
    elif data == 5:
        result = f"{country} until {now_str} has {api_handler.get_data(name=country,record='stringency_legacy_disp')} death percentage"
    elif data == 6:
        result = f"{country} until {now_str} has {api_handler.get_data(name=country,record='stringency')} vaccinated percentage"
    rep_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=result, reply_markup=rep_markup)
    print(f"query data : {data}")
    query.answer()


def main() -> None:
    
    # Create the Updater and pass it your bot's token.
    updater = Updater("YOUR BOT TOKEN")

    # handling handlers
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('menu', menu))
    updater.dispatcher.add_handler(CommandHandler('stop', stop))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(
        MessageHandler(filters=None, callback=show_stats))

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()

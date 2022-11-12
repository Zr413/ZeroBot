import telebot
from config import keys, TOKEN
from untils import ConvetrionExeption, CryptoConverter

bot = telebot.TeleBot(TOKEN)

# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате:\n <имя валюты> \
           <в какую валюту перевести> \
            <количество переведенной валюты>\nДля просмотра доступных валют команда: /values'
    bot.reply_to(message, text)


# Обрабатывается валюты
@bot.message_handler(commands=['values'])
def value(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvetrionExeption('Слишком много параметров')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvetrionExeption as e:
        bot.reply_to(message, f'Ошибка пользователя, \n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду, \n {e}')

    else:
        text = f'Курс {amount} {quote} -> {base} - {total_base}'
        bot.send_message(message.chat.id, text)



bot.polling(none_stop=True)
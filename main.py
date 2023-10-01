import telebot
import config
from extensions import CurrencyConverter, APIException

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Чтобы узнать цену валюты, отправьте сообщение в формате: \n"
                                      "<имя валюты, цену которой хотите узнать> <имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>\n"
                                      "Например: USD EUR 100\n"
                                      "Для получения списка доступных валют введите /values")


@bot.message_handler(commands=['values'])
def send_values(message):
    # Ваш код для отправки информации о доступных валютах
    available_currencies = "Доступные валюты:\n"
    # Ваш код для получения списка доступных валют и их описаний
    # Пример: available_currencies += "USD - Доллар США\n"
    bot.send_message(message.chat.id, available_currencies)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    try:
        text = message.text.split()
        if len(text) != 3:
            raise APIException(
                "Неверный формат запроса. Введите запрос в формате: <имя валюты> <имя валюты> <количество>")

        base_currency, quote_currency, amount = text[0], text[1], float(text[2])
        result = CurrencyConverter.get_price(base_currency, quote_currency, amount)
        bot.send_message(message.chat.id, f"{amount} {base_currency} = {result} {quote_currency}")
    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка: {e}')


if __name__ == '__main__':
    bot.polling(none_stop=True)
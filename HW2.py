import telebot
import conf
import flask
import re

WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)

bot = telebot.TeleBot(conf.TOKEN, threaded=False)
bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL_BASE+WEBHOOK_URL_PATH)

app = flask.Flask(__name__)

@bot.message_handler(commands=['start'])
def send_welcome(message): bot.send_message(message.chat.id, "А-йоу-йоу, супер-бот на связи. Я могу считать слова в сообениях. Какой я молодец. как я важен. Если тебе что-то непонятно, вызывай help.")

@bot.message_handler(commands=['help'])
def send_help(message): bot.send_message(message.chat.id, "Протягиваю тебе руку помощи, страдалец. Не нужно думать. Просто отправь мне сообщение, а я посчитаю, сколько в нём слов.")

@bot.message_handler(func=lambda m: True)
def send_len(message):
    count=message.text
    count=re.sub('[.,:;/\|{}@^!?<>-_*]+', '', count)
    count=re.findall(r'\w+', count)
    n=len(count)
    reply = str(n) + '. Именно столько слов я насчитал в вашем сообщении.'
    bot.send_message(message.chat.id, reply)

@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

if __name__ == '__main__':
    bot.polling(none_stop=True)

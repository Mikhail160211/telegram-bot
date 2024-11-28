import telebot 
from bot_logic import gen_pass, gen_emodji, flip_coin  # Импортируем функции из bot_logic
from model import  get_class

bot = telebot.TeleBot("")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Я твой Telegram бот. Напиши команду /hello, /bye, /pass, /emodji или /coin  ")

@bot.message_handler(commands=['hello'])
def send_hello(message):
    bot.send_message(message.chat.id, "Привет! Как дела?")

@bot.message_handler(commands=['bye'])
def send_bye(message):
    bot.send_message(message.chat.id, "Пока! Удачи!")

@bot.message_handler(commands=['pass'])
def send_password(message):
    password = gen_pass(10)  # Устанавливаем длину пароля, например, 10 символов
    bot.send_message(message.chat.id, f"Вот твой сгенерированный пароль: {password}")

@bot.message_handler(commands=['emodji'])
def send_emodji(message):
    emodji = gen_emodji()
    bot.send_message(message.chat.id, f"Вот эмоджи': {emodji}")

@bot.message_handler(commands=['coin'])
def send_coin(message):
    coin = flip_coin()
    bot.send_message(message.chat.id, f"Монетка выпала так: {coin}")

@bot.message_handler(content_types=['photo'])
def send_photo(message):
    if not message.photo:
        return bot.send_message(message.chat.id, f"no photo finded")
    # Получаем файл и сохраняем его
    file_info = bot.get_file(message.photo[-1].file_id)
    file_name = file_info.file_path.split('/')[-1]

    # Загружаем файл и сохраняем
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)
    
    result = get_class(model_path="keras_model.h5",labels_path="labels.txt",image_path=file_name)

    bot.send_message(message.chat.id, result)

# Запускаем бота
print("bot start")
bot.polling()

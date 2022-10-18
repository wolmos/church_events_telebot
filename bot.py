import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove

import config
from keyboards import kb_menu

bot = telebot.TeleBot(config.bot_token)

def answer_message_text(message_text):
	if message_text == 'О нас':
		return 'Мы современная церковь с древним посланием. \nЦерковь «Слово жизни» — место раскрытия даров и способностей, а также молитвы, поклонения, глубокого изучения Библии и библейского взгляда на разные сферы жизни. \n\nМы рады каждому! ❤️Больше о нас на сайте https://wolrus.org'
	elif message_text == 'Социальные сети':
		return """Мы в соцсетях

Телеграм: https://t.me/wolrusyouth_msk
ВКонтакте: https://vk.com/wolrusyouth
YouTube: https://www.youtube.com/c/wolrustv/videos 
Яндекс.Дзен: https://clck.ru/dZS3L

Сайт церкви «Слово жизни» https://wolrus.org

Присоединяйся к нашим телеграм-чатам по кнопке ниже"""
	elif message_text == 'Чаты':
		return 'У нас есть разные чаты по интересам. Переходи по ссылке, вступай в понравившиеся чаты и находи компанию, с которой будет комфортно дружить: https://taplink.cc/chats'
	return 'Ошибка'

@bot.message_handler(commands=['start'])
def first_message(message):
	start_text = 'Привет, это церковынй бот!\nЗдесь ты найдешь основную информацию о церкви и предстоящих событиях. Выбери первый запрос:'
	bot.send_message(message.from_user.id, start_text, reply_markup=kb_menu.menu_kb)

@bot.message_handler(regexp='Назад')
def get_back_reply_markup(message):
	bot.send_message(message.from_user.id, 'Вернулись к началу', reply_markup=kb_menu.menu_kb)

@bot.message_handler()
def answer_message(message):
	text = answer_message_text(message.text)
	if text != 'Ошибка':
		bot.send_message(message.from_user.id, text, reply_markup=kb_menu.about_us_kb)

bot.polling()

import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, InputMediaPhoto

import config
from keyboards import kb_menu
from keyboards import inline_donate

bot = telebot.TeleBot(config.bot_token)

SCHEDULE_MESSAGE_ID = int()
CHANNEL_ID = int()

def check_group_is_wolrus(message):
	try:
		if(message.forward_from_chat.type == 'channel' and
			message.forward_from_chat.username == 'wolrusyouth_msk' and
			message.forward_from_chat.id == -1001337574730):
			return True
		return False
	except Exception as e:
		print(e)

def check_is_private_chat(message):
	try:
		if(message.chat.type == 'private'):
			return True
		return False
	except Exception as e:
		print(e)

def send_map(message):
	photo_big_hall = open(os.getcwd() + '/photo/church_map_big_hall.jpg', 'rb')
	photo_first_floor = open(os.getcwd() + '/photo/church_map_first_floor.jpg', 'rb')
	photo_second_floor = open(os.getcwd() + '/photo/church_map_second_floor.jpg', 'rb')

	bot.send_media_group(message.from_user.id, [InputMediaPhoto(photo_first_floor, caption='Карта церкви «Слово жизни»'), InputMediaPhoto(photo_second_floor), InputMediaPhoto(photo_big_hall)])

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

@bot.message_handler(commands=['start'], func=check_is_private_chat)
def first_message(message):
	try:
		start_text = 'Привет, это церковынй бот!\nЗдесь ты найдешь основную информацию о церкви и предстоящих событиях. Выбери первый запрос:'
		bot.send_message(message.from_user.id, start_text, reply_markup=kb_menu.menu_kb)
	except Exception as e:
		print(e)

@bot.message_handler(regexp='Назад', func=check_is_private_chat)
def get_back_reply_markup(message):
	try:
		bot.send_message(message.from_user.id, 'Вернулись к началу', reply_markup=kb_menu.menu_kb)
	except Exception as e:
		print(e)

@bot.message_handler(regexp='Пожертвование', func=check_is_private_chat)
def donate_message(message):
	try:
		donate_msg = '''Добровольное пожертвование – намного удобнее онлайн, а также ещё один способ вашего участия в жизни церкви.
Ниже вы видите кнопки с разными видами пожертвований:
• целевое – ваши десятины;
• молодежный центр (второе здание) – ваша помощь в ремонте и открытии;
• другое – помощь служениям церкви (смотрите по ссылке).

Спасибо за ваши пожертвования!'''
		bot.send_message(message.from_user.id, donate_msg, reply_markup=inline_donate.donate_kb)
	except Exception as e:
		print(e)

@bot.message_handler(regexp='Расписание на неделю', func=check_is_private_chat)
def resend_week_schedule_from_channel(message):
	try:
		bot.forward_message(message.from_user.id, CHANNEL_ID, SCHEDULE_MESSAGE_ID)
	except Exception as e:
		print(e)
		print('in resend_week_schedule_from_channel()')

@bot.message_handler(content_types=['photo'], func=check_group_is_wolrus)
def search_new_schedule(message):
	try:
		if(message.caption is not None and ('#расписание' in message.caption or '#Расписание' in message.caption)):
			global SCHEDULE_MESSAGE_ID
			global CHANNEL_ID
			CHANNEL_ID = message.chat.id
			SCHEDULE_MESSAGE_ID = message.message_id
		else:
			print('Error, have not #расписание')
	except Exception as e:
		print(e)
		print('in search_new_schedule()')

@bot.message_handler(func=check_is_private_chat)
def answer_message(message):
	try:
		text = answer_message_text(message.text)

		if message.text == 'Карта церкви':
			send_map(message)

		if text != 'Ошибка':
			bot.send_message(message.from_user.id, text, reply_markup=kb_menu.about_us_kb)
	except Exception as e:
		print(e)

bot.polling()

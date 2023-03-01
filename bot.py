import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, InputMediaPhoto

import config
from keyboards import kb_menu
from keyboards import inline_donate

bot = telebot.TeleBot(config.bot_token)
n = 1
ANNOUNCE_DICT = dict()

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
	photo_big_hall = open(os.getcwd() + '/photo/church_map_big_hall.png', 'rb')
	photo_first_floor = open(os.getcwd() + '/photo/church_map_first_floor.png', 'rb')
	photo_second_floor = open(os.getcwd() + '/photo/church_map_second_floor.png', 'rb')

	bot.send_media_group(message.from_user.id, [InputMediaPhoto(photo_first_floor, caption='Карта церкви «Слово жизни»'), InputMediaPhoto(photo_second_floor), InputMediaPhoto(photo_big_hall)])

def answer_message_text(message_text):
	if message_text == 'О нас':
		return 'Мы современная церковь с древним посланием. \nЦерковь «Слово жизни» — место раскрытия даров и способностей, а также молитвы, поклонения, глубокого изучения Библии и библейского взгляда на разные сферы жизни. \n\nМы рады каждому! ❤️Больше о нас на сайте https://wolrus.org'
	
	elif message_text == 'Социальные сети':
		return '''Мы в соцсетях

- <a href="https://t.me/wolrusyouth_msk">молодежный канал церкви</a>
- <a href="https://www.youtube.com/c/wolrustv/videos">YouTube</a>

- <a href="https://wolrus.org/">Сайт церкви «Слово жизни</a>
- <a href="https://t.me/wolrus_msk">Канал церкви</a>

Другие молодежные каналы:

• <a href="https://t.me/you_pray">молитвенный канал</a>
• <a href="https://t.me/wolrusteens">подростковый канал</a>
• <a href="https://t.me/wolrusyouthph">фото с мероприятий</a>
• <a href="https://t.me/gdb_wolrus">проект Год для Бога</a>
• <a href="https://t.me/resisterwolrus">женский канал Ресистер</a>
• <a href="https://t.me/rebro_rus">мужской канал Ребро</a>'''
	
	elif message_text == 'Чаты':
		return 'У нас есть разные чаты по интересам. Переходи по ссылке, вступай в понравившиеся чаты и находи компанию, с которой будет комфортно дружить: https://taplink.cc/chats'

	return 'Ошибка'

@bot.message_handler(commands=['start'], func=check_is_private_chat)
def first_message(message):
	try:
		start_text = 'Привет, это церковный бот!\nЗдесь ты найдешь основную информацию о церкви и предстоящих событиях. Выбери первый запрос:'
		bot.send_message(message.from_user.id, start_text, reply_markup=kb_menu.menu_kb)
	except Exception as e:
		print(e)

@bot.message_handler(regexp='Назад', func=check_is_private_chat)
def get_back_reply_markup(message):
	try:
		bot.send_message(message.from_user.id, 'Вернулись к началу', reply_markup=kb_menu.menu_kb)
	except Exception as e:
		print(e)

@bot.message_handler(regexp='Пожертвовать', func=check_is_private_chat)
def donate_message(message):
	try:
		donate_msg = '''В век современных технологий гораздо удобнее жертвовать онлайн.

Добровольное пожертвование — ещё один способ вашего участия в жизни церкви.

Ниже вы видите кнопки с разными видами пожертвований:
• Добровольное пожертвование – ваши десятины, помощь служениям церкви;
• Целевое пожертвование (второе здание) – ваша помощь в ремонте здания;

Спасибо за ваши пожертвования!'''
		bot.send_message(message.from_user.id, donate_msg, reply_markup=inline_donate.donate_kb)
	except Exception as e:
		print(e)

@bot.message_handler(regexp='Мероприятия', func=check_is_private_chat)
def event(message):
	try:
		bot.send_message(message.from_user.id, 'Выберите, что вас интересует!', reply_markup=kb_menu.event_kb)
	except Exception as e:
		print(e)

@bot.message_handler(regexp='Анонсы', func=check_is_private_chat)
def resend_announce_from_channel(message):
	try:
		for i, y in ANNOUNCE_DICT.items():
			print(f'{i} === {y}')
			bot.forward_message(message.from_user.id, y['channel_id'], y['message_id'])
	except Exception as e:
		print(e)
		print('in resend_announce_from_channel()')

@bot.message_handler(regexp='Расписание на неделю', func=check_is_private_chat)
def resend_week_schedule_from_channel(message):
	try:
		f = open('schedule_data.txt')
		id_array = [line.strip() for line in f]
		SCHEDULE_CHANNEL_ID = int(id_array[0])
		SCHEDULE_MESSAGE_ID = int(id_array[1])
		f.close()

		bot.forward_message(message.from_user.id, SCHEDULE_CHANNEL_ID, SCHEDULE_MESSAGE_ID)
	except Exception as e:
		print(e)
		print('in resend_week_schedule_from_channel()')

@bot.message_handler(content_types=['photo'])
def search_new_events(message):
	try:
		a = 'a'
		if(message.caption is not None and ('#расписание' in message.caption or '#Расписание' in message.caption)):
			f = open('schedule_data.txt', 'w')
			f.write(f'{message.chat.id}\n{message.message_id}')
			f.close()
		else:
			print('Error, have not #расписание')

		if(message.caption is not None and ('#анонс' in message.caption or '#Анонс' in message.caption)):
			global ANNOUNCE_DICT, n
			date = '12.02.2023 18:30:00'
			ANNOUNCE_DICT.update({a + str(n): {'channel_id': message.chat.id, 'message_id': message.message_id, 'date_to_end': date}})
			n = n + 1
		else:
			print('Error, have not #анонс')
	except Exception as e:
		print(e)
		print('in search_new_events()')

@bot.message_handler(func=check_is_private_chat)
def answer_message(message):
	try:
		text = answer_message_text(message.text)

		if message.text == 'Карта церкви':
			send_map(message)

		if text != 'Ошибка':
			bot.send_message(message.from_user.id, text, reply_markup=kb_menu.about_us_kb, parse_mode='HTML')
	except Exception as e:
		print(e)

bot.polling()

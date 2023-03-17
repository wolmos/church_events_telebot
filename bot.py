from datetime import datetime
import os
import json
import telebot
from sqlalchemy import create_engine
import pandas as pd
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, \
    ReplyKeyboardRemove, InputMediaPhoto

import config
from keyboards import kb_menu
from keyboards import inline_button

bot = telebot.TeleBot(config.bot_token)
ENGINE = create_engine(
    f'postgresql://{config.db_user}:{config.db_password}@{config.db_hostname}:{config.db_port}/{config.db_name}?sslmode=require')

STATION = ''
MOSCOW_SUBWAYS = ['щелковская', 'авиамоторная', 'автозаводская', 'академическая', 'александровский сад', 'алексеевская',
                  'алма-атинская', 'алтуфьево', 'андроновка', 'аннино', 'арбатская', 'аэропорт', 'бабушкинская',
                  'багратионовская', 'балтийская', 'баррикадная', 'бауманская', 'беговая', 'белокаменная',
                  'беломорская', 'белорусская', 'беляево', 'бибирево', 'библиотека имени ленина', 'битцевский парк',
                  'борисово', 'боровицкая', 'боровское шоссе', 'ботанический сад', 'братиславская',
                  'бульвар адмирала ушакова', 'бульвар дмитрия донского', 'бульвар рокоссовского', 'бунинская аллея',
                  'бутырская', 'варшавская', 'вднх', 'верхние котлы', 'верхние лихоборы', 'владыкино', 'водный стадион',
                  'войковская', 'волгоградский проспект', 'волжская', 'волоколамская', 'воробьёвы горы', 'выставочная',
                  'выхино', 'говорово', 'деловой центр', 'динамо', 'дмитровская', 'добрынинская', 'домодедовская',
                  'достоевская', 'дубровка', 'жулебино', 'зил', 'зорге', 'зябликово', 'измайлово', 'измайловская',
                  'калужская', 'кантемировская', 'каховская', 'каширскаякиевская', 'китай-город', 'кожуховская',
                  'коломенская', 'коммунарка', 'комсомольская', 'коньково', 'коптево', 'косино', 'котельники',
                  'красногвардейская', 'краснопресненская', 'красносельская', 'красные ворота', 'крестьянская застава',
                  'кропоткинская', 'крылатское', 'крымская', 'кузнецкий мост', 'кузьминки', 'кунцевская', 'курская',
                  'кутузовская', 'ленинский проспект', 'лермонтовский проспект', 'лесопарковая', 'лефортово',
                  'лихоборы', 'локомотив', 'ломоносовский проспект', 'лубянка', 'лужники', 'лухмановская', 'люблино',
                  'марксистская', 'марьина роща', 'марьино', 'маяковская', 'медведково', 'международная',
                  'менделеевская', 'минская', 'митино', 'мичуринский проспект', 'мнёвники', 'молодёжная', 'мякинино',
                  'нагатинская', 'нагорная', 'народное ополчение', 'нахимовский проспект', 'некрасовка',
                  'нижегородская', 'новогиреево', 'новокосино', 'новокузнецкая', 'новопеределкино', 'новослободская',
                  'новохохловская', 'новоясеневская', 'новые черёмушки', 'озёрная', 'окружная', 'окская', 'октябрьская',
                  'октябрьское поле', 'ольховая', 'орехово', 'отрадное', 'охотный ряд', 'павелецкая', 'панфиловская',
                  'парк культуры', 'парк победы', 'партизанская', 'первомайская', 'перово', 'петровский парк',
                  'петровско-разумовская', 'печатники', 'пионерская', 'планерная', 'площадь гагарина', 'площадь ильича',
                  'площадь революции', 'полежаевская', 'полянка', 'пражская', 'преображенская площадь', 'прокшино',
                  'пролетарская', 'проспект вернадского', 'проспект мира', 'профсоюзная', 'пушкинская',
                  'пятницкое шоссе', 'раменки', 'рассказовка', 'речной вокзал', 'рижская', 'римская', 'ростокино',
                  'румянцево', 'рязанский проспект', 'савёловская', 'саларьево', 'свиблово', 'севастопольская',
                  'селигерская', 'семёновская', 'серпуховская', 'славянский бульвар', 'смоленская', 'сокол',
                  'соколиная гора', 'сокольники', 'солнцево', 'спартак', 'спортивная', 'сретенский бульвар',
                  'старокачаловская', 'стахановская', 'стрешнево', 'строгино', 'студенческая', 'сухаревская',
                  'сходненская', 'таганская', 'тверская', 'театральная', 'текстильщики', 'телецентр', 'технопарк',
                  'тёплый стан', 'тимирязевская', 'третьяковская', 'третьяковская', 'тропарёво', 'трубная', 'тульская',
                  'тургеневская', 'тушинская', 'угрешская', 'улица 1905 года', 'улица академика янгеля',
                  'улица горчакова', 'улица дмитриевского', 'улица старокачаловская', 'улица скобелевская',
                  'университет', 'филатов луг', 'филёвский парк', 'фили', 'фонвизинская', 'фрунзенская', 'ховрино',
                  'хорошёво', 'хорошёвская', 'царицыно', 'цветной бульвар', 'цска', 'черкизовская', 'чертановская',
                  'чеховская', 'чистые пруды', 'чкаловская', 'шаболовская', 'шелепиха', 'шипиловская',
                  'шоссе энтузиастов', 'щёлковская', 'щукинская', 'электрозаводская', 'юго-восточная', 'юго-западная',
                  'южная', 'ясенево', 'киевская', 'озерная']


def get_home_group_master_data(engine):
    try:
        sql = """
		    SELECT type_age, type_of_hg, weekday, time_of_hg, name_leader, subway
		    FROM master_data_history_view
		    WHERE status_of_hg = 'открыта' and vacation = 'false' and enable_for_site = 'true' and type_age != 'Взрослые'
		    """
        return pd.read_sql(sql, engine)
    except Exception as e:
        print(e)


def get_list_subway_of_home_group(engine):
    try:
        sql = """
			SELECT distinct subway
			FROM master_data_history_view
			WHERE status_of_hg = 'открыта' and vacation = 'false' and enable_for_site = 'true' and type_age != 'Взрослые'
			ORDER BY subway
			"""
        df = pd.read_sql(sql, engine)
        array_of_subways = []

        for s in df['subway']:
            array_of_subways.append(s.lower())

        return array_of_subways
    except Exception as e:
        print(e)


def save_accounts_data(message):
    try:
        with open('accounts.json', 'r') as f:
            data = json.load(f)
            n = int(list(data.keys())[-1])
        is_have_not = True
        for i, y in data.items():
            if int(y['id']) == int(message.from_user.id):
                is_have_not = False
        if is_have_not:
            data.update({str(n + 1): {'id': message.from_user.id, 'is_bot': message.from_user.is_bot,
                                      'first_name': message.from_user.first_name,
                                      'username': message.from_user.username,
                                      'last_name': message.from_user.last_name,
                                      'language_code': message.from_user.language_code,
                                      'can_join_groups': message.from_user.can_join_groups,
                                      'can_read_all_group_messages': message.from_user.can_read_all_group_messages,
                                      'supports_inline_queries': message.from_user.supports_inline_queries,
                                      'is_premium': message.from_user.is_premium,
                                      'added_to_attachment_menu': message.from_user.added_to_attachment_menu,
                                      'date_to_join': message.date}})
        with open('accounts.json', 'w', encoding='utf-8') as f:
            json.dump(data, f)
        return True
    except Exception as e:
        print(e)


def mailing(channel_id, message_id):
    with open('accounts.json') as f:
        users = json.load(f)

    for n, user in users.items():
        bot.forward_message(user['id'], channel_id, message_id)


def check_is_subway(message):
    return message.text.lower() in MOSCOW_SUBWAYS


def check_home_group_in_station(station):
    return station.lower() in get_list_subway_of_home_group(ENGINE)


def check_is_have_hg_nearby(station):
    with open('nearby.json') as f:
        subways_with_nearby = json.load(f)

    for i in subways_with_nearby.keys():
        for v in subways_with_nearby[i]:
            if station.lower() == v.lower():
                return True
    return False


def check_group_is_wolrus(message):
    try:
        if (message.forward_from_chat.type == 'channel' and
                message.forward_from_chat.username == 'wolrusyouth_msk' and
                message.forward_from_chat.id == -1001337574730):
            return True
        return False
    except Exception as e:
        print(e)


def send_map(message):
    photo_big_hall = open(os.getcwd() + '/photo/church_map_big_hall.png', 'rb')
    photo_first_floor = open(os.getcwd() + '/photo/church_map_first_floor.png', 'rb')
    photo_second_floor = open(os.getcwd() + '/photo/church_map_second_floor.png', 'rb')

    bot.send_media_group(message.from_user.id,
                         [InputMediaPhoto(photo_first_floor, caption='Карта церкви «Слово жизни»'),
                          InputMediaPhoto(photo_second_floor), InputMediaPhoto(photo_big_hall)])


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
• <a href="https://t.me/rebro_rus">мужской канал Ребро</a>
• <a href="https://t.me/dnevnikmp">дневник МПшника</a>'''
    elif message_text == 'Чаты':
        return '''У нас есть разные чаты по интересам. Вступай в понравившиеся чаты и находи компанию, с которой будет комфортно дружить:

• <a href="tg://join?invite=cPtVxUqmfqVhOGY6">Wolrus Youth Chat</a>
• <a href="tg://join?invite=3vffHKySKqwzNWEy">Веганы</a>
• <a href="tg://join?invite=-vq1Nzh31l9kYzIy">Танцы</a>
• <a href="tg://join?invite=cbdXgfVAdFg3OTJi">Чат на спорте</a>
• <a href="tg://join?invite=XI5fv2M0RgdlMWQy">Футбол</a>
• <a href="tg://join?invite=f1xGGFofocdiNTEy">IT</a>
• <a href="tg://join?invite=kOOQx_xHCLdjMTU6">Мужской чат Ребро</a>
• <a href="tg://join?invite=ASFNjBQKXe40ZGQy">My Style</a>
• <a href="tg://join?invite=vcvNkQwdsZhhYTQy">Хочу служить</a>
• <a href="tg://join?invite=hBjUJSgImgE3ZjYy">Шаурмечная</a>
• <a href="tg://join?invite=SMgF3Nw63d6kBbiI">Бизнесмены</a>'''
    elif message_text == 'Домашние группы':
        return '''Домашняя группа (домашка) — это маленькая церковь внутри большой церкви. Это место, где всегда можно получить утешение, поддержку и ответы на свои вопросы, найти друзей, вырасти и узнать о Боге еще больше.

Введите станцию метро, чтобы мы смогли подобрать подходящую домашку для вас.'''

    return 'Ошибка'


@bot.message_handler(commands=['start'], chat_types=['private'], func=save_accounts_data)
def first_message(message):
    try:
        start_text = 'Привет, это церковный бот!\nЗдесь ты найдешь основную информацию о церкви и предстоящих событиях. Выбери первый запрос:'
        bot.send_message(message.from_user.id, start_text, reply_markup=kb_menu.menu_kb)
    except Exception as e:
        print(e)


@bot.message_handler(regexp='Назад', chat_types=['private'])
def get_back_reply_markup(message):
    try:
        bot.send_message(message.from_user.id, 'Вернулись к началу', reply_markup=kb_menu.menu_kb)
    except Exception as e:
        print(e)


@bot.message_handler(regexp='Пожертвовать', chat_types=['private'], func=save_accounts_data)
def donate_message(message):
    try:
        donate_msg = '''В век современных технологий гораздо удобнее жертвовать онлайн.

Добровольное пожертвование — ещё один способ вашего участия в жизни церкви.

Ниже вы видите кнопки с разными видами пожертвований:
• Добровольное пожертвование – ваши десятины, помощь служениям церкви;
• Целевое пожертвование (второе здание) – ваша помощь в ремонте здания;

Спасибо за ваши пожертвования!'''
        bot.send_message(message.from_user.id, donate_msg, reply_markup=inline_button.donate_kb)
    except Exception as e:
        print(e)


@bot.message_handler(regexp='Мероприятия', chat_types=['private'], func=save_accounts_data)
def event(message):
    try:
        bot.send_message(message.from_user.id, 'Выберите, что вас интересует!', reply_markup=kb_menu.event_kb)
    except Exception as e:
        print(e)


@bot.message_handler(regexp='Анонсы', chat_types=['private'], func=save_accounts_data)
def resend_announce_from_channel(message):
    try:
        today = datetime.now()
        with open('announce.json', 'r') as f:
            data = json.load(f)
        for n, item in data.items():
            if item['date_to_end']:
                date_to_end = datetime.strptime(item['date_to_end'], '%d.%m.%y %H:%M')
                if date_to_end > today:
                    bot.forward_message(message.from_user.id, item['channel_id'], item['message_id'])
    except Exception as e:
        print(e.with_traceback())


@bot.message_handler(regexp='Расписание на неделю', chat_types=['private'], func=save_accounts_data)
def resend_week_schedule_from_channel(message):
    try:
        with open('schedule_data.txt') as f:
            id_array = [line.strip() for line in f]
        SCHEDULE_CHANNEL_ID = int(id_array[0])
        SCHEDULE_MESSAGE_ID = int(id_array[1])

        bot.forward_message(message.from_user.id, SCHEDULE_CHANNEL_ID, SCHEDULE_MESSAGE_ID)
    except Exception as e:
        print(e)
        print('in resend_week_schedule_from_channel()')


@bot.message_handler(content_types=['photo'])
def search_new_events(message):
    try:
        if (message.caption is not None and ('#расписание' in message.caption or '#Расписание' in message.caption)):
            with open('schedule_data.txt', 'w') as f:
                f.write(f'{message.chat.id}\n{message.message_id}')

        if (message.caption is not None and ('#анонс' in message.caption or '#Анонс' in message.caption)):
            with open('announce.json', 'r') as f:
                data = json.load(f)
                n = int(list(data.keys())[-1])
            caption = message.caption
            index = int

            if '#Анонс' in message.caption:
                index = caption.find('#Анонс')
            elif '#анонс' in message.caption:
                index = caption.find('#анонс')

            date = caption[index + 7:]
            if date:
                data.update(
                    {str(n + 1): {'channel_id': message.chat.id, 'message_id': message.message_id,
                                  'date_to_end': date}})
                with open('announce.json', 'w') as f:
                    json.dump(data, f)

                mailing(message.chat.id, message.message_id)

            else:
                print('Дата и время не указаны')
    except Exception as e:
        print(e.with_traceback())


@bot.message_handler(regexp='Показать', chat_types=['private'])
def nearby_home_groups_info(message):
    try:
        global STATION
        current_station = []
        text = ''
        with open('nearby.json') as f:
            subways_with_nearby = json.load(f)

        for i in subways_with_nearby.keys():
            for v in subways_with_nearby[i]:
                if STATION.lower() == v.lower():
                    current_station.append(i)

        homegroups = []
        df = get_home_group_master_data(ENGINE)

        for item in current_station:
            for i, c in df.iterrows():
                if item.lower() == c.subway.lower():
                    temp = {}
                    temp.update(c)
                    homegroups.append(temp)

        for i in homegroups:
            text = text + f'{i["type_of_hg"]} {i["type_age"]}\n{i["weekday"]} {i["time_of_hg"]}\nЛидер: {i["name_leader"]}\nСтанция: {i["subway"]}\n\n'
        bot.send_message(message.from_user.id, text, reply_markup=inline_button.hg_kb)
    except Exception as e:
        print(e)


@bot.message_handler(func=check_is_subway, chat_types=['private'])
def get_home_group_info(message):
    try:
        text = ''
        global STATION
        STATION = message.text.lower()
        if check_home_group_in_station(STATION):
            homegroups = []
            df = get_home_group_master_data(ENGINE)
            for i, c in df.iterrows():
                if STATION == c.subway.lower():
                    temp = {}
                    temp.update(c)
                    homegroups.append(temp)

            for i in homegroups:
                text = text + f'{i["type_of_hg"]} {i["type_age"]}\n{i["weekday"]} {i["time_of_hg"]}\nЛидер: {i["name_leader"]}\nСтанция: {i["subway"]}\n\n'

            bot.send_message(message.from_user.id, text, reply_markup=inline_button.hg_kb)
        elif check_is_have_hg_nearby(STATION):
            text = 'К сожалению, на этой станции метро еще не проходят домашки, но можем предложить вам домашки на ближайших станциях.'
            bot.send_message(message.from_user.id, text, reply_markup=kb_menu.homegroups_kb, parse_mode='HTML')
        else:
            text = '''К сожалению, на этой станции метро еще не проходят домашки, но можем предложить вам домашки на ближайших станциях.

https://wolrus.org/homegroup'''
            bot.send_message(message.from_user.id, text, reply_markup=kb_menu.about_us_kb, parse_mode='HTML')
    except Exception as e:
        print(e)


@bot.message_handler(chat_types=['private'], func=save_accounts_data)
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

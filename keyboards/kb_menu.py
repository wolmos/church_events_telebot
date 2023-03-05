from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Раздел Меню
menu_kb = ReplyKeyboardMarkup(resize_keyboard=True)
# menu_kb.row('Мероприятия','О нас')
menu_kb.row('Расписание на неделю','О нас')
menu_kb.row('Пожертвовать')

# Раздела "Мероприятия"
event_kb = ReplyKeyboardMarkup(resize_keyboard=True)
# event_kb.row('Расписание на неделю', 'Анонсы')
# event_kb.row('Назад')

# Раздела "О нас"
about_us_kb = ReplyKeyboardMarkup(resize_keyboard=True)
about_us_kb.row('Социальные сети', 'Чаты')
about_us_kb.row('Карта церкви', 'Домашние группы')
about_us_kb.row('Назад')

# Раздел "Домашние группы"
homegroups_kb = ReplyKeyboardMarkup(resize_keyboard=True)
homegroups_kb.row('Показать', 'Назад')
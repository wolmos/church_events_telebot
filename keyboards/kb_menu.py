from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Группировка кнопок для Меню
menu_kb = ReplyKeyboardMarkup(resize_keyboard=True)
menu_kb.row('Мероприятия','О нас')
menu_kb.row('Пожертвовать')

# Группировка кнопок раздела "Мероприятия"
event_kb = ReplyKeyboardMarkup(resize_keyboard=True)
event_kb.row('Расписание на неделю', 'Анонсы')
event_kb.row('Назад')

# Группировка кнопок раздела "О нас"

about_us_kb = ReplyKeyboardMarkup(resize_keyboard=True)
about_us_kb.row('Социальные сети', 'Чаты')
about_us_kb.row('Карта церкви', 'Назад')
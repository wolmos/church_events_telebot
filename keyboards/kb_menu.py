from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# Группировка кнопок для Меню
menu_kb = ReplyKeyboardMarkup(resize_keyboard=True)
menu_kb.row('Расписание на неделю','О нас')
menu_kb.row('Пожертвование')

# Группировка кнопок раздела "О нас"

about_us_kb = ReplyKeyboardMarkup(resize_keyboard=True)
about_us_kb.row('Социальные сети', 'Чаты')
about_us_kb.row('Карта церкви', 'Назад')
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

donate_kb = InlineKeyboardMarkup()
donate_kb.row(InlineKeyboardButton('Добровольное пожертвование', url='https://qr.nspk.ru/AS1A00748MOLS8598H39NKN3LFI626GB?type=01&bank=100000000111&crc=45A3', callback_data='main'))
donate_kb.row(InlineKeyboardButton('Целевое пожертвование', url='https://qr.nspk.ru/AS1A0008SDT324SI9HCRT3GQ44TS15L0?type=01&bank=100000000111&crc=2D53', callback_data='youth'))

hg_kb = InlineKeyboardMarkup()
hg_kb.row(InlineKeyboardButton('Оставить заявку', url='https://docs.google.com/forms/d/1BkrrJKp1C6i6Nxh4wK1hyds79UP3crCrlcPb1v_flUs/edit', callback_data='request_on_hg'))

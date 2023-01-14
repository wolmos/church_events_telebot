from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

donate_kb = InlineKeyboardMarkup()
donate_kb.row(InlineKeyboardButton('Пожертвование', url='https://qr.nspk.ru/AS1A00748MOLS8598H39NKN3LFI626GB?type=01&bank=100000000111&crc=45A3', callback_data='main'))
donate_kb.row(InlineKeyboardButton('Молодежный центр', url='https://qr.nspk.ru/AS1A0008SDT324SI9HCRT3GQ44TS15L0?type=01&bank=100000000111&crc=2D53', callback_data='youth'))

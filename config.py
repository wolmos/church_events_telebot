import os

# НЕ ПУШИМ в гит секретные данные

# Telegram bot token
bot_token = os.environ['BOT_TOKEN']

# PostgreSQL
db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']
db_hostname = os.environ['DB_HOSTNAME']
db_port = 6432
db_name = os.environ['DB_NAME']
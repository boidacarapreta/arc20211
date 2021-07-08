import logging
from os import environ
from dotenv import load_dotenv
load_dotenv()

BACKEND = 'Discord'
BOT_DATA_DIR = r'data'
BOT_EXTRA_PLUGIN_DIR = r'plugins'
BOT_EXTRA_BACKEND_DIR = r'backend'
BOT_LOG_FILE = r'errbot.log'
BOT_LOG_LEVEL = logging.DEBUG
BOT_ADMINS = ('boidacarapreta#3942', )
BOT_IDENTITY = {
    # Necessário o arquivo .env no formato:
    # DISCORD_TOKEN=<token>
    # onde <token> contém o valor obtido de
    # https://discord.com/developers/applications
    'token': environ.get('DISCORD_TOKEN')
}

# Se os plugins têm dependências, usar ambiente virtual e requirements.txt
AUTOINSTALL_DEPS = True

# Prefixo do bot
BOT_PREFIX = '!'
BOT_PREFIX_OPTIONAL_ON_CHAT = True

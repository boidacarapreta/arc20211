import logging

BACKEND = 'Text'

BOT_DATA_DIR = r'data'
BOT_EXTRA_PLUGIN_DIR = r'plugins'

BOT_LOG_FILE = r'errbot.log'
BOT_LOG_LEVEL = logging.DEBUG

BOT_ADMINS = ('@CHANGE_ME', )

# Se os plugins têm dependências, usar ambiente virtual e requirements.txt
AUTOINSTALL_DEPS = True

# Prefixo do bot
BOT_PREFIX = '!'
BOT_PREFIX_OPTIONAL_ON_CHAT = True

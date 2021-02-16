import sys
from logging import DEBUG, WARNING, basicConfig, getLogger, INFO
import os
from telethon import TelegramClient
from distutils.util import strtobool as sb
from telethon.sessions import StringSession
ENV = os.environ.get("ENV", False)

if ENV:
    from forwardbot.BotConfig import Config
else:
    from local_config import Development as Config

bot = TelegramClient('bot', Config.API_ID, Config.API_HASH).start(bot_token=Config.BOT_TOKEN)

client = TelegramClient(StringSession(Config.STRING_SESSION), Config.API_ID, Config.API_HASH)

if bool(ENV):
    CONSOLE_LOGGER_VERBOSE = sb(os.environ.get("CONSOLE_LOGGER_VERBOSE", "False"))

    if CONSOLE_LOGGER_VERBOSE:
        basicConfig(
            format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
            level=DEBUG,
        )
    else:
        basicConfig(
            format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=INFO
        )
    logger = getLogger(__name__)

if Config.API_ID is None:
    logger.info("API_ID is None. Bot Is Quiting")
    sys.exit(1)
if Config.API_HASH is None:
    logger.info("API_HASH is None. Bot Is Quiting")
    sys.exit(1)
if Config.BOT_TOKEN is None:
    logger.info("BOT_TOKEN is None. Bot Is Quiting")
    sys.exit(1)
if Config.STRING_SESSION is None:
    logger.info("STRING_SESSION is None. Bot Is Quiting")
    sys.exit(1)
if Config.SUDO_USERS is None:
    logger.info("STRING_SESSION is None. Bot Is Quiting")
    sys.exit(1)
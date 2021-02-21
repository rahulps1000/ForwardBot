from forwardbot.BotConfig import Config
from forwardbot import bot
from forwardbot import client
from pathlib import Path
from sys import argv
from forwardbot.utils import start_forwardbot
import glob

if len(argv) not in (1, 3, 4):
    bot.disconnect()
    client.disconnect()
else:
    bot.start(bot_token=Config.BOT_TOKEN)
    client.start()

path = "forwardbot/plugins/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as f:
        path1 = Path(f.name)
        shortname = path1.stem
        start_forwardbot(shortname.replace(".py", ""))

print("Your BOT is Ready.")
print("Try Sending /start")

if len(argv) not in (1, 3, 4):
    bot.disconnect()
    client.disconnect()
else:
    client.run_until_disconnected()

from telethon import events
from forwardbot import bot
from forwardbot.BotConfig import Config
bothandler = Config.COMMAND_HAND_LER
def forwardbot_cmd(add_cmd, is_args=False):
    def cmd(func):
        if is_args:
            pattern = bothandler + add_cmd + "(?: |$)(.*)"
        else:
            pattern = bothandler + add_cmd + "$"
        bot.add_event_handler(
            func, events.NewMessage(incoming=True, pattern=pattern)
        )
    return cmd

async def is_sudo(event):
    if str(event.sender_id) in Config.SUDO_USERS:
        return True
    else:
        return False

def start_forwardbot(shortname):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        import importlib
        import sys
        from pathlib import Path
        import forwardbot.utils
        path = Path(f"forwardbot/plugins/{shortname}.py")
        name = "forwardbot.plugins.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        print("Starting Your  Bot.")
        print("IMPORTED " + shortname)
    else:
        import importlib
        import sys
        from pathlib import Path
        import forwardbot.utils
        path = Path(f"forwardbot/plugins/{shortname}.py")
        name = "forwardbot.plugins.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        mod.forwardbot_cmd = forwardbot_cmd
        mod.forwardbot = bot
        mod.Config = Config
        spec.loader.exec_module(mod)
        sys.modules["forwardbot.plugins" + shortname] = mod
        print("IMPORTED " + shortname)

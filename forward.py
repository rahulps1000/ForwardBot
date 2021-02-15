from telethon.sync import TelegramClient, events
import re
import os
from os import environ
import sys
import asyncio
from telethon.sessions import StringSession
import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

string = int(environ.get("STRING"))
api_id = environ.get("API_ID")
api_hash = environ.get("API_HASH")


MessageCount = 0
help_msg = """
The Commands in the bot are:

**Command :** .fdoc channel_id
**Usage : ** Forwards all documents from the given channel to the chat where the command is executed.
**Command :** .count
**Usage : ** Returns the Total message sent using the bot.
**Command :** .reset
**Usage : ** Resets the message count to 0.
**Command :** .restart
**Usage : ** Updates and Restarts the Plugin
**Command :** .help
**Usage : ** Get the help of this bot.

Bot is created by @lal_bakthan
"""


with TelegramClient(StringSession(string), api_id, api_hash) as client:

    client.send_message('me', 'Running....')
    print("Running....")

    @client.on(events.NewMessage(pattern=r'.fdoc (.*) (.*)'))
    async def handler(event):
        await event.edit("Forwaring all messages")
        fromchat = int(event.pattern_match.group(1))
        tochat = int(event.pattern_match.group(2))
        count = 4500
        mcount = 1000
        global MessageCount
        print("Starting to forward")
        async for message in client.iter_messages(fromchat, reverse=True):
            if count:
                if mcount:
                    if message.document and not message.sticker :
                        try:
                            await client.send_file(tochat, message.document)
                            await asyncio.sleep(2)
                            mcount -= 1
                            count -= 1
                            MessageCount += 1
                        except:
                            pass
                else:
                    print(f"You have send {MessageCount} messages" )
                    print("Waiting for 10 mins")
                    await asyncio.sleep(600)
                    mcount = 1000
                    print("Starting after 10 mins")
            else:
                print(f"You have send {MessageCount} messages")
                print("Waiting for 30 mins")
                await asyncio.sleep(1800)
                count = 4500
                print("Starting after 30 mins")
        await event.delete()
        print("Finished")

    @client.on(events.NewMessage(pattern=r'.count'))
    async def handler(event):
      await event.edit(f"You have send {MessageCount} messages")
      print(f"You have send {MessageCount} messages")

    @client.on(events.NewMessage(pattern=r'.reset'))
    async def handler(event):
      global MessageCount
      MessageCount=0
      await event.edit("Message count has been reset to 0")
      print("Message count has been reset to 0")

    @client.on(events.NewMessage(pattern=r'.help'))
    async def handler(event):
      await event.edit(help_msg)

    @client.on(events.NewMessage(pattern=r'.restart'))
    async def handler(event):
      await event.edit('Updating Script')
      client.disconnect()
      os.system("git pull")
      os.execl(sys.executable, sys.executable, *sys.argv)
      


    client.run_until_disconnected()

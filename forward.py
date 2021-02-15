from telethon.sync import TelegramClient, events
import re
import os
from os import environ
import sys
import asyncio
from telethon.sessions import StringSession
from telethon import Button
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon import errors

import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)


import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.DEBUG)

api_id = int(environ.get("API_ID"))
api_hash = environ.get("API_HASH")
bot_token = environ.get("TOKEN")
string = environ.get("STRING")
MessageCount = 0
help_msg = """
The Commands in the bot are:

**Command :** /fdoc channel_id
**Usage : ** Forwards all documents from the given channel to the chat where the command is executed.
**Command :** /count
**Usage : ** Returns the Total message sent using the bot.
**Command :** /reset
**Usage : ** Resets the message count to 0.
**Command :** /restart
**Usage : ** Updates and Restarts the Plugin.
**Command :** /join channel_link
**Usage : ** Joins the channel.
**Command :** /help
**Usage : ** Get the help of this bot.

Bot is created by @lal_bakthan and @subinps
"""



bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@bot.on(events.NewMessage(pattern="^/start$"))
async def start(event):
    replied_user = await event.client(GetFullUserRequest(event.sender_id))
    firstname = replied_user.user.first_name
    await event.reply(message=f"**Hello, {firstname}, I Am Batch Forwarder Bot.** \n**Using me you can forward all the files in a channel to anothor easily** \n**USE AT OWN RISK !!!!! ACCOUNT MAY GET BAN**"
                     )
@bot.on(events.NewMessage(pattern=r'/count'))
async def handler(event):
    await event.reply(f"You have send {MessageCount} messages")
    print(f"You have send {MessageCount} messages")


@bot.on(events.NewMessage(pattern=r'/reset'))
async def handler(event):
    global MessageCount
    MessageCount=0
    await event.reply("Message count has been reset to 0")
    print("Message count has been reset to 0")

@bot.on(events.NewMessage(pattern=r'/help'))
async def handler(event):
    await event.reply(help_msg)

@bot.on(events.NewMessage(pattern=r'/restart'))
async def handler(event):
    try:
        await event.reply('Updating Script')
        client.disconnect()
        os.system("git pull")
        os.execl(sys.executable, sys.executable, *sys.argv)
    except:
        pass

@bot.on(events.NewMessage(pattern=r'/join (.*)'))
async def handler(event):
    link = event.pattern_match.group(1)
    type = ''
    if link:
        if 'joinchat' in link:
            chann = re.search(r".joinchat.(.*)", link)
            type = 'private'
        else:
            chann = re.search(r"t.me.(.*)", link)
            type = 'public'
        if type == 'private':
            try:
                updates = await client(ImportChatInviteRequest(chann.group(1)))
                await event.respond("Successfully joined the Channel")
            except errors.UserAlreadyParticipantError:
                await event.respond("You have already joined the Channel")
            except errors.InviteHashExpiredError:
                await event.respond("Wrong URL")
        if type == 'public':
            try:
                updates = await client(ImportChatInviteRequest(chann.group(1)))
                await event.respond("Successfully joined the Channel")
            except:
                await event.respond("Wrong URL")
    else:
        return




with TelegramClient(StringSession(string), api_id, api_hash) as client:

    client.send_message('me', 'Running....')
    print("Running....")

    @bot.on(events.NewMessage(pattern=r'/fdoc (.*) (.*)'))
    async def handler(event):
        await event.reply("Forwaring all messages")
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

    

    client.run_until_disconnected()
api_hash = environ.get("API_HASH")
bot_token = environ.get("TOKEN")
string = environ.get("STRING")

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



bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@bot.on(events.NewMessage(pattern="^/start$"))
async def start(event):
    replied_user = await event.client(GetFullUserRequest(event.sender_id))
    firstname = replied_user.user.first_name
    await event.respond(message=f"**Hello, {firstname}, I Am Batch Forwarder Bot.** \n**Using me you can forward all the files in a channel to anothor easily** \n**USE AT OWN RISK !!!!! ACCOUNT MAY GET BAN**"
                     )
@bot.on(events.NewMessage(pattern=r'/count'))
async def handler(event):
    await event.respond(f"You have send {MessageCount} messages")
    print(f"You have send {MessageCount} messages")


@bot.on(events.NewMessage(pattern=r'/reset'))
async def handler(event):
    global MessageCount
    MessageCount=0
    await event.respond("Message count has been reset to 0")
    print("Message count has been reset to 0")

@bot.on(events.NewMessage(pattern=r'/help'))
async def handler(event):
    await event.respond(help_msg)

@bot.on(events.NewMessage(pattern=r'/restart'))
async def handler(event):
    try:
        await event.respond('Updating Script')
        client.disconnect()
        os.system("git pull")
        os.execl(sys.executable, sys.executable, *sys.argv)
    except:
        pass


with TelegramClient(StringSession(string), api_id, api_hash) as client:

    client.send_message('me', 'Running....')
    print("Running....")

    @bot.on(events.NewMessage(pattern=r'/fdoc (.*) (.*)'))
    async def handler(event):
        await event.respond("Forwaring all documents")
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

    

    client.run_until_disconnected()

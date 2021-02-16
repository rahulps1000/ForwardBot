from forwardbot import Config
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
from forwardbot.utils import start_forwardbot
from telethon.sync import events
from forwardbot import bot
from forwardbot import client
from telethon import errors
from os import execl
import re
import asyncio

global MessageCount
help_msg = Config.HELP_MSG
sudo_users = Config.SUDO_USERS

@forwardbot_cmd("start", is_args=False)
async def start(event):
    if not await is_sudo(event):
        await event.respond("You are not authorized to use this Bot. Create your own.")
        return
    replied_user = await event.client(GetFullUserRequest(event.sender_id))
    firstname = replied_user.user.first_name
    await event.respond(message=f"**Hello, {firstname}, I Am Batch Forwarder Bot.** \n**Using me you can forward all the files in a channel to anothor easily** \n**USE AT OWN RISK !!!!! ACCOUNT MAY GET BAN**"
                     )
@forwardbot_cmd("count", is_args=False)
async def handler(event):
    if not await is_sudo(event):
        await event.respond("You are not authorized to use this Bot. Create your own.")
        return
    await event.respond(f"You have send {MessageCount} messages")
    print(f"You have send {MessageCount} messages")


@forwardbot_cmd("reset", is_args=False)
async def handler(event):
    if not await is_sudo(event):
        await event.respond("You are not authorized to use this Bot. Create your own.")
        return
    global MessageCount
    MessageCount=0
    await event.respond("Message count has been reset to 0")
    print("Message count has been reset to 0")

@forwardbot_cmd("help", is_args=False)
async def handler(event):
    if not await is_sudo(event):
        await event.respond("You are not authorized to use this Bot. Create your own.")
        return
    await event.respond(help_msg)

@forwardbot_cmd("restart", is_args=False)
async def handler(event):
    if not await is_sudo(event):
        await event.respond("You are not authorized to use this Bot. Create your own.")
        return
    try:
        await event.respond('Updated the Script.')
        await event.respond('Restarted')
        await bot.disconnect()
        execl(sys.executable, sys.executable, *sys.argv)
    except:
        pass

@forwardbot_cmd("admin", is_args=False)
async def handler(event):
    if str(event.sender_id) in sudo_users:
        await event.respond("You are an admin")
    else:
        await event.respond("You are not an admin")

@bot.on(events.NewMessage(pattern=r'/join (.*)'))
async def handler(event):
    if not await is_sudo(event):
        await event.respond("You are not authorized to use this Bot. Create your own.")
        return
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
                await client(ImportChatInviteRequest(chann.group(1)))
                await event.respond("Successfully joined the Channel")
            except errors.UserAlreadyParticipantError:
                await event.respond("You have already joined the Channel")
            except errors.InviteHashExpiredError:
                await event.respond("Wrong URL")
        if type == 'public':
            try:
                await client(JoinChannelRequest(chann.group(1)))
                await event.respond("Successfully joined the Channel")
            except:
                await event.respond("Wrong URL")
    else:
        return


async def is_sudo(event):
    if str(event.sender_id) in sudo_users:
        return True
    else:
        return False


@bot.on(events.NewMessage(pattern=r'/fdoc (.*) (.*)'))
async def handler(event):
    if not await is_sudo(event):
      await event.respond("You are not authorized to use this Bot. Create your own.")
      return
    m=await event.respond("Forwaring all messages")
    fromchat = int(event.pattern_match.group(1))
    tochat = int(event.pattern_match.group(2))
    count = 4500
    mcount = 1000
    global MessageCount
    print("Starting to forward")
    await m.edit('Starting to forward')
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
                await m.edit(f"You have send {MessageCount} messages.\nWaiting for 10 minutes.")
                await asyncio.sleep(600)
                mcount = 1000
                print("Starting after 10 mins")
                await m.edit("Starting after 10 mins")
        else:
            print(f"You have send {MessageCount} messages")
            print("Waiting for 30 mins")
            await m.edit(f"You have send {MessageCount} messages.\nWaiting for 30 minutes.")
            await asyncio.sleep(1800)
            count = 4500
            print("Starting after 30 mins")
            await m.edit("Starting after 30 mins")
    await event.delete()
    print("Finished")
    await bot.send_message(event.chat_id, message=f"Succesfully finished sending {MessageCount} messages")

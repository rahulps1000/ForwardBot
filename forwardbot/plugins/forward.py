from telethon.sync import events
from forwardbot import bot
from forwardbot import client
from forwardbot.utils import is_sudo
from forwardbot.tool import *
from telethon import Button
import asyncio
from forwardbot.utils import forwardbot_cmd
import datetime
from datetime import timedelta

MessageCount = 0
BOT_STATUS = "0"
status = set(int(x) for x in (BOT_STATUS).split())
datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'

start = None

@forwardbot_cmd("forward", is_args=False)
async def handler(event):
    if not await is_sudo(event):
        await event.respond("You are not authorized to use this Bot. Create your own.")
        return
    if "1" in status:
        await event.respond("A task is already running.")
        return
    if "2" in status:
        await event.respond("Sleeping the engine for avoiding ban.")
        return
    async with bot.conversation(event.chat_id) as conv:
        await conv.send_message("Please send the channel id from where you want to forward messages as a reply to this message.")
        while True:
            r = conv.wait_event(events.NewMessage(chats=event.chat_id))
            r = await r
            global fromchannel
            fromchannel = r.message.message.strip()
            if not r.is_reply:
                await conv.send_message("Please send the message as a reply to the message.")
            else:
                await conv.send_message("Okay now send me the channel id to where you want to forward messages as a reply to this message.")
                while True:
                    p = conv.wait_event(events.NewMessage(chats=event.chat_id))
                    p = await p
                    global tochannel
                    tochannel = p.message.message.strip()
                    if not p.is_reply:
                        await conv.send_message("Please send the message as a reply to the message.")
                    else:
                        await event.respond('Select What you need to forward', buttons=[
                            [Button.inline('All Messages', b'all'), Button.inline('Only Photos', b'photo')],
                            [Button.inline('Only Documents', b'docs'), Button.inline(' Only Video' , b'video')]
                            ])
                        break
                break

@forwardbot_cmd("reset", is_args=False)
async def handler(event):
    if not await is_sudo(event):
        await event.respond("You are not authorized to use this Bot. Create your own.")
        return
    global MessageCount
    MessageCount=0
    await event.respond("Message count has been reset to 0")
    print("Message count has been reset to 0")

@forwardbot_cmd("uptime", is_args=False)
async def handler(event):
    if not await is_sudo(event):
        await event.respond("You are not authorized to use this Bot. Create your own.")
        return
    global start
    if start:
        stop = str(datetime.datetime.now())
        diff = datetime.datetime.strptime(start, datetimeFormat) - datetime.datetime.strptime(stop, datetimeFormat)
        duration = abs(diff)
        days, seconds = duration.days, duration.seconds
        hours = int(seconds / 3600)
        minutes = int((seconds % 3600)/60)
        seconds = int(seconds % 60)
        await event.respond(f"The bot is forwarding files for {days} days, {hours} hours, {minutes} minutes and {seconds} seconds")
    else:
        await event.respond("Please start a forwarding to check the uptime")

@forwardbot_cmd("status", is_args=False)
async def handler(event):
    if not await is_sudo(event):
        await event.respond("You are not authorized to use this Bot. Create your own.")
        return

    if "1" in status:
        await event.respond("Currently Bot is forwarding messages.")
    if "2" in status:
        await event.respond("Now Bot is Sleeping")
    if "1" not in status and "2" not in status:
        await event.respond("Bot is Idle now, You can start a task.")


@forwardbot_cmd("count", is_args=False)
async def handler(event):
    if not await is_sudo(event):
        await event.respond("You are not authorized to use this Bot. Create your own.")
        return
    await event.respond(f"You have send {MessageCount} messages")
    print(f"You have send {MessageCount} messages")


@bot.on(events.CallbackQuery)
async def handler(event):
    if event.data == b'all':
        await event.delete()
        if not await is_sudo(event):
            await event.respond("You are not authorized to use this Bot. Create your own.")
            return
        if "1" in status:
            await event.respond("A task is already running.")
            return
        if "2" in status:
            await event.respond("Sleeping the engine for avoiding ban.")
            return
        try:
            m=await event.respond("Trying Forwarding")
            fromchat = int(fromchannel)
            tochat = int(tochannel)
            count = 4507
            mcount = 1009
            global MessageCount
            print("Starting to forward")
            global start
            start = str(datetime.datetime.now())
            async for message in client.iter_messages(fromchat, reverse=True):
                if count:
                    if mcount:
                        try:
                            await client.send_message(tochat, message)
                            try:
                              if message.document:
                                if len(str(message.file.name)) <= 95:
                                  print("Succesfully forwarded: " + str(message.file.name))
                                else:
                                  logmsg = str(message.file.name)
                                  logmsg = logmsg[:95] + "..."
                                  print("Succesfully forwarded: " + logmsg)
                              else:
                                if len(str(message.message)) <= 95:
                                  print("Now forwarding: " + str(message.message))
                                else:
                                  logmsg = str(message.message)
                                  logmsg = logmsg[:95] + "..."
                                  print("Now Forwarding: " + logmsg)
                            except:
                              print("Unable to retrive data.")
                            status.add("1")
                            try:
                                status.remove("2")
                            except:
                                pass
                            await asyncio.sleep(2)
                            
                            mcount -= 1
                            count -= 1
                            MessageCount += 1
                            await m.edit("Now Forwarding all messages.")
                        except:
                            pass
                    else:
                        print(f"You have send {MessageCount} messages" )
                        print("Waiting for 10 mins")
                        status.add("2")
                        status.remove("1")
                        await m.edit(f"You have send {MessageCount} messages.\nWaiting for 10 minutes.")
                        await asyncio.sleep(600)
                        mcount = 1009
                        print("Starting after 10 mins")
                        await m.edit("Starting after 10 mins")
                else:
                    print(f"You have send {MessageCount} messages")
                    print("Waiting for 30 mins")
                    status.add("2")
                    status.remove("1")
                    await m.edit(f"You have send {MessageCount} messages.\nWaiting for 30 minutes.")
                    await asyncio.sleep(1800)
                    count = 4507
                    print("Starting after 30 mins")
                    await m.edit("Starting after 30 mins")
                    
        except ValueError:
            await m.edit("You must join the channel before starting forwarding. Use /join")
            return
        print("Finished")
        stop = str(datetime.datetime.now())
        diff = datetime.datetime.strptime(start, datetimeFormat) - datetime.datetime.strptime(stop, datetimeFormat)
        duration = abs(diff)
        days, seconds = duration.days, duration.seconds
        hours = int(seconds / 3600)
        minutes = int((seconds % 3600)/60)
        seconds = int(seconds % 60)
        await event.respond(f"Succesfully finished sending {MessageCount} messages in {days} days, {hours} hours, {minutes} minutes and {seconds} seconds")
        try:
            status.remove("1")
        except:
            pass
        try:
            status.remove("2")
        except:
            pass



@bot.on(events.CallbackQuery)
async def handler(event):
    if event.data == b'docs':
        await event.delete()
        if not await is_sudo(event):
            await event.respond("You are not authorized to use this Bot. Create your own.")
            return
        if "1" in status:
            await event.respond("A task is already running.")
            return
        if "2" in status:
            await event.respond("Sleeping the engine for avoiding ban.")
            return
        try:
            m=await event.respond("Trying Forwarding")
            fromchat = int(fromchannel)
            tochat = int(tochannel)
            count = 4507
            mcount = 1009
            global MessageCount
            print("Starting to forward")
            global start
            start = str(datetime.datetime.now())
            async for message in client.iter_messages(fromchat, reverse=True):
                if count:
                    if mcount:
                        if media_type(message) == 'Document':
                            try:
                                await client.send_file(tochat, message.document) 
                                try:
                                  if len(str(message.file.name)) <= 95:
                                    print("Succesfully forwarded: " + str(message.file.name))
                                  else:
                                    logmsg = str(message.file.name)
                                    logmsg = logmsg[:95] + "..."
                                    print("Succesfully forwarded: " + logmsg)
                                except:
                                  print("Unable to retrive data.")
                                status.add("1")
                                try:
                                    status.remove("2")
                                except:
                                    pass
                                await asyncio.sleep(2)
                                mcount -= 1
                                count -= 1
                                MessageCount += 1
                                await m.edit("Now Forwarding all documents.")
                            except:
                                pass
                    else:
                        print(f"You have send {MessageCount} messages" )
                        print("Waiting for 10 mins")
                        status.add("2")
                        status.remove("1")
                        await m.edit(f"You have send {MessageCount} messages.\nWaiting for 10 minutes.")
                        await asyncio.sleep(600)
                        mcount = 1009
                        print("Starting after 10 mins")
                        await m.edit("Starting after 10 mins")
                else:
                    print(f"You have send {MessageCount} messages")
                    print("Waiting for 30 mins")
                    status.add("2")
                    status.remove("1")
                    await m.edit(f"You have send {MessageCount} messages.\nWaiting for 30 minutes.")
                    await asyncio.sleep(1800)
                    count = 4507
                    print("Starting after 30 mins")
                    await m.edit("Starting after 30 mins")
                    
        except ValueError:
            await m.edit("You must join the channel before starting forwarding. Use /join")
            return
        print("Finished")
        stop = str(datetime.datetime.now())
        diff = datetime.datetime.strptime(start, datetimeFormat) - datetime.datetime.strptime(stop, datetimeFormat)
        duration = abs(diff)
        days, seconds = duration.days, duration.seconds
        hours = int(seconds / 3600)
        minutes = int((seconds % 3600)/60)
        seconds = int(seconds % 60)
        await event.respond(f"Succesfully finished sending {MessageCount} messages in {days} days, {hours} hours, {minutes} minutes and {seconds} seconds")
        try:
            status.remove("1")
        except:
            pass
        try:
            status.remove("2")
        except:
            pass


@bot.on(events.CallbackQuery)
async def handler(event):
    if event.data == b'photo':
        await event.delete()
        if not await is_sudo(event):
            await event.respond("You are not authorized to use this Bot. Create your own.")
            return
        if "1" in status:
            await event.respond("A task is already running.")
            return
        if "2" in status:
            await event.respond("Sleeping the engine for avoiding ban.")
            return
        try:
            m=await event.respond("Trying Forwarding")
            fromchat = int(fromchannel)
            tochat = int(tochannel)
            count = 1009
            mcount = 4507
            global MessageCount
            print("Starting to forward")
            global start
            start = str(datetime.datetime.now())
            async for message in client.iter_messages(fromchat, reverse=True):
                if count:
                    if mcount:
                        if media_type(message) == 'Photo':
                            try:
                                await client.send_message(tochat, message)
                                try:
                                  if len(str(message.message)) <= 95:
                                    print("Succesfully forwarded: " + str(message.message))
                                  else:
                                    logmsg = str(message.message)
                                    logmsg = logmsg[:95] + "..."
                                    print("Succesfully forwarded: " + logmsg)
                                except:
                                  print("Unable to retrive data.")
                                status.add("1")
                                try:
                                    status.remove("2")
                                except:
                                    pass
                                await asyncio.sleep(2)
                                mcount -= 1
                                count -= 1
                                MessageCount += 1
                                await m.edit("Now Forwarding all photos.")
                            except:
                                pass
                    else:
                        print(f"You have send {MessageCount} messages" )
                        print("Waiting for 10 mins")
                        status.add("2")
                        status.remove("1")
                        await m.edit(f"You have send {MessageCount} messages.\nWaiting for 10 minutes.")
                        await asyncio.sleep(600)
                        mcount = 1009
                        print("Starting after 10 mins")
                        await m.edit("Starting after 10 mins")
                else:
                    print(f"You have send {MessageCount} messages")
                    print("Waiting for 30 mins")
                    status.add("2")
                    status.remove("1")
                    await m.edit(f"You have send {MessageCount} messages.\nWaiting for 30 minutes.")
                    await asyncio.sleep(1800)
                    count = 4507
                    print("Starting after 30 mins")
                    await m.edit("Starting after 30 mins")
                    
        except ValueError:
            await m.edit("You must join the channel before starting forwarding. Use /join")
            return
        print("Finished")
        stop = str(datetime.datetime.now())
        diff = datetime.datetime.strptime(start, datetimeFormat) - datetime.datetime.strptime(stop, datetimeFormat)
        duration = abs(diff)
        days, seconds = duration.days, duration.seconds
        hours = int(seconds / 3600)
        minutes = int((seconds % 3600)/60)
        seconds = int(seconds % 60)
        await event.respond(f"Succesfully finished sending {MessageCount} messages in {days} days, {hours} hours, {minutes} minutes and {seconds} seconds")
        try:
            status.remove("1")
        except:
            pass
        try:
            status.remove("2")
        except:
            pass


@bot.on(events.CallbackQuery)
async def handler(event):
    if event.data == b'video':
        await event.delete()
        if not await is_sudo(event):
            await event.respond("You are not authorized to use this Bot. Create your own.")
            return
        if "1" in status:
            await event.respond("A task is already running.")
            return
        if "2" in status:
            await event.respond("Sleeping the engine for avoiding ban.")
            return
        try:
            m=await event.respond("Trying Forwarding")
            fromchat = int(fromchannel)
            tochat = int(tochannel)
            count = 4507
            mcount = 1009
            global MessageCount
            print("Starting to forward")
            global start
            start = str(datetime.datetime.now())
            async for message in client.iter_messages(fromchat, reverse=True):
                if count:
                    if mcount:
                        if media_type(message) == 'Video':
                            try:
                                await client.send_message(tochat, message)
                                try:
                                  if len(str(message.message)) <= 95:
                                    print("Succesfully forwarded: " + str(message.message))
                                  else:
                                    logmsg = str(message.message)
                                    logmsg = logmsg[:95] + "..."
                                    print("Succesfully forwarded: " + logmsg)
                                except:
                                  print("Unable to retrive data.")
                                status.add("1")
                                try:
                                    status.remove("2")
                                except:
                                    pass
                                await asyncio.sleep(2)
                                mcount -= 1
                                count -= 1
                                MessageCount += 1
                                await m.edit("Now Forwarding all videos.")
                            except:
                                pass
                    else:
                        print(f"You have send {MessageCount} messages" )
                        print("Waiting for 10 mins")
                        status.add("2")
                        status.remove("1")
                        await m.edit(f"You have send {MessageCount} messages.\nWaiting for 10 minutes.")
                        await asyncio.sleep(600)
                        mcount = 1009
                        print("Starting after 10 mins")
                        await m.edit("Starting after 10 mins")
                else:
                    print(f"You have send {MessageCount} messages")
                    print("Waiting for 30 mins")
                    status.add("2")
                    status.remove("1")
                    await m.edit(f"You have send {MessageCount} messages.\nWaiting for 30 minutes.")
                    await asyncio.sleep(1800)
                    count = 4507
                    print("Starting after 30 mins")
                    await m.edit("Starting after 30 mins")
                    
        except ValueError:
            await m.edit("You must join the channel before starting forwarding. Use /join")
            return
        print("Finished")
        stop = str(datetime.datetime.now())
        diff = datetime.datetime.strptime(start, datetimeFormat) - datetime.datetime.strptime(stop, datetimeFormat)
        duration = abs(diff)
        days, seconds = duration.days, duration.seconds
        hours = int(seconds / 3600)
        minutes = int((seconds % 3600)/60)
        seconds = int(seconds % 60)
        await event.respond(f"Succesfully finished sending {MessageCount} messages in {days} days, {hours} hours, {minutes} minutes and {seconds} seconds")
        try:
            status.remove("1")
        except:
            pass
        try:
            status.remove("2")
        except:
            pass

from telethon import TelegramClient, events, connection
from telethon.tl.custom import Button
from telethon.tl.functions.messages import GetScheduledHistoryRequest, DeleteScheduledMessagesRequest
from telethon.tl.patched import Message
import time
import datetime
import random
import logging
import asyncio
import os
import json
import sys

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.ERROR)

api_id = 1167185
api_hash = 'eccec789bc056dda4f7919712a91840f'


clientM = TelegramClient("Admin", api_id, api_hash)
clientM.start(+5358033572)

clientAdmin: TelegramClient = TelegramClient("Admin", api_id, api_hash)
#clientAdmin.start(+5352725779)


async def my_event():
    #async for dialog in clientM.iter_dialogs():
    #   print(dialog.id, dialog.title)
    async for message in clientM.iter_messages(1001616554837, limit=50):
        try:
            if message.text is not None:
                m = message.text + "\nButtons:"
                if(message.button_count > 0):
                    for btLine in message.buttons:
                        for bt in btLine:
                            m += '\n' + bt.text
                #print(message)
                m += "\n" + message.date.strftime("%m/%d/%Y, %H:%M:%S")
                print(m)
                #await clientAdmin.send_message("me", m)
        except Exception as e:
            print(e)

loop = asyncio.get_event_loop()


@clientM.on(events.NewMessage(chats=("me")))
async def my_event_handlerTelegramMessage_M(event):
    print(event.raw_text)


def init_old_accounts():
    with open("contacts.json", "r") as file:
        dic = json.load(file)
        i = 0
        for key in dic:
            # if i >= 10 and (key != "Lucky Luciano" and key != "Benito" and key != "Hawkeye") :
            if key == "Zaraki" or key == "Oscar" or key == "Manu Manu":
                client = TelegramClient(str(i), api_id, api_hash)
                client.start(phone=dic[key], password="Gusta199621")
            i += 1


async def init_new_accounts():
    with open("phones.txt", "r") as file:
        lines = file.readlines()
        i = 57
        for line in lines:
            print(line)
            client = TelegramClient(str(i), api_id, api_hash)
            await client.start(phone='+13147424492')
            #await client.send_code_request(line)
            #code = input('enter code: ')
            #await client.sign_up(code, first_name=resources[random.randint(0, len(resources))])
            #client.start(phone=line)#, password="Gusta199621")
            i += 1

#loop.create_task(init_new_accounts())

#loop.run_until_complete(my_event())
loop.run_forever()
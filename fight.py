#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging 
import logging.config
from sqlalchemy.log import echo_property
from sqlalchemy.sql.functions import user, random
from sqlalchemy import create_engine, MetaData, Table, Integer, String, Boolean, Column, ForeignKey, text
from sqlalchemy.sql.expression import Update, Insert, Delete, Select
from sqlalchemy.engine.result import ResultProxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, session, sessionmaker
from sqlalchemy.orm.query import Query
from sqlalchemy.orm.session import Session
from telethon import TelegramClient, events, sync, utils, functions, types, errors, connection
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from telethon.tl.functions.messages import GetScheduledHistoryRequest, StartBotRequest, DeleteScheduledMessagesRequest
from telethon.tl.functions.account import GetNotifySettingsRequest, UpdateNotifySettingsRequest
from telethon.tl.types import InputPeerChat, InputPeerUser, InputPeerNotifySettings, User, MessageEntityTextUrl
from telethon.tl.custom.message import Message
from telethon.tl.custom.forward import Forward
from telethon.tl.custom.messagebutton import MessageButton
from telethon.tl.custom.conversation import Conversation
from time import time, perf_counter
import time
from Player import *
import datetime
import random
from datetime import timedelta
import math
import asyncio
import json
import sys
import os.path
import emoji
import webbrowser
import requests
import signal
import pytz

logging.basicConfig(format='[%(levelname)s 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.ERROR)

##################################################################################
#                                        Init variables
##################################################################################
api_id = 1193595
api_hash = '2e588001214d2c25fca7a3abeac619f2'
id_chats = {"gt_chat": 1456226318, "moon_pve": 1408823679, "la_chat": 1233002681, "mem_chat": 1490803916,
            "hs_chat": 1576422147, "yoama_chat": "https://t.me/joinchat/hVuWf9I1nfJhMDQx"}
blacklist_monsters_chats = {"Nobody3": ["chtwrsbot"],"Force2": ["chtwrsbot"],
                            "Luis": ["chtwrsbot"], "Nico1": ["chtwrsbot"], "Fernan20": ["chtwrsbot"],
                            "Jean": ["chtwrsbot"], "Jean4": ["chtwrsbot"], "Masiel": ["chtwrsbot"],
                            "Jean2": ["chtwrsbot"], "Fernan14": ["chtwrsbot"], "Jean1": ["chtwrsbot"],
                            "Yoan": ["chtwrsbot"], "Sylvanna": ["chtwrsbot"],
                            "Force": ["chtwrsbot"],
                            "Yoama": ["chtwrsbot"], "Dani1": ["chtwrsbot"], "Nico": ["chtwrsbot"],
                            "Mask": ["chtwrsbot"], "Legendary": ["chtwrsbot"], "Blaze1": ["chtwrsbot"],
                            "Nico3": ["chtwrsbot"], "Julio5": ["chtwrsbot"],
                            "Julio6": ["chtwrsbot"], "Julio7": ["chtwrsbot"],
                            "Nico2": ["chtwrsbot"], "Yoandris": ["chtwrsbot"], "Julio2": ["chtwrsbot"],
                             "Sleep": ["chtwrsbot"], "Unknown": ["chtwrsbot"], "Kirito": ["chtwrsbot"],
                             "Naruto": ["chtwrsbot"],
                            "Unknown1": ["chtwrsbot"], "Unknown2": ["chtwrsbot"], "Unknown3": ["chtwrsbot"]
                            , "Unknown4": ["chtwrsbot"], "Unknown5": ["chtwrsbot"],"Fernan13": ["chtwrsbot"], "Negan": ["chtwrsbot"],
                            "Fernan17": ["chtwrsbot"], "Negan1":["chtwrsbot"], "Mahalo1": ["chtwrsbot"], "Fernan16": ["chtwrsbot"], "Nobody2": ["chtwrsbot"], "Trinity1": ["chtwrsbot"],
                          "Trinity2": ["chtwrsbot"], "Trinity3": ["chtwrsbot"], "Trinity4": ["chtwrsbot"],
                           "Trinity7": ["chtwrsbot"], "Nobody1": ["chtwrsbot"],
                           "Nobody": ["chtwrsbot"], "Sleep": ["chtwrsbot"]}
forward_chat = "MyFirst96_bot"
personal_chat = "TheRealEirvain"
config_bot = "ScriptCWBot"
skills_code_coll = ["gp", "cll", "se", "prn", "pe", "cft", "et", "br", "lb", "ps", "ew", "pn", "bwm", "dl", "aim"]
seller = "1"
buyer = "2"
guild_masters = ["1"]
num_users = 2
alts = {}
#Julio5, Julio6
#Masiel1, Masiel
alts_service: dict = {"Fernan11": 0, "Smith1": 1, "Unknown": 2, "Fernan22": 3, "Fernan12": 4, "Trinity4": 5, "Trinity3": 6, "Fernan31": 7,
                "Jay1": 8, "Jay8": 9, "Fernan10": 10, "Fernan9": 11, "Fernan1": 12, "Julio5": 13, "Julio6": 14,
                "Jay2": 15, "Unknown7": 16, "Julio7": 17, "VladiY": 18, "Fernan29": 19, "Fernan37": 20, "Unknown4": 21,
                "Trinity2": 22, "Fernan2": 23, "Fernan3": 24, "Fernan14": 25, "Pain3": 26, "Nell": 27
                , "Trinity1": 28, "Fernan39": 29, "Jay4": 30, "Unknown1": 31, "Unknown2": 32, "Masiel1": 33, "Jay9": 34,
                "Fernan21": 35, "Smith": 36, "Fernan32": 37, "Azur": 38, "Unknown6": 38, "Masiel": 39, "Gato": 40,
                "Fernan30": 41, "Ceeb": 42, "Unknow3": 43, "Fernan26": 44, "Fernan17": 45, "Pain10": 46
                , "Unknown3": 47, "Julio2": 48, "Unknow2": 49, "Fernan4": 50, "Fernan5": 51, "Fernan6": 52, "Pain9": 53,
                "Ceeb1": 54, "Pain6": 55, "Unknown5": 56, "Fernan27": 57, "Unknow1": 58, "Fernan28": 59,
                "Pain2": 61, "Fernan33": 62, "Fernan13": 63, "Fernan7": 64, "Fernan8": 65, "Unknow": 66, "Fernan36": 67,
                "Fernan16": 68, "Jay7": 69, "Jay6": 70, "Jay5": 71, "Fernan15": 72, "A2": 73, "Jay3": 74,
                "Lu": 75, "Koki": 76, "Koki1": 77, "Koki3": 78, "Fernan18": 79,  "Fernan19": 80, "Jay10": 81, "A1": 82, "Fernan24": 83,
                "Fernan35": 84, "Fernan34": 85, "Fernan25": 86, "Fernan41": 87, "Fernan40": 88, "Trinity7": 89}
#Alistar solo
#Masiel
usersCharacter: dict = {"Trinity7": 0, "Mahalo1": 1, "Sleep": 2, "Jean4": 3, "Trinity4": 4, "Mask": 5, "Julio2": 6, "Negan1": 7,
                  "Naruto": 8, "Dani1": 9, "Masiel": 9, "Jean": 10, "Yoama": 11, "Fernan14": 12, "Trinity3": 13, "Trinity1": 14,
                  "Jean2": 15, "Fernan16": 16, "Julio7": 17, "Trinity2": 18, "Julio5": 19, "Julio6": 20, "Unknown": 21, "Negan": 22, "Sleep":23}
#intervine script migration
intervine_users = {"Koki2": 0, "Deadpool": 1, "Assasin": 2, "Yo": 3, "Jean1": 4, "Alexis": 5,
                   "FernanI5": 6, "Jean8": 7, "FernanI4": 8, "Jean9": 9, "Auri": 10, "FernanI3": 11, "Jean5": 12,
                   "Tiger": 13, "Erisbel": 14, "FernanI2": 15, "FernanI1": 16, "Jean10": 17, "Jean3": 18, "Smith2": 19,
                   "Naruto1": 20, "Smith3": 21, "Sleep1": 22}
trader = {"Fernan2": "07", "Fernan1": "07", "Fernan3": "07", "Fernan4": "07", "Fernan5": "07"}
usersCW3 = {}
guild_extraction = {}#"Mask": "1674483077"} {"Pain1": "1656339328"}#"Legendary": "1383884691"}
snipping = {}#"Godfather": 1}
alts_group = {"GTO": {"chat": 1001383840079, "users": 2}}
advisers = {"1": 0}
clients = {"alts": alts, "alts_service": alts_service, "usersCharacter": usersCharacter, "usersCW3": usersCW3}
me = {}
meService = {}
meCharacter = {}
id_arrays = {"me": me, "meService": meService, "meCharacter": meCharacter}
stop = False
fightsFromGuild = {"Yoama": False, "Trinity1": False, "Dani1": False, "Force2": False, "Naruto": False, "Sleep": False,
                   "Jean": False, "Trinity2": False, "Mask": False, "Blaze": False, "Jean1": False,
                   "Sylvanna": False, "Force": False, "Legendary2": False, "Fernan14": False,
                   "Masiel": False, "Nico": False, "Legendary": False,
                   "Sleep": False, "Julio4": False, "Julio5": False, "Julio6": False, "Julio7": False,
                   "Julio8": False, "Nico2": False, "Nico3": False, "Fernan16": False, "Unknown": False, "Kirito": False,
                   "Yoan": False, "Unknown1": False, "Unknown2": False, "Unknown3": False,
                   "Unknown4": False, "Unknown5": False,"Fernan13": False, "Negan": False, "Fernan17": False, "Negan1": False,
                   "Jean2": False, "Jean4": False, "Mahalo1": False, "Fernan20": False, "Trinity3": False, "Trinity4": False, "Trinity7": False}

# Click bots
messages = ['🤖 Message bots', '📣 Join chats']  # ,'🖥 Visit sites',
bots = ['Dogecoin_click_bot']  # , 'Zcash_click_bot', 'Litecoin_click_bot', 'BCH_clickbot', 'BitcoinClick_bot']

loop = asyncio.get_event_loop()

file = open("resources.json")
resources = json.load(file)
file.close()

file = open("items.json")
items = json.load(file)
file.close()
print('EEEEEEEEEEEE')
print(os.environ)
DATABASE_URL = os.environ['DATABASE_URL']
engine = create_engine(DATABASE_URL)
metadata = MetaData()

Session = sessionmaker(bind=engine)


async def send_message(client, chat, txt):
    await client.send_message(chat, txt)


def send_message1(client, chat, txt):
    loop.create_task(send_message(client, chat, txt))


try:
    clientAdmin = TelegramClient("Admin", api_id, api_hash)
    clientAdmin.start()
except EOFError as e:
    print("El clientAdmin cerró su sesión")
except errors.AuthKeyDuplicatedError:
    print("El clientAdmin session esta duplicado")

cli_start = """
try:
    if "{0}" not in alts_service or "{1}" == "alts_service":
        client{0} = TelegramClient("{0}", api_id, api_hash)
        client{0}.start()
    {1}["{0}"] = client{0}
except errors.AuthKeyDuplicatedError:
    if "{0}" != "0":
        loop.create_task(send_message(clientAdmin, "RealScript", "The authorization key (session file) was used under two"
         "different IP addresses simultaneously, and can no longer be used. Use the same session exclusively,"
         "or use different sessions: "+ "{0}"))
except EOFError as e:
    loop.create_task(send_message(clientAdmin, "RealScript", "The session was closed by the user: "+ "{0}"))
"""
# Lamazares alt num 1
# Benito alt num 0
time.sleep(60)

for i in range(num_users):
    exec(cli_start.format(i, "alts"))
for i in alts_service:
    exec(cli_start.format(i, "alts_service"))
for i in usersCharacter:
    exec(cli_start.format(i, "usersCharacter"))
for i in usersCW3:
    exec(cli_start.format(i, "usersCW3"))
for i in snipping:
    exec(cli_start.format(i, "snipping"))
for i in intervine_users:
    exec(cli_start.format(i, "intervine_users"))


##################################################################################
#                         Getting info for first time
##################################################################################
async def f():
    print("Script started")
    dic = dict()
    for i in usersCharacter:
        if isinstance(usersCharacter[i], TelegramClient):
            try:
                myself = await usersCharacter[i].get_me()
                meCharacter[i] = myself.id
            except Exception as e:
                print(i)
    for i in alts_service:
        if isinstance(alts_service[i], TelegramClient):
            try:
                myself = await alts_service[i].get_me()
                meService[i] = myself.id
            except Exception as e:
                print(i)
    for i in usersCW3:
        if isinstance(usersCW3[i], TelegramClient):
            myself = await usersCW3[i].get_me()
            meService[i] = myself.id
    for i in snipping:
        if isinstance(snipping[i], TelegramClient):
            try:
                myself = await snipping[i].get_me()
                meService[i] = myself.id
            except errors.AuthKeyDuplicatedError:
                print(i)
    for i in alts:
        if isinstance(alts[i], TelegramClient):
            try:
                myself = await alts[str(i)].get_me()
                # if myself is not None:
                me[str(i)] = myself.id
                #if int(i) > 59:
                #    await alts[str(i)].send_message('chtwrsbot', emoji.emojize(':sports_medal:Me'))
                #    await asyncio.sleep(random.randint(2, 4))
                dic[utils.get_display_name(myself)] = str(myself.phone)
                level = get_config_parameter("Player", myself.id, "level")
                print(utils.get_display_name(myself) + " " + str(myself.phone) + " " + str(i) + " " + str(level))
            except Exception as e:
                print(i)
    # json_file = json.dumps(dic)
    # with open("contacts.json", "w") as file:
    #     file.write(json_file)
    # await clients["alts"][guild_masters[0]].send_file("me", "contacts.json", force_document=True)


async def disconnect():
    print("SIGTERM handler")
    try:
        await clientAdmin.disconnect()
    except errors.AuthKeyDuplicatedError:
        print(i)
    for i in usersCharacter:
        if isinstance(usersCharacter[i], TelegramClient):
            try:
                await usersCharacter[i].disconnect()
            except errors.AuthKeyDuplicatedError:
                print(i)
    for i in alts_service:
        if isinstance(alts_service[i], TelegramClient):
            try:
                await alts_service[i].disconnect()
            except errors.AuthKeyDuplicatedError:
                print(i)
    for i in usersCW3:
        if isinstance(usersCW3[i], TelegramClient):
            await usersCW3[i].disconnect()
    for i in snipping:
        if isinstance(snipping[i], TelegramClient):
            try:
                await snipping[i].disconnect()
            except errors.AuthKeyDuplicatedError:
                print(i)
    for i in alts:
        if isinstance(alts[i], TelegramClient):
            try:
                await alts[str(i)].disconnect()
            except errors.AuthKeyDuplicatedError:
                print(i)
    await asyncio.sleep(35)
    print("Exits")
    sys.exit(0)


def disconnect_sync(s, s1):
    print("Handling SIGTERM")
    loop.create_task(disconnect())


signal.signal(signal.SIGTERM, disconnect_sync)



##################################################################################
#                              General Functions
##################################################################################
def get_name(text):
    i = 2
    if "Congratulations!" in text:
        i = 5
    return text.split('\n')[i].split(' ')[0][1:]


def get_hp(text):
    return text[text.index('Hp:'):].split('\n')[0].split(' ')[1].split('/')[0]


def get_hp_total(text):
    return text[text.index('Hp:'):].split('\n')[0].split(' ')[1].split('/')[1]


def get_curent_stamina(text):
    return text[text.index('Stamina:'):].split('\n')[0].split(' ')[1].split('/')[0]


def get_stamina(text):
    return text[text.index('Stamina:'):].split('\n')[0].split(' ')[1].split('/')[1]


def get_stamina_time(text):
    stamina = "0"
    if "now" not in text and text[text.index('Stamina:'):].split('\n')[0].count(' ') != 1:
        stamina = text[text.index('Stamina:'):].split('\n')[0].split(' ')[2][1:-3]
    elif text[text.index('Stamina:'):].split('\n')[0].count(' ') == 1:
        stamina = "60"
    return stamina


def get_money(text):
    i = 1
    if "Mana" in text:
        i = 2
    return text[text.index("Stamina:"):].split('\n')[i].split(' ')[0][1:]


def get_level(text):
    return text[text.index('Level:'):].split('\n')[0].split(' ')[1]


def save_me(player: Player, my_alts=False):
    session = Session()
    query: Query = session.query(Player).filter(Player.id_telegram == player.id_telegram)
    if query.count() > 0:
        # set quest per level to my alts
        if my_alts:
            if player.level < 20:
                set_config_parameter("Config", player.id_telegram, "quest", "0")
            elif player.level < 46:
                set_config_parameter("Config", player.id_telegram, "quest", "1")
            elif 46 <= player.level < 60:
                set_config_parameter("Config", player.id_telegram, "quest", "2")
            else:
                set_config_parameter("Config", player.id_telegram, "quest", "0")
                set_config_parameter("Config", player.id_telegram, "prefered_time", "2")

        query.update({Player.name: player.name, Player.stamina_reg_time: player.stamina_reg_time,
                      Player.stamina: player.stamina, Player.total_stamina: player.total_stamina,
                      Player.health: player.health, Player.total_health: player.total_health,
                      Player.level: player.level, Player.money: player.money})
    else:
        player.config = Config(False, False, 200, 2, 0, 3, 2, "Thread,Powder,Magic stone,Pelt,Coke,Leather,Charcoal",
                               True, 10)
        player.permission = Permission(True, True, True, True, True, True, True, True)
        session.add(player)
    session.commit()
    session.close()


def load_player(telegram_id):
    session = Session()
    result = session.query(Player).filter(Player.id_telegram == telegram_id).first()
    session.close()
    return result


def get_cw_time():
    return datetime.time((datetime.datetime.utcnow().hour + 1) % 8, datetime.datetime.utcnow().minute, 0)


##################################################################################
#                                     Test Manage
##################################################################################
def set_config(config: Config, telegram_id):
    session = Session()
    p: Player = session.query(Player).filter(Player.id_telegram == telegram_id).first()
    query: Query = session.query(Config).filter(Config.id_config == p.config_id)
    if query.count() > 0:
        query.update({Config.monsters: config.monsters, Config.monsters_on: config.monsters_on,
                      Config.min_hp: config.min_hp, Config.cant_monsters: config.cant_monsters,
                      Config.quest: config.quest, Config.stamina_step: config.stamina_step,
                      Config.prefered_time: config.prefered_time, Config.resources_for_hide: config.resources_for_hide,
                      Config.trader_on: config.trader_on, Config.trader_resource: config.trader_resource})
    else:
        player = Player(telegram_id, None, None, None, None, None, None, None, None, None, config,
                        Permission(False, False, False, False, False, False, False, False))
        session.add(player)
    session.commit()
    session.close()


def set_permission(permission: Permission, telegram_id):
    session = Session()
    p: Player = session.query(Player).filter(Player.id_telegram == telegram_id).first()
    query: Query = session.query(Permission).filter(Permission.id_permission == p.permission_id)
    if query.count() > 0:
        query.update({Permission.quest: permission.quest, Permission.arena: permission.arena,
                      Permission.crafting: permission.crafting, Permission.intervine: permission.intervine,
                      Permission.orders: permission.orders, Permission.pet: permission.pet,
                      Permission.spend_hide: permission.spend_hide, Permission.withdraw: permission.withdraw})
    session.commit()
    session.close()


def set_permission_guild(permission: PermissionGuilds, telegram_id):
    session = Session()
    query: Query = session.query(PermissionGuilds).filter(PermissionGuilds.id_telegram == telegram_id)
    if query.count() > 0:
        query.update({PermissionGuilds.alch: permission.alch, PermissionGuilds.misc: permission.misc,
                      PermissionGuilds.rec: permission.rec, PermissionGuilds.parts: permission.parts,
                      PermissionGuilds.others: permission.others, PermissionGuilds.invite: permission.invite})
    else:
        permission_guild = PermissionGuilds(telegram_id, permission.alch, permission.misc, permission.rec,
                                            permission.parts, permission.others, permission.invite)
        session.add(permission_guild)
    session.commit()
    session.close()


def set_config_parameter(name, telegram_id, atribute, value):
    task = """session = Session()
if "{0}" == "Player" or "{0}" == "PermissionGuilds":
    session.query({0}).filter({0}.id_telegram == telegram_id).first().{1} = {2}
elif "{0}" == "Config" or "{0}" == "Permission":
    r = session.query({0}).join(Player).filter(Player.id_telegram == telegram_id).first().{1} = {2}
session.commit()
session.close()
"""
    if isinstance(value, str):
        task = task.replace("{2}", "'{2}'")
    exec(task.format(name, atribute, value))


def get_config(telegram_id):
    session = Session()
    result = session.query(Config).join(Player).filter(Player.id_telegram == telegram_id).first()
    session.close()
    return result


def get_permission(telegram_id):
    session = Session()
    result = session.query(Permission).join(Player).filter(Player.id_telegram == telegram_id).first()
    session.close()
    return result


def get_permission_guild(telegram_id):
    session = Session()
    result = session.query(PermissionGuilds).filter(PermissionGuilds.id_telegram == telegram_id).first()
    session.close()
    return result


def get_config_parameter(name, telegram_id, atribute):
    result = ""
    _locals = locals()
    task = """session = Session()
if "{0}" == "Player" or "{0}" == "PermissionGuilds":
    result = session.query({0}).filter({0}.id_telegram == telegram_id).first().{1}
elif "{0}" == "Config" or "{0}" == "Permission":
    result = session.query({0}).join(Player).filter(Player.id_telegram == telegram_id).first().{1}
session.close()
"""
    exec(task.format(name, atribute), globals(), _locals)
    return _locals["result"]


async def existThisScheduledMessage(clients_str, user, text_message, chat):
    messages = await clients[clients_str][user](GetScheduledHistoryRequest(peer=chat, hash=0))
    for it in messages.messages:
        it: Message
        date_message = it.date.replace(tzinfo=None)
        if text_message in it.message:
            if date_message < datetime.datetime.now():
                await clients[clients_str][user](DeleteScheduledMessagesRequest(
                    peer=chat,
                    id=[it.id]  # !imporant you need to pass a list here
                ))
                return False
            return True
        elif date_message < datetime.datetime.now():
            await clients[clients_str][user](DeleteScheduledMessagesRequest(
                peer=chat,
                id=[it.id]  # !imporant you need to pass a list here
            ))
    return False


async def deleteScheduledMessage(chat, arr):
    for i in clients[arr]:
        try:
            print(i)
            messages = await clients[arr][i](GetScheduledHistoryRequest(peer=chat, hash=0))
            for it in messages.messages:
                await clients[arr][i](DeleteScheduledMessagesRequest(
                    peer=chat,
                    id=[it.id]  # !imporant you need to pass a list here
                ))
            await clients[arr][i].send_message('chtwrsbot', emoji.emojize(':sports_medal:Me'))
            await asyncio.sleep(random.randint(1, 2))
        except Exception as e:
            print(e)





##################################################################################
#                               Settings
##################################################################################
async def setupScript(clients_str, user, me_array, txt1):
    myself = id_arrays[me_array][user]
    global stop
    if '/send_message_script' in txt1:
        text_message = "Hola, soy RealScript. Esta es mi nueva cuenta, la anterior esta eliminada. Comuniquense inmediatamente por aki para restablecer los servicios. Dentro de 10 dias quitaré los servicios. Saludos"
        for i in usersCharacter:
            if isinstance(usersCharacter[i], TelegramClient):
                try:
                    myself = await usersCharacter[i].get_me()
                    meCharacter[i] = myself.id
                    await alts[str(1)].send_message(myself.username, text_message)
                    await asyncio.sleep(random.randint(1, 2))
                except Exception as e:
                    print(i)
                    print(e)
        for i in alts_service:
            if isinstance(alts_service[i], TelegramClient):
                try:
                    myself = await alts_service[i].get_me()
                    meService[i] = myself.id
                    await alts[str(1)].send_message(myself.username, text_message)
                    await asyncio.sleep(random.randint(1, 2))
                except Exception as e:
                    print(i)
                    print(e)
    if '/hp' in txt1:
        set_config_parameter("Config", myself, "min_hp", int(txt1.split('_')[1]))
        await clients[clients_str][user].send_message("ScriptCWBot",
                                                      "Su umbral de salud para capturar monstruos ahora es de " + str(
                                                          txt1.split('_')[1]))
    if '/do_arena' in txt1:
        await clients[clients_str][user].send_message("chtwrsbot", '🗺Quests')
    elif '/quest_time' in txt1:
        dic = {"mañana": "0", "dia": "1", "tarde": "2", "noche": "3", "normal": "4"}
        set_config_parameter("Config", myself, "prefered_time", dic[txt1.split('_')[2].lower()])
        await clients[clients_str][user].send_message('ScriptCWBot',
                                                      "Se ha definido como tipo de quest: " + txt1.split('_')[2])
    elif '/quest' in txt1:
        dic = {"Forest": "0", "Swamp": "1", "Valley": "2", "Foray": "3"}
        set_config_parameter("Config", myself, "quest", dic[txt1.split('_')[1].capitalize()])
        await clients[clients_str][user].send_message('ScriptCWBot', "Se ha definido hacer " + txt1.split('_')[1])
    elif '/restart' in txt1:
        set_config(Config(False, False, 200, 2, 0, 4, 2,
                          "Thread,Powder,Magic stone,Pelt,Coke,Leather,Charcoal", True, "10"), myself)
        await clients[clients_str][user].send_message('ScriptCWBot', "Se ha restablecido los valores predeterminados")
    elif '/jump' in txt1:
        set_config_parameter("Config", myself, "stamina_step", int(txt1.split('_')[1]))
        await clients[clients_str][user].send_message('ScriptCWBot',
                                                      "Se ha establecido " + str(
                                                          txt1.split('_')[1]) + " como salto de estamina")
    elif '/values' in txt1:
        await clients[clients_str][user].send_message('ScriptCWBot', get_config(myself))
    elif '/me_' in txt1:
        await clients[clients_str][user].send_message('ScriptCWBot', load_player(myself))
    elif '/arenas' in txt1:
        arena = get_config_parameter("Player", myself, "cant_arenas")
        await clients[clients_str][user].send_message("ScriptCWBot", "El número de arenas por hacer es: " + arena)
    elif '/c_arenas' in txt1:
        set_config_parameter("Player", myself, "cant_arenas", int(txt1.split('_')[1]))
        await clients[clients_str][user].send_message("ScriptCWBot", "Se ha definido " + str(
            txt1.split('_')[2]) + " como cantidad de arenas por hacer")
    elif '/start_send' in txt1:
        stop = False
    elif '/stop_send' in txt1:
        stop = True
    elif "/c_" in txt1 and get_config_parameter("Permission", id_arrays[me_array][user], "crafting"):
        for i in range(5):
            await asyncio.sleep(random.randint(7, 10))
            await clients[clients_str][user].send_message("chtwrsbot", txt1)
    elif "/set_arena" in txt1 and "Smith" in user:
        p = txt1.split(" ")[1]
        if p == "True" or p == "true":
            set_config_parameter("Permission", myself, "arena", True)
            await clients[clients_str][user].send_message("ScriptCWBot", "Se ha encendido la funcionalidad de las arenas")
        elif p == "False" or p == "false":
            set_config_parameter("Permission", myself, "arena", False)
            await clients[clients_str][user].send_message("ScriptCWBot", "Se ha apagado la funcionalidad de las arenas")
        else:
            await clients[clients_str][user].send_message("ScriptCWBot", "El comando no es correcto")
    elif "/fernan_orders" in txt1 and user == "Fernan1":
        for c in alts_service.keys():
            try:
                if "Fernan" in c:
                    await alts_service[c].send_message("botniatobot", "/order")
                    await asyncio.sleep(random.randint(3, 6))
            except Exception as e:
                continue
        await clients[clients_str][user].send_message('ScriptCWBot', "/fernan_orders",
                                                      schedule=timedelta(minutes=480))
    elif "/go_attack" in txt1 and user == "Fernan1":
        castle_order = txt1.split(" ")[1]
        for c in alts_service.keys():
            try:
                if "Fernan" in c:
                    await alts_service[c].send_message('chtwrsbot', "⚔️Attack")
                    await asyncio.sleep(random.randint(2, 3))
                    await alts_service[c].send_message("chtwrsbot", castle_order)
                    await asyncio.sleep(random.randint(3, 6))
            except Exception as e:
                continue
        await clients[clients_str][user].send_message('ScriptCWBot', "/fernan_castle_orders",
                                                      schedule=timedelta(minutes=480))
    elif "/command" in txt1 and user == "Fernan1":
        command = txt1.split(" ")[1]
        for c in alts_service.keys():
            try:
                if "Fernan" in c:
                    await alts_service[c].send_message("chtwrsbot", command)
                    await asyncio.sleep(random.randint(3, 6))
            except Exception as e:
                continue
        await clients[clients_str][user].send_message('ScriptCWBot', "/fernan_castle_orders",
                                                      schedule=timedelta(minutes=480))
    elif "/orders" in txt1 and user == "Jay7":
        for c in alts_service.keys():
            try:
                if "Jay" in c: #  and "Jay2" not in c and "Jay3" not in c
                    await alts_service[c].send_message("chtwrsbot", "/g_def")
                    await asyncio.sleep(random.randint(3, 6))
            except Exception as e:
                continue
        await clients[clients_str][user].send_message('ScriptCWBot', "/orders",
                                                      schedule=timedelta(minutes=480))
    elif "/orders" in txt1 and user == "Koki":
        for c in alts_service.keys():
            try:
                if "Koki" in c and "Koki1" not in c:
                    await alts_service[c].send_message("chtwrsbot", "/g_def")
                    await asyncio.sleep(random.randint(3, 6))
            except Exception as e:
                continue
        await clients[clients_str][user].send_message('ScriptCWBot', "/orders",
                                                      schedule=timedelta(minutes=480))
    elif '/hide' in txt1:
        rec = ""
        if len(txt1.split('_')) != 0:
            rec = ",".join(txt1.split('_')[1:])
        set_config_parameter("Config", myself, "resources_for_hide", rec)
        await clients[clients_str][user].send_message('ScriptCWBot',
                                                      "Se han establecido " + rec + " como recursos a gastar")
    elif '/help' in txt1:
        ayuda = """Pulse /quest_Forest para definir quest a realizar (Forest, Swamp, Valley, Foray)
Pulse /quest_time_noche para definir quest preferido (mañana, dia,tarde, noche o normal)
Pulse /jump_2 para establecer un salto de estamina
Pulse /hide_Thread_Stick_Powder para establecer productos a ocultar(Thread_Stick_Powder)
Deje /stop_script como último mensaje en este bot para apagar el script
Pulse /restart para restablecer valores"""
        await clients[clients_str][user].send_message('ScriptCWBot', ayuda)
    if user in guild_masters:
        if "Defend" in txt1:
            scheduled = await existThisScheduledMessage(clients_str, user, "Defend", config_bot)
            if not scheduled:
                schedule_time: datetime = (datetime.datetime.utcnow() + timedelta(hours=8)).\
                    replace(minute=random.randint(47, 52))
                await clients[clients_str][user].send_message(config_bot, txt1, schedule=schedule_time)
        elif "/t_01" in txt1:
            scheduled = await existThisScheduledMessage(clients_str, user, "/t_01", config_bot)
            if not scheduled:
                schedule_time: datetime = (datetime.datetime.utcnow() + timedelta(hours=8)).\
                    replace(minute=random.randint(36, 42))
                await clients[clients_str][user].send_message(config_bot, txt1, schedule=schedule_time)
        elif "/sg_" in txt1:
            scheduled = await existThisScheduledMessage(clients_str, user, "/sg_", config_bot)
            if not scheduled:
                await clients[clients_str][user].send_message(config_bot, txt1,
                                                              schedule=timedelta(hours=24,
                                                                                 minutes=random.randint(4, 7)))
        elif "resetArena" in txt1:
            scheduled = await existThisScheduledMessage(clients_str, user, "resetArena", config_bot)
            if not scheduled:
                for i in alts_service:
                    try:
                        print(i)
                        set_config_parameter("Player", id_arrays["meService"].get(i), "cant_arenas", 5)
                    except Exception as e:
                        continue
                for i in alts:
                    try:
                        set_config_parameter("Player", id_arrays[me_array].get(str(i)), "cant_arenas", 5)
                    except Exception as e:
                        continue
                await clients[clients_str][user].send_message(config_bot, txt1, schedule=timedelta(hours=24))
        if ("/g_all " in txt1):
            loop.create_task(sendAllAlt(txt1.split(" ")[1]))
        elif "/delete " in txt1:
            loop.create_task(deleteScheduledMessage(forward_chat, txt1.split(" ")[1]))
        elif ("/g_services " in txt1):
            for i in alts_service:
                loop.create_task(handlerCommands("alts_service", i, txt1.split(" ")[1], "meService"))
        elif ("/g_invite " in txt1):
            start = txt1.split(" ")[1]
            end = ""
            if (txt1.count(" ") == 2):
                end = txt1.split(" ")[2]
            else:
                end = start + 1
            for i in range(int(start), int(end)):
                try:
                    if i > 10 or i == 2:
                        ids = me[str(i)]
                        await clients[clients_str][user].send_message("chtwrsbot", "/g_invite " + str(ids))
                        await asyncio.sleep(random.randint(15, 25))
                except Exception as e:
                    continue
        elif ("/g_order " in txt1 or "/g_deposit " in txt1):
            start = ""
            end = ""
            if ("/g_deposit " in txt1):
                order = txt1.split(")")[0]
                start = int(txt1.split(" ")[-2])
                end = int(txt1.split(" ")[-1])
            else:
                order = txt1.split(" ")[1:-2][0]
                start = int(txt1.split(" ")[2])
                if (txt1.count(" ") == 3):
                    end = int(txt1.split(" ")[3])
                else:
                    end = start + 1
            for i in range(start, end):
                try:
                    if i <= 10 and i != 2 and ("Crafting " in txt1 or "/g_deposit " in txt1):
                        continue
                    else:
                        loop.create_task(handlerCommands(clients_str, str(i), order, me_array))
                        await asyncio.sleep(random.randint(2, 5))
                except Exception as e:
                    continue
        elif ("/g_compare" in txt1):
            l = await clients[clients_str][user].get_messages(config_bot, limit=3)
            newMessage: str = l[1].message.split("\n")
            oldMessage = l[2].message.split("\n")
            cont = 0
            order = "/g_withdraw"
            for i in range(1, len(newMessage)):
                if newMessage[i].startswith(emoji.emojize(':jigsaw:')):
                    newMessage[i] = newMessage[i][1:]
                item = " ".join(newMessage[i].split(" ")[1:-2])
                cant = newMessage[i].split(" ")[-1]
                if (item in l[2].message):
                    for h in range(1, len(oldMessage)):
                        if oldMessage[i].startswith(emoji.emojize(':jigsaw:')):
                            oldMessage[i] = oldMessage[i][1:]
                        itemA = " ".join(oldMessage[h].split(" ")[1:-2])
                        if (itemA == item):
                            dif = int(cant) - int(oldMessage[h].split(" ")[-1])
                            if (dif > 0):
                                cont += 1
                                order += " " + newMessage[i].split(" ")[0] + " " + str(dif)
                            break
                else:
                    cont += 1
                    order += " " + newMessage[i].split(" ")[0] + " " + str(cant)
                if (cont == 9 or i == len(newMessage) - 1):
                    cont = 0
                    await asyncio.sleep(random.randint(10, 15))
                    await clients[clients_str][user].send_message("chtwrsbot", order)
                    order = "/g_withdraw"
        elif "/set_permission" in txt1:
            p = txt1.split(" ")[2].split(",")
            telegram_id = int(txt1.split(" ")[1])
            set_permission(Permission(False, False, False, False, False, False, False, False), telegram_id)
            for i in p:
                set_config_parameter("Permission", telegram_id, i, True)
        elif "/disconnect" in txt1:
            for i in usersCharacter:
                if isinstance(usersCharacter[i], TelegramClient):
                    try:
                        await usersCharacter[i].disconnect()
                    except errors.AuthKeyDuplicatedError:
                        print(i)
            for i in alts_service:
                if isinstance(alts_service[i], TelegramClient):
                    try:
                        await alts_service[i].disconnect()
                    except errors.AuthKeyDuplicatedError:
                        print(i)
            for i in usersCW3:
                if isinstance(usersCW3[i], TelegramClient):
                    await usersCW3[i].disconnect()
            for i in snipping:
                if isinstance(snipping[i], TelegramClient):
                    try:
                        await snipping[i].disconnect()
                    except errors.AuthKeyDuplicatedError:
                        print(i)
            for i in alts:
                if isinstance(alts[i], TelegramClient):
                    try:
                        await alts[str(i)].disconnect()
                    except errors.AuthKeyDuplicatedError:
                        print(i)
        elif "/get_phone" in txt1:
            u = txt1.split(" ")[1]
            if u in alts_service:
                myself = await alts_service[u].get_me()
                await clients[clients_str][user].send_message('ScriptCWBot', str(myself.phone) + " " + u)
            elif u in intervine_users:
                myself = await intervine_users[u].get_me()
                await clients[clients_str][user].send_message('ScriptCWBot', str(myself.phone) + " " + u)
            elif u in usersCharacter:
                myself = await usersCharacter[u].get_me()
                await clients[clients_str][user].send_message('ScriptCWBot', str(myself.phone) + " " + u)
            elif u in alts:
                myself = await alts[u].get_me()
                await clients[clients_str][user].send_message('ScriptCWBot', str(myself.phone) + " " + u)
        elif "/get_cw_names" in txt1:
            for i in usersCharacter:
                if isinstance(usersCharacter[i], TelegramClient):
                    try:
                        info = load_player(id_arrays["meCharacter"][i])
                        await clients[clients_str][user].send_message('ScriptCWBot', i + " " + info.name)
                    except errors.AuthKeyDuplicatedError:
                        continue
            for i in alts_service:
                try:
                    info = load_player(id_arrays["meService"][i])
                    await clients[clients_str][user].send_message('ScriptCWBot', i + " " + info.name)
                except Exception as e:
                    continue
        elif "/get_alias" in txt1:
            u = txt1.split(" ")[1]
            if u in alts_service:
                myself = await alts_service[u].get_me()
                await clients[clients_str][user].send_message('ScriptCWBot', "@" + str(myself.username) + " " + u)
            elif u in intervine_users:
                myself = await intervine_users[u].get_me()
                await clients[clients_str][user].send_message('ScriptCWBot', "@" + str(myself.username) + " " + u)
            elif u in usersCharacter:
                myself = await usersCharacter[u].get_me()
                await clients[clients_str][user].send_message('ScriptCWBot', "@" + str(myself.username) + " " + u)
            elif u in alts:
                myself = await alts[u].get_me()
                await clients[clients_str][user].send_message('ScriptCWBot', "@" + str(myself.username) + " " + u)
    if (user == buyer):
        if ("/lots" in txt1):
            i = txt1.split("_")[1]
            if os.path.exists("lots_" + str(i) + ".txt"):
                with open("lots_" + str(i) + ".txt", 'r') as fd:
                    arr = fd.readlines()
                for it in arr:
                    await asyncio.sleep(random.randint(15, 20))
                    await clients[clients_str][user].send_message("chtwrsbot", it)
    if (user in guild_extraction) and "/set_guild_permission" in txt1:
        p = txt1.split(" ")[2].split(",")
        telegram_id = int(txt1.split(" ")[1])
        set_permission_guild(PermissionGuilds(telegram_id, False, False, False, False, False, False), telegram_id)
        for i in p:
            if i == "res":
                set_config_parameter("PermissionGuilds", telegram_id, "rec", True)
            else:
                set_config_parameter("PermissionGuilds", telegram_id, i, True)


##################################################################################
#                             Questing
##################################################################################
async def questingPriority(user, i, me_array):
    ret = timedelta(days=-1)
    estamina_reg_time = 0
    cw_time: timedelta = timedelta(hours=get_cw_time().hour, minutes=get_cw_time().minute)
    if get_config_parameter("Player", id_arrays[me_array][user], "stamina_reg_time") == 60:  # estamina rellena
        estamina_reg_time = timedelta(hours=0)
    else:
        estamina_reg_time = timedelta(
            hours=get_config_parameter("Player", id_arrays[me_array][user], "total_stamina") - 1) - timedelta(
            hours=get_config_parameter("Player", id_arrays[me_array][user], "stamina")) \
                            + timedelta(
            minutes=get_config_parameter("Player", id_arrays[me_array][user], "stamina_reg_time") == 60)
    it = 0
    zero_hour = timedelta(hours=8) - cw_time
    start_hour = 0
    if i == 0:  # mañana
        it = zero_hour + timedelta(minutes=14)
    elif i == 1:  # dia
        start_hour = 2
    elif i == 2:  # tarde
        start_hour = 4
    else:  # noche
        start_hour = 6
    if it == 0:
        if cw_time < timedelta(hours=start_hour):
            it = timedelta(hours=start_hour) - cw_time
        else:
            it = zero_hour + timedelta(hours=start_hour)
    if it <= estamina_reg_time and get_cw_time().hour != start_hour and get_cw_time().hour != (start_hour + 1):
    #if it <= estamina_reg_time and \
    #        (cw_time < timedelta(hours=start_hour, minutes=3) or cw_time > timedelta(hours=start_hour, minutes=6)
    #         and (get_cw_time().minute != 14)):
        ret = it
    return ret


async def cw_event(clients_str, user, me_array, event):
    l = await clients[clients_str][user].get_messages("chtwrsbot", limit=2)
    r = await clients[clients_str][user].get_messages(config_bot, limit=1)
    is_stop = False
    if len(r) > 0:
        is_stop = r[0].message == "/stop_script"
    # Handle the level up
    if event.sticker is not None and user.isnumeric():
        await asyncio.sleep(random.randint(4, 7))
        await clients[clients_str][user].send_message("chtwrsbot", "/level_up")
    elif 'It is time for you to decide upon your destiny' in event.raw_text and user.isnumeric():
        if 77 < int(user) < 97:
            await asyncio.sleep(random.randint(4, 7))
            await clients[clients_str][user].send_message("chtwrsbot", "⚔Esquire🛡")
        else:
            await asyncio.sleep(random.randint(4, 7))
            await clients[clients_str][user].send_message("chtwrsbot", "⚒Master📦")
        await asyncio.sleep(random.randint(4, 7))
        await clients[clients_str][user].send_message("chtwrsbot", "/level_up")
    elif "you're done with your apprenticeship, but now" in event.raw_text and user.isnumeric():
        if 77 < int(user) < 97:
            await asyncio.sleep(random.randint(4, 7))
            await clients[clients_str][user].send_message("chtwrsbot", "🏹Ranger")
        else:
            await asyncio.sleep(random.randint(4, 7))
            await clients[clients_str][user].send_message("chtwrsbot", "📦Collector")
        await asyncio.sleep(random.randint(4, 7))
        await clients[clients_str][user].send_message("chtwrsbot", "/level_up")
    elif 'Learned skills:' in event.raw_text and user.isnumeric():
        for code in skills_code_coll:
            if "_" + code in event.raw_text:
                if (code == "lb" and int(
                        event.raw_text[event.raw_text.find("Labeling"):].split("\n")[0].split(" ")[1]) > 10):
                    continue
                elif (code == "br" and int(
                        event.raw_text[event.raw_text.find("Broker"):].split("\n")[0].split(" ")[1]) > 6):
                    continue
                await asyncio.sleep(random.randint(5, 7))
                await clients[clients_str][user].send_message("chtwrsbot", "/learn_" + code)
    # Getting information and setting questing and arena
    elif 'Battle of the' in event.raw_text and not is_stop:
        text = event.raw_text
        save_me(Player(id_arrays[me_array][user], get_name(text), int(get_level(text)), int(get_hp(text)),
                       int(get_hp_total(text)),
                       int(get_curent_stamina(text)), int(get_stamina(text)), int(get_stamina_time(text)),
                       int(get_money(text)), 5,
                       get_config(id_arrays[me_array][user]), get_permission(id_arrays[me_array][user])),
                user.isnumeric())
        if get_config_parameter("Permission", id_arrays[me_array][user], "quest"):
            priority = get_config_parameter("Config", id_arrays[me_array][user], "prefered_time")
            arena_time = 10
            time = timedelta(days=-1)
            delay = 7
            start = random.randint(1, 2)
            night = get_cw_time().hour >= 6
            # start time for questing
            quest_start_time = timedelta(hours=get_cw_time().hour, minutes=get_cw_time().minute)
            me_schedule = await existThisScheduledMessage(clients_str, user, emoji.emojize(':sports_medal:Me'),
                                                          forward_chat)
            if not me_schedule and user not in alts_group:
                if night:
                    delay = 9
                if priority != 4:
                    time = await questingPriority(user, priority, me_array)
                if time.days != -1:
                    await clients[clients_str][user].send_message(forward_chat, emoji.emojize(':sports_medal:Me'),
                                                                  schedule=time + timedelta(
                                                                      minutes=random.randint(3, 5)))
                    #delayMe = (time + timedelta(minutes=random.randint(7, 8))).total_seconds()
                    #loop.call_later(delayMe, send_message1(clients[clients_str][user], "chtwrsbot",
                    #                                   emoji.emojize(':sports_medal:Me')))
                else:
                    cant_quest = int(get_curent_stamina(event.raw_text))
                    if get_config_parameter("Config", id_arrays[me_array][user], "quest") == 3:
                        cant_quest = cant_quest // 2
                    for i in range(cant_quest):
                        time_quest = quest_start_time + timedelta(minutes=start + delay * i)
                        seconds_time_quest = time_quest.seconds
                        minutes_to_battle = (seconds_time_quest // 3600) == 7 \
                                            and ((seconds_time_quest // 60) % 60) >= 30
                        if user == "VladiY":
                            minutes_to_battle = (seconds_time_quest // 3600) == 7
                            if minutes_to_battle:
                                clientAdmin.send_message("RealScript", str((seconds_time_quest // 3600)))
                        if priority != 4:  # have time priority
                            if minutes_to_battle:
                                break
                            if (seconds_time_quest // 3600) - (quest_start_time.seconds // 3600) >= 2:
                                break
                        elif minutes_to_battle:
                            delay = 7
                            start = 60 - (((seconds_time_quest // 60) % 60) + start) + random.randint(18, 25)
                        #if user != "11":
                        await clients[clients_str][user].send_message(forward_chat, '🗺Quests',
                                                                          schedule=timedelta(minutes=start + delay * i))
                        #else:
                        #ts = timedelta(minutes=start + delay * i).total_seconds()
                        #loop.call_later(ts, send_message1, clients[clients_str][user], "chtwrsbot",
                        #                                     '🗺Quests')
                        arena_time = start + delay * i + 10
                    if get_config_parameter("Permission", id_arrays[me_array][user], "arena") and \
                            int(get_level(event.raw_text)) >= 5 and \
                            get_config_parameter("Player", id_arrays[me_array][user], "cant_arenas") != 0:
                        if get_cw_time().hour <= 4:
                            #if user != "11":
                            await clients[clients_str][user].send_message(forward_chat, '🗺Quests',
                                                                              schedule=timedelta(
                                                                                  minutes=arena_time +
                                                                                          (random.randint(3, 12))))
                            #else:
                            #    ts = timedelta(minutes=arena_time + (random.randint(3, 12))).total_seconds()
                            #    loop.call_later((arena_time + (random.randint(3, 12))) * 60, send_message1, clients[clients_str][user], "chtwrsbot",
                            #                                         '🗺Quests')
                        else:
                            time_to_battle = timedelta(hours=8, minutes=0) - quest_start_time
                            #if user != "11":
                            await clients[clients_str][user].send_message(forward_chat, '🗺Quests',
                                                                              schedule=timedelta(
                                                                                  minutes=60 + (
                                                                                      random.randint(3, 12))) +
                                                                                       time_to_battle)
                            #else:
                            #    ts = (timedelta(minutes=60 + (random.randint(3, 12))) + time_to_battle).total_seconds()
                            #    loop.call_later(ts, send_message1, clients[clients_str][user], "chtwrsbot",
                            #                                         '🗺Quests')

                    if user == "Kururo":
                        await clients[clients_str][user].send_message(forward_chat, '/myshop_open',
                                                                      schedule=timedelta(
                                                                          minutes=start + delay * cant_quest))
                        # await clients[clients_str][user].send_message(forward_chat, '/ws_3aWH3',
                        #                                              schedule=timedelta(
                        #                                                  minutes=(start + delay * cant_quest) + 1))
                    await clients[clients_str][user].send_message(forward_chat, emoji.emojize(':sports_medal:Me'),
                                                                  schedule=timedelta(
                                                                      hours=get_config_parameter("Config",
                                                                                                 id_arrays[me_array][
                                                                                                     user],
                                                                                                 "stamina_step"),
                                                                      minutes=random.randint(10, 12)))
                    #delayMe = (timedelta(hours=get_config_parameter("Config",id_arrays[me_array][user],
                    #                                                                         "stamina_step"),
                    #                                              minutes=random.randint(14, 16))).total_seconds()
                    #loop.call_later(delayMe, send_message1(clients[clients_str][user], "chtwrsbot",
                    #                                   emoji.emojize(':sports_medal:Me')))
    # Questing
    elif 'Many things can happen in the forest.' in event.raw_text and not is_stop:
        messages = await clients[clients_str][user](GetScheduledHistoryRequest(peer=forward_chat, hash=0))
        m = await clients[clients_str][user].get_messages(config_bot, limit=1)
        arena = False
        if len(m) > 0:
            if "/do_arena" in m[0].message:
                arena = True
                n = 1
        if ((len(messages.messages) == 1 and messages.messages[0].message == emoji.emojize(':sports_medal:Me')
             or arena) and
            get_config_parameter("Permission", id_arrays[me_array][user], "arena")) and get_cw_time().hour < 6 \
                and get_config_parameter("Player", id_arrays[me_array][user], "level") >= 5 and \
                get_config_parameter("Player", id_arrays[me_array][user], "cant_arenas") != 0:
            btn = 2
            await asyncio.sleep(random.randint(15, 25))
            await clients[clients_str][user].send_message('chtwrsbot', emoji.emojize(':castle:Castle'))
            await asyncio.sleep(random.randint(10, 15))
            await clients[clients_str][user].send_message('chtwrsbot', "⚖Exchange")
            await asyncio.sleep(random.randint(100, 120))
            await clients[clients_str][user].send_message('chtwrsbot', "/t_01")
            await asyncio.sleep(random.randint(50, 60))
            if get_config_parameter("Player", id_arrays[me_array][user], "level") >= 20:
                await event.click(1, 1)
            else:
                await event.click(btn)
        elif get_config_parameter("Permission", id_arrays[me_array][user], "quest"):
            await asyncio.sleep(random.randint(10, 12))
            quest_click = get_config_parameter("Config", id_arrays[me_array][user], "quest")
            if "Fernan" in user or "A1" == user or "A2" == user:
                quest_click = random.randint(0, 2)
            await event.click(quest_click)
    # Arena
    elif '📯Welcome to Arena!' in event.raw_text and \
            get_config_parameter("Permission", id_arrays[me_array][user], "arena") and get_cw_time().hour < 6 \
            and get_config_parameter("Player", id_arrays[me_array][user], "level") >= 5 and \
            get_config_parameter("Player", id_arrays[me_array][user], "cant_arenas") != 0 and not is_stop:
        text = event.raw_text
        to_do = 5 - int(text.split('/5')[0][-1])
        set_config_parameter("Player", id_arrays[me_array][user], "cant_arenas", str(to_do))
        start = 2
        delay = random.randint(6, 7)
        for i in range(to_do):
            try:
                await clients[clients_str][user].send_message(forward_chat, '▶️Fast fight',
                                                              schedule=timedelta(minutes=start + delay * i))
            except errors.YouBlockedUserError:
                print("You block the bot", str(user))
        delay_all = start + delay * (to_do) + random.randint(1, 2)
        # await clients[clients_str][user].send_message(forward_chat, "⚖Exchange", schedule=timedelta(minutes=delay_all))
        if("Koki" not in user):
            await clients[clients_str][user].send_message(forward_chat, '/stock',
                                                      schedule=timedelta(minutes=delay_all))
    # Manage stamina restored
    elif 'Stamina restored' in event.raw_text and get_config_parameter("Permission", id_arrays[me_array][user],
                                                                       "quest") and not is_stop:
        await asyncio.sleep(random.randint(180, 200))
        await clients[clients_str][user].send_message('chtwrsbot', emoji.emojize(':sports_medal:Me'))
    # Catch go
    elif ('You were strolling around on your horse when you noticed' in event.raw_text and
          get_config_parameter("Permission", id_arrays[me_array][user], "intervine")):
        number = 1
        print(user)
        if user.isnumeric():
            print(user, "n")
            number = 0 #random.randint(0, 1)
        if number == 1:
            print(user, "no")
            await asyncio.sleep(random.randint(5, 60))
            await event.click(0)
    elif 'You met some hostile creatures' in event.raw_text and "Force" not in user:
        print(user)
        if id_arrays[me_array][user] == 1356228488:
            await event.forward_to(1162259006)
        elif "Red" in user and not (id_arrays[me_array][user] == 1760990483):
            await event.forward_to(id_chats["hs_chat"])
        elif "Yoama" in user:
            await event.forward_to(id_chats["yoama_chat"])
        elif "Unknown" in user:
            print("entro")
            await event.forward_to("https://t.me/joinchat/H20zrJQVg0E1YmVh")
            if "Unknown" == user:
                await event.forward_to(885077781)
                await event.forward_to("https://t.me/joinchat/GRTdzRZXjcDOLDvexYlcfQ")
    #elif 'You defended villagers well. In exchange for your help,' in event.raw_text:
    #    cant = event.raw_text.split("carry ")[1].split(".")[0]
    #    wait_time = random.randint(5, 10)
    #    await asyncio.sleep(wait_time)
    #    await clients[clients_str][user].send_message("chtwrsbot", f"/sc 07 {cant}")
    elif ("After a successful act" in event.raw_text) and \
            get_config_parameter("Permission", id_arrays[me_array][user], "intervine"):
        await asyncio.sleep(random.randint(10, 25))
        await clients[clients_str][user].send_message('chtwrsbot', "/pledge")
    # Hide items for stock
    elif "Storage" in event.raw_text and get_config_parameter("Player", id_arrays[me_array][user], "level") >= 10 \
            and get_config_parameter("Permission", id_arrays[me_array][user], "spend_hide") and not is_stop:
        r = await clients["alts"][guild_masters[0]].get_messages(config_bot, limit=1)
        if ("/g_deposit " in r[0].message and user.isnumeric()):
            arrItems = r[0].message.split(")")[0].split("/g_deposit (")[1].split(",")
            for i in range(len(arrItems)):
                item = arrItems[i].capitalize()
                text = event.raw_text
                if (item in text):
                    linea = text[text.index(item):].split("\n")[0]
                    cht_messages = await clients["alts"][guild_masters[0]].get_messages("chtwrsbot", limit=1)
                    if ("Not enough space" not in cht_messages[0].message):
                        await asyncio.sleep(random.randint(5, 7))
                        await clients[clients_str][user].send_message('chtwrsbot',
                                                                      "/g_deposit " + resources[item.lower()][0] + " " +
                                                                      linea.split('(')[
                                                                          1][:-1])
                    else:
                        await clients[clients_str][user].send_message(personal_chat, cht_messages[0].message)
                        break
                else:
                    continue
        else:
            if user != buyer:
                await stock(clients_str, user, event.raw_text, me_array)
    # Clean the exchange
    elif "Here you can" in event.raw_text and \
            get_config_parameter("Permission", id_arrays[me_array][user], "spend_hide") and user != buyer \
            and not is_stop:
        await Exchange(clients_str, user, event.raw_text, me_array)
    elif "offers now:" in event.raw_text and \
            (get_config_parameter("Permission", id_arrays[me_array][user], "spend_hide") or \
             get_config_parameter("Permission", id_arrays[me_array][user], "arena")) and not is_stop:
        loop.create_task(tInfo(clients_str, user, event.raw_text, me_array))
    elif "Crafting" in l[1].raw_text and user.isnumeric():
        r = await clients["alts"][guild_masters[0]].get_messages(config_bot, limit=1)
        if user == seller:
            arr = event.raw_text.split("\n")
            cont = 0
            t = random.randint(0, len(arr) - 1)
            for i in range(len(arr)):
                arr[i] = arr[i][1:]
                if arr[i].count(" /") > 0:
                    arr[i] = arr[i].split(" /")[0]
            while (cont != 10 and len(arr) != 0):
                if ("Clarity Bracers" not in arr[t] and "Clarity Shoes" not in arr[t] and "Order Boots" not in arr[t]
                        and "Order Gauntlets" not in arr[t] and "Guard's" not in arr[t] and "Imperial Axe" not in arr[t]
                        and "War hammer" not in arr[t] and "Trident" not in arr[t] and "Hunter blade" not in arr[t]):
                    cont += 1
                    cde = items[arr[t].split(" (")[0]]
                    await asyncio.sleep(random.randint(10, 20))
                    await clients[clients_str][user].send_message("chtwrsbot", "/lot_" + cde)
                    await asyncio.sleep(random.randint(15, 20))
                    await clients[clients_str][user].send_message("cwauctionbot", "/t " + cde)
                    await asyncio.sleep(random.randint(35, 40))
                    cant = int(arr[t].split("(")[1][:-1])
                    if (cant != 1):
                        arr[t] = arr[t].split("(")[0] + "(" + str(cant - 1) + ")"
                    else:
                        arr.pop(t)
                t = random.randint(0, len(arr) - 1)
            await asyncio.sleep(random.randint(10, 20))
            await clients[clients_str][user].send_message("chtwrsbot", "/lots")
        elif (emoji.emojize(':hammer_and_pick:Crafting') in r[0].message):
            text = l[0].raw_text.split("\n")
            for i in range(len(text)):
                text[i] = text[i][1:]
                if ("recipe" in text[i]):
                    text[i] = text[i].split(" /")[0]
                cant = text[i].split(" (")[1][:-1]
                item = items[text[i].split(" (")[0]]
                cht_messages = await clients["alts"][guild_masters[0]].get_messages("chtwrsbot", limit=1)
                if ("Not enough space" not in cht_messages[0].message):
                    await asyncio.sleep(random.randint(10, 15))
                    await clients[clients_str][user].send_message("chtwrsbot", "/g_deposit " + item + " " + cant)
                else:
                    clients[clients_str][user].send_message(personal_chat, cht_messages[0].message)
                    break
    elif "The wind is howling " in l[0].raw_text and \
            get_config_parameter("Permission", id_arrays[me_array][user], "quest"):
        await clients[clients_str][user].send_message(forward_chat, l[1].raw_text,
                                                      schedule=timedelta(
                                                          minutes=random.randint(10, 12) - (get_cw_time().minute)))

    elif "You don't even have enough gold for a pint" in event.raw_text:
        if "/wtb_01" in l[1].raw_text and isTimeForHideAndSpend():
            await asyncio.sleep(random.randint(10, 20))
            await clients[clients_str][user].send_message("chtwrsbot", "/t_01")
    elif "You have been invited to the Guild: DarkAngels." in event.raw_text and user.isnumeric():
        await asyncio.sleep(random.randint(5, 10))
        await clients[clients_str][user].send_message("chtwrsbot", "/join")
    # Auction
    elif ("Welcome to auction!" in event.raw_text and user == seller):
        arr = event.raw_text.split("\n")[5:-5]
        cont = 0
        t = 0
        if (len(arr) > 10):
            t = random.randint(0, len(arr) - 10)
        else:
            t = 0
        missedC = 0
        while (t < len(arr)):
            item = " ".join(arr[t].split(" ")[1:-1])
            if ((arr[t].split(" ")[0].split("_")[1].startswith("k") or arr[t].split(" ")[0].split("_")[1].startswith(
                    "r")) and (
                    "Clarity Bracers" not in item and "Clarity Shoes" not in item and "Order Boots" not in item
                    and "Order Gauntlets" not in item and "Guard's" not in item and "Imperial Axe" not in item
                    and "War hammer" not in item and "Trident" not in item and "Hunter blade" not in item)):
                cont += 1
                await asyncio.sleep(random.randint(10, 20))
                await clients[clients_str][user].send_message("chtwrsbot", arr[t].split(" ")[0])
                await asyncio.sleep(random.randint(15, 20))
                await clients[clients_str][user].send_message("cwauctionbot",
                                                              "/t " + arr[t].split(" ")[0].split("_")[1])
                await asyncio.sleep(random.randint(35, 40))
                cant = int(arr[t].split("(")[1][:-1])
                if (cant > 1):
                    arr[t] = arr[t].split("(")[0] + "(" + str(cant - 1) + ")"
                else:
                    arr.pop(t)
                    t = t - 1
            else:
                missedC += 1
            t += 1
            cht_messages = await clients["alts"][guild_masters[0]].get_messages("chtwrsbot", limit=1)
            await asyncio.sleep(random.randint(5, 10))
            if (cont == 10 or missedC == len(arr) or "You can list up to 10" in cht_messages[0].message):
                break
            if (t == len(arr) and cont != 10):
                t = 0
                missedC = 0
        await asyncio.sleep(random.randint(10, 20))
        await clients[clients_str][user].send_message("chtwrsbot", "/lots")
    # Lots
    elif ("You are selling now:" in event.raw_text and user == seller):
        with open("lots_" + str(user) + ".txt", 'w+') as file:
            arr = event.raw_text.split("\n")
            for i in range(1, len(arr)):
                if (arr[i].count("_") > 0):
                    arr[i - 1] = "/l_" + arr[i].split("_")[1] + "\n"
            file.writelines(arr[0:-1])
        me_schedule = await existThisScheduledMessage(clients_str, user, "/lots_" + str(user), config_bot)
        if not me_schedule:
            await clients[clients_str][buyer].send_message("ScriptCWBot", "/lots_" + str(user),
                                        schedule=timedelta(minutes=random.randint(45, 47)))
    # Lot del Auction
    elif ("You have 15 minutes to configure it." in event.raw_text and user == seller):
        await asyncio.sleep(random.randint(5, 10))
        await clients[clients_str][user].send_message("chtwrsbot", "/" + event.raw_text.split("/")[1])
    elif ("is willing to sell:" in event.raw_text and user == buyer):
        if ("No bets!" in event.raw_text):
            await asyncio.sleep(random.randint(5, 10))
            await clients[clients_str][buyer].send_message("chtwrsbot", event.raw_text.split("make a bet:")[1])

#Orders Fernan
async def ordersBotniato(clients_str, user, event):
    if "Orders for next battle" in event.raw_text:
        for entity in event.entities:
            if isinstance(entity, MessageEntityTextUrl):
                if("/ga" in entity.url):
                    print(entity.url)
                    await clients[clients_str][user].send_message("chtwrsbot", entity.url.split("url=")[1])
    elif "For security reasons you are asked" in event.raw_text:
        await asyncio.sleep(random.randint(3, 6))
        await clients[clients_str][user].send_message("botniatobot", "/" + event.raw_text.split("/")[1])


async def AuctionBot(clients_str, user, event):
    l = await clients[clients_str][user].get_messages("chtwrsbot", limit=1)
    if ("You are willing to sell:" in l[0].message and "Times sold: " in event.raw_text):
        cant = 0
        if ("Cloak" in l[0].message or "Lion" in l[0].message or "Ghost" in l[0].message or "Griffin" in
                l[0].message or "Bulawa part" in l[0].message or "Phoenix Sword" in l[0].message
                or "Manticore" in l[0].message or "Assault" in l[0].message or "Craftsman" in l[0].message
                or "Windstalker" in l[0].message or "Discarnate" in l[0].message or "Overseer" in l[0].message
                or "Nightfall" in l[0].message):
            cant = int(float(event.raw_text.split("\n")[12].split(" ")[1]))
        else:
            cant = int(float(event.raw_text.split("\n")[14].split(" ")[1].split("/")[0]))
        lot = l[0].message.split("\n")[7].split(" ")[0].split("_pri")[0]
        await asyncio.sleep(random.randint(7, 10))
        await clients[clients_str][user].send_message("chtwrsbot", lot + "_time 3")
        await asyncio.sleep(random.randint(7, 10))
        if (cant <= 50):
            if ("Cloak" in l[0].message or "Lion" in l[0].message or "Ghost" in l[0].message or "Griffin" in
                    l[0].message or "Bulawa part" in l[0].message or "Phoenix Sword" in l[0].message
                    or "Manticore" in l[0].message or "Assault" in l[0].message or "Craftsman" in l[0].message
                    or "Windstalker" in l[0].message or "Discarnate" in l[0].message or "Overseer" in l[0].message
                    or "Nightfall" in l[0].message):
                if (cant > 4):
                    await clients[clients_str][user].send_message("chtwrsbot", lot + "_price " + str(cant - 4))
                else:
                    await clients[clients_str][user].send_message("chtwrsbot", lot + "_price " + str(cant - 1))
            else:
                if (cant == 0):
                    await clients[clients_str][user].send_message("chtwrsbot", lot + "_price " + str(cant))
                else:
                    await clients[clients_str][user].send_message("chtwrsbot", lot + "_price " + str(cant - 1))
        else:
            await clients[clients_str][user].send_message("chtwrsbot", lot + "_price 50")
        await asyncio.sleep(random.randint(6, 10))
        await clients[clients_str][user].send_message("chtwrsbot", lot + "_start")


##################################################################################
#                             Daily commands
##################################################################################
async def handlerCommands(clients_str, user, txt, me_array):
    if user != "Fernan":
        if "Defend" in txt and get_config_parameter("Permission", id_arrays[me_array][user], "orders"):
            if user == "VladiY" and (datetime.datetime.now().hour == 22):
                await clients[clients_str][user].send_message('chtwrsbot', "/use_crl")
            elif user != "VladiY" and user != "Kisame" and "Julio" not in user:
                m = []
                if "Jay" in user:
                    await clients[clients_str][user].send_message('chtwrsbot', "/g_def")
                elif "Trinity" in user:
                    await clients[clients_str][user].send_message('chtwrsbot', "⚔Attack")
                    await asyncio.sleep(random.randint(8, 13))
                    await clients[clients_str][user].send_message('chtwrsbot', "🌑")
                else:
                    if me_array == "meService":
                        m = await clients[clients_str][user].get_messages(config_bot, search="/set_order ", limit=1)
                    await asyncio.sleep(random.randint(15, 20))
                    if len(m) == 0 or "Defend" in m[0].text:
                        await clients[clients_str][user].send_message('chtwrsbot', txt)
                    else:
                        await clients[clients_str][user].send_message('chtwrsbot', "⚔Attack")
                        await asyncio.sleep(random.randint(15, 20))
                        await clients[clients_str][user].send_message('chtwrsbot', m[0].text.split(" ")[1])
                await clients[clients_str][user].send_message(forward_chat, "/report",
                                                              schedule=timedelta(minutes=60 - get_cw_time().minute + \
                                                                                         random.randint(12, 14)))
        elif (("🌑" in txt or "🦌" in txt or "🦅" in txt or "🐉" in txt or "🦈" in txt or "🥔" in txt)
              and get_config_parameter("Permission", id_arrays[me_array][user], "orders")):
            await asyncio.sleep(random.randint(10, 20))
            await clients[clients_str][user].send_message('chtwrsbot', "⚔Attack")
            await asyncio.sleep(random.randint(15, 20))
            await clients[clients_str][user].send_message('chtwrsbot', txt)
            await clients[clients_str][user].send_message(forward_chat, "/report",
                                                          schedule=timedelta(minutes=60 - get_cw_time().minute
                                                                                     + random.randint(12, 14)))
        elif "g_def" in txt and get_config_parameter("Permission", id_arrays[me_array][user], "orders"):
            await asyncio.sleep(random.randint(15, 20))
            await clients[clients_str][user].send_message('chtwrsbot', txt)
            await clients[clients_str][user].send_message(forward_chat, "/report",
                                                          schedule=timedelta(minutes=60 - get_cw_time().minute
                                                                                     + random.randint(12, 14)))
        elif (("/sg_" in txt or "Me" in txt or "/level_up" in txt or (
                "/g_leaveconfirmation" in txt and user not in guild_masters))):
            await asyncio.sleep(random.randint(15, 20))
            await clients[clients_str][user].send_message('chtwrsbot', txt)
        elif "Me" in txt and get_config_parameter("Permission", id_arrays[me_array][user], "quest"):
            await asyncio.sleep(random.randint(15, 20))
            await clients[clients_str][user].send_message('chtwrsbot', txt)
        elif (("/c_" in txt and get_config_parameter("Player", id_arrays[me_array][user], "level") >= 10)
              and get_config_parameter("Permission", id_arrays[me_array][user], "crafting")):
            res = txt.split("_")[1]
            resource = resources[res.lower()][0]
            text = "/c_" + resource
            await asyncio.sleep(random.randint(10, 15))
            await clients[clients_str][user].send_message('chtwrsbot', emoji.emojize(':castle:Castle'))
            await asyncio.sleep(random.randint(15, 20))
            await clients[clients_str][user].send_message('chtwrsbot', "⚖Exchange")
            await asyncio.sleep(random.randint(240, 250))
            await clients[clients_str][user].send_message('chtwrsbot', emoji.emojize(':castle:Castle'))
            await asyncio.sleep(random.randint(10, 15))
            await clients[clients_str][user].send_message('chtwrsbot', emoji.emojize(':hammer_and_pick:Workshop'))
            await asyncio.sleep(random.randint(10, 15))
            for i in range(5):
                await clients[clients_str][user].send_message("chtwrsbot", text)
                await asyncio.sleep(random.randint(10, 15))
        # await clients[clients_str][user].send_message(forward_chat,"⚖Exchange",
        #                                              schedule=timedelta(minutes=7+random.randint(-4,4)))
        # await clients[clients_str][user].send_message(forward_chat,'/stock',
        #                                              schedule=timedelta(minutes=11+random.randint(-1,1)))
        elif "/g_deposit " in txt:
            await asyncio.sleep(random.randint(10, 20))
            await clients[clients_str][user].send_message('chtwrsbot', "/stock")
        elif (("Exchange" in txt and get_config_parameter("Player", id_arrays[me_array][user], "level") >= 10)
              and get_config_parameter("Permission", id_arrays[me_array][user], "spend_hide")):
            await asyncio.sleep(random.randint(10, 15))
            await clients[clients_str][user].send_message('chtwrsbot', emoji.emojize(':castle:Castle'))
            await asyncio.sleep(random.randint(10, 20))
            await clients[clients_str][user].send_message('chtwrsbot', txt)
        elif (("/t_01" in txt and get_config_parameter("Player", id_arrays[me_array][user], "level") >= 10)
              and get_config_parameter("Permission", id_arrays[me_array][user], "spend_hide")):
            await asyncio.sleep(random.randint(10, 20))
            await clients[clients_str][user].send_message('chtwrsbot', txt)
        elif ("Crafting" in txt):
            await asyncio.sleep(random.randint(10, 15))
            await clients[clients_str][user].send_message('chtwrsbot', "/inv")
            await asyncio.sleep(random.randint(10, 20))
            await clients[clients_str][user].send_message('chtwrsbot', txt)
        elif ("Auction" in txt):
            await asyncio.sleep(random.randint(10, 15))
            await clients[clients_str][user].send_message('chtwrsbot', emoji.emojize(':castle:Castle'))
            await asyncio.sleep(random.randint(10, 20))
            await clients[clients_str][user].send_message('chtwrsbot', txt)


async def sendAllAlt(txt):
    for i in alts:
        loop.create_task(handlerCommands("alts", str(i), txt, "me"))
    for i in alts_service:
        loop.create_task(handlerCommands("alts_service", i, txt, "meService"))
    #m = await clients["alts_service"]["Julio1"].get_messages(config_bot, limit=1)
    #texto = m[0].text
    #print(texto, "Julio order")
    #for i in range(1, 9):
    #    if ("Julio" + str(i)) in usersCharacter:
    #        loop.create_task(handlerCommands("usersCharacter", ("Julio" + str(i)), texto, "meCharacter"))
    #    else:
    #        loop.create_task(handlerCommands("alts_service", ("Julio" + str(i)), texto, "meService"))


##################################################################################
#                             Buy,spend and hide
##################################################################################

def isTimeForHideAndSpend():
    if get_cw_time().hour >= 7 and get_cw_time().minute > 20:
        return True
    else:
        return False


async def Exchange(clients_str, user, txt, me_array):
    loop.create_task(cleanExchange(clients_str, user, txt))
    if (isTimeForHideAndSpend()):
        resource = resources[
            get_config_parameter("Config", id_arrays[me_array][user], "resources_for_hide").split(",")[0].lower()][0]
        # await clients[clients_str][user].send_message(forward_chat, "/t_" + resource, schedule=timedelta(minutes=2))
        scheduled = await existThisScheduledMessage(clients_str, user, "/stock", forward_chat)
        if not scheduled:
            await clients[clients_str][user].send_message(forward_chat, "/stock", schedule=timedelta(minutes=2))


async def cleanExchange(clients_str, user, txt):
    txt_f = txt.split("\n")
    cantExc = txt_f[6].split(" ")[2].split("/")[0][1:]
    row = 6
    for i in range(int(cantExc)):
        row += 2
        text_send = "/" + txt_f[row].split("/")[1]
        cantidad = int(txt_f[row].split(" ")[0])
        if (cantidad == 1000 or cantidad == 500):
            continue
        await asyncio.sleep(random.randint(10, 15))
        await clients[clients_str][user].send_message("chtwrsbot", text_send)


async def tInfo(clients_str, user, txt, me_array):
    if (isTimeForHideAndSpend()):
        if get_config_parameter("Config", id_arrays[me_array][user], "resources_for_hide").split(",")[0].capitalize() \
                in txt and user != "Fernan":
            item = resources[(
                get_config_parameter("Config", id_arrays[me_array][user], "resources_for_hide").split(",")[0]).lower()][
                0]
            loop.create_task(buy(clients_str, user, txt, item))
            await asyncio.sleep(random.randint(10, 15))
            # await clients[clients_str][user].send_message(forward_chat, "/stock", schedule=timedelta(minutes=2))
            scheduled = await existThisScheduledMessage(clients_str, user, emoji.emojize(':castle:Castle'),
                                                        forward_chat)
            if not scheduled:
                await clients[clients_str][user].send_message(forward_chat, emoji.emojize(':castle:Castle'),
                                                              schedule=timedelta(minutes=2))
                await clients[clients_str][user].send_message(forward_chat, "⚖Exchange", schedule=timedelta(minutes=3))
    else:
        txt_f = txt.split("\n")
        resource = resources[txt_f[0].split(" offers now:")[0].lower()][0]
        if resource == "01":
            money = int(txt[txt.index("You have"):].split("\n")[0].split(" ")[2][:-1])
            cant_arenas = get_config_parameter("Player", id_arrays[me_array][user], "cant_arenas")
            if money < (cant_arenas * 5):
                price = int(txt_f[1].split(" ")[3][:-1]) - 1
                if price == 0:
                    price = 1
                cant = math.floor(((cant_arenas * 5) - money) / price) + 1
                await asyncio.sleep(random.randint(10, 15))
                await clients[clients_str][user].send_message("chtwrsbot",
                                                              "/wts_" + "01_" + str(cant) + "_" + str(price))


async def buy(clients_str, user, txt, item):
    if (isTimeForHideAndSpend()):
        txt_f = txt.split("\n")
        price = txt_f[1].split(" ")[3][:-1]
        money = txt[txt.index("You have"):].split("\n")[0].split(" ")[2][:-1]
        cant = math.floor(float(int(money) / int(price)))
        if (cant != 0):
            await asyncio.sleep(random.randint(10, 15))
            await clients[clients_str][user].send_message("chtwrsbot", "/wtb_" + item + "_" + str(cant))


async def stock(clients_str, user, text, me_array):
    # if (isTimeForHideAndSpend()):
    arr = get_config_parameter("Config", id_arrays[me_array][user], "resources_for_hide").split(",")
    await asyncio.sleep(random.randint(3, 5))
    for i in range(len(arr)):
        code = ""
        cantForSell = 0
        item = arr[i].capitalize()
        if (item in text):
            linea = text[text.index(item):].split("\n")[0]
            cantidad = int(linea.split('(')[1][:-1])
            code = resources[item.lower()][0]
        else:
            continue
        if ("ore" in item):
            cantForSell = 500
        else:
            cantForSell = 1000
        await asyncio.sleep(random.randint(10, 15))
        for h in range(cantidad // cantForSell):
            loop.create_task(hide(clients_str, user, str(cantForSell), code))
            await asyncio.sleep(random.randint(10, 15))
        if cantidad % cantForSell != 0:
            loop.create_task(hide(clients_str, user, str(cantidad % cantForSell), code))


async def hide(clients_str, user, cant, item):
    # cht_messages = await client2.get_messages("chtwrsbot", limit=1)
    # if ("Too many active deals" not in cht_messages[0].message):
    # await asyncio.sleep(random.randint(10, 15))
    await clients[clients_str][user].send_message("chtwrsbot", "/wts_" + item + "_" + cant + "_1000")


##################################################################################
#                                Funciones de Monstruos
##################################################################################
def get_monsters(a):
    l = a.split('\n')
    n = len(l)
    c = 0
    lvls = []
    beast = False
    if "Wolf" in a or "Bear" in a or "Boar" in a:
        beast = True
    # forbiden = False
    for x in l[1:n - 2]:
        if not ('.' in x):
            continue
        if x[0].isdigit():
            c += int(x[0])
        else:
            c += 1
        m = x.split('.')
        lvl = m[1]

        lvls.append(lvl)
    return (int(c), int(min(lvls)), int(max(lvls)), beast)


def anyone(mylevel, min_l, max_l):
    if (mylevel - 10 >= min_l):
        return False
    if (mylevel + 10 < max_l):
        return False

    return True


"d".isnumeric()
##################################################################################
#                               Alts
##################################################################################
cli_task = """
try:
    @client{0}.on(events.NewMessage(chats=('chtwrsbot')))
    async def my_event_handlerCW_U{0}(event):
        loop.create_task(cw_event("{1}","{0}","{2}",event))
    
    @client{0}.on(events.NewMessage(chats=('wolf_pve_bot')))
    async def my_event_handlerPve_U{0}(event):
        if "{0}".isnumeric():
            channelMbs = "https://t.me/joinchat/NlNbhU8H34yH0C1FzD6D_w"
            result = await alts["{0}"].get_messages(channelMbs, limit=3, search=event.text)
            if(len(result) == 0):
                await event.forward_to(channelMbs)
                await asyncio.sleep(random.randint(3,6))
                await event.click(0)
    
    @client{0}.on(events.NewMessage(chats=(777000)))
    async def my_event_handlerTelegramMessage_{0}(event):
        #if "{0}".isnumeric():
        me = await {1}["{0}"].get_entity('me')
        await clientAdmin.send_message("RealScript",event.raw_text + " " + utils.get_display_name(me) + " " + me.phone)
    
    @client{0}.on(events.NewMessage(chats=(personal_chat), incoming=True))
    async def my_event_handlerPersonalChat_U{0}(event):
        loop.create_task(handlerCommands("{1}", "{0}", event.raw_text,"{2}"))	
    
    @client{0}.on(events.NewMessage(chats=(config_bot)))
    async def setupScript_U{0}(event):
        loop.create_task(setupScript("{1}","{0}","{2}",event.raw_text))	
    
    @client{0}.on(events.NewMessage(chats=(forward_chat)))
    async def my_event_handlerForSend_U{0}(event):
        if not stop or not "{0}".isnumeric():
            await asyncio.sleep(random.randint(10,15))
            await client{0}.send_message('chtwrsbot', event.raw_text)
    
    if "Fernan" in "{0}":
        @client{0}.on(events.NewMessage(chats="botniatobot"))
        async def ordersBotniato_U{0}(event):
            loop.create_task(ordersBotniato("{1}","{0}", event))
except Exception as e:
    print("{0}")
"""

cli_task2 = """
@client{0}.on(events.NewMessage(chats="cwauctionbot"))
async def my_event_AuctionBot{0}(event):
    loop.create_task(AuctionBot("alts","{0}",event))
"""

for i in alts:
    exec(cli_task.format(i, "alts", "me"))
for i in alts_service:
    exec(cli_task.format(i, "alts_service", "meService"))
exec(cli_task2.format(seller))

##################################################################################
#                                        Extracciones
##################################################################################
allow = False


def get_permissions_order(rec_order):
    permission_in_order = set([])
    i = 1
    if (len(rec_order) % 2) != 0:
        return permission_in_order
    for rec in rec_order:
        if (i % 2) == 0:
            i += 1
            continue
        if rec in items.values():
            permission_in_order.add("parts")
        elif [rec] in resources.values():
            if rec.isnumeric() and int(rec) >= 39:
                permission_in_order.add("alch")
            elif rec.isnumeric():
                permission_in_order.add("rec")
        elif rec.startswith("u") or rec.startswith("w") or rec.startswith("a"):
            permission_in_order.add("others")
        elif rec.startswith("p") or rec.startswith("s"):
            permission_in_order.add("misc")
        i += 1
    return permission_in_order


cli_extrac = """
@client{0}.on(events.NewMessage(chats=('chtwrsbot')))
async def my_event_CWExtract(event):
    global allow
    if ("Withdrawing" in event.raw_text or "Invite has been sent" in event.raw_text or
            "Not enough items on guild" in event.raw_text) and allow:
        await event.forward_to({1})
        allow = False


@client{0}.on(events.NewMessage(chats=({1})))
async def my_event_ChanelExtract(event):
    global allow
    id_sender = event.sender_id
    if "/g_withdraw" in event.raw_text:
        permission_in_order = get_permissions_order(event.raw_text.split(" ")[1:])
        if len(permission_in_order) == 0:
            await client{0}.send_message({1}, "Formato incorrecto del comando withdraw")
            return
        for permission in permission_in_order:
            if not get_config_parameter("PermissionGuilds", id_sender, permission):
                await client{0}.send_message({1}, "No tienes permiso para extraer los items")
                return
        allow = True
        await client{0}.send_message("chtwrsbot", event.raw_text)
    elif "/g_invite" in event.raw_text:
        if get_config_parameter("PermissionGuilds", id_sender, "invite"):
            allow = True
            await client{0}.send_message("chtwrsbot", event.raw_text)
        else:
            await client{0}.send_message({1}, "No tienes permiso para invitar personas")
"""
for user in guild_extraction:
    print(user)
    print(guild_extraction.get(user))
    exec(cli_extrac.format(user, guild_extraction.get(user)))




##################################################################################
#                                        6,2
##################################################################################
#@clientAdmin.on(events.NewMessage(chats="Antuan2196"))
#async def my_event_receive_storm(event: Message):
#    seller_user: User = await clients["alts"][seller].get_me()
#    if datetime.datetime.utcnow().utcnow().hour == 7 or datetime.datetime.utcnow().utcnow().hour == 8:
#        await clientAdmin.send_message(seller_user.username, event.raw_text,
#                                                   schedule=timedelta(hours=5, minutes=random.randint(4, 7)))
#    else:
#        await clientAdmin.send_message(seller_user.username, event.raw_text,
#                                                   schedule=timedelta(hours=1, minutes=random.randint(25, 30)))


##################################################################################
#                                        Characters
##################################################################################
async def cw_eventCharacters(user, event, me_array):
    global fightsFromGuild
    # Intervine
    if 'You were strolling around on your horse when you noticed' in event.raw_text and \
            get_config_parameter("Permission", id_arrays[me_array][user], "intervine"):
        await asyncio.sleep(random.randint(5, 60))
        await event.click(0)
        if (user == "Ariel"):
            await asyncio.sleep(random.randint(20, 30))
            await event.forward_to(id_chats["gt_chat"])
    elif 'You successfully defeated' in event.raw_text and \
            get_config_parameter("Permission", id_arrays[me_array][user], "intervine"):
        await event.forward_to('ForaySpaiBot')
    elif 'You tried stopping' in event.raw_text and \
            get_config_parameter("Permission", id_arrays[me_array][user], "intervine"):
        await event.forward_to('ForaySpaiBot')
    # Get pledge
    elif ("After a successful act" in event.raw_text) and \
            get_config_parameter("Permission", id_arrays[me_array][user], "intervine"):
        await asyncio.sleep(random.randint(10, 25))
        await usersCharacter[user].send_message('chtwrsbot', "/pledge")
    # Getting information
    elif 'Battle of the' in event.raw_text:
        text = event.raw_text
        save_me(Player(meCharacter[user], get_name(text), int(get_level(text)), int(get_hp(text)),
                       int(get_hp_total(text)), int(get_curent_stamina(text)), int(get_stamina(text)),
                       int(get_stamina_time(text)), int(get_money(text)), 5,
                       get_config(meCharacter[user]), get_permission(meCharacter[user])))
        if (int(get_hp(event.raw_text)) < get_config_parameter("Config", meCharacter[user], "min_hp")
                and get_config_parameter("Config", meCharacter[user], "monsters_on")):
            me_schedule = await existThisScheduledMessage("usersCharacter", user,
                                                          emoji.emojize(':sports_medal:Me'), "MyFirst96_bot")
            if not me_schedule:
                await usersCharacter[user].send_message('MyFirst96_bot',
                                                        emoji.emojize(':sports_medal:Me'),
                                                        schedule=timedelta(
                                                            minutes=random.randint(30, 34)))
    # Respond for finish Monsters
    elif 'Hostile creatures are defeated.' in event.raw_text:
        await asyncio.sleep(random.randint(3, 6))
        if user != "Legendary":
            await event.respond("/f_report")
            await asyncio.sleep(random.randint(3, 6))
            await usersCharacter[user].send_message('chtwrsbot', "/whois")
            await asyncio.sleep(random.randint(3, 6))
        await event.respond(emoji.emojize(':sports_medal:Me'))
    elif 'This is sad but' in event.raw_text:
        # await usersCharacter[user].send_message(
        #    'MyFirst96_bot', emoji.emojize(':sports_medal:Me'),
        #    schedule=timedelta(
        #        hours=get_config_parameter("Config", meCharacter[user], "stamina_step")))
        await asyncio.sleep(random.randint(3, 6))
        await event.respond(emoji.emojize(':sports_medal:Me'))
    elif ("You are preparing for a fight" in event.raw_text):
        fightsFromGuild[user] = True
        await asyncio.sleep(28)
        fightsFromGuild[user] = False
    elif 'You met some hostile creatures' in event.raw_text and "Force" in user:
        print(user, "cw_event_character")
        await event.forward_to(679956294)


async def wolf_pve(user, event):
    on = get_config_parameter("Config", meCharacter[user], "monsters_on")
    if user == "Valen":
        on = True
    if (on and get_config_parameter("Config", meCharacter[user], "min_hp") <
            get_config_parameter("Player", meCharacter[user], "health") and event.message.buttons is not None):
        if event.message.buttons[0][0].url is not None:
            await usersCharacter[user].send_message('chtwrsbot',
                                                    event.message.buttons[0][0].url.split("=")[1])


async def shark_pve(user, event):
    if (get_config_parameter("Config", meCharacter[user], "monsters_on")
            and get_config_parameter("Config", meCharacter[user], "min_hp") <
            get_config_parameter("Player", meCharacter[user], "health") and event.message.buttons is not None):
        for line in event.raw_text.split("\n"):
            if "lvl" in line:
                level = 10
                if (abs(int(line.split("lvl")[0].split(" ")[-1]) - get_config_parameter(
                        "Player", meCharacter[user], "level")) > level):
                    return
        loop.create_task(shark_pve_aux(user, event.chat_id))
        await event.message.click(0, 0)


async def shark_pve_aux(user, chat_id):
    await asyncio.sleep(1)
    m = await usersCharacter[user].get_messages(chat_id, limit=1)
    await usersCharacter[user].send_message('chtwrsbot',
                                            m[0].buttons[0][0].url.split("=")[1])


async def botniato_pve(user, event):
    if (get_config_parameter("Config", meCharacter[user], "monsters_on")
            and get_config_parameter("Config", meCharacter[user], "min_hp") <
            get_config_parameter("Player", meCharacter[user], "health")
            and "/fight_" in event.raw_text):
        await usersCharacter[user].send_message('chtwrsbot', event.raw_text)


async def deer_pve(user, event):
    if (get_config_parameter("Config", meCharacter[user], "monsters_on") and
            get_config_parameter("Config", meCharacter[user], "min_hp") <
            get_config_parameter("Player", meCharacter[user], "health")):
        for item in event.raw_text.split('\n'):
            if 'lvl.' in item:
                if (abs(int(item.split('.')[1]) - get_config_parameter(
                        "Player", meCharacter[user], "level")) > 10):
                    return
        # loop.create_task(deer_pve_aux(user, event.chat_id))
        # if "forward" not in event.message.buttons[0][0].text:
        await asyncio.sleep(random.randint(2, 3))
        await event.message.click(0, 0)


async def deer_pve_aux(user, chat_id):
    await asyncio.sleep(3)
    m = await usersCharacter[user].get_messages(chat_id, limit=1)
    if m[0].buttons is None:
        return
    await usersCharacter[user].send_message('chtwrsbot',
                                            m[0].buttons[0][0].url.split("=")[1])
    await asyncio.sleep(random.randint(3, 5))
    await m[0].click(1, 0)


async def Moon_Pve(user, event):
    if (get_config_parameter("Config", meCharacter[user], "monsters_on")
            and 'You met some hostile ' in event.raw_text and
            get_config_parameter("Config", meCharacter[user], "min_hp") <
            get_config_parameter("Player", meCharacter[user], "health")):
        level_player = get_config_parameter("Player", meCharacter[user], "level")
        if "ambush" in event.raw_text and "Unknown" in user:
            return
        if user == "Blaze1":
            max = get_monsters(event.raw_text)[2]
            min = get_monsters(event.raw_text)[1]
            if abs(level_player - min) > 10:  # or abs(max - level_player) > 15:
                return
        else:
            for item in event.raw_text.split('\n'):
                if 'lvl.' in item:
                    level = 10
                    if user == "Valen":
                        level = 5
                    if abs(int(item.split('.')[1]) - level_player) > level:
                        return
        global fightsFromGuild
        await usersCharacter[user].send_message('chtwrsbot', event.raw_text)
        await asyncio.sleep(18)
        m = await usersCharacter[user].get_messages(event.chat_id, limit=1)
        if fightsFromGuild[user] and m[0].buttons is not None:
            await asyncio.sleep(random.randint(3, 7))
            await usersCharacter[user].send_message('chtwrsbot', emoji.emojize(':sports_medal:Me'))
            for bl in m[0].buttons:
                for b in bl:
                    if b.text == "I am helping!" and \
                            (get_config_parameter("Player", meCharacter[user], "stamina") > 0)\
                            and (user != "Sylvanna" and user != "Azur"):
                        await asyncio.sleep(random.randint(5, 10))
                        await b.click()


async def setupScriptCharacters(user, event):
    txt1 = event.raw_text
    if '/hp' in event.raw_text:
        set_config_parameter("Config", meCharacter[user], "min_hp", int(event.raw_text.split('_')[1]))
        await usersCharacter[user].send_message(
            "ScriptCWBot", "Su umbral de salud para capturar monstruos ahora es de " + str(
                event.raw_text.split('_')[1]))
    elif '/cant' in event.raw_text:
        set_config_parameter("Config", myself, "cant_monsters", int(txt1.split('_')[1]))
        await users[user].send_message("ScriptCWBot",
                                       "Se ha definido " + str(txt1.split('_')[1]) + " como mínimo de monstruos")
    elif '/trader_resource' in event.raw_text:
        set_config_parameter("Config", myself, "trader_resource", txt1.split(' ')[1])
        await usersCharacter[user].send_message("ScriptCWBot", "Se ha definido " + str(
            txt1.split(' ')[1]) + " como recurso para el trader")
    elif '/startMonsters' in event.raw_text:
        set_config_parameter("Config", meCharacter[user], "monsters_on", True)
        await usersCharacter[user].send_message("ScriptCWBot", "Se ha iniciado la caza de monstruos")
    elif '/stopMonsters' in event.raw_text:
        set_config_parameter("Config", meCharacter[user], "monsters_on", False)
        await usersCharacter[user].send_message('ScriptCWBot',
                                                "Se ha detenido la caza de monstruos")
    elif '/values' in event.raw_text:
        await usersCharacter[user].send_message('ScriptCWBot', get_config(
            meCharacter[user]))
    elif '/me_' in event.raw_text:
        await usersCharacter[user].send_message('ScriptCWBot',
                                                load_player(meCharacter[user]))
    elif '/help' in event.raw_text:
        ayuda = """Pulse /startMonsters para cazar monstruos
        Pulse /stopMonsters para detener peleas con monstruos
        Pulse /hp_260 para definir la salud mínima para cazar mostruos
        Pulse /trader_resource para definir el recurso a ofrecerle al mercader
        """
        await usersCharacter[user].send_message('ScriptCWBot', ayuda)
    if (user in guild_extraction) and "/set_guild_permission" in txt1:
        p = txt1.split(" ")[2].split(",")
        telegram_id = int(txt1.split(" ")[1])
        set_permission_guild(PermissionGuilds(telegram_id, False, False, False, False, False, False), telegram_id)
        for i in p:
            if i == "res":
                set_config_parameter("PermissionGuilds", telegram_id, "rec", True)
            else:
                set_config_parameter("PermissionGuilds", telegram_id, i, True)


# elif (user == "Antonio"):
#    if '/item' in event.raw_text:
#        set_config_parameter("Config", meCharacter[user], "trader_resource",
#                             int(event.raw_text.split('_')[1]))
#        await usersCharacter[user].send_message("ScriptCWBot",
#                                                                 "Su item para el trader ahora es " + str(
#                                                                     event.raw_text.split('_')[1]))
#    if '/help' in event.raw_text:
#        ayuda = "Pulse /item_10 para seleccionar silver ore como item para el trader"
#        await usersCharacter[user].send_message('ScriptCWBot', ayuda)


async def guildCharactersGT(user, event):
    if 'You met some hostile creatures.' in event.raw_text:
        if (user == "Ariel" and get_config_parameter("Config", meCharacter[user], "monsters_on") and
                'ambush' not in event.raw_text and
                get_config_parameter("Config", meCharacter[user], "min_hp") <
                get_config_parameter("Player", meCharacter[user], "health")
                and not (get_cw_time().hour == 7 and get_cw_time().minute >= 15)):
            global fightsFromGuild
            for item in event.raw_text.split('\n'):
                if 'lvl.' in item:
                    if (abs(int(item.split('.')[1]) -
                            get_config_parameter("Player", meCharacter[user], "level")) > 10):
                        return
            await asyncio.sleep(random.randint(2, 4))
            fightsFromGuild[user] = True
            await usersCharacter[user].send_message('chtwrsbot', event.raw_text)
            await asyncio.sleep(20)
            fightsFromGuild[user] = False


# Getting orders in Wolfpack
# @clientAriel.on(events.NewMessage(chats=(-1001466103062)))
# async def my_event_handlerScript(event):
# await event.forward_to(personal_chat)
#  from_users=976918452


#@clientAdmin.on(events.NewMessage(chats="RealScript"))
@clientVladiY.on(events.NewMessage(chats=1247785159, from_users=976918452))
async def my_event_handler_orders_vladi(event):
    if "Attack" in event.raw_text and not isTimeForHideAndSpend():
        delay = (8 - get_cw_time().hour) * 60
        text = event.raw_text.split("\n")[0].split(" ")[1][0]
        await clientAdmin.send_message("RealScript", text)
        await clientVladiY.send_message(forward_chat, "⚔Attack",
                                        schedule=timedelta(minutes=delay - get_cw_time().minute - 58))
        await asyncio.sleep(random.randint(4, 25))
        await clientVladiY.send_message(forward_chat, text,
                                        schedule=timedelta(minutes=delay - get_cw_time().minute - 56))
        await clientAdmin.send_message("RealScript", text)
        # await clients["alts"][guild_masters[0]].send_message(config_bot, "/g_order "+ text + " 11 19",
        #                                schedule=timedelta(minutes = random.randint(53, 55)))
        # await clients["alts"][guild_masters[0]].send_message(config_bot, "/g_order " + text + " 2 3",
        #                                schedule=timedelta(minutes = random.randint(53, 55)))
        await clientVladiY.send_message(forward_chat, "/report",
                                        schedule=timedelta(minutes=delay - get_cw_time().minute +
                                                                   random.randint(20, 23)))
        #task = """
        #await client{0}.send_message(forward_chat, "/advlist",schedule=timedelta(minutes=delay - get_cw_time().minute + 15))
        #"""
        #for item in advisers:
        #    exec(task.format(item))
        #print(text)
    elif "DEFEND" in event.raw_text and "⚔"not in event.raw_text: # and not isTimeForHideAndSpend():
        delay = (8 - get_cw_time().hour) * 60
        text = event.raw_text[0] + "Defend"
        await clientVladiY.send_message(forward_chat, "/report",
                                        schedule=timedelta(minutes=delay - get_cw_time().minute +
                                                           random.randint(20, 23)))
        await clientAdmin.send_message("RealScript", text)
        await clientVladiY.send_message(forward_chat, text, schedule=timedelta(minutes=delay - 40))


#@clientPein1.on(events.NewMessage(chats="t.me/alliancega"))
#async def my_event_handler_orders_red(event: Message):
#    if event.forward.original_fwd.from_id.user_id == 609517172:
#        level = get_config_parameter("Player", id_arrays["meService"]["Red"], "level")
#        delay_battle = timedelta(hours=8, minutes=0) - timedelta(hours=get_cw_time().hour, minutes=get_cw_time().minute)
#        delay = delay_battle - timedelta(hours=1, minutes=35)
#       if event.button_count == 1:
#            if delay.days != -1:
#               await clientPein1.send_message(forward_chat, event.buttons[0][0].url.split("url=")[1], schedule=delay)
#           else:
#               await clientPein1.send_message("chtwrsbot", event.buttons[0][0].url)
#       else:
#            for bl in event.buttons:
#                text = ""
#                for b in bl:
#                    bu: str = b.text.split("Lvl.")[1]
#                    min = 0
#                    max = 0
#                    lvl = 10000
#                    if bu.count("-") > 0:
#                        min = int(bu.split("-")[0])
#                        max = int(bu.split("-")[1][0:2])
#                    else:
#                        lvl = int(bu[0:2])
#                    if min <= level <= max:
#                        text = b.url.split("url=")[1]
#                    elif level >= lvl:
#                        text = b.url.split("url=")[1]
#                if text != "":
#                    if delay.days != -1:
#                        await clientPein1.send_message(forward_chat, text, schedule=delay)
#                        break
#                    else:
#                        await clientPein1.send_message("chtwrsbot", text)
#                        break

#@clientGodfather.on(events.NewMessage(chats='deer_daily_inn_bot'))
#async def my_event_handlerSnipingGodfatherDaily(event):
#    if (("Could not buy" in event.raw_text and "Thread" in event.raw_text)
#        or ("Successfully purchased" in event.raw_text and "Thread" in event.raw_text)  or "BattleIsNear" in event.raw_text)\
#           and (get_config_parameter("Permission", id_arrays["meService"]["Godfather"], "pet")):
#       #if "Could not buy" in event.raw_text and "Thread" in event.raw_text:
#       #    await asyncio.sleep(1)
#       #elif "Successfully purchased" in event.raw_text and "Thread" in event.raw_text:
#        await asyncio.sleep(1)
#        await clientGodfather.send_message("deer_daily_inn_bot", "/wtb_01_3000_1")

#@clientGodfather.on(events.NewMessage(chats='chtwrsbot'))
#async def my_event_handlerSnipingGodfather(event):
#    if (("Purchase begins, track your order" in event.raw_text and "Thread" in event.raw_text)
#            or "enough gold for a pint" in event.raw_text)\
#           and (get_config_parameter("Permission", id_arrays["meService"]["Godfather"], "withdraw")):
#       if "Purchase begins, track your order" in event.raw_text and "Thread" in event.raw_text:
#           await asyncio.sleep(5)
#       elif "enough gold for a pint" in event.raw_text:
#           await asyncio.sleep(1)
#       await clientGodfather.send_message("chtwrsbot", "/wtb_01_3000")
    #elif ("offers now:" in event.raw_text \
    #        and (get_config_parameter("Permission", id_arrays["meService"]["Godfather"], "quest"))):
    #    txt_f = event.raw_text.split('\n')
    #    resource = resources[txt_f[0].split(" offers now:")[0].lower()][0]
    #    if resource == "01":
    #        if int(txt_f[1].split(" ")[3][:-1]) == 1:
    #            pcs = int(txt_f[1].split(" ")[0])
    #            cant = 0
    #            money = int(event.raw_text[event.raw_text.index("You have"):].split("\n")[0].split(" ")[2][:-1])
    #            if money == 0:
    #                return
    #            if money > pcs:
    #                cant = pcs
    #            else:
    #                cant = money
    #            for i in range(2):
    #                await clientGodfather.send_message("chtwrsbot", "/wtb_01_" + str(cant))
    #                await asyncio.sleep(1)
    #            await asyncio.sleep(10)
    #            await clientGodfather.send_message("chtwrsbot", "/t_01")
    #        else:
    #            await asyncio.sleep(1)
    #            await clientGodfather.send_message("chtwrsbot", "/t_01")


#@clientGodfather.on(events.NewMessage(chats=config_bot))
#async def my_event_setupGodfather(event):
#    if "/start_buy" == event.raw_text:
#        set_config_parameter("Permission", id_arrays["meService"]["Godfather"], "withdraw", False)
#        set_config_parameter("Permission", id_arrays["meService"]["Godfather"], "pet", True)
#        await clientGodfather.send_message("deer_daily_inn_bot", "/wtb_01_3000_1")
#    elif "/stop_buy" == event.raw_text:
#        set_config_parameter("Permission", id_arrays["meService"]["Godfather"], "pet", False)
#    elif "/stop_buy2" == event.raw_text:
#        set_config_parameter("Permission", id_arrays["meService"]["Godfather"], "withdraw", False)
#    elif "/start_buy2" == event.raw_text:
#        set_config_parameter("Permission", id_arrays["meService"]["Godfather"], "pet", False)
#        set_config_parameter("Permission", id_arrays["meService"]["Godfather"], "withdraw", True)
#        await clientGodfather.send_message("chtwrsbot", "/wtb_01_3000")


#for i in snipping:
#    exec(task.format(i))

cli_taskCharacters = """
try:
    @client{0}.on(events.NewMessage(chats=('chtwrsbot')))
    async def my_event_handlerCW_{0}(event):
        loop.create_task(cw_eventCharacters("{0}",event, "{1}"))
    
    
    # button with the url
    @client{0}.on(events.NewMessage(chats=(["wolf_pve_bot", "PotatoCastle_bot"]), incoming=True))
    async def my_event_handlerWolfPve_{0}(event):
        loop.create_task(wolf_pve("{0}",event))	
    
    
    # two buttons and the first button with the url
    @client{0}.on(events.NewMessage(chats=([1322152512, 1235360309, 1463028733]), incoming=True))
    async def my_event_handlerDeerPve_{0}(event):
        loop.create_task(deer_pve("{0}",event))
    
    # botniato 3.0
    @client{0}.on(events.NewMessage(chats=("botniatobot"), incoming=True))
    async def my_event_handlerBotniato3_{0}(event):
        loop.create_task(botniato_pve("{0}",event))
    
    @client{0}.on(events.NewMessage(chats=(["deerhorn_os_bot"]), incoming=True))
    async def my_event_handlerDeerPveBot_{0}(event):
        m = await usersCharacter["{0}"].get_messages(event.chat_id, limit=1)
        if m[0].buttons is None and "Link of the fight" not in event.raw_text :
            return
        await usersCharacter["{0}"].send_message('chtwrsbot',
                                                m[0].buttons[0][0].url.split("=")[1])
                                                
                                                
    # two buttons and the last button with the url
    @client{0}.on(events.NewMessage(chats=(["deepbluesharkbot", "AngryBirbs_bot"]), incoming=True))
    async def my_event_handlerSharkPve_{0}(event):
        loop.create_task(shark_pve("{0}",event))
    
    
    @client{0}.on(events.NewMessage(chats=(config_bot)))
    async def setupScript_{0}(event):
        loop.create_task(setupScriptCharacters("{0}",event))
    
    
    @client{0}.on(events.NewMessage(chats=(forward_chat)))
    async def my_event_handlerForSend_U{0}(event):
        if "{0}" not in alts_service:
            await asyncio.sleep(random.randint(10,15))
            await usersCharacter["{0}"].send_message('chtwrsbot', event.raw_text)
    
    
    #@client{0}.on(events.NewMessage(chats=(id_chats["gt_chat"]), incoming=True))
    #async def my_event_handlerGuildGT_{0}(event):
    #    loop.create_task(guildCharactersGT("{0}",event))
    
    
    # all chats and if it has the helper click the button
    if "{0}" != "Ariel": 
        @client{0}.on(events.NewMessage(pattern="(You met some hostile creatures.)+", incoming=True,
                                        chats=blacklist_monsters_chats["{0}"], blacklist_chats=True))
        async def my_event_handlerPersonalMonster_{0}(event):
            if event.from_id != id_arrays["{1}"]["{0}"]:
                if event.forward.sender_id != 408101137:
                    return
                loop.create_task(Moon_Pve("{0}",event))
except Exception as e:
    print("{0}")
"""


@clientAdmin.on(events.NewMessage(chats="me", incoming=True))
async def my_event_handler_connect(event):
    if "/connect" in event.raw_text:
        for i in range(num_users):
            exec(cli_start.format(i, "alts"))
            # exec("alts['" + str(i) + "'] = client" + str(i))
        for i in alts_service:
            exec(cli_start.format(i, "alts_service"))
            # exec("alts_service['" + i + "'] = client" + i)
        for i in usersCharacter:
            exec(cli_start.format(i, "usersCharacter"))
            # exec("usersCharacter['" + i + "'] = client" + str(i))
        for i in usersCW3:
            exec(cli_start.format(i, "usersCW3"))
        for i in snipping:
            exec(cli_start.format(i, "snipping"))


async def setupScriptCharactersCW3(user, event):
    txt1 = event.raw_text
    if '/hp' in event.raw_text:
        set_config_parameter("Config", meService[user], "min_hp", int(event.raw_text.split('_')[1]))
        await usersCW3[user].send_message(
            "ScriptCWBot", "Su umbral de salud para capturar monstruos ahora es de " + str(
                event.raw_text.split('_')[1]))
    elif '/cant' in event.raw_text:
        set_config_parameter("Config", myself, "cant_monsters", int(txt1.split('_')[1]))
        await users[user].send_message("ScriptCWBot",
                                       "Se ha definido " + str(txt1.split('_')[1]) + " como mínimo de monstruos")
    elif '/trader_resource' in event.raw_text:
        set_config_parameter("Config", myself, "trader_resource", txt1.split(' ')[1])
        await usersCW3[user].send_message("ScriptCWBot", "Se ha definido " + str(
            txt1.split(' ')[1]) + " como recurso para el trader")
    elif '/startMonsters' in event.raw_text:
        set_config_parameter("Config", meService[user], "monsters_on", True)
        await usersCW3[user].send_message("ScriptCWBot", "Se ha iniciado la caza de monstruos")
    elif '/stopMonsters' in event.raw_text:
        set_config_parameter("Config", meService[user], "monsters_on", False)
        await usersCW3[user].send_message('ScriptCWBot',
                                                "Se ha detenido la caza de monstruos")
    elif '/values' in event.raw_text:
        await usersCW3[user].send_message('ScriptCWBot', get_config(
            meService[user]))
    elif '/me_' in event.raw_text:
        await usersCW3[user].send_message('ScriptCWBot',
                                                load_player(meService[user]))
    elif '/help' in event.raw_text:
        ayuda = """Pulse /startMonsters para cazar monstruos
        Pulse /stopMonsters para detener peleas con monstruos
        Pulse /hp_260 para definir la salud mínima para cazar mostruos
        """
        await usersCW3[user].send_message('ScriptCWBot', ayuda)


async def CW3_Pve(user, event: Message):
    if "Kururo" in user and get_config_parameter("Config", meService[user], "monsters_on"):
        r = await usersCW3[user].get_messages(config_bot, limit=1)
        low = int(r[0].message.split("-")[0])
        high = int(r[0].message.split("-")[1])
        max = get_monsters(event.raw_text)[2]
        min = get_monsters(event.raw_text)[1]
        if min < low or max > high:
            return
        text = event.raw_text
        if event.chat_id == -1001170363538:
            text = event.buttons[0][0].url.split("url=")[1]
        await usersCW3[user].send_message('ChatWarsBot', text)
        await asyncio.sleep(18)
    elif (get_config_parameter("Config", meService[user], "monsters_on") and
            get_config_parameter("Config", meService[user], "min_hp") <
            get_config_parameter("Player", meService[user], "health")):
        for item in event.raw_text.split('\n'):
            if 'lvl.' in item:
                if (abs(int(item.split('.')[1]) - get_config_parameter(
                        "Player", meService[user], "level")) > 10):
                    return
        text = event.raw_text
        if event.chat_id == -1001170363538:
            text = event.buttons[0][0].url.split("url=")[1]
        await usersCW3[user].send_message('ChatWarsBot', text)
        await asyncio.sleep(18)
        # m = await usersCharacter[user].get_messages(event.chat_id, limit=1)
        # if fightsFromGuild[user] and m[0].buttons is not None:
        #    await asyncio.sleep(random.randint(3, 7))
        #    await usersCharacter[user].send_message('ChatWarsBot', emoji.emojize(':sports_medal:Me'))
        #    for bl in m[0].buttons:
        #        for b in bl:
        #            if b.text == "I am helping!" and \
        #                    (get_config_parameter("Player", meCharacter[user], "stamina") > 0):
        #                await asyncio.sleep(random.randint(5, 10))
        #                await b.click()


async def mobs_notify(user, event):
    if "Kururo" in user and get_config_parameter("Config", meService[user], "monsters_on"):
        r = await usersCW3[user].get_messages(config_bot, limit=1)
        low = int(event.message.buttons[0][0].text[1:-1].split("-")[0])
        high = int(event.message.buttons[0][0].text[1:-1].split("-")[1])
        max = get_monsters(event.raw_text)[2]
        min = get_monsters(event.raw_text)[1]
        if min < low or max > high:
            return
        if event.message.buttons[0][0].url is not None:
            await usersCW3[user].send_message('ChatWarsBot', event.message.buttons[0][0].url.split("=")[1])
    elif (get_config_parameter("Config", meService[user], "monsters_on")
            and get_config_parameter("Config", meService[user], "min_hp") <
            get_config_parameter("Player", meService[user], "health") and event.message.buttons is not None):
        low_level = int(event.message.buttons[0][0].text[1:-1].split("-")[0])
        high_level = int(event.message.buttons[0][0].text[1:-1].split("-")[1])
        level = get_config_parameter("Player", meService[user], "level")
        # if abs((high_level - 5) - get_config_parameter("Player", meService[user], "level")) > 10:
        #    return
        if abs(high_level - get_config_parameter("Player", meService[user], "level")) > 10 and \
                abs(low_level - get_config_parameter("Player", meService[user], "level")) > 10:
            return
        if event.message.buttons[0][0].url is not None:
            await usersCW3[user].send_message('ChatWarsBot', event.message.buttons[0][0].url.split("=")[1])


def get_name_cw3(text):
    i = 2
    if "Поздравляем!" in text:
        i = 5
    return text.split('\n')[i].split(' ')[0][1:]


def get_hp_cw3(text):
    return text[text.index('Здоровье:'):].split('\n')[0].split(' ')[1].split('/')[0]


def get_hp_total_cw3(text):
    return text[text.index('Здоровье:'):].split('\n')[0].split(' ')[1].split('/')[1]


def get_curent_stamina_cw3(text):
    return text[text.index('Выносливость:'):].split('\n')[0].split(' ')[1].split('/')[0]


def get_stamina_cw3(text):
    return text[text.index('Выносливость:'):].split('\n')[0].split(' ')[1].split('/')[1]


def get_stamina_time_cw3(text):
    stamina = "0"
    if "now" not in text and text[text.index('Выносливость:'):].split('\n')[0].count(' ') != 1:
        stamina = text[text.index('Выносливость:'):].split('\n')[0].split(' ')[2][1:-4]
    elif text[text.index('Выносливость:'):].split('\n')[0].count(' ') == 1:
        stamina = "60"
    return stamina


def get_money_cw3(text):
    i = 1
    if "Мана" in text:
        i = 2
    return text[text.index("Выносливость:"):].split('\n')[i].split(' ')[0][1:]


def get_level_cw3(text):
    return text[text.index('Уровень:'):].split('\n')[0].split(' ')[1]


async def cw3_eventCharacters(user, event, me_array):
    if 'Битва семи замков ' in event.raw_text and "Kururo1" not in user:
        text = event.raw_text
        save_me(Player(meService[user], get_name_cw3(text), int(get_level_cw3(text)), int(get_hp_cw3(text)),
                       int(get_hp_total_cw3(text)), int(get_curent_stamina_cw3(text)), int(get_stamina_cw3(text)),
                       int(get_stamina_time_cw3(text)), int(get_money_cw3(text)), 5,
                       get_config(meService[user]), get_permission(meService[user])))
        if (int(get_hp_cw3(event.raw_text)) < get_config_parameter("Config", meService[user], "min_hp")
                and get_config_parameter("Config", meService[user], "monsters_on")):
            me_schedule = await existThisScheduledMessage("usersCW3", user,
                                                          emoji.emojize(':sports_medal:Герой'), "MyFirst96_bot")
            if not me_schedule:
                await usersCW3[user].send_message('MyFirst96_bot',
                                                        emoji.emojize(':sports_medal:Герой'),
                                                        schedule=timedelta(
                                                            minutes=random.randint(30, 34)))
    # Respond for finish Monsters
    elif 'Ура! Ты всё еще жив.' in event.raw_text:
        await asyncio.sleep(random.randint(3, 6))
        await event.respond("/f_report")
        await asyncio.sleep(random.randint(3, 6))
        await usersCW3[user].send_message('ChatWarsBot', "/whois")
        await asyncio.sleep(random.randint(3, 6))
        await event.respond(emoji.emojize(':sports_medal:Герой'))
    elif 'Ты скорее мёртв чем жив.' in event.raw_text:
        await asyncio.sleep(random.randint(3, 6))
        await event.respond(emoji.emojize(':sports_medal:Герой'))



cli_taskCW3 = """

@client{0}.on(events.NewMessage(chats=(config_bot)))
async def setupScript_{0}(event):
    loop.create_task(setupScriptCharactersCW3("{0}",event))	


@client{0}.on(events.NewMessage(chats=(forward_chat)))
async def my_event_handlerForSend_U{0}(event):
    if "Kururo1" not in "{0}":
        await asyncio.sleep(random.randint(10,15))
        await usersCW3["{0}"].send_message('ChatWarsBot', event.raw_text)

@client{0}.on(events.NewMessage(chats=('ChatWarsBot')))
async def my_event_handlerCW_{0}(event):
    loop.create_task(cw3_eventCharacters("{0}",event, "{1}"))

# Chat wars 3 mobs
@client{0}.on(events.NewMessage(pattern="(Ты заметил враждебных существ. )+", incoming=True,
                                chats=blacklist_monsters_chats["{0}"], blacklist_chats=True))
async def my_event_handlerPersonalMonster_{0}(event):
    if event.from_id != id_arrays["{1}"]["{0}"]:
        loop.create_task(CW3_Pve("{0}",event))


@client{0}.on(events.NewMessage(chats=('CwMobsNotifyBot'), incoming=True))
async def my_event_handlerSharkPve_{0}(event):
    loop.create_task(mobs_notify("{0}",event))
"""

alts_group_task = """
try: 
    @client{0}1.on(events.NewMessage(chats=(alts_group['{0}']["chat"])))
    async def event_alts_group_commands(event):
        print("Entro")
        users = alts_group['{0}']["users"]
        #if "/help" in event.raw_text:
        #    txt = "Pulse /quest_Forest para definir quest a realizar (Forest, Swamp, Valley, Foray)
        #    await alts_service['{0}1'].send_message(alts_group['{0}']["chat"], txt)
        #elif "/quest" in event.raw_text:
        #    for i in range(1, users + 1):
        #        myself = id_arrays["meService"]['{0}'+str(i)]
        #        dic = {"Forest": "0", "Swamp": "1", "Valley": "2", "Foray": "3"}
        #        set_config_parameter("Config", myself, "quest", dic[event.raw_text.split('_')[1].capitalize()])
        #    await alts_service['{0}1'].send_message(alts_group['{0}']["chat"], "Se ha definido hacer " + event.raw_text.split('_')[1])
        #else:
        for i in range(1, users + 1):
            await alts_service['{0}'+str(i)].send_message("chtwrsbot", event.raw_text)
            await asyncio.sleep(random.randint(1,8))
except NameError:
    print("NameError")
"""


adviser_task = """
try: 
    @client{0}.on(events.NewMessage(chats="chtwrsbot"))
    async def event_advisers(event):
        if "Advisers available for hire today" in event.raw_text:
            r = await client{0}.get_messages(config_bot, limit=1)
            level_config = int(r[0].message[r[0].message.index("Level: "):].split("\\n")[0].split(" ")[1])
            type_config = r[0].message[r[0].message.index("Type: "):].split("\\n")[0].split(" ")[1]
            for line in event.raw_text.split("\\n")[1:]:
                level = int(line.split("lvl.")[1][0])
                type_adv = line.split("lvl.")[1].split(" ")[1]
                if level_config == level and type_config == type_adv:
                    await asyncio.sleep(2)
                    await client{0}.send_message("chtwrsbot", line.split(" ")[0])
                await asyncio.sleep(2)
        elif "Hire: /g_hire" in event.raw_text:
            r = await client{0}.get_messages(config_bot, limit=1)
            value1= int(r[0].message[r[0].message.index("Stats: "):].split("\\n")[0].split(" ")[1].split(",")[0])
            value2 = int(r[0].message[r[0].message.index("Stats: "):].split("\\n")[0].split(" ")[1].split(",")[1])
            effects = event.raw_text[event.raw_text.index("Effect:"):].split("\\n")[1:-3]
            print(value1,value2,effects[0].split("+")[1][:-1],effects[1].split("-")[1])
            if "Level" in effects[0]:
                if value1 > int(effects[0].split("-")[1]) or value2 > int(effects[1].split("+")[1][:-1]):
                    return
            elif "Level" in effects[1]:
                if value1 > int(effects[0].split("+")[1][:-1]) or value2 > int(effects[1].split("-")[1]):
                    return
            elif value1 > int(effects[0].split("+")[1][:-1]) or value2 > int(effects[1].split("+")[1][:-1]):
                return
            await asyncio.sleep(2)
            await client{0}.send_message("chtwrsbot", event.raw_text.split("\\n")[-1].split("Hire: ")[1])
except NameError:
    print("NameError")
"""

cli_taskIntervine = """
@client{0}.on(events.NewMessage(chats=('chtwrsbot')))
async def my_event_handlerCW_{0}(event):
    loop.create_task(cw_eventIntervine("{0}",event))

if "{0}" == "Smith" or "{0}" == "Smith1":
    @client{0}.on(events.NewMessage(chats=('ChatWarsBot')))
    async def my_event_handlerCW3_{0}(event):
        loop.create_task(cw_eventCharacters3("{0}",event))

"""
async def cw_eventIntervine(user, event):
    # Intervine
    if 'You were strolling around on your horse when you noticed' in event.raw_text:
        r = await intervine_users[user].get_messages("ScriptCWBot", limit=1)
        try:
            if len(r) > 0 and "/stop_intervine" in r[0].raw_text:
                return
        except Exception:
            print("No message in config bot")
        wait_time = random.randint(5, 60)
        await asyncio.sleep(wait_time)
        await event.click(0)
    if 'You successfully defeated' in event.raw_text:
        await event.forward_to('ForaySpaiBot')
    if 'You tried stopping' in event.raw_text:
        await event.forward_to('ForaySpaiBot')
    # Get pledge
    if "After a successful act" in event.raw_text:
        wait_time = random.randint(10, 20)
        await asyncio.sleep(wait_time)
        await intervine_users[user].send_message('chtwrsbot', "/pledge")
    if 'You defended villagers well. In exchange for your help,' in event.raw_text\
            and ("Jean" in user or "Naruto1" in user or "Fernan" in user or "Deadpool" in user or "Koki1" in user):
        cant = event.raw_text.split("carry ")[1].split(".")[0]
        wait_time = random.randint(5, 10)
        await asyncio.sleep(wait_time)
        if user in trader:
            await intervine_users[user].send_message("chtwrsbot", f"/sc {trader[user]} {cant}")
        else:
            r = await intervine_users[user].get_messages("ScriptCWBot", limit=1)
            await intervine_users[user].send_message("chtwrsbot", f"/sc {r[0].raw_text} {cant}")


async def cw_eventCharacters3(user, event):
    if 'Ты заметил' in event.raw_text:
        wait_time = random.randint(5, 60)
        await asyncio.sleep(wait_time)
        await event.click(0)
    if 'You defended villagers well. In exchange for your help,' in event.raw_text:
        cant = event.raw_text.split("carry ")[1].split(".")[0]
        wait_time = random.randint(5, 10)
        await asyncio.sleep(wait_time)
        if user in trader:
            await intervine_users[user].send_message("ChatWarsBot", f"/sc {trader[user]} {cant}")
        else:
            r = await intervine_users[user].get_messages("ScriptCWBot", limit=1)
            await intervine_users[user].send_message("ChatWarsBot", f"/sc {r[0].raw_text} {cant}")



for user in usersCharacter:
    exec(cli_taskCharacters.format(user, "meCharacter"))
for user in usersCW3:
    exec(cli_taskCW3.format(user, "meService"))
for item in advisers:
    exec(adviser_task.format(item))
for i in intervine_users:
    exec(cli_taskIntervine.format(i))
#for item in alts_group:
#    exec(alts_group_task.format(item))


# Click bots
async def leave_channel_async(client_temp, channel):
    print('Entro1')
    await client_temp(LeaveChannelRequest(channel))


def leave_channel(client_temp, channel):
    print('Entro')
    loop.create_task(leave_channel_async(client_temp, channel))


mss = """
async def mss():
    for bot in bots:
        await client{0}.send_message(bot, messages[{1}])
client{0}.loop.run_until_complete(mss())
"""

click_bots = """for bot in bots:
    cantChannelsNew = 0
    @client{0}.on(events.NewMessage(chats=bot))
    async def new_message_event_click_bots{0}(event):
        if 'Press the "Message bot" botton below' in event.raw_text:
            try:
                if '.me/' in event.raw_text:
                    domain = event.raw_text[event.raw_text.index(".me/"):].split('\\n')[0].split('.me/')[1]
                    name_bot = domain.split('?start=')[0]
                    await client{0}(StartBotRequest(name_bot, name_bot, domain.split('?start=')[1]))
                else:
                    output = requests.get(event.buttons[0][0].url).text
                    print("var protoUrl" in output)
                    print("domain" in output)
                    print(output[output.index("var protoUrl"):].split('\\n')[0])
                    domain = output[output.index("var protoUrl"):].split('\\n')[0].split("domain=")[1][:-2].replace('&','?')
                    print(domain)
                    if domain.count('?') > 0:
                        name_bot = domain.split('?')[0]
                        await client{0}(StartBotRequest(name_bot, name_bot, domain.split('?')[1]))
                    else:
                        name_bot = domain
                        await client{0}.send_message(name_bot, '/start')
                    await client{0}(UpdateNotifySettingsRequest(name_bot, InputPeerNotifySettings(show_previews=False,
                                                                                              mute_until=datetime.datetime.now()+
                                                                                              timedelta(days=21))))
                    await asyncio.sleep(10)
                    messages_bot = await client{0}.get_messages(name_bot, limit=1)
                    if messages_bot[0].text != '/start':
                        await messages_bot[0].forward_to(bot)
                    else:
                        # await client{0}.send_message(name_bot, '/start')
                        await event.click(1, 1)
                    await client{0}.delete_dialog(name_bot)
            except Exception as e:
                await event.click(1, 1)
        elif 'Sorry, there are no new ads available' in event.raw_text:
            if 'bot' in event.raw_text:
                await client{0}.send_message(bot, messages[1])
            else:
                await client{0}.send_message(bot, messages[0], schedule=timedelta(hours=2))
        elif 'Press the "Go to channel" button below' in event.raw_text or \\
                'Press the "Go to group" button below' in event.raw_text:
            global cantChannelsNew
            print(cantChannelsNew)
            if cantChannelsNew < 10: 
                try:
                    output = requests.get(event.buttons[0][0].url).text
                    channel = output[output.index("var protoUrl"):].split('\\n')[0].split("domain=")[1][:-2]
                    print(channel)
                    await client{0}(JoinChannelRequest(channel))
                    await client{0}(UpdateNotifySettingsRequest(channel, InputPeerNotifySettings(show_previews=False,
                                                                                                 mute_until=datetime.datetime.now() +
                                                                                                 timedelta(days=21))))
                    cantChannelsNew = cantChannelsNew + 1
                except errors.UsernameInvalidError as e:
                    print(e.message)
                    await event.click(1, 1)
                except errors.FloodWaitError as e:
                    print(e.message)
                    # time.sleep(e.seconds)
                except Exception as e:
                    await event.click(1, 1)
                if cantChannelsNew < 10:   
                    await event.click(0, 1)
                    await asyncio.sleep(10)
                    messages_bot = await client{0}.get_messages(bot, limit=2)
                    if 'We cannot find you in the group' in messages_bot[1].text:
                        await event.click(1, 1)
                    elif 'Success' in messages_bot[1].text:
                        chhours: int = int(messages_bot[1].raw_text.split('at least ')[1].split(' ')[0])
                        loop.call_at(loop.time() + chhours*60*60, leave_channel, client{0}, channel)
                else:
                    cantChannelsNew = 0
                    await client{0}.send_message(bot, messages[0], schedule=timedelta(minutes=120))
        elif 'Press the "Visit website" button' in event.raw_text:
            # output = requests.get(event.buttons[0][0].url)
            print(event.buttons[0][0].url)
            webbrowser.open(event.buttons[0][0].url)
"""
# for i in range(num_users):
# exec(click_bots.format(2))
# exec(mss.format(2, 0))

loop.run_until_complete(f())
loop.run_forever()

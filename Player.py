from sqlalchemy import Integer, String, Boolean, Column, ForeignKey, text, create_engine, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
import os

Base = declarative_base()


class Permission(Base):
    __tablename__ = 'permission'
    id_permission = Column(Integer, primary_key=True)
    arena = Column(Boolean)
    quest = Column(Boolean)
    spend_hide = Column(Boolean)
    crafting = Column(Boolean)
    intervine = Column(Boolean)
    withdraw = Column(Boolean)
    orders = Column(Boolean)
    pet = Column(Boolean)

    def __init__(self, arena, quest, spend_hide, crafting, intervine, withdraw, orders, pet):
        self.arena = arena
        self.quest = quest
        self.spend_hide = spend_hide
        self.crafting = crafting
        self.intervine = intervine
        self.withdraw = withdraw
        self.orders = orders
        self.pet = pet

    def __repr__(self):
        text = "{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n{6}\n{7}\n{8}"
        return text.format(self.arena, self.quest, self.health, self.spend_hide, self.crafting,
                           self.intervine, self.withdraw, self.orders)


class PermissionGuilds(Base):
    __tablename__ = 'permission_guilds'
    id_permission_guild = Column(Integer, primary_key=True)
    id_telegram = Column(BigInteger)
    alch = Column(Boolean)
    misc = Column(Boolean)
    rec = Column(Boolean)
    parts = Column(Boolean)
    others = Column(Boolean)
    invite = Column(Boolean)

    def __init__(self, id_telegram, alch, misc, rec, parts, others, invite):
        self.id_telegram = id_telegram
        self.alch = alch
        self.misc = misc
        self.rec = rec
        self.parts = parts
        self.others = others
        self.invite = invite

    def __repr__(self):
        text = "{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n{6}\n{7}\n{8}"
        return text.format(self.id_telegram, self.alch, self.misc, self.rec, self.parts,
                           self.others, self.invite)


class Config(Base):
    __tablename__ = 'configs'
    id_config = Column(Integer, primary_key=True)
    monsters = Column(Boolean)
    monsters_on = Column(Boolean)
    min_hp = Column(Integer)
    cant_monsters = Column(Integer)
    quest = Column(Integer)
    prefered_time = Column(Integer)
    stamina_step = Column(Integer)
    resources_for_hide = Column(String)
    trader_on = Column(Boolean)
    trader_resource = Column(String)

    def __init__(self, monsters, monsters_on, min_hp, cant_monsters, quest, prefered_time, stamina_step,
                 resources_for_hide, trader_on, trader_resource):
        self.monsters = monsters
        self.monsters_on = monsters_on
        self.min_hp = min_hp
        self.cant_monsters = cant_monsters
        self.quest = quest
        self.prefered_time = prefered_time
        self.stamina_step = stamina_step
        self.resources_for_hide = resources_for_hide
        self.trader_on = trader_on
        self.trader_resource = trader_resource

    def __repr__(self):
        text = "{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n{6}\n{7}\n{8}\n{9}"
        return text.format(self.monsters, self.monsters_on, self.min_hp, self.cant_monsters, self.quest,
                           self.prefered_time, self.stamina_step, self.resources_for_hide, self.trader_on,
                           self.trader_resource)


class Player(Base):
    __tablename__ = 'players'
    id_player = Column(Integer, primary_key=True)
    id_telegram = Column(BigInteger)
    name = Column(String)
    level = Column(Integer)
    health = Column(Integer)
    total_health = Column(Integer)
    stamina = Column(Integer)
    total_stamina = Column(Integer)
    stamina_reg_time = Column(Integer)
    money = Column(Integer)
    cant_arenas = Column(Integer)
    config_id = Column(Integer, ForeignKey('configs.id_config'))
    config = relationship(Config, backref=backref('players', order_by=id_player))
    permission_id = Column(Integer, ForeignKey('permission.id_permission'))
    permission = relationship(Permission, backref=backref('players', order_by=id_player))

    def __init__(self, id_telegram, name, level, health, total_health, stamina, total_stamina, stamina_reg_time, money,
                 cant_arenas, config, permission):
        self.id_telegram = id_telegram
        self.name = name
        self.level = level
        self.health = health
        self.total_health = total_health
        self.stamina = stamina
        self.total_stamina = total_stamina
        self.stamina_reg_time = stamina_reg_time
        self.money = money
        self.cant_arenas = cant_arenas
        self.config = config
        self.permission = permission

    def __repr__(self):
        text = "{0}\n{1}\n{2}\n{3}\n{4}\n{5}\n{6}\n{7}\n{8}"
        return text.format(self.name, self.level, self.health, self.total_health, self.stamina,
                           self.total_stamina, self.stamina_reg_time, self.money, self.cant_arenas)


DATABASE_URL = os.environ['DATABASE_URL']
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

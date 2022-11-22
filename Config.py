from sqlalchemy import Integer, String, Boolean, Column, ForeignKey, text, create_engine
from sqlalchemy.ext.declarative import declarative_base
import os

Base = declarative_base()


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


DATABASE_URL = os.environ['DATABASE_URL']
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)

#encoding: utf-8

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import *

SQLALCHEMY_ENGINE_STR = 'mysql://root:mysql@127.0.0.1/bizkaisense'
#SQLALCHEMY_ENGINE_STR = 'sqlite:///bizkaisense.db'

engine = create_engine(SQLALCHEMY_ENGINE_STR, convert_unicode=True, pool_recycle=3600)

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind = engine)

'''Session = sessionmaker(bind = engine)
session = Session()

station = Station(code="asa", name="adss", municipality="adss", province="adss", url="adss", lat="adss", lng="adss", address="adss", geonames="adss", uri="adss")
session.add(station)

termtype = TermType(name="hooo")

prop = Property(ontology_uri="asdsa", name="sdsad", termtype=termtype)
session.add(prop)

#station.properties.append(prop)
prop.stations.append(station)

#print session.query(Property).filter_by(ontology_uri="asdsa", name="sdsad").first().stations

#print session.query(Station).filter_by(code="asa", name="adss").all()[-1].id

#station2 = Station(code="asa", name="adss", municipality="adss", province="adss", url="adss", lat="adss", lng="adss", address="adss", geonames="adss", uri="adss")
#session.merge(station2)

session.commit()

#print session.query(Station).filter_by(code="asa", name="adss").all()[-1].id

session.close()'''

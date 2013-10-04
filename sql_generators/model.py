from sqlalchemy import Column, Integer, Unicode, Float, DateTime, ForeignKey, UniqueConstraint, Boolean, Table
from sqlalchemy.orm import relation, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Many to many relation table
station_measured_props = Table('StationMeasuredProps', Base.metadata,
    Column('station_id', Integer, ForeignKey('Stations.id'), primary_key=True),
    Column('prop_id', Integer, ForeignKey('Properties.id'), primary_key=True)
    )

class DataType(Base):
	__tablename__ = 'Datatypes'

	id = Column(Integer, primary_key = True)
	uri = Column(Unicode(400))

	def __init__(self, uri):
		self.uri = uri

class Unit(Base):
	__tablename__ = 'Units'

	id = Column(Integer, primary_key = True)
	uri = Column(Unicode(400))

	def __init__(self, uri):
		self.uri = uri

class TermType(Base):
	__tablename__ = 'TermTypes'

	id = Column(Integer, primary_key = True)
	name = Column(Unicode(50))

	def __init__(self, name):
		self.name = name

class Station(Base):
	__tablename__ = 'Stations'

	id = Column(Integer)
	code = Column(Unicode(10), index=True, primary_key=True)
	name = Column(Unicode(50))
	municipality = Column(Unicode(50))
	province = Column(Unicode(50))
	url = Column(Unicode(200))
	lat = Column(Unicode(15))
	lng = Column(Unicode(15))
	address = Column(Unicode(200))
	geonames = Column(Unicode(50))
	uri = Column(Unicode(400))

	# Many to many relation
	properties = relation("Property", secondary=station_measured_props, backref="stations")

	def __init__(self):
		pass

	def __init__(self, code, name, municipality, province, url, lat, lng, address, geonames, uri):
		self.code = code
		self.name = name
		self.municipality = municipality
		self.province = province
		self.url = url
		self.lat = lat
		self.lng = lng
		self.address = address
		self.geonames = geonames
		self.uri = uri

class Property(Base):
	__tablename__ = 'Properties'

	id = Column(Integer, primary_key = True)
	ontology_uri = Column(Unicode(400))
	name = Column(Unicode(50))

	termtype_id = Column(Integer, ForeignKey('TermTypes.id'), nullable = False)
	termtype = relation(TermType.__name__, backref = backref('termtypes', order_by=id, cascade = 'all,delete'))
	
	def __init__(self, ontology_uri, name, termtype):
		self.ontology_uri = ontology_uri
		self.name = name
		self.termtype = termtype

class Observation(Base):
	__tablename__ = 'Observations'

	id = Column(Integer, primary_key = True)
	date = Column(DateTime, index = True)
	value = Column(Unicode(20))
	uri = Column(Unicode(400))

	station_id = Column(Integer, ForeignKey('Stations.id'), nullable = False)
	station = relation(Station.__name__, backref = backref('stations', order_by=id, cascade = 'all,delete'))

	prop_id = Column(Integer, ForeignKey('Properties.id'), nullable = False)
	prop = relation(Property.__name__, backref = backref('properties', order_by=id, cascade = 'all,delete'))

	datatype_id = Column(Integer, ForeignKey('Datatypes.id'), nullable = False)
	datatype = relation(DataType.__name__, backref = backref('datatypes', order_by=id, cascade = 'all,delete'))

	unit_id = Column(Integer, ForeignKey('Units.id'), nullable = False)
	unit = relation(Unit.__name__, backref = backref('units', order_by=id, cascade = 'all,delete'))

	def __init__(self, date, value, station, prop, datatype, unit, uri):
		self.date = date
		self.value = value
		self.station = station
		self.prop = prop
		self.datatype = datatype
		self.unit = unit
		self.uri = uri

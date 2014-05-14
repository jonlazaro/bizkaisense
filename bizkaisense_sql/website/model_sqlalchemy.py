from sqlalchemy import Column, Integer, Unicode, DateTime, ForeignKey, Table
from sqlalchemy.orm import relation, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Many to many relation table
station_measured_props = Table('StationMeasuredProps', Base.metadata,
    Column('station_id', Integer, ForeignKey('Stations.code'), primary_key=True),
    Column('prop_id', Integer, ForeignKey('Properties.name'), primary_key=True)
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

    id = Column(Integer)
    ontology_uri = Column(Unicode(400))
    name = Column(Unicode(50), primary_key = True)
    unit = Column(Unicode(400))

    termtype_id = Column(Integer, ForeignKey('TermTypes.id'), nullable = False)
    termtype = relation(TermType.__name__, backref = backref('termtypes', order_by=id, cascade = 'all,delete'))

    def __init__(self, ontology_uri, name, unit, termtype):
        self.ontology_uri = ontology_uri
        self.name = name
        self.unit = unit
        self.termtype = termtype

class Observation(Base):
	__tablename__ = 'Observations'

	id = Column(Integer, primary_key = True)
	date = Column(DateTime, index = True)
	value = Column(Unicode(20))
	#uri = Column(Unicode(400))

	station_id = Column(Integer, ForeignKey('Stations.code'), nullable = False)
	station = relation(Station.__name__, backref = backref('stations', order_by=id, cascade = 'all,delete'))

	prop_id = Column(Integer, ForeignKey('Properties.name'), nullable = False)
	prop = relation(Property.__name__, backref = backref('properties', order_by=id, cascade = 'all,delete'))

	#datatype_id = Column(Integer, ForeignKey('Datatypes.id'), nullable = False)
	#datatype = relation(DataType.__name__, backref = backref('datatypes', order_by=id, cascade = 'all,delete'))

	#unit_id = Column(Integer, ForeignKey('Units.id'), nullable = False)
	#unit = relation(Unit.__name__, backref = backref('units', order_by=id, cascade = 'all,delete'))

	def __init__(self, date, value, station, prop, datatype, unit, uri):
		self.date = date
		self.value = value
		self.station = station
		self.prop = prop
		#self.datatype = datatype
		#self.unit = unit
		#self.uri = uri

'''class WaterZone(Base):
	__tablename__ = 'WaterZone'

	id = Column(Integer, primary_key = True)
	zona = Column(Unicode(50))

	def __init__(self, zona):
		self.zona = zona'''


class WaterSample(Base):
	__tablename__ = 'WaterSample'

	id = Column(Integer, primary_key = True)

	fecha = Column(DateTime, index = True)
	parametro = Column(Unicode(50))
	provincia = Column(Unicode(50))
	municipio = Column(Unicode(50))
	localidad = Column(Unicode(50))
	zona = Column(Unicode(100))
	punto_muestreo = Column(Unicode(100))
	tipo_punto = Column(Unicode(50))
	laboratorio = Column(Unicode(100))
	elemento = Column(Unicode(100))
	tipo_analisis = Column(Unicode(50))
	motivo = Column(Unicode(50))
	calificacion = Column(Unicode(100))
	resultado = Column(Unicode(50))
	valor_parametrico = Column(Unicode(50))
	unidad = Column(Unicode(50))

	def __init__(self, fecha, parametro, provincia, municipio, localidad, zona, punto_muestreo, tipo_punto, laboratorio, elemento, tipo_analisis, motivo, calificacion, resultado, valor_parametrico, unidad):

		self.fecha = fecha
		self.parametro = parametro
		self.provincia = provincia
		self.municipio = municipio
		self.localidad = localidad
		self.zona = zona
		self.punto_muestreo = punto_muestreo
		self.tipo_punto = tipo_punto
		self.laboratorio = laboratorio
		self.elemento = elemento,
		self.tipo_analisis = tipo_analisis
		self.motivo = motivo
		self.calificacion = calificacion
		self.resultado = resultado
		self.valor_parametrico = valor_parametrico
		self.unidad = unidad;

class WaterSource(Base):
	__tablename__ = 'WaterSource'

	id = Column(Integer, primary_key = True)

	provincia = Column(Unicode(50))
	municipio = Column(Unicode(50))
	localidad = Column(Unicode(50))
	zona = Column(Unicode(100))
	latitud = Column(Unicode(15))
	longitud = Column(Unicode(15))
	altitud = Column(Unicode(15))
	tipo_elemento = Column(Unicode(50))
	captacion = Column(Unicode(200))
	fluoracion = Column(Unicode(15))

	def __init__(self, provincia, municipio, localidad, zona, latitud, longitud, altitud, tipo_elemento, captacion, fluoracion):
		self.provincia = provincia
		self.municipio = municipio
		self.localidad = localidad
		self.zona = zona
		self.latitud = latitud
		self.longitud = longitud
		self.altitud = altitud
		self.tipo_elemento = tipo_elemento
		self.captacion = captacion
		self.fluoracion = fluoracion
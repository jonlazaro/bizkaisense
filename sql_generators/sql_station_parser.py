# encoding: utf-8

import urllib
import urllib2
import re
import csv
import simplejson
import os

from BeautifulSoup import BeautifulSoup

import pyproj

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import *

here = os.path.dirname(__file__)

#CSV_PATH = here + '/stations/estacionesnuevas.csv'
CSV_PATH = 'stations/estacionesnuevas.csv'

STATION_RESOURCE_URI = 'http://helheim.deusto.es/bizkaisense/resource/station/'
SQLALCHEMY_ENGINE_STR = 'mysql://root:mysql@localhost/bizkaisense'
#SQLALCHEMY_ENGINE_STR = 'sqlite:///bizkaisense.db'

engine = create_engine(SQLALCHEMY_ENGINE_STR, convert_unicode=True, pool_recycle=3600)
#engine.raw_connection().connection.text_factory = str

Session = sessionmaker(bind = engine)
session = Session()

#Function for encoding strings in 'latin-1' format as UTF-8, avoiding errors with special characters
def utf8encoding(badstr):
	return badstr.decode('latin-1').encode('utf-8')

#Function for formating codes as it's needed
def formatCod(cod):
	cod = re.split('\&', cod)[0]
	cod = cod.replace('ñ', 'n')
	cod = cod.replace('Ñ', 'N')
	return cod

def get_geonames_uri(lat, lng):
	try:
		json = simplejson.load(urllib.urlopen("http://api.geonames.org/findNearbyPlaceNameJSON?lat=" + str(lat) + "&lng=" + str(lng) + "&username=morelab"))
		return "http://www.geonames.org/" + str(json['geonames'][0]['geonameId'])
	except:
		return None

def transform_utm_to_ll(utm_x, utm_y):
	# Transformation from UTM to Spherical Mercator, and from SM to Lat Long (WGS84) with "pyproj"
	utm = pyproj.Proj(init='epsg:23030')
	sm = pyproj.Proj(init='epsg:3785')
	wgs = pyproj.Proj(init='epsg:4326')
	sm_x, sm_y = pyproj.transform(utm, sm, utm_x, utm_y)
	lng, lat = pyproj.transform(sm, wgs, sm_x, sm_y)
	return lat, lng


#Function for generating RDFs for Stations with the details gotten from given CSV
def generate_stations():
	with open(CSV_PATH, 'r') as stdoc:
		#Each line of CSV represents an station. Content of each line: OBJECTID, IDEST, NAME, DIR, POBL, URL, ZONE, URL_ZONE, PROV_COD,..., XUTM, YUTM
		reader = csv.reader(stdoc, delimiter=';', quoting=csv.QUOTE_NONE)
		for details in reader:
			#It only saves an station if it has an URL (details[5])
			if ("http://" in details[5]):
				lat = None
				lng = None

				#Get codes and format as needed
				cod = re.sub('CodEst=', '', re.findall('CodEst=.+\&', details[5])[0])
				cod = formatCod(cod = utf8encoding(cod))
				codzone = re.sub('CodZona=\@', '', re.findall('CodZona=\@.+\&', details[5])[0])
				codzone = formatCod(cod = utf8encoding(codzone))

				utm_x, utm_y = float(details[-2].replace(',', '.')), float(details[-1].replace(',', '.'))
				lat, lng = transform_utm_to_ll(utm_x, utm_y)

				if cod == "ZUMARR":
					lat = float(43.08395)
					lng = float(-2.315733)

				#Get internal id
				id = re.split(',', details[1])[0]

				geonamesuri = get_geonames_uri(lat=lat, lng=lng)

				#Get and format url (quote) avoiding errors with special characters
				url = utf8encoding(details[5])
				url = url[:-1] if url[-1] == '"' else url
				url = "http:" + urllib.quote(url[5:])

				#Get address and province
				try:
					address = utf8encoding(details[3])
				except:
					address = None

				prov = utf8encoding(details[8])

				zonedesc = utf8encoding(details[6])

				# Create station
				if cod.find("BETO") == -1:
					station = Station(code=cod, name=utf8encoding(details[2]), municipality=utf8encoding(details[4]), province=prov, url=url, lat=str(lat), lng=str(lng), address=address, geonames=geonamesuri, uri=STATION_RESOURCE_URI + cod)
					session.add(station)
					print cod + " object created."
			else:
				pass#print "SIN WEB: " + details[2].decode('latin-1').encode('utf-8')

def generate_missing_stations():
	lat, lng = 43.285890624612605, -2.0001983642578125
	station = Station(code="ANORGA", name="Añorga", municipality="Donostia", province="GIPUZKOA", url="http://www.ingurumena.ejgv.euskadi.net/r49-n82/es/vima_ai_vigilancia/estaciones.apl?CodZona=@DONOS&CodEst=A%D1ORGA&lenguaje=C", lat=str(lat), lng=str(lng), address=None, geonames=get_geonames_uri(lat=lat, lng=lng), uri=STATION_RESOURCE_URI + "ANORGA")
	session.add(station)
	print "ANORGA object created."

	lat, lng = transform_utm_to_ll(537791.53, 4775458.32)
	station = Station(code="ELORIO", name="Elorrio", municipality="Elorrio", province="BIZKAIA", url="http://www.ingurumena.ejgv.euskadi.net/r49-n82/es/vima_ai_vigilancia/estaciones.apl?CodZona=@IBDEB&CodEst=ELORIO&lenguaje=C", lat=str(lat), lng=str(lng), address="C/Padura s/n, Elorrio", geonames=get_geonames_uri(lat=lat, lng=lng), uri=STATION_RESOURCE_URI + "ELORIO")
	session.add(station)
	print "ELORIO object created."

	lat, lng = transform_utm_to_ll(528629.73, 4746400.9)
	station = Station(code="BETONO", name="Betoño", municipality="Vitoria-Gasteiz", province="ARABA", url="http://www.ingurumena.ejgv.euskadi.net/r49-n82/es/vima_ai_vigilancia/estaciones.apl?CodZona=@LLALV&codest=BETO%D1O&lenguaje=c", lat=str(lat), lng=str(lng), address=None, geonames=get_geonames_uri(lat=lat, lng=lng), uri=STATION_RESOURCE_URI + "BETONO")
	session.add(station)
	print "BETONO object created."

	lat, lng = transform_utm_to_ll(504952.62, 4789929.93)
	station = Station(code="INDAUC", name="Indautxu Reubicada", municipality="Bilbao", province="BIZKAIA", url="http://www.ingurumena.ejgv.euskadi.net/r49-n82/es/vima_ai_vigilancia/estaciones.apl?CodZona=@BJNVN&codest=INDAUC&lenguaje=c", lat=str(lat), lng=str(lng), address="Plaza Indautxu s/n, Bilbao", geonames=get_geonames_uri(lat=lat, lng=lng), uri=STATION_RESOURCE_URI + "INDAUC")
	session.add(station)
	print "INDAUC object created."

	lat, lng = transform_utm_to_ll(501909.51, 4792781.51)
	station = Station(code="MUNOA", name="CEP Munoa LHI", municipality="Barakaldo", province="BIZKAIA", url="http://www.ingurumena.ejgv.euskadi.net/r49-n82/es/vima_ai_vigilancia/estaciones.apl?CodZona=@BJNVN&CodEst=MUNOA&lenguaje=c", lat=str(lat), lng=str(lng), address="Llano,55-Lutxana, Barakaldo", geonames=get_geonames_uri(lat=lat, lng=lng), uri=STATION_RESOURCE_URI + "MUNOA")
	session.add(station)
	print "MUNOA object created."

	lat, lng = 43.332779, -3.111966
	station = Station(code="SANJUL", name="San Julián", municipality="Muskiz", province="BIZKAIA", url="http://www.ingurumena.ejgv.euskadi.net/r49-n82/es/vima_ai_vigilancia/estaciones.apl?CodZona=@KOSTA&CodEst=SANJUL&lenguaje=C", lat=str(lat), lng=str(lng), address=None, geonames=get_geonames_uri(lat=lat, lng=lng), uri=STATION_RESOURCE_URI + "SANJUL")
	session.add(station)
	print "SANJUL object created."

# Call to the function
generate_stations()
generate_missing_stations()

# Save in DB
print "Saving into DB..."
session.commit()
print "Done!"
session.close()

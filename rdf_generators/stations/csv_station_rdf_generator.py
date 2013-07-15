# encoding: utf-8

import urllib
import urllib2
import re
import csv
import simplejson

from BeautifulSoup import BeautifulSoup

import sys
sys.path.append('../lib/')
from station import Station
from utmll import UTMtoLL
import pyproj

#RESOURCE_URI = "http://dev.morelab.deusto.es/bizkaisense/resource/"
#RESOURCE_URI = "http://192.168.59.116/resource/"
RESOURCE_URI = "http://helheim.deusto.es/bizkaisense/resource/"
CSV_PATH = "estacionesnuevas.csv"

#If you put ST_PATH to None, it inserts automatically in sparql endpoint at VIRTUOSO_URL.
#If you put a path, it creates a RDF file for each medition in given path.
#ST_PATH = "rdf/stations/"
ST_PATH = None
#If ST_PATH is used, VIRTUOSO_URL isn't needed
#VIRTUOSO_URL = "http://dev.morelab.deusto.es/bizkaisense/sparql"
VIRTUOSO_URL = "http://helheim.deusto.es:8890/sparql"
#VIRTUOSO_URL = "http://192.168.59.116:8890/sparql"



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

#Function for generating RDFs for Stations with the details gotten from given CSV
def generateRDFs():
	with open(CSV_PATH, 'r') as stdoc:
		#Each line of CSV represents an station. Content of each line: OBJECTID, IDEST, NAME, DIR, POBL, URL, ZONE, URL_ZONE, PROV_COD,..., XUTM, YUTM
		reader = csv.reader(stdoc, delimiter=';', quoting=csv.QUOTE_NONE)
		for details in reader:
			#It only saves an station if it has an URL (details[5])
			if ("http://" in details[5]):
				lat = None
				lng = None

				#Call to "utmll" library for converting from UTM to LatLng coordinates
				#lat, lng = UTMtoLL(23, float(details[-2].replace(',', '.')), float(details[-1].replace(',', '.')), "30T")

				#Transformation from UTM to Spherical Mercator, and from SM to Lat Long (WGS84) with "pyproj"
				utm = pyproj.Proj(init='epsg:23030')
				sm = pyproj.Proj(init='epsg:3785')
				wgs = pyproj.Proj(init='epsg:4326')
				sm_x, sm_y = pyproj.transform(utm, sm, float(details[-2].replace(',', '.')), float(details[-1].replace(',', '.')))
				lng, lat = pyproj.transform(sm, wgs, sm_x, sm_y)

				#Get codes and format as needed
				cod = re.sub('CodEst=', '', re.findall('CodEst=.+\&', details[5])[0])
				cod = formatCod(cod = utf8encoding(cod))
				codzone = re.sub('CodZona=\@', '', re.findall('CodZona=\@.+\&', details[5])[0])
				codzone = formatCod(cod = utf8encoding(codzone))

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

				print utf8encoding(details[2])

				#Create station
				station = Station(cod=cod, codzone=codzone, id=id, name=utf8encoding(details[2]), location=utf8encoding(details[4]), url=url, lat=lat, lng=lng, address=address, prov=prov, zonedesc=zonedesc, geonames=geonamesuri)

				#Generate all RDFs
				sparql = None
				path = None
				if ST_PATH:
					path = ST_PATH + station.internal_id + "_" + station.cod + "_at_" + station.codzone + ".rdf"
				else:
					sparql = VIRTUOSO_URL

				if cod.find("BETO") == -1:
					station.generateRDF(resourceuri=RESOURCE_URI, sparql=sparql, path=path)
			else:
				pass#print "SIN WEB: " + details[2].decode('latin-1').encode('utf-8')

def generateMissingRDFs():
	lat, lng = 43.285890624612605, -2.0001983642578125
	station = Station(cod="ANORGA", codzone="DONOS", id=100, name="Añorga", location="Donostia", url="http://www.ingurumena.ejgv.euskadi.net/r49-n82/es/vima_ai_vigilancia/estaciones.apl?CodZona=@DONOS&CodEst=A%D1ORGA&lenguaje=C", lat=lat, lng=lng, address=None, prov="GIPUZKOA", zonedesc="Donostialdea", geonames=get_geonames_uri(lat=lat, lng=lng))
	station.generateRDF(resourceuri=RESOURCE_URI, sparql=VIRTUOSO_URL, path=None)

	lat, lng = UTMtoLL(23, 537791.53, 4775458.32, "30T")
	station = Station(cod="ELORIO", codzone="IBDEB", id=51, name="Elorrio", location="Elorrio", url="http://www.ingurumena.ejgv.euskadi.net/r49-n82/es/vima_ai_vigilancia/estaciones.apl?CodZona=@IBDEB&CodEst=ELORIO&lenguaje=C", lat=lat, lng=lng, address=None, prov="BIZKAIA", zonedesc="Ibaizabal-Alto Deba/Ibaizabal-Deba garaia", geonames=get_geonames_uri(lat=lat, lng=lng))
	station.generateRDF(resourceuri=RESOURCE_URI, sparql=VIRTUOSO_URL, path=None)

	lat, lng = UTMtoLL(23, 528629.73, 4746400.9, "30T")
	station = Station(cod="BETONO", codzone="LLALV", id=19, name="Betoño", location="Vitoria-Gasteiz", url="http://www.ingurumena.ejgv.euskadi.net/r49-n82/es/vima_ai_vigilancia/estaciones.apl?CodZona=@LLALV&codest=BETO%D1O&lenguaje=c", lat=lat, lng=lng, address="Portal de Vergara,10", prov="ARABA", zonedesc="Llanada Alavesa/Arabako lautada", geonames=get_geonames_uri(lat=lat, lng=lng))
	station.generateRDF(resourceuri=RESOURCE_URI, sparql=VIRTUOSO_URL, path=None)

	lat, lng = UTMtoLL(23, 504952.62, 4789929.93, "30T")
	station = Station(cod="INDAUC", codzone="BJNVN", id=35, name="Indautxu Reubicada", location="Bilbao", url="http://www.ingurumena.ejgv.euskadi.net/r49-n82/es/vima_ai_vigilancia/estaciones.apl?CodZona=@BJNVN&codest=INDAUC&lenguaje=c", lat=lat, lng=lng, address=None, prov="BIZKAIA", zonedesc="Bajo Nervión/Nerbioi behera", geonames=get_geonames_uri(lat=lat, lng=lng))
	station.generateRDF(resourceuri=RESOURCE_URI, sparql=VIRTUOSO_URL, path=None)

#Call to the function
generateRDFs()
generateMissingRDFs()

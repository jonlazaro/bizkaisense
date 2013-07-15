# encoding: utf-8

import urllib
import urllib2
import re
import simplejson

from BeautifulSoup import BeautifulSoup
from rdflib import Namespace, BNode, Literal, URIRef, Graph, ConjunctiveGraph, RDF
from rdflib.plugins.memory import IOMemory
from datetime import datetime, timedelta


import sys
sys.path.append('../lib/')
from rdf_parser import insertGraph


#VIRTUOSO_URL = "http://dev.morelab.deusto.es/bizkaisense/sparql"
VIRTUOSO_URL = "http://helheim.deusto.es:8890/sparql"
RESOURCE_URI = "http://dev.morelab.deusto.es/bizkaisense/resource/"
ENDPOINT_URL = VIRTUOSO_URL + "?query="
#If you put OBS_PATH to None, it inserts automatically in sparql endpoint at VIRTUOSO_URL.
#If you put a path, it creates a RDF file for each medition in given path.
OBS_PATH = "rdf/"
#OBS_PATH = None

#Cookie enable url opener
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor)

imposibleconns = []
done = []
lilifor = []

def get_info(prop):
    if prop == 'Temperatura' or prop == 'TemperaturaJaizkibel' or prop == 'Temp' or prop == 'T':
        return 'http://sweet.jpl.nasa.gov/2.3/propTemperature.owl#Temperature', 'http://purl.oclc.org/NET/muo/ucum/unit/temperature/degree-Celsius', 'Class', 'http://www.w3.org/2001/XMLSchema#integer', 'Temp'
    elif prop == 'Radiacion' or prop == 'RS' or prop == 'Rad':
        return 'http://sweet.jpl.nasa.gov/2.3/matrIsotope.owl#Radiation', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#watt-per-meter-squared', 'Class', 'http://www.w3.org/2001/XMLSchema#float', 'Rad'
    elif prop.encode("utf-8") == 'Radiación' or prop == 'RadUV':
        return 'http://sweet.jpl.nasa.gov/2.3/stateSpectralBand.owl#Ultraviolet', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#milliwatt-per-meter-squared', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'UVRad'
    elif prop == 'DV' or prop == 'Dir_Viento' or prop == 'DirV':
        return 'http://purl.oclc.org/NET/ssnx/meteo/WM30#WindDirection', 'http://purl.oclc.org/NET/muo/ucum/unit/plane-angle/degree', 'Class', 'http://www.w3.org/2001/XMLSchema#integer', 'DirV'
    elif prop == 'Humedad' or prop == 'HR' or prop == 'Humed':
        return 'http://sweet.jpl.nasa.gov/2.3/propFraction.owl#Humidity', 'http://purl.oclc.org/NET/muo/ucum/unit/fraction/percent', 'Class', 'http://www.w3.org/2001/XMLSchema#integer', 'Humedad'
    elif prop == 'O3' or prop == 'Ozono':
        return 'http://sweet.jpl.nasa.gov/2.3/matrElementalMolecule.owl#O3', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#integer', 'O3'
    elif prop == 'NO2':
        return 'http://sweet.jpl.nasa.gov/2.3/matrCompound.owl#NO2', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#integer', 'NO2'
    elif prop == 'Humos' or prop == 'HN':
        return 'http://sweet.jpl.nasa.gov/2.3/matrAerosol.owl#Smoke', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Class', 'http://www.w3.org/2001/XMLSchema#float', 'Humos'
    elif prop == 'SH2':
        return 'http://dev.morelab.deusto.es/bizkaisense/sweetAll-extended.owl#HydrogenSulfide', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-metre', 'Instance', 'http://www.w3.org/2001/XMLSchema#integer', 'SH2'
    elif prop == 'NO':
        return 'http://sweet.jpl.nasa.gov/2.3/matrCompound.owl#NO', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#integer', 'NO'
    elif prop == 'HC met.' or prop == 'HCMet':
        return 'http://sweet.jpl.nasa.gov/2.3/matrOrganicCompound.owl#CH4', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#milligram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'CH4'
    elif prop == 'HC no met.' or prop == 'HCNoMet':
    	return 'http://sweet.jpl.nasa.gov/2.3/matrOrganicCompound.owl#NMHC', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#milligram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'NMHC'
    elif prop == 'HC':
        return 'http://sweet.jpl.nasa.gov/2.3/matrOrganicCompound.owl#HC', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#milligram-per-cubic-meter', 'Class', 'http://www.w3.org/2001/XMLSchema#float', 'HC'
    elif prop == 'X-Xileno' or prop == 'Ortoxileno':
        return 'http://sweet.jpl.nasa.gov/2.3/matrOrganicCompound.owl#Xylene', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'Xileno'
    elif prop == 'Tolueno':
        return 'http://sweet.jpl.nasa.gov/2.3/matrOrganicCompound.owl#Toluene', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'Tolueno'
    elif prop == 'Benceno':
        return 'http://sweet.jpl.nasa.gov/2.3/matrOrganicCompound.owl#Benzene', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'Benceno'
    elif prop == 'PM25' or prop == 'PM2_5' or prop == 'PM2.5':
        return 'http://sweet.jpl.nasa.gov/2.3/matrAerosol.owl#PM2point5', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Class', 'http://www.w3.org/2001/XMLSchema#integer', 'PM25'
    elif prop == 'Vel_Viento' or prop == 'Velo_Viento' or prop == 'VV' or prop == 'VelV':
        return 'http://sweet.jpl.nasa.gov/2.3/propSpeed.owl#WindSpeed', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#meter-per-second', 'Class', 'http://www.w3.org/2001/XMLSchema#float', 'VelV'
    elif prop == 'CO':
        return 'http://sweet.jpl.nasa.gov/2.3/matrCompound.owl#CO', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'CO'
    elif prop == 'SO2':
        return 'http://sweet.jpl.nasa.gov/2.3/matrCompound.owl#SO2', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#integer', 'SO2'
    elif prop == 'NH3':
        return 'http://sweet.jpl.nasa.gov/2.3/matrCompound.owl#NH3', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance' , 'http://www.w3.org/2001/XMLSchema#float', 'NH3'
    elif prop == 'Etilbenceno':
        return 'http://dev.morelab.deusto.es/bizkaisense/sweetAll-extended.owl#Ethylbenzene', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'Etilbenceno'
    elif prop == 'PM10':
        return 'http://sweet.jpl.nasa.gov/2.3/matrAerosol.owl#PM10', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Class', 'http://www.w3.org/2001/XMLSchema#float', 'PM10'
    elif prop == 'Presion' or prop == 'P':
        return 'http://sweet.jpl.nasa.gov/2.3/propPressure.owl#BarometricPressure', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#millibar', 'Class' , 'http://www.w3.org/2001/XMLSchema#float', 'Presion'
    else:
        if prop not in lilifor:
        	lilifor.append(prop)


def getStations():
	stations = []

	prefixes = "PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns%23> \
				PREFIX geo: <http://www.w3.org/2003/01/geo/wgs84_pos%23> \
				PREFIX dc: <http://purl.org/dc/elements/1.1/> \
				PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema%23>"
	
	query = "SELECT DISTINCT ?cod ?url WHERE { \
				?s rdf:type <http://purl.oclc.org/NET/ssnx/ssn%23Sensor> . \
				?s dc:identifier ?cod .  \
				?s rdfs:seeAlso ?url . }"
	
	url = ENDPOINT_URL + prefixes + query + "&output=json"
	
	json = simplejson.load(urllib.urlopen(url))

	for st in json['results']['bindings']:
		station = {}
		station["cod"] = st['cod']['value']
		station["url"] = st['url']['value']
		
		if station["cod"] in ["ALGORT", "ALONSO", "ARRAIZ", "CASTRE", "ESMUN", "FARMAC"]:
			stations.append(station)
	
	return stations

def connection(url):
	print "Connecting to... " + url
	soup = None
	try:
		response = opener.open(url)
		data = response.read()
		soup = BeautifulSoup(data)
		soup.prettify()
		print "Connection OK"
		return soup
	except urllib2.HTTPError:
		print "ERROR in connection. Ignoring that station..."
		imposibleconns.append(url)
		return None
	except urllib2.URLError:
		print "ERROR! Trying again..."
		connection(url=url)


#Function for getting meditions RDF files by web-scrapping over stations' URL
def webScrapper():
	#Counter for amount of RDF files
	i = 0
	
	#Initial and final dates
	#init = datetime(2012, 01, 1)
	deltaday = timedelta(days=1)
	fin = datetime.now() - deltaday
	init = fin
	
	stations = getStations()

	for station in stations:
		typeslist = []
		if station["cod"] not in done:
			date = init
			done.append(station["cod"])
		else:
			date = fin + deltaday

		while (date <= fin):
			#Access and parse HTML
			url = station["url"] + "&Fecha=" + date.strftime('%m/%d/%Y')
			soup = connection(url)

			if (soup):
				#Start diving into HTML structure
				tables = soup.findAll('table')

				for table in tables:
					if (table.has_key('class') and table['class'] ==  "aizetable"):
						porhoras = False
						try:
							porhoras = str(table.caption.contents[0]) == "HORAS GMT"
						except:
							porhoras = False
						if porhoras:
							tds = table.findAll('td')
							dateday = date
							for td in tds:
								#td's order is: Type of medition + 24 values of different meditions
								if (td.has_key('valign') and td['valign'] == 'top'):
									#Type of medition
									dateday = date
									pallist = td.contents[0].split('(')[0].split(' ')
									pallist.remove(pallist[-1])
									if len(pallist) > 1:
										if pallist[0] == 'Rad':
											typeofobs = 'RadUV'
										elif pallist[0] == 'HC':
											typeofobs = 'HCMet' if pallist[1] == 'met' else 'HCNoMet'
									else:
										typeofobs = pallist[0]

									#obsunit = re.sub('\)', '', td.contents[0].split('(')[1])
									#obsunit = 'percent' if obsunit == '%' else obsunit
									
								else:
									#Medition values (if not valid: -1) -> Generate RDF
									medition = -1 if (td.contents[0] in [" ", "&nbsp;"]) else td.contents[0]

									#print str(medition) + ' ' + obsunit
									#str(medition) + ' ' + obsunit
									if medition != -1:
										observedprop, obsunit, typeofuri, xsdclass, uriprefix = get_info(typeofobs)

										if uriprefix not in typeslist:
											typeslist.append(uriprefix)

										generateMeditionRDF(medition=float(medition), typeofobs=observedprop, typeofuri=typeofuri, obsunit=obsunit, stationcod=station["cod"], dateday=dateday, uriprefix=uriprefix)
									dateday += timedelta(hours=1)
									i += 1
									#print i
			#Add a day to the date
			if url not in imposibleconns:
				date += deltaday
			else:
				date = fin + deltaday
				
	    #Update every station's "ssn:observes" properties
		#updateObservationProps(stationcod=station["cod"], typeslist=typeslist)
		print "Las PROPS que faltan son: "
		print lilifor
		print "Las ESTACIONES que petan son: "
		print imposibleconns
		print "FIN"

#Function for generating RDF files for meditions.
def updateObservationProps(stationcod, typeslist):
	for obstype in typeslist:
		uri = RESOURCE_URI + 'station/' + stationcod
	
		#Initialization of the graph
		ssn = Namespace("http://purl.oclc.org/NET/ssnx/ssn#")

		store = IOMemory()
	
		g = ConjunctiveGraph(store=store)
		g.bind("ssn", ssn)

		cpr = URIRef(uri)
		gpr = Graph(store=store, identifier=cpr)
	
		#Add data to the graph
		gpr.add((cpr, RDF.type, ssn['Sensor']))
		gpr.add((cpr, ssn['observes'], RESOURCE_URI + 'prop/' + obstype))
	
		#Update RDF
		print uri + ' | ' + obstype
		insertGraph(g=gpr, sparql=VIRTUOSO_URL, resourceuri=RESOURCE_URI)

def generateMeditionRDF(medition, typeofobs, typeofuri, obsunit, stationcod, dateday, uriprefix):
	'''  
		<?xml version="1.0"?>
			<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
			  xmlns:ssn="http://purl.oclc.org/NET/ssnx/ssn#"
			  xmlns:dc="http://purl.org/dc/elements/1.1/"
			  xmlns:xsd="http://www.w3.org/2001/XMLSchema"
			  xmlns:obs="http://www.bidei.com/resource/station/ZORRO2/1510211/02/N02#"
			  xmlns:dul="http://www.loa.istc.cnr.it/ontologies/DUL.owl#"
			  xmlns:owl="http://www.w3.org/2002/07/owl#"
			>

			  <ssn:Observation rdf:about="http://www.bidei.com/resource/station/ZORRO2/1510211/02/N02">
				<ssn:observedProperty rdf:resource="obs:property"/>
				<ssn:observationResult rdf:resource="obs:sensoroutput"/>
				<ssn:observedBy rdf:resource="http://www.bidei.com/resource/station/ZORRO2"/>
				<dc:date>1997-07-16T19:20+01:00</dc:date>
			  </ssn:Observation>

			  <ssn:Property rdf:about="obs:property>
				<owl:sameAs rdf:resource=" URI  a NASA Instance " />
			      OR
			    <rdf:type rdf:resource=" URI a NASA Class " />
			  </ssn:Property>
			  
			  <ssn:SensorOutput rdf:about="obs:sensoroutput">
				<ssn:hasValue rdf:resource="obs:outputvalue"/>
			  </ssn:SensorOutput>
			  
			  <ssn:ObservationValue rdf:about="obs:outputvalue">
		      	<dul:isClassifiedBy rdf:resource=" URI a Celsius, Farenheit, Microgramo/metro..."/>
				<ssn:hasQuantityValue rdf:datatype="xsd:float">0.98</ssn:hasQuantityValue>
			  </ssn:ObservationValue>
		</rdf:RDF>
	'''
	
	#.../station/ZORRO2/NO2/15022011/10
	uri = RESOURCE_URI + 'station/' + stationcod + "/" + uriprefix + dateday.strftime('/%d%m%Y/%H')
	
	#Initialization of graph
	ssn = Namespace("http://purl.oclc.org/NET/ssnx/ssn#")
	dc = Namespace("http://purl.org/dc/elements/1.1/")
	xsd = Namespace("http://www.w3.org/2001/XMLSchema")
	dul = Namespace("http://www.loa.istc.cnr.it/ontologies/DUL.owl#")
	owl = Namespace("http://www.w3.org/2002/07/owl#")
	obs = Namespace(uri + "#")

	store = IOMemory()
	
	g = ConjunctiveGraph(store=store)
	g.bind("ssn", ssn)
	g.bind("dc", dc)
	g.bind("xsd", xsd)
	g.bind("dul", dul)
	g.bind("owl", owl)
	g.bind("obs", obs)
	
	cpr = URIRef(uri)
	gpr = Graph(store=store, identifier=cpr)
	
	#Add data to the graph
	gpr.add((cpr, RDF.type, ssn['Observation']))
	
	gpr.add((cpr, ssn['observationResult'], obs["sensoroutput"]))

	gpr.add((cpr, ssn['observedProperty'], URIRef(RESOURCE_URI + 'prop/' + uriprefix)))

	gpr.add((cpr, ssn['observedBy'], URIRef(RESOURCE_URI + 'station/' + stationcod)))
	
	gpr.add((cpr, dc['date'], Literal(dateday.isoformat())))
	
	#SUBGRAPH1 (sensoroutput)
	cpr1 = obs["sensoroutput"]
	gpr.add((cpr1, RDF.type, ssn['SensorOutput']))
	gpr.add((cpr1, ssn['hasValue'], obs["outputvalue"]))
	
	#SUBGRAPH2 (outputvalue)
	cpr2 = obs["outputvalue"]
	gpr.add((cpr2, RDF.type, ssn['ObservationValue']))
	gpr.add((cpr2, dul['isClassifiedBy'], URIRef(obsunit)))
	gpr.add((cpr2, ssn['hasQuantityValue'], Literal(medition)))
	
	#Create RDF file
	if OBS_PATH:
		print gpr.serialize(format='pretty-xml')
		filename = "Med_" + dateday.strftime('%d_%m_%Y') + '.nt'
		f = open(OBS_PATH + filename, 'a')
		f.write(gpr.serialize(format='nt'))#'pretty-xml'))
		f.close()
	else:
		print "Inserting " + uri + "..."
		insertGraph(g=gpr, sparql=VIRTUOSO_URL, resourceuri=RESOURCE_URI)
		print "OK"

#Call to main function
webScrapper()

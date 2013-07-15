# encoding: utf-8

import urllib
import urllib2
import re

from rdflib import Namespace, BNode, Literal, URIRef, Graph, ConjunctiveGraph, RDF
from rdflib.plugins.memory import IOMemory
from BeautifulSoup import BeautifulSoup

import sys
sys.path.append('../lib/')
from rdf_parser import insertGraph


def unquotestr(strng):
	return strng[1:-1] if (strng and strng[0] == '"' and strng[-1] == '"') else strng

class Station():
	def __init__(self):
		pass

	def __init__(self, cod, codzone, id, name, location, url, lat, lng, address, prov, zonedesc, geonames):
		self.cod = cod
		self.codzone = codzone
		self.internal_id = id
		self.name = unquotestr(name)
		self.location = unquotestr(location)
		self.url = url
		self.lat = lat
		self.lng = lng
		self.address = unquotestr(address)
		self.province = unquotestr(prov)
		self.zonedesc = unquotestr(zonedesc)
		self.geonames = geonames

	def generateRDF(self, resourceuri, sparql=None, path=None):
		#print sparql
		'''  
			<?xml version="1.0"?>
				<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
				  xmlns:ssn="http://purl.oclc.org/NET/ssnx/ssn#"
				  xmlns:dc="http://purl.org/dc/elements/1.1/"
				  xmlns:xsd="http://www.w3.org/2001/XMLSchema"
				  xmlns:geo="http://www.w3.org/2003/01/geo/wgs84_pos#"
				  xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
				  xmlns:dul="http://www.loa.istc.cnr.it/ontologies/DUL.owl#"
				  xmlns:st="http://dev.morelab.deusto.es/bizkaisense/ZORRO2#"
				>

				<ssn:Sensor rdf:about="http://dev.morelab.deusto.es/bizkaisense/ZORRO2">
					<dc:identifier>EASO</rdfs:label>
					<dc:title>Easo</dc:title>
					<dc:description>Easo (EASO) @ Donostia (GUIPUZKOA)</rdfs:comment>
					<rdfs:seeAlso rdf:resource="http://www.ingurumena.ejgv.euskadi.net/r49-n82/es/vima_ai_vigilancia/estaciones.apl?CodZona=@DONOS&CodEst=EASO&lenguaje=c"/>
					<dul:hasLocation rdf:resource="st:point"/>
					<dul:nearTo rdf:resource="http://www.geonames.org/4654365"/>
				</ssn:Sensor>

				<geo:Point rdf:about="st:point">
					<geo:lat>43.3142945841</geo:lat>
					<geo:long>-1.97927578309</geo:long>	
				</geo:Point>
			</rdf:RDF>
		'''
	
		#.../station/ZORRO2/NO2/15022011/10
		uri = resourceuri + 'station/' + self.cod
	
		#Initialization of the graph
		ssn = Namespace("http://purl.oclc.org/NET/ssnx/ssn#")
		dc = Namespace("http://purl.org/dc/elements/1.1/")
		xsd = Namespace("http://www.w3.org/2001/XMLSchema")
		geo = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")
		rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
		foaf = Namespace("http://xmlns.com/foaf/0.1/")
		dul = Namespace("http://www.loa.istc.cnr.it/ontologies/DUL.owl#")
		st = Namespace(uri + "#")

		store = IOMemory()
	
		g = ConjunctiveGraph(store=store)
		g.bind("ssn", ssn)
		g.bind("dc", dc)
		g.bind("xsd", xsd)
		g.bind("geo", geo)
		g.bind("rdfs", rdfs)
		g.bind("foaf", foaf)
		g.bind("dul", dul)
		g.bind("st", st)
	
		cpr = URIRef(uri)
		gpr = Graph(store=store, identifier=cpr)
	
		#Add data to the graph
		gpr.add((cpr, RDF.type, ssn['Sensor']))

		gpr.add((cpr, dc['identifier'], Literal(str(self.cod))))

		gpr.add((cpr, dc['title'], Literal(str(self.name))))

		desc = str(self.name) + " (" + str(self.cod) + ") @ " + str(self.location) + " (" + str(self.zonedesc) + " (" + str(self.codzone) + ") - " + str(self.province) + ")"

		gpr.add((cpr, dc['description'], Literal(desc)))

		gpr.add((cpr, rdfs['seeAlso'], URIRef(self.url)))

		gpr.add((cpr, dul['hasLocation'], st["point"]))

		if self.geonames:
			gpr.add((cpr, dul['nearTo'], URIRef(self.geonames)))
	
		#SUBGRAPH1 (point)
		cpr1 = st["point"]
		gpr.add((cpr1, RDF.type, geo['Point']))
		if self.address:
			gpr.add((cpr1, dc['description'], Literal(str(self.address) + ", " + str(self.location))))
		gpr.add((cpr1, geo['lat'], Literal(self.lat)))
		gpr.add((cpr1, geo['long'], Literal(self.lng)))

		#img = self.__getStationImage()
		img = None
		if img:
			gpr.add((cpr, foaf['img'], URIRef(img)))
	
		#Create RDF file
		if not sparql:
			f = open(path, 'w')
			f.write(gpr.serialize(format='pretty-xml'))
			f.close()
		else:
			insertGraph(g=gpr, sparql=sparql, resourceuri=resourceuri)

	def __getStationImage(self):
		img = None

		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor)

		soup = None
		print "Connecting to " + self.url
		try:
			response = opener.open(self.url)
			data = response.read()
			soup = BeautifulSoup(data)
			soup.prettify()
			print "Connection OK"
		except urllib2.HTTPError:
			print "ERROR in connection"

		if (soup):
			img = str(soup)
			try:
				img = re.findall('[fF]oto\=.+\&amp\;lenguaje', img)[0]
				img = re.sub('([fF]oto\=\s?|\&amp\;lenguaje)', '', img)
				img = 'http://www.ingurumena.ejgv.euskadi.net' +  urllib.quote(img)
			except:
				img = None

		return img
	
	def __str__(self):
		return "Station " + str(self.cod) + ": " + str(self.lat) + " | " + str(self.lng)

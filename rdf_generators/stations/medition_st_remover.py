import urllib
import urllib2
import re
import simplejson
import csv

from BeautifulSoup import BeautifulSoup
from rdflib import Namespace, BNode, Literal, URIRef, Graph, ConjunctiveGraph, RDF
from rdflib.plugins.memory import IOMemory
from datetime import datetime, timedelta

import sys
sys.path.append('../lib/')
from virtuosordflib import VirtuosoManager

VIRTUOSO_URL = "http://helheim.deusto.es:8890/sparql"
RESOURCE_URI = "http://dev.morelab.deusto.es/bizkaisense/resource/"
ENDPOINT_URL = VIRTUOSO_URL + "?query="

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor)


def get_all_obs():
	query= "SELECT distinct ?a where {\
		 ?a <http://www.w3.org/1999/02/22-rdf-syntax-ns%23type> <http://purl.oclc.org/NET/ssnx/ssn%23Station> . }"

	url = ENDPOINT_URL + query + "&output=csv"
	
	print "connecting..."
	a = urllib.urlopen(url)
	print "ok"
	f = open("hola.csv", 'a')
	f.write(a.read())
	f.close()

	i = 0
	dale = False
	vm = VirtuosoManager(VIRTUOSO_URL)
	with open('hola.csv', 'r') as stdoc:
		reader = csv.reader(stdoc)
		for details in reader:
			#if details[0] == "http://dev.morelab.deusto.es/bizkaisense/resource/station/EUROPA/PM10/01012010/21":
			#	dale = True
			if i > 0:
				dale = True
			if dale:
				query = 'DELETE DATA {<' + details[0] + '> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.oclc.org/NET/ssnx/ssn#Station> }'
				vm.update(query, RESOURCE_URI)
				query = 'INSERT DATA {<' + details[0] + '> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.oclc.org/NET/ssnx/ssn#Observation> }'
				vm.update(query, RESOURCE_URI)
				print str(i) + ' - ' + details[0]
			i += 1
			

	#f.close()
	

get_all_obs()
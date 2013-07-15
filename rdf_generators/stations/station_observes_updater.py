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

#VIRTUOSO_URL = "http://helheim.deusto.es:8890/sparql"
VIRTUOSO_URL = "http://helheim.deusto.es:8892/sparql"
#RESOURCE_URI = "http://dev.morelab.deusto.es/bizkaisense/resource/"
RESOURCE_URI = "http://helheim.deusto.es/bizkaisense/resource/"
ENDPOINT_URL = VIRTUOSO_URL + "?query="

opener = urllib2.build_opener(urllib2.HTTPCookieProcessor)


def get_all_obs():
	query= "SELECT distinct ?a ?c where {\
		 ?a <http://www.w3.org/1999/02/22-rdf-syntax-ns%23type> <http://purl.oclc.org/NET/ssnx/ssn%23Sensor> . \
		 ?b <http://purl.oclc.org/NET/ssnx/ssn%23observedBy> ?a . \
		 ?b <http://purl.oclc.org/NET/ssnx/ssn%23observedProperty> ?c . }"

	url = ENDPOINT_URL + query + "&output=json"

	print "Resolving URL..."
	json = simplejson.load(urllib.urlopen(url))
	print "Done!"
	#f = open("allprop.n3", 'a')
	store = IOMemory()
	gpr = Graph(store=store)

	#Add data to the graph


	for st in json['results']['bindings']:
		#f.write('<' + st['a']['value'] + '> <http://purl.oclc.org/NET/ssnx/ssn#observes> "' + st['c']['value'] + '" . \n')
		gpr.add((st['a']['value'], 'http://purl.oclc.org/NET/ssnx/ssn#observes', st['c']['value']))
		suprint st['a']['value']

	print "Inserting graph in SPARQL endpoint..."
	insertGraph(g=gpr, sparql=VIRTUOSO_URL, resourceuri=RESOURCE_URI)
	print "Done!"
	print "Finish!"


	#f.close()

get_all_obs()

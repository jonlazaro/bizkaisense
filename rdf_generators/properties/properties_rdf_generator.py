# encoding: utf-8

from rdflib import Namespace, BNode, Literal, URIRef, Graph, ConjunctiveGraph, RDF
from rdflib.plugins.memory import IOMemory

import sys
sys.path.append('../lib/')
from rdf_parser import insertGraph

#VIRTUOSO_URL = "http://dev.morelab.deusto.es/bizkaisense/sparql"
VIRTUOSO_URL = "http://helheim.deusto.es:8890/sparql"
RESOURCE_URI = "http://dev.morelab.deusto.es/bizkaisense/resource/"
ENDPOINT_URL = VIRTUOSO_URL + "?query="

properties = [
		{'Temperatura':('http://sweet.jpl.nasa.gov/2.3/propTemperature.owl#Temperature', 'http://purl.oclc.org/NET/muo/ucum/unit/temperature/degree-Celsius', 'Class', 'http://www.w3.org/2001/XMLSchema#integer', 'Temp')}, 
		{'Radiacion': ('http://sweet.jpl.nasa.gov/2.3/matrIsotope.owl#Radiation', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#watt-per-meter-squared', 'Class', 'http://www.w3.org/2001/XMLSchema#float', 'Rad')},
		{'Radiacion UV': ('http://sweet.jpl.nasa.gov/2.3/stateSpectralBand.owl#Ultraviolet', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#milliwatt-per-meter-squared', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'UVRad')}, 
		{'Dir. Viento': ('http://purl.oclc.org/NET/ssnx/meteo/WM30#WindDirection', 'http://purl.oclc.org/NET/muo/ucum/unit/plane-angle/degree', 'Class', 'http://www.w3.org/2001/XMLSchema#integer', 'DirV')}, 
		{'Humedad': ('http://sweet.jpl.nasa.gov/2.3/propFraction.owl#Humidity', 'http://purl.oclc.org/NET/muo/ucum/unit/fraction/percent', 'Class', 'http://www.w3.org/2001/XMLSchema#integer', 'Humedad')},
		{'O3': ('http://sweet.jpl.nasa.gov/2.3/matrElementalMolecule.owl#O3', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#integer', 'O3')},
		{'NO2': ('http://sweet.jpl.nasa.gov/2.3/matrCompound.owl#NO2', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#integer', 'NO2')},
		{'Humos Negros': ('http://sweet.jpl.nasa.gov/2.3/matrAerosol.owl#Smoke', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Class', 'http://www.w3.org/2001/XMLSchema#float', 'Humos')},
		{'SH2': ('http://dev.morelab.deusto.es/bizkaisense/sweetAll-extended.owl#HydrogenSulfide', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-metre', 'Instance', 'http://www.w3.org/2001/XMLSchema#integer', 'SH2')},
		{'NO': ('http://sweet.jpl.nasa.gov/2.3/matrCompound.owl#NO', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#integer', 'NO')},
		{'HC metanicos': ('http://sweet.jpl.nasa.gov/2.3/matrOrganicCompound.owl#CH4', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#milligram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'CH4')},
		{'HC no metanicos': ('http://sweet.jpl.nasa.gov/2.3/matrOrganicCompound.owl#NMHC', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#milligram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'NMHC')},
		{'HC': ('http://sweet.jpl.nasa.gov/2.3/matrOrganicCompound.owl#HC', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#milligram-per-cubic-meter', 'Class', 'http://www.w3.org/2001/XMLSchema#float', 'HC')},
		{'Ortoxileno': ('http://sweet.jpl.nasa.gov/2.3/matrOrganicCompound.owl#Xylene', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'Xileno')},
		{'Tolueno': ('http://sweet.jpl.nasa.gov/2.3/matrOrganicCompound.owl#Toluene', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'Tolueno')},
		{'Benceno': ('http://sweet.jpl.nasa.gov/2.3/matrOrganicCompound.owl#Benzene', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'Benceno')},
		{'PM 2.5': ('http://sweet.jpl.nasa.gov/2.3/matrAerosol.owl#PM2point5', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Class', 'http://www.w3.org/2001/XMLSchema#integer', 'PM25')},
		{'Vel. Viento': ('http://sweet.jpl.nasa.gov/2.3/propSpeed.owl#WindSpeed', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#meter-per-second', 'Class', 'http://www.w3.org/2001/XMLSchema#float', 'VelV')},
		{'CO': ('http://sweet.jpl.nasa.gov/2.3/matrCompound.owl#CO', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'CO')},
		{'SO2': ('http://sweet.jpl.nasa.gov/2.3/matrCompound.owl#SO2', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#integer', 'SO2')},
		{'NH3': ('http://sweet.jpl.nasa.gov/2.3/matrCompound.owl#NH3', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance' , 'http://www.w3.org/2001/XMLSchema#float', 'NH3')},
		{'Etilbenceno': ('http://dev.morelab.deusto.es/bizkaisense/sweetAll-extended.owl#Ethylbenzene', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'Etilbenceno')},
		{'PM 10': ('http://sweet.jpl.nasa.gov/2.3/matrAerosol.owl#PM10', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Class', 'http://www.w3.org/2001/XMLSchema#float', 'PM10')},
		{'Presion': ('http://sweet.jpl.nasa.gov/2.3/propPressure.owl#BarometricPressure', 'http://dev.morelab.deusto.es/bizkaisense/ucum-extended.owl#millibar', 'Class' , 'http://www.w3.org/2001/XMLSchema#float', 'Presion')}
	]

def properties_rdf_generator():
	for prop in properties:
		observedprop, obsunit, typeofuri, xsdclass, uriprefix = prop.values()[0]

		if observedprop:
			#.../station/ZORRO2/NO2/15022011/10
			uri = RESOURCE_URI + 'prop/' + uriprefix
			
			#Initialization of graph
			ssn = Namespace("http://purl.oclc.org/NET/ssnx/ssn#")
			dc = Namespace("http://purl.org/dc/elements/1.1/")
			owl = Namespace("http://www.w3.org/2002/07/owl#")

			store = IOMemory()
			
			g = ConjunctiveGraph(store=store)
			g.bind("ssn", ssn)
			g.bind("dc", dc)
			g.bind("owl", owl)
			
			cpr = URIRef(uri)
			gpr = Graph(store=store, identifier=cpr)
			
			#Add data to the graph
			gpr.add((cpr, dc['description'], prop.keys()[0]))
			if typeofuri == 'Class':
				gpr.add((cpr, RDF.type, URIRef(observedprop)))
			else:
				gpr.add((cpr, owl["sameAs"], URIRef(observedprop)))

			gpr.add((cpr, RDF.type, ssn['Property']))

			#print g.serialize(format="pretty-xml")
			insertGraph(g=gpr, sparql=VIRTUOSO_URL, resourceuri=RESOURCE_URI)



properties_rdf_generator()
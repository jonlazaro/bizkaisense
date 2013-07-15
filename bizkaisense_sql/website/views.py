# coding: utf-8

from django.shortcuts import render_to_response, get_object_or_404
from rdflib import Namespace
from django.utils.encoding import smart_str
from django.template import RequestContext
from datetime import datetime, timedelta
from django.http import Http404

import re

from model_sqlalchemy import *

from website.forms import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_ENGINE_STR = 'mysql://bizkaisense:bizkaisense@127.0.0.1/air_quality'
engine = create_engine(SQLALCHEMY_ENGINE_STR, convert_unicode=True, pool_recycle=3600)
Session = sessionmaker(bind = engine)
session = Session()

lim_values = {
	'http://sweet.jpl.nasa.gov/2.3/matrCompound.owl#SO2': [125, "Valor medio en 24 horas que no podrá superarse en más de 3 ocasiones por año"],
	'http://sweet.jpl.nasa.gov/2.3/matrCompound.owl#NO2': [200, "Valor medio en 1 hora que no podrá superarse en más de 18 ocasiones por año civil"],
	'http://sweet.jpl.nasa.gov/2.3/matrAerosol.owl#PM10': [50, "Valor medio en 24 horas que no podrá superarse en más de 35 ocasiones por año civil"],
	'http://sweet.jpl.nasa.gov/2.3/matrCompound.owl#CO': [10000, "Valor máximo de las medias octohorarias móviles del día"],
	'http://sweet.jpl.nasa.gov/2.3/matrElementalMolecule.owl#O3': [180, "Valor medio en 1 hora"],
}

def index(request):
	details={}
	
	stations = []
	details["stations"] = stations

	dbstations = session.query(Station).all()

	for st in dbstations:
		if len(st.properties) > 0:
			station = {}
			station["lat"] = st.lat
			station["lng"] = st.lng
			station["url"] = st.url

			'''station["url"] = station["url"].replace('%3F', '?')
			station["url"] = station["url"].replace('%3D', '=')
			station["url"] = station["url"].replace('%40', '@')
			station["url"] = station["url"].replace('%26', '&')'''

			if st.address is not None:
				station["address"] = st.address
			station["name"] = st.name
			station["uri"] = st.uri
			station["id"] = st.code

			stations.append(station)

	return render_to_response('index.html', details, context_instance=RequestContext(request))

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //																														//
# //																														//
# //																														//
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def station(request, stid):

	details={}
	
	#uri = resource_uri + stid

	station = {}
	obstypes = []

	st = session.query(Station).filter_by(code=stid).first()

	if st is not None:
		station["lat"] = st.lat
		station["lng"] = st.lng
		station["url"] = st.url
		if st.address is not None:
			station["address"] = st.address
		#if 'img' in st:
		#	station["img"] = st['img']['value']
		station["name"] = st.name
		station["uri"] = st.uri
		station["id"] = stid

		if len(st.properties) > 0:
			for prop in st.properties:
				obstypes.append((prop.ontology_uri, prop.name))
			obstypes = sorted(set(obstypes))
			obstypes.sort()
		else:
			obstypes = [('-', '-')]
	else:
		raise Http404

	details["station"] = station

	dt = date.today() - timedelta(days=1)
	obstype = obstypes[0][0]

	if request.method == 'POST':
		form = ObservationDetailsForm(obstypes, request.POST)
		details["form"] = form
		if form.is_valid():
			dt = form.cleaned_data['date']#datetime.strptime(form.cleaned_data['date'], '%Y-%m-%d') + timedelta(seconds=1)
			obstype = form.cleaned_data['obstypes']
	else:
		details["form"] = ObservationDetailsForm(obstypes=obstypes)

	startdt = datetime(dt.year, dt.month, dt.day) + timedelta(seconds=1)
	enddt = startdt + timedelta(hours=23, minutes=59)

	observations = session.query(Observation).join(Station).join(Property).filter(Station.code == stid, Observation.date.between(startdt, enddt), Property.ontology_uri == obstype).all()

	results = []

	for res in observations:
		med = {}
		med["uri"] = res.uri
		med["date"] = res.date
		med["value"] = res.value
		med["obsunit"] = res.unit.uri.split('#')[1] if res.unit.uri.find('#') != -1 else res.unit.uri.split('/')[-1]
		#med["obsunit"] = res['value']['value'][len(med["value"])+1:]
		#med["obsunit"] = '%' if med["obsunit"] == 'percent' else med["obsunit"]
		if med["value"] != '-1':
			results.append(med)
	
	#Sort the list of dicts using the date (using "key", sorting function uses the return of the lambda function as the value to sort)
	results.sort(key=lambda med: med["date"])

	limvalue = lim_values.get(obstype, None)
	details["limvalue"] = limvalue[0] if limvalue else None
	details["limvalueobs"] = limvalue[1] if limvalue else None
	details["results"] = results
	details["obstype"] = obstypes[0][1]

	return render_to_response('station.html', details, context_instance=RequestContext(request))


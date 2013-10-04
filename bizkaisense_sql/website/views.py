# coding: utf-8

from django.shortcuts import render_to_response, get_object_or_404
from rdflib import Namespace
from django.utils.encoding import smart_str
from django.template import RequestContext
from datetime import datetime, timedelta
from django.http import Http404, HttpResponse
from django.conf import settings

#import csv
import json
import re

from model_sqlalchemy import *

from website.forms import *

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy.sql.expression import alias

SQLALCHEMY_ENGINE_STR = getattr(settings, 'DATABASE_CONNECTION_STRING', '')
engine = create_engine(SQLALCHEMY_ENGINE_STR, convert_unicode=True, pool_recycle=3600)
Session = sessionmaker(bind = engine)

lim_values = {
	'http://sweet.jpl.nasa.gov/2.3/matrCompound.owl#SO2': [125, "Valor medio en 24 horas que no podrá superarse en más de 3 ocasiones por año"],
	'http://sweet.jpl.nasa.gov/2.3/matrCompound.owl#NO2': [200, "Valor medio en 1 hora que no podrá superarse en más de 18 ocasiones por año civil"],
	'http://sweet.jpl.nasa.gov/2.3/matrAerosol.owl#PM10': [50, "Valor medio en 24 horas que no podrá superarse en más de 35 ocasiones por año civil"],
	'http://sweet.jpl.nasa.gov/2.3/matrCompound.owl#CO': [10000, "Valor máximo de las medias octohorarias móviles del día"],
	'http://sweet.jpl.nasa.gov/2.3/matrElementalMolecule.owl#O3': [180, "Valor medio en 1 hora"],
}


def json_response(func):
    """
    A decorator thats takes a view response and turns it
    into json. If a callback is added through GET or POST
    the response is JSONP.
    """
    def decorator(request, *args, **kwargs):
        objects = func(request, *args, **kwargs)
        if isinstance(objects, HttpResponse):
            return objects
        try:
            data = json.dumps(objects)
            if 'callback' in request.REQUEST:
                # a jsonp response!
                data = '%s(%s);' % (request.REQUEST['callback'], data)
                return HttpResponse(data, "text/javascript")
        except:
            data = json.dumps(str(objects))
        return HttpResponse(data, "application/json")
    return decorator



def index(request):
	session = Session()

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

	session.close()
	return render_to_response('index.html', details, context_instance=RequestContext(request))

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# //																														//
# //																														//
# //																														//
# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def station(request, stid):
	session = Session()

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
	
	details["obstype"] = session.query(Property).filter_by(ontology_uri=obstype).first().name

	for res in observations:
		med = {}
		#med["uri"] = res.uri
		med["uri"] = st.uri + '/' + details["obstype"] + '/' + res.date.isoformat()
		med["date"] = res.date
		med["value"] = res.value
		med["obsunit"] = res.prop.unit.split('#')[1] if res.prop.unit.find('#') != -1 else res.prop.unit.split('/')[-1]
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

	session.close()
	return render_to_response('station.html', details, context_instance=RequestContext(request))

@json_response
def api_obs_day(request, stid, propid, date):
	session = Session()

	#response = HttpResponse(mimetype='text/csv')
	#response['Content-Disposition'] = 'attachment; filename="obs_' + stid + '_' + propid + '_' + date + '.csv"'

	startdate = datetime(int(date.split('-')[0]), int(date.split('-')[1]), int(date.split('-')[2]))
	enddate = startdate + timedelta(hours=23, minutes=59)

	observations = session.query(Observation).join(Station).join(Property).filter(Station.code == stid, Observation.date.between(startdate, enddate), Property.name == propid).all()

	#writer = csv.writer(response)
	#for obs in observations:
	#    writer.writerow([obs.station.lat, obs.station.lng, obs.date, obs.value])

	resp = []
	for obs in observations:
		o = {}
		o['lat'] = obs.station.lat
		o['lng'] = obs.station.lng
		o['date'] = obs.date.isoformat()
		o['value'] = obs.value
		resp.append(o)

	session.close()
	#return response
	return resp
	#return json.dumps(resp)
	#return HttpResponse(json.dumps(resp), content_type="application/json", mimetype="application/json")
	#return HttpResponse(json.dumps(resp), mimetype="application/x-javascript")

def endpoint(request):
	return render_to_response('endpoint.html')

def docs(request):
        return render_to_response('docs.html')

@json_response
def api_outlimit_stations(request, propid, startdate, enddate, limit):
        session = Session()

        #response = HttpResponse(mimetype='text/csv')
        #response['Content-Disposition'] = 'attachment; filename="obs_' + stid + '_' + propid + '_' + date + '.csv"'

        startdate = datetime(int(startdate.split('-')[0]), int(startdate.split('-')[1]), int(startdate.split('-')[2]))
        enddate = datetime(int(enddate.split('-')[0]), int(enddate.split('-')[1]), int(enddate.split('-')[2]))

	#max = aliased(func.max(Observation.value))
	#currentdate = aliased(func.date(Observation.date))

        observations = session.query(func.max(Observation.value), Station.municipality, Station.lat, Station.lng, func.date(Observation.date)).\
		join(Station).join(Property).\
		filter(Observation.date.between(startdate, enddate), Property.name == propid).\
		group_by(func.date(Observation.date), Station.code).having(func.max(Observation.value) >= float(limit)).all()
	
	#Observation.value >= limit
        #writer = csv.writer(response)
        #for obs in observations:
        #    writer.writerow([obs.station.lat, obs.station.lng, obs.date, obs.value])

        resp = []
        for obs in observations:
                o = {}
                o['lat'] = obs[2]
                o['lng'] = obs[3]
                o['date'] = obs[4].isoformat()
                o['municipality'] = obs[1]
		o['value'] = obs[0]
                resp.append(o)

        session.close()
        #return response
        return resp


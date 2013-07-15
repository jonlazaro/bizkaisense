# coding=iso-8859-15
from xml.dom.minidom import parse, parseString
import codecs
import string
import datetime
import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from model import *

def get_info(prop):
    if prop == 'Temperatura' or prop == 'TemperaturaJaizkibel' or prop == 'Temp' or prop == 'T':
        return 'http://sweet.jpl.nasa.gov/2.3/propTemperature.owl#Temperature', 'http://purl.oclc.org/NET/muo/ucum/unit/temperature/degree-Celsius', 'Class', 'http://www.w3.org/2001/XMLSchema#integer', 'Temperature'
    elif prop == 'Radiacion' or prop == 'RS' or prop == 'Rad':
        return 'http://sweet.jpl.nasa.gov/2.3/matrIsotope.owl#Radiation', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#watt-per-meter-squared', 'Class', 'http://www.w3.org/2001/XMLSchema#float', 'Radiation'
    elif prop.encode("utf-8") == 'Radiación' or prop == 'RadUV' or prop == 'Radia':
        return 'http://sweet.jpl.nasa.gov/2.3/stateSpectralBand.owl#Ultraviolet', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#milliwatt-per-meter-squared', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'UVRadiation'
    elif prop == 'DV' or prop == 'Dir_Viento' or prop == 'DirV' or prop == 'Direc':
        return 'http://purl.oclc.org/NET/ssnx/meteo/WM30#WindDirection', 'http://purl.oclc.org/NET/muo/ucum/unit/plane-angle/degree', 'Class', 'http://www.w3.org/2001/XMLSchema#integer', 'WindDirection'
    elif prop == 'Humedad' or prop == 'HR' or prop == 'Humed':
        return 'http://sweet.jpl.nasa.gov/2.3/propFraction.owl#Humidity', 'http://purl.oclc.org/NET/muo/ucum/unit/fraction/percent', 'Class', 'http://www.w3.org/2001/XMLSchema#integer', 'Humidity'
    elif prop == 'O3' or prop == 'Ozono':
        return 'http://sweet.jpl.nasa.gov/2.3/matrElementalMolecule.owl#O3', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#integer', 'O3'
    elif prop == 'NO2':
        return 'http://sweet.jpl.nasa.gov/2.3/matrCompound.owl#NO2', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#integer', 'NO2'
    elif prop == 'Humos' or prop == 'HN':
        return 'http://sweet.jpl.nasa.gov/2.3/matrAerosol.owl#Smoke', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Class', 'http://www.w3.org/2001/XMLSchema#float', 'Smoke'
    elif prop == 'SH2' or prop == 'H2S':
        return 'http://helheim.deusto.es/bizkaisense/sweetAll-extended.owl#HydrogenSulfide', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-metre', 'Instance', 'http://www.w3.org/2001/XMLSchema#integer', 'SH2'
    elif prop == 'NO':
        return 'http://sweet.jpl.nasa.gov/2.3/matrCompound.owl#NO', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#integer', 'NO'
    elif prop == 'HC met.' or prop == 'HCMet':
        return 'http://sweet.jpl.nasa.gov/2.3/matrOrganicCompound.owl#CH4', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#milligram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'CH4'
    elif prop == 'HC no met.' or prop == 'HCNoMet':
        return 'http://sweet.jpl.nasa.gov/2.3/matrOrganicCompound.owl#NMHC', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#milligram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'NMHC'
    elif prop == 'HC':
        return 'http://sweet.jpl.nasa.gov/2.3/matrOrganicCompound.owl#HC', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#milligram-per-cubic-meter', 'Class', 'http://www.w3.org/2001/XMLSchema#float', 'HC'
    elif prop == 'X-Xileno' or prop == 'Ortoxileno' or prop == 'Xileno':
        return 'http://sweet.jpl.nasa.gov/2.3/matrOrganicCompound.owl#Xylene', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'Xylene'
    elif prop == 'Tolueno':
        return 'http://sweet.jpl.nasa.gov/2.3/matrOrganicCompound.owl#Toluene', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'Toluene'
    elif prop == 'Benceno':
        return 'http://sweet.jpl.nasa.gov/2.3/matrOrganicCompound.owl#Benzene', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'Benzene'
    elif prop == 'PM25' or prop == 'PM2_5' or prop == 'PM2.5':
        return 'http://sweet.jpl.nasa.gov/2.3/matrAerosol.owl#PM2point5', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Class', 'http://www.w3.org/2001/XMLSchema#integer', 'PM25'
    elif prop == 'Vel_Viento' or prop == 'Velo_Viento' or prop == 'VV' or prop == 'VelV' or prop == 'Velic':
        return 'http://sweet.jpl.nasa.gov/2.3/propSpeed.owl#WindSpeed', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#meter-per-second', 'Class', 'http://www.w3.org/2001/XMLSchema#float', 'WindSpeed'
    elif prop == 'CO':
        return 'http://sweet.jpl.nasa.gov/2.3/matrCompound.owl#CO', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'CO'
    elif prop == 'SO2':
        return 'http://sweet.jpl.nasa.gov/2.3/matrCompound.owl#SO2', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#integer', 'SO2'
    elif prop == 'NH3':
        return 'http://sweet.jpl.nasa.gov/2.3/matrCompound.owl#NH3', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance' , 'http://www.w3.org/2001/XMLSchema#float', 'NH3'
    elif prop == 'Etilbenceno' or prop == 'EtilbencenoElorrieta':
        return 'http://helheim.deusto.es/bizkaisense/sweetAll-extended.owl#Ethylbenzene', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'Ethylbenzene'
    elif prop == 'PM10' or prop == 'PM1o':
        return 'http://sweet.jpl.nasa.gov/2.3/matrAerosol.owl#PM10', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Class', 'http://www.w3.org/2001/XMLSchema#float', 'PM10'
    elif prop == 'Presion' or prop == 'P':
        return 'http://sweet.jpl.nasa.gov/2.3/propPressure.owl#BarometricPressure', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#millibar', 'Class' , 'http://www.w3.org/2001/XMLSchema#float', 'Pressure'
    else:
        print 'La propiedad ' + prop + ' no esta mapeada!'

def generate_historic():
    missing_sts = []

    horarias = codecs.open(HORARIAS_FILE, 'r', "iso-8859-15")
    mediciones = codecs.open(MEDICIONES_FILE, 'r', "iso-8859-15")

    mediciones_dict = {}

    for line in mediciones.readlines():
        line_list = line.split(';')
        mediciones_dict[line_list[1]] = line_list

    for line in horarias.readlines():
        line_list = line.split(';')
        identifier = mediciones_dict[line_list[0]][0]
        identifier = identifier.encode('utf-8').replace('Ñ', 'N')

        station = session.query(Station).filter_by(code = identifier).first()

        #query = 'SELECT ?s WHERE { ?s dc:identifier "' + identifier + '" . ?s rdf:type ssn:Sensor}'
        #uri_list = get_uris_from_xml(vm.select(query, 'application/sparql-results+xml', ))
        if station is not None:
            station_subject = station.uri
            date = line_list[1]
            date_list = line_list[1].split('/')
            formated_date = datetime.date(int(date_list[2]), int(date_list[1]), int(date_list[0]))

            i = 0
            for j in range(2, len(line_list) - 1):
                code = line_list[j].split(' ')[1]
                if code in ['A', 'O', 'R']:
                    time = datetime.time(i)
                    dt = datetime.datetime.combine(formated_date, time)
                    iso_date = dt.isoformat()                

                    # Sacamos la info necesaria
                    prop = string.replace(mediciones_dict[line_list[0]][2].split(' ')[0], '.', '_')
                    if len(mediciones_dict[line_list[0]][2].split(' ')) > 1:
                        if mediciones_dict[line_list[0]][2].split(' ')[1] == 'met':
                            prop = 'HC met.'
                        elif mediciones_dict[line_list[0]][2].split(' ')[1] == 'no':
                            prop = 'HC no met.'

                    ontology_resource, measure_unit, ontology_type, data_type, uri_value = get_info(prop)
                    
                    # Create Observation
                    termtype = session.query(TermType).filter_by(name=ontology_type).first()
                    if termtype is None:
                        termtype = TermType(name=ontology_type)
                        session.add(termtype)
                    
                    dbprop = session.query(Property).filter_by(ontology_uri=ontology_resource, name=uri_value, termtype=termtype).first()
                    if dbprop is None:
                        dbprop = Property(ontology_uri=ontology_resource, name=uri_value, termtype=termtype)
                        session.add(dbprop)

                    if station not in dbprop.stations:
                        dbprop.stations.append(station)

                    obsuri = station_subject.encode('utf-8') + '/' + uri_value + '/' +  string.replace(date, '/', '') + '/' + str('%02d' % i)
                    quantity = line_list[j].split(' ')[0]

                    dbdatatype = session.query(DataType).filter_by(uri=data_type.encode('utf-8')).first()
                    if dbdatatype is None:
                        dbdatatype = DataType(uri=data_type.encode('utf-8'))
                        session.add(dbdatatype)

                    dbunit = session.query(Unit).filter_by(uri=measure_unit.encode('utf-8')).first()
                    if dbunit is None:
                        dbunit = Unit(uri=measure_unit.encode('utf-8'))
                        session.add(dbunit)

                    dbobservation = Observation(date=dt, value=quantity.encode('utf-8'), station=station, prop=dbprop, datatype=dbdatatype, unit=dbunit, uri=obsuri.encode('utf-8'))
                    session.add(dbobservation)
                    print iso_date, station.code, uri_value, "object created."
                    
                i = i + 1
        else:
           missing_sts.append(identifier)

    print "missing_sts: "
    print missing_sts

def generate_historic_2012():
    missing_sts = []

    horarias = codecs.open(HORARIAS_FILE, 'r', "iso-8859-15")
    mediciones = codecs.open(MEDICIONES_FILE, 'r', "iso-8859-15")

    mediciones_dict = {}

    for line in mediciones.readlines():
        line_list = line.split(';')
        mediciones_dict[line_list[1]] = line_list

    for line in horarias.readlines():
        line_list = line.split('\t')
        identifier = mediciones_dict[line_list[0]][0]
        identifier = identifier.encode('utf-8').replace('Ñ', 'N')

        station = session.query(Station).filter_by(code = identifier).first()

        #query = 'SELECT ?s WHERE { ?s dc:identifier "' + identifier + '" . ?s rdf:type ssn:Sensor}'
        #uri_list = get_uris_from_xml(vm.select(query, 'application/sparql-results+xml', ))
        if station is not None:
            station_subject = station.uri
            date = line_list[1]
            date_list = line_list[1].split('/')
            formated_date = datetime.date(int(date_list[2]), int(date_list[1]), int(date_list[0]))

            i = 0
            for j in range(2, len(line_list) - 1, 2):
                code = line_list[j+1]
                if code in ['A', 'O', 'R']:
                    time = datetime.time(i)
                    dt = datetime.datetime.combine(formated_date, time)
                    iso_date = dt.isoformat()                

                    # Sacamos la info necesaria
                    prop = string.replace(mediciones_dict[line_list[0]][2].split(' ')[0], '.', '_')
                    if len(mediciones_dict[line_list[0]][2].split(' ')) > 1:
                        if mediciones_dict[line_list[0]][2].split(' ')[1] == 'met':
                            prop = 'HC met.'
                        elif mediciones_dict[line_list[0]][2].split(' ')[1] == 'no':
                            prop = 'HC no met.'

                    ontology_resource, measure_unit, ontology_type, data_type, uri_value = get_info(prop)
                    
                    # Create Observation
                    termtype = session.query(TermType).filter_by(name=ontology_type).first()
                    if termtype is None:
                        termtype = TermType(name=ontology_type)
                        session.add(termtype)
                    
                    dbprop = session.query(Property).filter_by(ontology_uri=ontology_resource, name=uri_value, termtype=termtype).first()
                    if dbprop is None:
                        dbprop = Property(ontology_uri=ontology_resource, name=uri_value, termtype=termtype)
                        session.add(dbprop)

                    if station not in dbprop.stations:
                        dbprop.stations.append(station)

                    obsuri = station_subject.encode('utf-8') + '/' + uri_value + '/' +  string.replace(date, '/', '') + '/' + str('%02d' % i)
                    quantity = line_list[j].split(' ')[0]

                    dbdatatype = session.query(DataType).filter_by(uri=data_type.encode('utf-8')).first()
                    if dbdatatype is None:
                        dbdatatype = DataType(uri=data_type.encode('utf-8'))
                        session.add(dbdatatype)

                    dbunit = session.query(Unit).filter_by(uri=measure_unit.encode('utf-8')).first()
                    if dbunit is None:
                        dbunit = Unit(uri=measure_unit.encode('utf-8'))
                        session.add(dbunit)

                    dbobservation = Observation(date=dt, value=quantity.encode('utf-8'), station=station, prop=dbprop, datatype=dbdatatype, unit=dbunit, uri=obsuri.encode('utf-8'))
                    session.add(dbobservation)
                    print iso_date, station.code, uri_value, "object created."
                    
                i = i + 1
        else:
           missing_sts.append(identifier)

    print "missing_sts: "
    print missing_sts


if __name__ == '__main__':
    if len(sys.argv) == 4:
        # TO-DO: Validation of arguments

        here = os.path.dirname(__file__)

        SQLALCHEMY_ENGINE_STR = 'mysql://bizkaisense:bizkaisense@127.0.0.1/air_quality'
        #SQLALCHEMY_ENGINE_STR = 'sqlite:///bizkaisense.db'
        engine = create_engine(SQLALCHEMY_ENGINE_STR, convert_unicode=True, pool_recycle=3600)


        #MEDICIONES_FILE = here + '/observations/2011/Medidas.txt'
        MEDICIONES_FILE = sys.argv[2]
        #HORARIAS_FILE = here + '/observations/2011/H2011_Trimestre_01.txt'
        HORARIAS_FILE = sys.argv[3]

        Session = sessionmaker(bind = engine)
        session = Session()

        # Generate historic
        if bool(int(sys.argv[1])):
            print "Executing 2012 parser..."
            generate_historic_2012()
        else:
            print "Executing default parser..."
            generate_historic()

        print "Saving into DB..."
        session.commit()
        print "Done!"
        session.close()
    else:
        print "USAGE: python sql_historic_parser.py IS_2012 MEDIDAS_FILE OBS_HORA_FILE"
        print "IS_2012 gets 0 (it's not 2012) or 1 (it is 2012) to know if 2012 parser has to be executed"
        print "MEDIDAS_FILE and OBS_HORA_FILE get paths to CSV files"
        print "Example: python sql_historic_parser.py 0 observations/2011/Medidas.txt observations/2011/H2011_Trimestre_01.txt"

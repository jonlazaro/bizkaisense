# coding=iso-8859-15
from virtuosordflib import VirtuosoManager
from xml.dom.minidom import parse, parseString
import rdflib
import codecs
import string
import datetime
from sets import Set
import logging

def get_uris_from_xml(data):
    #print data
    dom = parseString(data)
    element_list = dom.getElementsByTagName('uri')
    uri_list = []
    for element in element_list:
        for child in element.childNodes:
            uri_list.append(child.data)
    return uri_list

    
def get_info(prop):
    #if prop == 'Temperatura' or prop == 'TemperaturaJaizkibel' or prop == 'Temp':
        #return 'http://sweet.jpl.nasa.gov/2.3/propTemperature.owl#Temperature', 'http://purl.oclc.org/NET/muo/ucum/unit/temperature/degree-Celsius', 'Class', 'http://www.w3.org/2001/XMLSchema#integer', 'Temp'
    #elif prop == 'Radiacion' or prop == 'RS':
        #return 'http://sweet.jpl.nasa.gov/2.3/matrIsotope.owl#Radiation', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#watt-per-meter-squared', 'Class', 'http://www.w3.org/2001/XMLSchema#float', 'Rad'
    #elif prop.encode("utf-8") == 'Radiación':
        #return 'http://sweet.jpl.nasa.gov/2.3/stateSpectralBand.owl#Ultraviolet', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#milliwatt-per-meter-squared', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'UVRad'
    #elif prop == 'DV' or prop == 'Dir_Viento':
        #return 'http://purl.oclc.org/NET/ssnx/meteo/WM30#WindDirection', 'http://purl.oclc.org/NET/muo/ucum/unit/plane-angle/degree', 'Class', 'http://www.w3.org/2001/XMLSchema#integer', 'DirV'
    #elif prop == 'Humedad' or prop == 'HR':
        #return 'http://sweet.jpl.nasa.gov/2.3/propFraction.owl#Humidity', 'http://purl.oclc.org/NET/muo/ucum/unit/fraction/percent', 'Class', 'http://www.w3.org/2001/XMLSchema#integer', 'Humedad'
    #elif prop == 'O3' or prop == 'Ozono':
        #return 'http://sweet.jpl.nasa.gov/2.3/matrElementalMolecule.owl#O3', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#integer', 'O3'
    #elif prop == 'NO2':
        #return 'http://sweet.jpl.nasa.gov/2.3/matrCompound.owl#NO2', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#integer', 'NO2'
    #elif prop == 'Humos':
        #return 'http://sweet.jpl.nasa.gov/2.3/matrAerosol.owl#Smoke', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Class', 'http://www.w3.org/2001/XMLSchema#float', 'Humos'
    #elif prop == 'SH2':
        #return 'http://helheim.deusto.es/bizkaisense/sweetAll-extended.owl#HydrogenSulfide', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-metre', 'Instance', 'http://www.w3.org/2001/XMLSchema#integer', 'SH2'
    #elif prop == 'NO':
        #return 'http://sweet.jpl.nasa.gov/2.3/matrCompound.owl#NO', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#integer', 'NO'
    #elif prop == 'HC met.':
        #return 'http://sweet.jpl.nasa.gov/2.3/matrOrganicCompound.owl#HC', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#milligram-per-cubic-meter', 'Class', 'http://www.w3.org/2001/XMLSchema#float', 'HC'
    #elif prop == 'HC no met.':
        #return 'http://sweet.jpl.nasa.gov/2.3/matrOrganicCompound.owl#NMHC', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#milligram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'NMHC'
    #elif prop == 'X-Xileno':
        #return 'http://sweet.jpl.nasa.gov/2.3/matrOrganicCompound.owl#Xylene', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'Xileno'
    #elif prop == 'Tolueno':
        #return 'http://sweet.jpl.nasa.gov/2.3/matrOrganicCompound.owl#Toluene', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'Tolueno'
    #elif prop == 'Benceno':
        #return 'http://sweet.jpl.nasa.gov/2.3/matrOrganicCompound.owl#Benzene', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'Benceno'
    #elif prop == 'PM25' or prop == 'PM2_5':
        #return 'http://sweet.jpl.nasa.gov/2.3/matrAerosol.owl#PM2point5', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Class', 'http://www.w3.org/2001/XMLSchema#integer', 'PM25'
    #elif prop == 'Vel_Viento' or prop == 'Velo_Viento' or prop == 'VV':
        #return 'http://sweet.jpl.nasa.gov/2.3/propSpeed.owl#WindSpeed', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#meter-per-second', 'Class', 'http://www.w3.org/2001/XMLSchema#float', 'VelV'
    #elif prop == 'CO':
        #return 'http://sweet.jpl.nasa.gov/2.3/matrCompound.owl#CO', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'CO'
    #elif prop == 'SO2':
        #return 'http://sweet.jpl.nasa.gov/2.3/matrCompound.owl#SO2', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#integer', 'SO2'
    #elif prop == 'NH3':
        #return 'http://sweet.jpl.nasa.gov/2.3/matrCompound.owl#NH3', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance' , 'http://www.w3.org/2001/XMLSchema#float', 'NH3'
    #elif prop == 'Etilbenceno':
        #return 'http://helheim.deusto.es/bizkaisense/sweetAll-extended.owl#Ethylbenzene', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'Etilbenceno'
    #elif prop == 'PM10':
        #return 'http://sweet.jpl.nasa.gov/2.3/matrAerosol.owl#PM10', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Class', 'http://www.w3.org/2001/XMLSchema#float', 'PM10'
    #elif prop == 'Presion':
        #return 'http://sweet.jpl.nasa.gov/2.3/propPressure.owl#BarometricPressure', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#millibar', 'Class' , 'http://www.w3.org/2001/XMLSchema#float', 'Presion'
    #else:
        #logger.info('La propiedad ' + prop + ' no esta mapeada!')
        
    if prop == 'Temperatura' or prop == 'TemperaturaJaizkibel' or prop == 'Temp' or prop == 'T':
        return 'http://sweet.jpl.nasa.gov/2.3/propTemperature.owl#Temperature', 'http://purl.oclc.org/NET/muo/ucum/unit/temperature/degree-Celsius', 'Class', 'http://www.w3.org/2001/XMLSchema#integer', 'Temp'
    elif prop == 'Radiacion' or prop == 'RS' or prop == 'Rad':
        return 'http://sweet.jpl.nasa.gov/2.3/matrIsotope.owl#Radiation', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#watt-per-meter-squared', 'Class', 'http://www.w3.org/2001/XMLSchema#float', 'Rad'
    elif prop.encode("utf-8") == 'Radiación' or prop == 'RadUV':
        return 'http://sweet.jpl.nasa.gov/2.3/stateSpectralBand.owl#Ultraviolet', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#milliwatt-per-meter-squared', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'UVRad'
    elif prop == 'DV' or prop == 'Dir_Viento' or prop == 'DirV':
        return 'http://purl.oclc.org/NET/ssnx/meteo/WM30#WindDirection', 'http://purl.oclc.org/NET/muo/ucum/unit/plane-angle/degree', 'Class', 'http://www.w3.org/2001/XMLSchema#integer', 'DirV'
    elif prop == 'Humedad' or prop == 'HR' or prop == 'Humed':
        return 'http://sweet.jpl.nasa.gov/2.3/propFraction.owl#Humidity', 'http://purl.oclc.org/NET/muo/ucum/unit/fraction/percent', 'Class', 'http://www.w3.org/2001/XMLSchema#integer', 'Humedad'
    elif prop == 'O3' or prop == 'Ozono':
        return 'http://sweet.jpl.nasa.gov/2.3/matrElementalMolecule.owl#O3', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#integer', 'O3'
    elif prop == 'NO2':
        return 'http://sweet.jpl.nasa.gov/2.3/matrCompound.owl#NO2', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#integer', 'NO2'
    elif prop == 'Humos' or prop == 'HN':
        return 'http://sweet.jpl.nasa.gov/2.3/matrAerosol.owl#Smoke', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Class', 'http://www.w3.org/2001/XMLSchema#float', 'Humos'
    elif prop == 'SH2':
        return 'http://helheim.deusto.es/bizkaisense/sweetAll-extended.owl#HydrogenSulfide', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-metre', 'Instance', 'http://www.w3.org/2001/XMLSchema#integer', 'SH2'
    elif prop == 'NO':
        return 'http://sweet.jpl.nasa.gov/2.3/matrCompound.owl#NO', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#integer', 'NO'
    elif prop == 'HC met.' or prop == 'HCMet':
        return 'http://sweet.jpl.nasa.gov/2.3/matrOrganicCompound.owl#CH4', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#milligram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'CH4'
    elif prop == 'HC no met.' or prop == 'HCNoMet':
        return 'http://sweet.jpl.nasa.gov/2.3/matrOrganicCompound.owl#NMHC', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#milligram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'NMHC'
    elif prop == 'HC':
        return 'http://sweet.jpl.nasa.gov/2.3/matrOrganicCompound.owl#HC', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#milligram-per-cubic-meter', 'Class', 'http://www.w3.org/2001/XMLSchema#float', 'HC'
    elif prop == 'X-Xileno' or prop == 'Ortoxileno':
        return 'http://sweet.jpl.nasa.gov/2.3/matrOrganicCompound.owl#Xylene', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'Xileno'
    elif prop == 'Tolueno':
        return 'http://sweet.jpl.nasa.gov/2.3/matrOrganicCompound.owl#Toluene', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'Tolueno'
    elif prop == 'Benceno':
        return 'http://sweet.jpl.nasa.gov/2.3/matrOrganicCompound.owl#Benzene', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'Benceno'
    elif prop == 'PM25' or prop == 'PM2_5' or prop == 'PM2.5':
        return 'http://sweet.jpl.nasa.gov/2.3/matrAerosol.owl#PM2point5', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Class', 'http://www.w3.org/2001/XMLSchema#integer', 'PM25'
    elif prop == 'Vel_Viento' or prop == 'Velo_Viento' or prop == 'VV' or prop == 'VelV':
        return 'http://sweet.jpl.nasa.gov/2.3/propSpeed.owl#WindSpeed', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#meter-per-second', 'Class', 'http://www.w3.org/2001/XMLSchema#float', 'VelV'
    elif prop == 'CO':
        return 'http://sweet.jpl.nasa.gov/2.3/matrCompound.owl#CO', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'CO'
    elif prop == 'SO2':
        return 'http://sweet.jpl.nasa.gov/2.3/matrCompound.owl#SO2', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#integer', 'SO2'
    elif prop == 'NH3':
        return 'http://sweet.jpl.nasa.gov/2.3/matrCompound.owl#NH3', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance' , 'http://www.w3.org/2001/XMLSchema#float', 'NH3'
    elif prop == 'Etilbenceno':
        return 'http://helheim.deusto.es/bizkaisense/sweetAll-extended.owl#Ethylbenzene', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Instance', 'http://www.w3.org/2001/XMLSchema#float', 'Etilbenceno'
    elif prop == 'PM10':
        return 'http://sweet.jpl.nasa.gov/2.3/matrAerosol.owl#PM10', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#microgram-per-cubic-meter', 'Class', 'http://www.w3.org/2001/XMLSchema#float', 'PM10'
    elif prop == 'Presion' or prop == 'P':
        return 'http://sweet.jpl.nasa.gov/2.3/propPressure.owl#BarometricPressure', 'http://helheim.deusto.es/bizkaisense/ucum-extended.owl#millibar', 'Class' , 'http://www.w3.org/2001/XMLSchema#float', 'Presion'
    else:
        logger.info('La propiedad ' + prop + ' no esta mapeada!')
        
    
MEDICIONES_FILE='/home/mikel/PROYECTOS/Bizkaisense/estaciones_ambientales/historicos/CSV/2012/febrero/Medidas.txt'
HORARIAS_FILE='/home/mikel/PROYECTOS/Bizkaisense/estaciones_ambientales/historicos/CSV/2012/febrero/H201202.txt'
OUT_FILE='/home/mikel/PROYECTOS/Bizkaisense/estaciones_ambientales/historicos/NT/2012/febrero/H201202.nt'
HOST='http://helheim.deusto.es:8890/sparql'


logger = logging.getLogger('parser_historico')
hdlr = logging.FileHandler('main.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)
logger.info('Empieza la fiesta')

horarias = codecs.open(HORARIAS_FILE, 'r', "iso-8859-15")
mediciones = codecs.open(MEDICIONES_FILE, 'r', "iso-8859-15")

mediciones_dict = {}

for line in mediciones.readlines():
    line_list = line.split(';')
    mediciones_dict[line_list[1]] = line_list



vm = VirtuosoManager(HOST)

out = open(OUT_FILE, 'w')

set_estaciones = Set()
#set_props = Set()

for line in horarias.readlines():
    line_list = line.split(';')
    #print line_list
    identifier = mediciones_dict[line_list[0]][0]
    identifier = identifier.encode('utf-8').replace('Ñ', 'N')
    query = 'SELECT ?s WHERE { ?s dc:identifier "' + identifier + '" . ?s rdf:type ssn:Sensor}'
    uri_list = get_uris_from_xml(vm.select(query, 'application/sparql-results+xml', ))
    if len(uri_list) > 0:
        
        #print subject
        station_subject = uri_list[0]
        date = line_list[1]
        date_list = line_list[1].split('/')
        formated_date = datetime.date(int(date_list[2]), int(date_list[1]), int(date_list[0]))

        i = 0
        for j in range(2, len(line_list) - 1):
            time = datetime.time(i)
            dt = datetime.datetime.combine(formated_date, time)
            iso_date = dt.isoformat()
            # Definimos la estación
            
            
            # Sacamos la info necesaria
            prop = string.replace(mediciones_dict[line_list[0]][2].split(' ')[0], '.', '_')
            if len(mediciones_dict[line_list[0]][2].split(' ')) > 1:
                if mediciones_dict[line_list[0]][2].split(' ')[1] == 'met':
                    prop = 'HC met.'
                elif mediciones_dict[line_list[0]][2].split(' ')[1] == 'no':
                    prop = 'HC no met.'
            #print prop
            ontology_resource, measure_unit, ontology_type, data_type, uri_value = get_info(prop)
            
            
            
            
            subject =  station_subject.encode('utf-8') + '/' + uri_value + '/' +  string.replace(date, '/', '') + '/' + str('%02d' % i)
            out.write('<' + subject.encode('utf-8') + '> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.oclc.org/NET/ssnx/ssn#Observation> . \n')
            out.write('<' + subject.encode('utf-8') + '> <http://purl.oclc.org/NET/ssnx/ssn#observedBy> <' + station_subject.encode('utf-8') + '> . \n')
            out.write('<' + subject.encode('utf-8') + '> <http://purl.org/dc/elements/1.1/date> "' + str(iso_date) + '" . \n')
            sensor_output = subject + '#sensoroutput'.encode('utf-8')
            out.write('<' + subject.encode('utf-8') + '> <http://purl.oclc.org/NET/ssnx/ssn#observationResult> <' + sensor_output.encode('utf-8') + '> . \n')
            #observed_property = subject + '#property'.encode('utf-8')
            #observed_property = 'http://helheim.deusto.es/bizkaisense/resource/prop/' + uri_value
            observed_property = ontology_resource
            out.write('<' + subject.encode('utf-8') + '> <http://purl.oclc.org/NET/ssnx/ssn#observedProperty> <' + observed_property.encode('utf-8') + '> . \n')
            
           
            
            
#            #Definimos la property        
#            out.write('<' + observed_property.encode('utf-8') + '> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.oclc.org/NET/ssnx/ssn#Property> . \n') 
#            if ontology_type == 'Class':
#                out.write('<' + observed_property.encode('utf-8') + '> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <' + ontology_resource.encode('utf-8') + '> . \n')
#            else:
#                out.write('<' + observed_property.encode('utf-8') + '> <http://www.w3.org/2002/07/owl#sameAs> <' + ontology_resource.encode('utf-8') + '> . \n')
            #set_props.add(string.replace(mediciones_dict[line_list[0]][2].split(' ')[0], '.', '_'))
            # Definimos el SensorOutput
            out.write('<' + sensor_output.encode('utf-8') + '> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.oclc.org/NET/ssnx/ssn#SensorOutput> . \n')
            output_value = subject.encode('utf-8') + '#outputvalue'.encode('utf-8')
            out.write('<' + sensor_output.encode('utf-8') + '> <http://purl.oclc.org/NET/ssnx/ssn#hasValue> <' + output_value + '> . \n')
            
            
            #Definimos el outputvalue
            
            quantity = line_list[j].split(' ')[0]
            code = line_list[j].split(' ')[1]
            if code != 'N':
                out.write('<' + output_value + '> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.oclc.org/NET/ssnx/ssn#ObservationValue> . \n')
                out.write('<' + output_value + '> <http://purl.oclc.org/NET/ssnx/ssn#hasQuantityValue> "' + quantity.encode('utf-8') + '"^^<' + data_type.encode('utf-8') + '> . \n')
                out.write('<' + output_value + '> <http://www.loa-cnr.it/ontologies/DUL.owl#isClassifiedBy> <' + measure_unit.encode('utf-8') + '> . \n')
            i = i + 1
            
    elif not identifier in set_estaciones:
        logger.info('No existe la estación ' + identifier.encode('utf-8'))
        set_estaciones.add(identifier)
        subject = 'http://helheim.deusto.es/bizkaisense/page/station/' + identifier.encode('utf-8')
        out.write('<' + subject + '> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://purl.oclc.org/NET/ssnx/ssn#Station> . \n')
        out.write('<' + subject + '> <http://purl.org/dc/elements/1.1/identifier> "' + identifier.encode('utf-8') + '" . \n')
        out.flush()
        
out.close()
logger.info('Fin del proceso!')

print set_estaciones
#print set_props

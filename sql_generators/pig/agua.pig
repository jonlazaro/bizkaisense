Register 'aux.py' using jython as myfuncs;

fs -rm -r bizkaisense/aguas/output/origenes;
fs -rm -r bizkaisense/aguas/output/datos;

data = load 'bizkaisense/aguas/input/origenes' using PigStorage(';') as (provincia:chararray, municipio:chararray, localidad:chararray, zona:chararray, ubicacion:chararray, longitud:chararray, latitud:chararray, altitud:chararray, tipo_elemento:chararray, captacion:chararray, fluoracion:chararray);

datasample = sample data 1;

origenes = foreach datasample generate myfuncs.quote(provincia) as provincia, myfuncs.quote(municipio) as municipio, myfuncs.quote(localidad) as localidad, myfuncs.quote(zona) as zona, CONCAT(CONCAT(SUBSTRING(REPLACE(longitud, '\\.', ''), 0, 2), '.'), SUBSTRING(REPLACE(longitud, '\\.', ''), 2, (int)SIZE(longitud))), CONCAT(CONCAT(SUBSTRING(REPLACE(latitud, '\\.', ''), 0, 2), '.'), SUBSTRING(REPLACE(latitud, '\\.', ''), 2, (int)SIZE(latitud))), myfuncs.int_or_zero(altitud) as altitud, myfuncs.quote(tipo_elemento) as tipo_elemento, myfuncs.quote(captacion) as captacion, myfuncs.quote(fluoracion) as fluoracion;

store origenes into 'bizkaisense/aguas/output/origenes' using PigStorage(',');

datos = load 'bizkaisense/aguas/input/datos' using PigStorage(';') as (fecha:chararray, parametro:chararray, provincia:chararray, municipio:chararray, localidad:chararray, zona:chararray, punto_muestreo:chararray, tipo_punto:chararray, laboratorio:chararray, elemento:chararray, tipo_analisis:chararray, motivo:chararray, calificacion:chararray, resultado:chararray, valor_parametrico:chararray, unidad:chararray);

dump datos;

datossample = sample datos 1;

datos_mod = foreach datossample generate myfuncs.conversion_fecha(fecha) as fecha, myfuncs.quote(parametro) as parametro, myfuncs.quote(provincia) as provincia, myfuncs.quote(municipio) as municipio, myfuncs.quote(localidad) as localidad, myfuncs.quote(zona) as zona, myfuncs.quote(punto_muestreo) as punto_muestreo, myfuncs.quote(tipo_punto) as tipo_punto, myfuncs.quote(laboratorio) as laboratorio, myfuncs.quote(elemento) as elemento, myfuncs.quote(tipo_analisis) as tipo_analisis, myfuncs.quote(motivo) as motivo, myfuncs.quote(calificacion) as calificacion, myfuncs.quote(resultado) as resultado, myfuncs.quote(valor_parametrico) as valor_parametrico, myfuncs.quote(unidad) as unidad;

datos_filter = filter datos_mod by not fecha matches 'Fecha';

store datos_filter into 'bizkaisense/aguas/output/datos' using PigStorage(',');

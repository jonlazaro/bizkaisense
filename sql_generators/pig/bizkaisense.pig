%declare uri 'http://helheim.deusto.es/bizkaisense/resource/station/';

define generate_measurement (data, time) returns measurement {
        rawMeasurement = foreach $data generate  code as code:chararray, CONCAT(CONCAT(CONCAT(splittedDate.$2, '-'), CONCAT(splittedDate.$1, '-')), CONCAT(splittedDate.$0, ' $time:00:00')) as date:chararray, STRSPLIT(time$time, ' ').$0 as value:chararray, station, abrev, medDesc;
        filteredMeasurement = filter rawMeasurement by not value matches '100001' and not value matches '1000.01';
        $measurement = foreach filteredMeasurement generate CONCAT(CONCAT(code, '-'), date) as id:chararray, code, date, value, station, abrev, medDesc;
}

fs -rm -r bizkaisense/observations;
fs -rm -r bizkaisense/stations;
--fs -rm -r bizkaisense/properties;
fs -rm -r bizkaisense/stationMeasuredProps;

data = load 'bizkaisense/input' using PigStorage(';') as (code:chararray, date:chararray, time00:chararray, time01:chararray, time02:chararray, time03:chararray, time04:chararray, time05:chararray, time06:chararray, time07:chararray, time08:chararray, time09:chararray, time10:chararray, time11:chararray, time12:chararray, time13:chararray, time14:chararray, time15:chararray, time16:chararray, time17:chararray, time18:chararray, time19:chararray, time20:chararray, time21:chararray, time22:chararray, time23:chararray);

datasample = sample data 1;

medidas = load 'bizkaisense/Medidas-all.txt' using PigStorage(';') as (station:chararray, code:chararray, abrev:chararray, desc:chararray);

st = foreach medidas generate null, REPLACE(station, 'Ñ', 'N') as station;
stdisct = distinct st;
stdisct = filter stdisct by not station matches 'CRUCES';
stdisct = filter stdisct by not station matches 'DONOS1';
stdisct = filter stdisct by not station matches 'ALBIA';
stdisct = filter stdisct by not station matches 'ESVIT1';
stdisct = filter stdisct by not station matches 'INGENI';

store stdisct into 'bizkaisense/stations' using PigStorage(',');

jointData = join datasample by code, medidas by code;
jointData = distinct jointData;
jointData = filter jointData by not medidas::abrev matches 'Rain';
jointData = filter jointData by not medidas::abrev matches 'PST';
jointData = filter jointData by not medidas::station matches 'CRUCES';
jointData = filter jointData by not medidas::station matches 'DONOS1';
jointData = filter jointData by not medidas::station matches 'ALBIA';
jointData = filter jointData by not medidas::station matches 'ESVIT1';
jointData = filter jointData by not medidas::station matches 'INGENI';


filteredData = foreach jointData generate REPLACE(datasample::code, 'Ñ', 'N') as code, datasample::date as date, REPLACE(medidas::station, 'Ñ', 'N') as station, medidas::abrev as abrev, medidas::desc as medDesc, datasample::time00..datasample::time23;

splittedData = foreach filteredData generate code, STRSPLIT(date, '/') as splittedDate, station, abrev, medDesc, datasample::time00..;

measurement00 = generate_measurement(splittedData, '00');
measurement01 = generate_measurement(splittedData, '01');
measurement02 = generate_measurement(splittedData, '02');
measurement03 = generate_measurement(splittedData, '03');
measurement04 = generate_measurement(splittedData, '04');
measurement05 = generate_measurement(splittedData, '05');
measurement06 = generate_measurement(splittedData, '06');
measurement07 = generate_measurement(splittedData, '07');
measurement08 = generate_measurement(splittedData, '08');
measurement09 = generate_measurement(splittedData, '09');
measurement10 = generate_measurement(splittedData, '10');
measurement11 = generate_measurement(splittedData, '11');
measurement12 = generate_measurement(splittedData, '12');
measurement13 = generate_measurement(splittedData, '13');
measurement14 = generate_measurement(splittedData, '14');
measurement15 = generate_measurement(splittedData, '15');
measurement16 = generate_measurement(splittedData, '16');
measurement17 = generate_measurement(splittedData, '17');
measurement18 = generate_measurement(splittedData, '18');
measurement19 = generate_measurement(splittedData, '19');
measurement20 = generate_measurement(splittedData, '20');
measurement21 = generate_measurement(splittedData, '21');
measurement22 = generate_measurement(splittedData, '22');
measurement23 = generate_measurement(splittedData, '23');

total = union measurement00, measurement01, measurement02, measurement03, measurement04, measurement05, measurement06, measurement07, measurement08, measurement09, measurement10, measurement11, measurement12, measurement13, measurement14, measurement15, measurement16, measurement17, measurement18, measurement19, measurement20, measurement21, measurement22, measurement23;

total = foreach total generate null, date, value, station, abrev;

--properties = foreach total generate null, abrev;
--properties = distinct properties;
--store properties into 'bizkaisense/properties' using PigStorage(',');

stationMeasuredProps = foreach total generate station, abrev;
stationMeasuredProps = distinct stationMeasuredProps;
store stationMeasuredProps into 'bizkaisense/stationMeasuredProps' using PigStorage(',');

--store total into 'hbase://bizkaisense' using org.apache.pig.backend.hadoop.hbase.HBaseStorage('bs:code, bs:datetime, bs:value, bs:station, bs:abrev, bs:medDesc');
store total into 'bizkaisense/observations' using PigStorage(',');

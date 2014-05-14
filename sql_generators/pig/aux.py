@outputSchema("word:chararray")
def quote(word):
    if word != None:
    	#print word
    	return "'%s'" % word.replace(',', '_')
    else:
  	return 'Null'

@outputSchema("word:chararray")
def int_or_zero(word):
    if word != None:
        return word
    else:
        return '0'

@outputSchema("word:chararray")
def conversion_fecha(word):
    sdate = word.split('/')
    if len(sdate) == 3:
    	return "'%s-%s-%s'" % (sdate[2], sdate[1], sdate[0])
    else:
	return word

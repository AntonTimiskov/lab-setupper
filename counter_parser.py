from logger import log
import csv, time, json, socket
from datetime import datetime

__All__ = ('Parse')

def Parse(filename):
	reader = csv.reader(open(filename, 'r'), delimiter=',')		
	headers = reader.next()[1:]
	r = {
		'labname': socket.gethostname(),
		'counters': {}
	}
	result = r['counters']
	startValue = 'startValue'
	maxValue = 'maxValue'
	finishValue = 'finishValue'
	startValueChecked = False
	for header in headers:
		result[header] = { startValue: None, maxValue: None, finishValue: None}

	data = []		
	while True:
		try:
			data = reader.next()
		except:
			break
		data = data[1:]

		index = 0
		for value in data:
			try:
				value = int(value)
			except:
				if not startValueChecked:
					result[headers[index]][startValue] = None
				result[headers[index]][finishValue] = None
				index += 1
				continue
			if not startValueChecked:
				result[headers[index]][startValue] = value
			result[headers[index]][finishValue] = value
			if result[headers[index]][maxValue] == None or result[headers[index]][maxValue] < value:
				result[headers[index]][maxValue] = value
			index += 1
		startValueChecked = True
	log.Debug(json.dumps(r, indent=4, sort_keys=True))
	return r

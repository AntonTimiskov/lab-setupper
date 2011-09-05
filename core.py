import os, sys, time, tempfile, re
from logger import log

_counter_name = 'SAIP'

class ExecutingError(Exception): pass

def _runProcess(cmd_line):
	log.Debug(cmd_line)
	import subprocess
	res = subprocess.Popen( cmd_line , shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
	res.wait()
	log.Debug("returned code: %s" % res.returncode)
	if res.returncode != 0:
		log.Debug('stdout: %s' % res.stdout.read())
		log.Debug('stderr: %s' % res.stderr.read())
		raise ExecutingError(res.returncode)
	return res.stdout.read()

def deleteCounters(counter_name=_counter_name):
	cmd_line = "logman.exe delete %(counter_name)s" % { 'counter_name': counter_name }
	return _runProcess( cmd_line )

def queryCounters(counter_name=_counter_name):
	cmd_line = "logman.exe query %(counter_name)s" % { 'counter_name': counter_name }
	return _runProcess( cmd_line )

def createCounters(counter_name=_counter_name, counters=[], output=tempfile.mkstemp(prefix="labSetuper_")[1], format='csv', interval=1):
	try:
		os.remove(output)
	except:pass
	
	if not counters:
		for i in range(5):
			counters += ['"\\Process(http#%d)\\Private Bytes"' % i]
			counters += ['"\\Process(pythonw#%d)\\Private Bytes"' % i]
			counters += ['"\\Process(pythonservice#%d)\\Private Bytes"' % i]
	cmd_line = "logman.exe create counter %(counter_name)s -c %(counters)s -o %(output)s -f %(format)s -si %(interval)s" % { 'counter_name': counter_name, 'counters': " ".join(counters), 'output': output, 'format': format, 'interval': interval }
	return _runProcess( cmd_line )

def startCounters(counter_name=_counter_name):
	cmd_line = "logman.exe start %(counter_name)s" % { 'counter_name': counter_name }
	return _runProcess( cmd_line )

def stopCounters(counter_name=_counter_name):
	cmd_line = "logman.exe stop %(counter_name)s" % { 'counter_name': counter_name }
	return _runProcess( cmd_line )

def parseCountersFile(counter_name=_counter_name):
	output = queryCounters(counter_name=counter_name)
	import re
	m = re.search('Output Location:\s*([^\r\n]*?)[\n\r]', output, re.DOTALL)
	if not m:
		raise Exception('Output file not found')
	filename = m.group(1)
	del m
	import counter_parser
	result = counter_parser.Parse(filename)
	#os.remove( filename )
	print filename
	return result
	



#!/usr/bin/env python

__ALL__ = ('setup', 'teardown', 'status')

import os, sys
import core, logger

def setup(*args):
	try:
		core.deleteCounters()
	except core.ExecutingError: pass
	core.createCounters()
	core.startCounters()

def teardown(*args):
	try:
		core.stopCounters()
		core.parseCountersFile()
	finally: 
		core.deleteCounters()

def status(*args):
	print 'STATUS OK'

if __name__ == "__main__":
	try:
		logger.log.Init(os.path.normpath(os.path.join(os.path.dirname(__file__),'labsetupper.log')))
	
		if 'setup' == sys.argv[1]:
			setup(sys.argv[2:])
		elif 'teardown' == sys.argv[1]:
			teardown(sys.argv[2:])
		elif 'status' == sys.argv[1]:
			status(sys.argv[2:])
		else:
			raise Exception("Unknown command")
		sys.exit(0)
	except Exception,ex:
		print "%s" % ex
		print "usage: %s setup|teardown|status" % sys.argv[0]
		sys.exit(2)

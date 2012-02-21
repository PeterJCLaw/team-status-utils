#!/usr/bin/env python

import util
import sys

if len(sys.argv) != 2:
	print "Usage: %s [TEAM|FILE]" % sys.argv[0]
	print ' Must be run from the directory containing the status files'
	exit(1)

team, fileName = util.getInfo(sys.argv[1])

util.review(fileName, True)

print 'Image accepted'

try:
	import localconfig as conf
except ImportError:
	print 'Unable to move image to live location without a local config.'
	print 'You should add a localconfig.py based on localconfig.py.txt'
	exit(1)

import shutil
shutil.move(conf.src, conf.dest)

#!/usr/bin/env python

import util
import sys

if len(sys.argv) != 2:
	print "Usage: %s [TEAM|FILE]" % sys.argv[0]
	print ' Must be run from the directory containing the status files'
	exit(1)

fileName = util.getFileName(sys.argv[1])

util.review(fileName, False)

print 'Image rejected'

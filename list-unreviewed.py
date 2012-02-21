#!/usr/bin/env python

from __future__ import with_statement

import util
import os
import sys

if len(sys.argv) == 1:
	path = os.path.abspath('.')
else:
	path = sys.argv[1]

count = 0
none = True

for team, fp in util.getFileNames(path):
	count += 1
	if util.needsImageReview(fp):
		print team
		none = False

if none:
	print "Found no teams (of %d) in need of review in '%s'." % (count, path)

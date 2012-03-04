#!/usr/bin/env python

from __future__ import with_statement

import json
import os.path
import sys

import srusers as sr

TEAM_PREFIX = 'team-'
STATUS_POSTFIX = '-status.json'

def putUrlInStatus(entry, filePath):
	url = entry['url']

	info = dict()
	if entry['valid'] and entry['checked']:
		info['live'] = url
		info['reviewed'] = True
	else:
		info['draft'] = url

	data = None
	with open(filePath, 'w+') as fp:
		try:
			data = json.load(fp)
		except ValueError:
			data = dict()

		data['feed'] = info
		json.dump(data, fp)

if len(sys.argv) != 3:
	print "Usage: convert.py path/to/blog-feeds.json path/to/team-status-folder"
	exit(1)

filePath = sys.argv[1]
statusPath = sys.argv[2]

print "Converting %s." % filePath

data = None
with open(filePath) as fp:
	data = json.load(fp)

#print data

for entry in data:
#	print entry
	uid = entry['user']
	user = sr.user(uid)
#	print user
	for group in user.groups():
		if group[:len(TEAM_PREFIX)] == TEAM_PREFIX:
			tid = group[len(TEAM_PREFIX):]
			print "Adding value to %s." % tid
			statusFilePath = os.path.join(statusPath, tid+STATUS_POSTFIX)
			putUrlInStatus(entry, statusFilePath)

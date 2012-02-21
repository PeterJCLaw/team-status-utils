
from __future__ import with_statement

import os.path
import json

TEAM_PREFIX = 'team-'
STATUS_POSTFIX = '-status.json'

def getInfo(arg):

	if arg[-1 * len(STATUS_POSTFIX):] == STATUS_POSTFIX:
		team = arg[:-1 * len(STATUS_POSTFIX)]
		fileName = arg
	else:
		team = arg
		fileName = arg + STATUS_POSTFIX

	if not os.path.exists(fileName):
		print "Could not find status file '%s' for team '%s'" % (fileName, team)
		exit(1)

	return team, fileName

def getFileName(arg):
	return getInfo(arg)[1]

def review(fileName, accept):
	data = None

	with open(fileName) as f:
		data = json.load(f)

#	print data['image']

	if data is None or not data.has_key('image') or not data['image'].has_key('draft'):
		print 'This team does not have a valid image to review!'
		exit(1)

	data['image']['reviewed'] = True

	if accept:
		data['image']['live'] = data['image']['draft']

	with open(fileName, 'w') as f:
		json.dump(data, f)

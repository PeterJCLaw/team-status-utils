
from __future__ import with_statement

import os.path
import json

TEAM_PREFIX = 'team-'
STATUS_POSTFIX = '-status.json'

def _getInfo(arg):

	if arg[-1 * len(STATUS_POSTFIX):] == STATUS_POSTFIX:
		team = arg[:-1 * len(STATUS_POSTFIX)]
		fileName = arg
	else:
		team = arg
		fileName = arg + STATUS_POSTFIX

	return team, fileName

def getInfo(arg):

	team, fileName = _getInfo(arg)

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

def getFileNames(path):
	for fn in os.listdir(path):
		if fn[-1 * len(STATUS_POSTFIX):] == STATUS_POSTFIX:
			t, fn = _getInfo(fn)
			fp = os.path.join(path, fn)
			yield t, fp

def needsImageReview(fileName):
	data = None

	with open(fileName) as f:
		data = json.load(f)

	if data is None or not data.has_key('image'):
		return False

	imgData = data['image']

	return imgData.has_key('reviewed') and not imgData['reviewed']

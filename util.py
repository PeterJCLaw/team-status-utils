
from __future__ import with_statement

import json
import hashlib
import os
import os.path
import sys

TEAM_PREFIX = 'team-'
STATUS_POSTFIX = '-status.json'

def checkAndMoveImageWithOutput(team, md5):
	ret = False
	try:
		ret = checkAndMoveImage(team, md5)
	except ImportError:
		print >> sys.stderr, 'Unable to move image to live location without a local config.'
		print >> sys.stderr, 'You should add a localconfig.py based on localconfig.py.txt'
		exit(1)

	if ret:
		print "Moved image for team '{0}'.".format(team)
	else:
		print "Image for team '{0}' failed hash check.".format(team)
	return ret

def checkAndMoveImage(team, md5):
	import localconfig as conf

	def read(fn):
		src = os.path.join(conf.src, fn)
		data = None
		with open(src) as fp:
			data = fp.read()
		dest = os.path.join(conf.dest, fn)
		return data, dest

	def write(dest, data):
		folder = os.path.dirname(dest)
		if not os.path.exists(folder):
			os.makedirs(folder)

		with open(dest, 'w') as fp:
			fp.write(data)

	thumb_data, thumb_dest = read(team + '_thumb.png')
	main_data, main_dest = read(team + '.png')

	actualMD5 = hashlib.md5(main_data).hexdigest()
	if actualMD5 != md5:
		return False

	write(main_dest, main_data)
	write(thumb_dest, thumb_data)
	return True

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
	if not needsImageReview(fileName):
		t = _getInfo(fileName)[0]
		print "Team %s's image has already been reviewed!" % t
		exit(1)

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

def hasReviewedImage(fileName):
	data = None

	with open(fileName) as f:
		data = json.load(f)

	if data is None or not data.has_key('image'):
		return False, None

	imgData = data['image']

	review_state = imgData.has_key('reviewed') and imgData['reviewed']
	live_value = imgData['live']

	return review_state, live_value

def getReviewedImages(possible_teams):

	images = {}

	for team in possible_teams:
		fileName = _getInfo(team)[1]
		reviewed, md5 = hasReviewedImage(fileName)
		if reviewed:
			images[team] = md5

	return images

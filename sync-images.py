#!/usr/bin/env python

import re

import srusers as sr
import util

def get_team_list():
	glist = sr.groups.list()
	#glist = ['team-ABC', 'team-13']
	tlist = []

	for gname in glist:
		if re.match( '^' + util.TEAM_PREFIX + "[A-Z]{3}[0-9]?$", gname ) is not None:
			tname = gname[len(util.TEAM_PREFIX):]
			tlist.append(tname)

	return tlist

teams = get_team_list()
images = util.getReviewedImages(teams)

if len(images) == 0:
	print 'Nothing to do.'

for team, md5 in images.iteritems():
	util.checkAndMoveImageWithOutput(team, md5)

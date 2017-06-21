#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pylast
import operator
import time
import datetime
import lastfmsettings

def fix_duplicates(song):
	if song == "Jax Jones - Instruction" or song == "Jax Jones - Instruction ft. Demi Lovato, Stefflon Don" or song == "Jax Jones, Demi Lovato, Stefflon Don - Instruction":
		return("Jax Jones - Instruction (feat. Demi Lovato & Stefflon Don)")
	elif song == "Clean Bandit - Symphony" or song == "Zara Larsson - Symphony" or song == "Zara Larsson - Symphony (feat. Clean Bandit)" or song == "Clean Bandit - Symphony (f. Zara Larsson)" or song == "Clean Bandit - Symphony feat. Zara Larsson":
		return("Clean Bandit - Symphony (feat. Zara Larsson)")
	elif song == "Halsey - Strangers" or song == "Halsey, Lauren Jauregui - Strangers" or song == "Halsey - Strangers  ft. Lauren Jauregui":
		return("Halsey - Strangers (feat. Lauren Jauregui)")
	elif song == "DJ Khaled - Wild Thoughts" or song == "DJ Khaled, Rihanna, Bryson Tiller - Wild Thoughts" or song == "DJ Khaled - Wild Thoughts ft. Rihanna, Bryson Tiller":
		return("DJ Khaled - Wild Thoughts (feat. Rihanna & Bryson Tiller)")
	elif song == "Calvin Harris - Feels" or song == "Calvin Harris, Pharrell Williams, Katy Perry, Big Sean - Feels":
		return("Calvin Harris - Feels (feat. Pharrell Williams, Katy Perry & Big Sean)")
	elif song == "Calvin Harris - Heatstroke (fEaT. yoUnG ThUG, pHaRrELl wIlLiAmS & Ariana Grande)" or song == "Calvin Harris - Heatstroke":
		return("Calvin Harris - Heatstroke (feat. Young Thug, Pharrell Williams & Ariana Grande)")
	elif song == "Calvin Harris - Slide" or song == "Calvin Harris - sLiDe (feat. frank ocean & MIGOS)":
		return("Calvin Harris - Slide (feat. Frank Ocean & Migos)")
	elif song == "Calvin Harris - Rollin":
		return("Calvin Harris - Rollin (feat. Future & Khalid)")
	elif song == "David Guetta - 2U (Ft. Justin Bieber)" or song == "David Guetta - 2U":
		return("David Guetta - 2U (feat. Justin Bieber)")
	elif song == "Luis Fonsi & Daddy Yankee - Despacito (feat. Justin Bieber) [Remix]" or song == "Luis Fonsi - Despacito - Remix":
		return("Luis Fonsi & Daddy Yankee - Despacito (feat. Justin Bieber)")
	elif song == "Fifth Harmony - Down" or song == "Fifth Harmony, Gucci Mane - Down":
		return("Fifth Harmony - Down (feat. Gucci Mane)")
	elif song == "Katy Perry - Swish Swish" or song == "Katy Perry - Swish Swish  ft. Nicki Minaj" or song == "Katy Perry - Swish Swish (Feat. Nicki Minaj)":
		return("Katy Perry - Swish Swish (feat. Nicki Minaj)")
	elif song == "Lorde - Hard Feelings / Loveless":
		return("Lorde - Hard Feelings/Loveless")
	elif song == "Katy Perry - bOn aPpétIT" or song == "Katy Perry - Bon Appetit" or song == "Katy Perry - Bon Appétit  ft. Migos":
		return("Katy Perry - Bon Appétit (feat. Migos)")
	elif song == "Dua Lipa - Lost In Your Light":
		return("Dua Lipa - Lost In Your Light (feat. Miguel)")
	elif song == "Young Thug, Millie Go Lightly - Family Don't Matter (feat. Millie Go Lightly)":
		return("Young Thug - Family Don't Matter (feat. Millie Go Lightly)")
	else:
		return(song)

names = open("lastfm.txt", "r") #A text file where each line is a username

API_KEY = lastfmsettings.API_KEY
API_SECRET = lastfmsettings.API_SECRET

username = lastfmsettings.username
password_hash = pylast.md5(lastfmsettings.password)

from_date = "1497484800" #Edit these to run at different times - time is in unix
to_date = "1498132799"

usernames = []

for line in names:
	name = line.strip("\n").strip()
	if name not in usernames:
		usernames.append(name)
names.close()

network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET, username=username, password_hash=password_hash)

chart_full = {}

for username in usernames:
	user = network.get_user(username)
	chart = user.get_weekly_track_charts(from_date=from_date, to_date=to_date)
	temp_rank = []
	try:
		chart[9]
	except IndexError:
		print(username + " does not have enough plays.")
		continue
	counter = 9
	try:
		end_weight = chart[counter].weight
		curr_weight = end_weight
		while curr_weight == end_weight:
			counter += 1
			curr_weight = chart[counter].weight
		counter -=1
	except IndexError:
		pass
	for i in range(counter):
		song = fix_duplicates(str(chart[i].item))
		weight = chart[i].weight
		temp_rank.append((song, weight))
	res = {}
	prev = None
	for i,(k,v) in enumerate(temp_rank):
		if v!=prev:
			place,prev = i+1,v
		res[k] = place
	all_placements = res.values()
	for song in res:
		weight = res[song]
		total = all_placements.count(weight)
		if total > 1:
			last_place = weight + total - 1
			average = float(weight + last_place) / 2
			rank = float(max(16 - average, 1))
		else:
			rank = float(16 - weight)
		if song not in chart_full:
			chart_full[song] = 0.0
		chart_full[song] += rank
chart_full_temp = reversed(sorted(chart_full.items(), key=operator.itemgetter(1)))
rank = {}
outputfile = open("chart.txt", "w")
outputfile.write("Rank|Song|Total Points\n---|---|---\n")
for i,(k,v) in enumerate(chart_full_temp):
	if v!=prev:
		place,prev = i+1,v
	rank[k] = place
for i in range(len(rank)):
	song = min(rank.items(), key=operator.itemgetter(1))
	name = str(song[0])
	outputfile.write(str(song[1]) + "|" + name + "|" + str(float(chart_full.get(name))) + "\n")
	del rank[name]
outputfile.close()



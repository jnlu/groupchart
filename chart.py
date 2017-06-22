#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pylast
import operator
import time
import datetime
import lastfmsettings


names = open("lastfm.txt", "r") #A text file where each line is a username
duplicates = open("duplicates.txt", "r")

duplicate_array = []

def get_duplicates(file, array):
	for line in file:
		songs = line.split("|")
		stripped_songs = [j.strip("\n").strip(" ") for j in songs]
		array.append(stripped_songs)

get_duplicates(duplicates, duplicate_array)

duplicates.close()

def fix_duplicates(song, array):
	for songs in array:
		for i in range(len(songs)):
			check_song = songs[i]
			if song == check_song:
				return songs[-1]
	return(song)

API_KEY = lastfmsettings.API_KEY
API_SECRET = lastfmsettings.API_SECRET

username = lastfmsettings.username
password_hash = pylast.md5(lastfmsettings.password)

from_date = "1497484800" #Edit these to run at different times - time is in unix
to_date = "1498132799"

from_date2 = "1483228800"
to_date2 = "1498694400"

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
		song = fix_duplicates(str(chart[i].item), duplicate_array)
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
		if weight == 1 and song == "Lorde - Homemade Dynamite":
			print(username)
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

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pylast
import operator
import time
import datetime
import sys
import lastfmsettings #A separate python file that holds your API Key, API Secret, last.fm username, and last.fm password

chart_full = {}
number_ones = {}
total_listeners = {}
duplicate_array = []
setting = None

if len(sys.argv) != 1:
	if sys.argv[1] == "album":
		setting = "album"
	else:
		setting = "song"
else:
	setting = "song"

def get_duplicates(file, array):
	for line in file:
		array.append([j.strip("\n").strip(" ") for j in line.split("|")])

def fix_duplicates(song, array):
	song = song.replace("[", "(").replace("]", ")")
	song = song.replace("(Explicit)", "").replace("(Explicit Version)", "")
	song = song.replace("(Clean)", "").replace("(Clean Version)", "")
	song = song.replace("Ke$ha", "Kesha")
	song = song.replace("ASAP Rocky", "A$AP Rocky")
	song = song.replace(" to ", " To ")
	if setting == "album":
		song = song.replace("(Deluxe Edition)","")
		song = song.replace("(Digital Deluxe Version)", "")
		song = song.replace("(Deluxe Version)", "")
		song = song.replace("(Special Edition)", "")
		song = song.replace("(International Deluxe)", "")
		song = song.replace("(UK Deluxe)", "")
		song = song.replace("(Platinum Edition)", "")
		song = song.replace("(Deluxe)","")
		song = song.replace("(Remastered)", "")
		song = song.replace("(Extended)", "")
		song = song.replace("(International Special Edition Version)", "")
		song = song.replace("(Bonus Track Version)", "")
		song = song.replace("(Platinum Edition)", "")
		song = song.replace("(deluxe)", "")
		song = song.replace("(+digital booklet)", "")
	elif setting == "song":
		song = song.replace("(Audio)", "")
		song = song.replace("(Official Video)", "")
		song = song.replace("(Official)", "")
		song = song.replace("(Album Visual)", "")
		song = song.replace("(Album Version)", "")
		song = song.replace("(Radio Edit)", "")
		song = song.replace(" - Single Version", "")
		song = song.replace("Ft.", "feat.")
		song = song.replace("Feat.", "feat.")
		song = song.replace("ft.", "feat.")
		song = song.replace(" f. ", " feat. ")
		song = song.replace("Featuring", "feat.")
		if (song.find(" feat.") > song.find(" - ")):
			song = song.replace(" feat.", " (feat.")
			song = song + ")"
	song = song.replace("  ", " ")
	song = song.rstrip()
	for songs in array:
		for i in range(len(songs) - 1):
			if song == songs[i]:
				return songs[-1]
	return(song)

def parse_chart(chart, username):
	username = str(username)
	temp_rank = []
	try:
		chart[9]
	except IndexError:
		print(username + " does not have enough plays.")
		return
	counter = 0
	old_weight = 0
	while True:
		song = fix_duplicates(str(chart[counter].item), duplicate_array)
		weight = chart[counter].weight
		found = False
		if ((weight != old_weight) and (len(temp_rank) > 9)):
			break
		for i in range(len(temp_rank)):
			if song in temp_rank[i]:
				temp_rank[i] = (song, weight + temp_rank[i][1])
				found = True
		if not found:
			temp_rank.append((song, weight))
		if (counter >= len(chart) - 1):
			break
		old_weight = weight
		counter += 1
	try: 
		temp_rank[9]
	except IndexError:
		print(username + " does not have enough plays.")
		return
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
			rank = float(max(16 - weight, 1))
		if song not in chart_full:
			chart_full[song] = 0.0
		chart_full[song] += rank
		if song not in number_ones:
			number_ones[song] = 0
		if song not in total_listeners:
			total_listeners[song] = 0
		total_listeners[song] += 1
		if rank == 15:
			number_ones[song] += 1

def main():
	if __name__ == '__main__':
		names = open("lastfm.txt", "r") #A text file where each line is a username
		
		duplicates = open(setting + "_duplicates.txt", "r")

		get_duplicates(duplicates, duplicate_array)
		duplicates.close()

		API_KEY = lastfmsettings.API_KEY
		API_SECRET = lastfmsettings.API_SECRET

		username = lastfmsettings.username
		password_hash = pylast.md5(lastfmsettings.password)

		from_date = "1501761600" #Edit these to run at different times - time is in unix
		to_date = "1502366399"

		#from_date = "1498867200"
		#to_date = "1501545599"

		timerange = datetime.datetime.fromtimestamp(int(from_date)).strftime('%Y-%m-%d %H:%M:%S') + " to " + datetime.datetime.fromtimestamp(int(to_date)).strftime('%Y-%m-%d %H:%M:%S')
		print("current time is: " + datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S'))
		print(timerange)

		usernames = []

		for line in names:
			name = line.strip("\n").strip()
			if name not in usernames:
				usernames.append(name)
			else:
				print(name + " appeared twice.")
		names.close()

		network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET, username=username, password_hash=password_hash)

		for username in usernames:
			user = network.get_user(username)
			if setting == "album":
				try:
					chart = user.get_weekly_album_charts(from_date=from_date, to_date=to_date)
				except pylast.WSError:
					print(str(user) + " was not found.")
					continue
				else:
					parse_chart(chart, user)
			elif setting == "song":
				try:
					chart = user.get_weekly_track_charts(from_date=from_date, to_date=to_date)
				except pylast.WSError:
					print(str(user) + " was not found.")
					continue
				else:
					parse_chart(chart, user)
		chart_full_temp = reversed(sorted(chart_full.items(), key=operator.itemgetter(1)))
		rank = {}
		prev = None
		outputfile = open(setting + "_chart.txt", "w")
		outputfile.write("Rank|" + setting.title() + "|Total Points|Number Ones|Total Listeners\n---|---|---|---|---|---\n")
		for i,(k,v) in enumerate(chart_full_temp):
			if v!=prev:
				place,prev = i+1,v
			rank[k] = place
		for i in range(len(rank)):
			song = min(rank.items(), key=operator.itemgetter(1))
			name = str(song[0])
			outputfile.write(str(song[1]) + "|" + name + "|" + str(float(chart_full.get(name))) + "|")
			outputfile.write(str(number_ones[name]) + "|" + str(total_listeners[name]) + "\n")
			del rank[name]
		outputfile.close()
	print("current time is: " + datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S'))
main()


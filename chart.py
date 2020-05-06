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
exclusion_array = []
setting = None
dup_cleaner = False
all_dups = []
all_dup_targets = []
total_dup_targets = 0

if len(sys.argv) != 1:
	if "clean" in sys.argv:
		dup_cleaner = True
	if "album" in sys.argv:
		setting = "album"
	else:
		setting = "song"
else:
	setting = "song"

def get_duplicates(file, array):
	for line in file:
		if dup_cleaner:
			newline = line.split("|")
			all_dup_targets.append(newline.pop().strip("\n").strip(" "))
			for entry in newline:
				all_dups.append(entry.strip("\n").strip("|"))
		array.append([j.strip("\n").strip(" ") for j in line.split("|")])
	if dup_cleaner:
		total_dup_targets = len(all_dup_targets)
		return total_dup_targets
	else:
		return 0

def get_exclusions(file, array):
	for line in file:
		song = line.strip("\n").strip(" ")
		array.append(song)

def fix_duplicates(song, array):
	song = song.replace("[", "(").replace("]", ")")
	song = song.replace("(Explicit)", "").replace("(Explicit Version)", "")
	song = song.replace("(Clean)", "").replace("(Clean Version)", "")
	song = song.replace("Ke$ha", "Kesha")
	song = song.replace("ASAP Rocky", "A$AP Rocky")
	song = song.replace(" to ", " To ")
	song = song.replace(" of ", " Of ")
	song = song.replace(" the ", " The ")
	song = song.replace("’", "\'")
	song = song.replace("ロード", "Lorde")
	song = song.replace(" - Single", "")
	song = song.replace("N*E*R*D", "N.E.R.D")
	song = song.replace("That Poppy", "Poppy")
	song = song.replace("Ft.", "feat.")
	song = song.replace("Feat.", "feat.")
	song = song.replace("ft.", "feat.")
	song = song.replace(" f. ", " feat. ")
	song = song.replace("Featuring", "feat.")
	song = song.replace(" - From SR3MM", "")
	song = song.replace(" (From SR3MM)", "")
	song = song.replace(" - From Jxmtro", "")
	song = song.replace(" - From Swaecation", "")
	song = song.replace(" (Official Music Video)", "")
	song = song.replace(" (Lyrics)", "")
	song = song.replace("LOOΠΔ", "Loona")
	song = song.replace("Marina & The Diamonds", "Marina")
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
		song = song.replace("(U.S. Version)", "")
		if "Black Panther" in song and "The Album" in song:
			song = "Various Artists - Black Panther: The Album – Music from and Inspired By"
	elif setting == "song":
		song = song.replace("(Audio)", "").replace("(audio)", "")
		song = song.replace("(Official Audio)", "")
		song = song.replace("(Official Video)", "").replace("(Vertical)", "")
		song = song.replace("(Lyric Video)", "")
		song = song.replace("(Official)", "")
		song = song.replace("(Album Visual)", "")
		song = song.replace("(Album Version)", "")
		song = song.replace("(Radio Edit)", "")
		song = song.replace(" - Single Version", "")
		song = song.replace("(CDQ)", "")
		song = song.replace(" - Radio Edit", "")
		song = song.replace(" - Edit", "")
		song = song.replace(" (Original Version)", "")
		if (song.find(" feat.") > song.find(" - ")):
			song = song.replace(" feat.", " (feat.")
			song = song + ")"
		if "Savage" in song and "Megan" in song:
			if (("feat" in song) or ("Remix" in song)):
				song = "Megan Thee Stallion - Savage Remix (feat. Beyoncé)"
	song = song.replace("  ", " ")
	song = song.rstrip()
	for songs in array:
		for i in range(len(songs) - 1):
			songs[i] = songs[i].replace("(divider)", "|")
			if song == songs[i]:
				if dup_cleaner:
					if song in all_dups:
						all_dups.remove(song)
				return songs[-1]
	return(song)

def test_exclusions(song, array):
	for compsong in array:
		if song == compsong:
			return False
	return True

def parse_chart(chart, username, errorfile):
	username = str(username)
	temp_rank = []
	test_len = len(chart)
	if test_len == 0:
		errorfile.write(username + " does not have any plays.\n")
		return(1)
	elif test_len < 9:
		if test_len == 1:
			errorfile.write(username + " only has 1 play.\n")
		else:
			errorfile.write(username + " only has " + str(test_len) + " plays.\n")
		return(1)
	counter = 0
	old_weight = 0
	while True:
		song = fix_duplicates(str(chart[counter].item), duplicate_array)
		if dup_cleaner:
			if song in all_dup_targets:
				all_dup_targets.remove(song)
		if test_exclusions(song, exclusion_array):
			weight = chart[counter].weight
			found = False
			if ((weight != old_weight) and (len(temp_rank) > 9)):
				break
			for i in range(len(temp_rank)):
				if song == temp_rank[i][0]:
					temp_rank[i] = (song, weight + temp_rank[i][1])
					found = True
			if not found:
				temp_rank.append((song, weight))
			old_weight = weight
		if (counter >= len(chart) - 1):
			break
		counter+=1
	test_len = len(temp_rank)
	if test_len == 0:
		errorfile.write(username + " does not have any plays.\n")
		return(1)
	elif test_len < 9:
		if test_len == 1:
			errorfile.write(username + " only has 1 play.\n")
		else:
			errorfile.write(username + " only has " + str(test_len) + " plays.\n")
		return(1)
	res = {}
	prev = None
	for i,(k,v) in enumerate(temp_rank):
		if v!=prev:
			place,prev = i+1,v
		res[k] = place
	all_placements = list(res.values())
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
	return(0)


def main():
	if __name__ == '__main__':
		start_time = datetime.datetime.now()

			
		names = open("lastfm.txt", "r") #A text file where each line is a username
		
		duplicates = open(setting + "_duplicates.txt", "r")
		exclusions = open(setting + "_exclusions.txt", "r")
		problems = open("errors.txt", "w")

		total_dup_targets = get_duplicates(duplicates, duplicate_array)
		duplicates.close()

		get_exclusions(exclusions, exclusion_array)
		exclusions.close()

		API_KEY = lastfmsettings.API_KEY
		API_SECRET = lastfmsettings.API_SECRET

		username = lastfmsettings.username
		password_hash = pylast.md5(lastfmsettings.password)

		from_date = lastfmsettings.fromdate
		to_date = lastfmsettings.todate

		if setting == "album":
			from_date = lastfmsettings.fromdatealbum
			to_date = lastfmsettings.todatealbum

		print("Current time: " + datetime.datetime.fromtimestamp(int(time.time())).strftime('%Y-%m-%d %H:%M:%S'))
		timerange = datetime.datetime.fromtimestamp(int(from_date)).strftime('%Y-%m-%d %H:%M:%S') + " to " + datetime.datetime.fromtimestamp(int(to_date)).strftime('%Y-%m-%d %H:%M:%S')
		print("Chart range: " + str(timerange))

		usernames = []

		for line in names:
			name = line.strip("\n").strip().lower()
			if name not in usernames:
				usernames.append(name)
			else:
				problems.write(name + " appeared twice.\n")
		names.close()

		network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET, username=username, password_hash=password_hash)

		total = 0
		sum_total = len(usernames)
		counter = 0
		num_rejected = 0

		for username in usernames:
			counter += 1
			i = int(100 * counter / sum_total)
			sys.stdout.write('\r')
			# the exact output you're looking for:
			sys.stdout.write("[%-20s] %d%%" % ('='*int(i / 5), i))
			sys.stdout.flush()

			user = network.get_user(username)
			total += 1
			if setting == "album":
				try:
					chart = user.get_weekly_album_charts(from_date=from_date, to_date=to_date)
				except (pylast.WSError, pylast.MalformedResponseError):
					problems.write(str(user) + " was not found.\n")
					num_rejected += 1
					continue
				except :
					problems.write(str(user) + " returned MalformedResponseError.\n")
					num_rejected += 1
					continue
				else:
					num_rejected += parse_chart(chart, user, problems)
			elif setting == "song":
				try:
					chart = user.get_weekly_track_charts(from_date=from_date, to_date=to_date)
				except pylast.WSError:
					problems.write(str(user) + " was not found.\n")
					num_rejected += 1
					continue
				except :
					problems.write(str(user) + " returned MalformedResponseError.\n")
					num_rejected += 1
					continue
				else:
					num_rejected += parse_chart(chart, user, problems)
		chart_full_temp = reversed(sorted(chart_full.items(), key=lambda x:(x[1], int(total_listeners[str(x[0])]), int(number_ones[str(x[0])]))))
		rank = {}
		prev = None
		prev_t = None
		prev_n = None
		outputfile = open(setting + "_chart_" + str(from_date) + "_" + str(to_date) +".txt", mode="w", errors="ignore")
		outputfile.write("Rank|" + setting.title() + "|Total Points|Number Ones|Total Listeners\n---|---|---|---|---|---\n")
		for i,(k,v) in enumerate(chart_full_temp):
			if v == prev and total_listeners[k] == prev_t and number_ones[k] == prev_n:
				rank[k] = place
				prev,prev_t,prev_n = v,total_listeners[k],number_ones[k]
			else:
				place,prev,prev_t,prev_n = i+1,v,total_listeners[k],number_ones[k]
				rank[k] = place
		curr_time = datetime.datetime.now()

		sorted_rank_temp = sorted(rank.items(), key=lambda x:(x[1], str(x[0]).lower()))
		for song in sorted_rank_temp:
			name = str(song[0])
			outputfile.write(str(song[1]) + "|" + name + "|" + str(float(chart_full.get(name))) + "|")
			outputfile.write(str(number_ones[name]) + "|" + str(total_listeners[name]) + "\n")
		outputfile.close()
		percentage = float(100 - (float(num_rejected) * 100 / float(total)))
		print("")
		print("%d users rejected out of %d (%.2f%%)"%(num_rejected, total, percentage))
		print("Total elapsed time: " + str(datetime.datetime.now() - start_time))
		if dup_cleaner:
			remaining_dups = len(all_dup_targets)
			duppercentage = float(100 - (float(remaining_dups) * 100 / float(total_dup_targets)))
			cleanfile = open(setting + "_unused_dupes.txt", "w")
			cleanfile.write("The following songs were not found. It's recommended that you remove them from your duplicates file to speed up the chart creation process.\n\n")
			for entry in all_dup_targets:
				cleanfile.write(entry + "\n")
			cleanfile.write("\n\n---\n\nThe following individual duplicate options were not found.\n\n")
			for entry in all_dups:
				cleanfile.write(entry + "\n")

			print("Cleaned dupes")
			print("%d dups unused out of %d in file (%.2f%%)"%(remaining_dups, total_dup_targets, duppercentage))
main()

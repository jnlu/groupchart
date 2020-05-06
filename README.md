# Summary

Groupchart was created to replace last.fm’s community functunality, which has not been available for several years. With groupchart, users can create a music chart that showcases which songs or albums were most popular for a group of users within a certain timeframe. Groupchart is a popular feature in online communities such as ATRL and Reddit, with thousands of users currently being tracked to create weekly song charts.

# Requirements

  - Python 2.7
  - [The pylast interface](https://github.com/pylast/pylast)

# Set Up
 
You can find the groupchart program in [its github repository](https://github.com/jnlu/groupchart). To use the program, you will need to create these additional files:

  - A text file that contains the list of last.fm usernames you wish to include in your chart. Each username should be in its own separate line, with no additional text. Name this file “lastfm.txt”. There is [an example with the same name](https://github.com/jnlu/groupchart/blob/master/examples/lastfm.txt) in the github repository.
  - A Python file containing your last.fm settings. You will need to provide your username, your password, and your two API keys, which you can request at last.fm/api. You will also set your desired timeframe for your chart here, which needs to be given in Unix time. Name this file “lastfmsettings.py”. Look at [the example with the same file name](https://github.com/jnlu/groupchart/blob/master/examples/lastfmsettings.py) in the repository to see how to set these parameters.
    - There are [several websites](https://www.epochconverter.com/) that convert times and dates into Unix time.
  - A text file containing song name duplicates. See the Duplicates section.
  - A text file containing songs to exclude from the chart. See the Exclusions section.
 
  These files should be all be saved in the same folder as the chart program. Again, see the github repository for examples of  these files.
 
# Running & Output
 
  To run this program, open your terminal and navigate to the folder containing the chart program. Run “python chart.py”, and the program should begin. It will display the timeframe (start and end date) it is using to calculate the group chart, the current time, and a progress bar.
  
  When the program is done running, it will display how many usernames were rejected out of how many total, the percent success rate, and the elapsed time. Rejected usernames are not used to calculate the final chart. A username is rejected if:
  
  - It is a duplicate username
  - Its account was not found in the last.fm database
  - Its account has not listened to at least ten unique songs in the given time frame

  Rejected usernames and the reasons for their rejections are printed to the file "errors.txt".

  The program prints the chart to a file titled “song_chart_<chart start date>_<chart end date>.txt”. There, each song is listed in order of rank, ascending. Each line displays a song’s rank, its title and artist, its total points, its number ones (how many users listened to that song the most in the timeframe), and its total number of listeners (how many users contributed to that song’s placement). 
  
  Songs are ranked by total points, then number of total listeners, then by which song was the most played track by the most listeners. If all of those values are equal, then their ranks are tied and the songs are sorted alphabetically.
 
## Points and Ties

  For each user, the program looks at which songs they listened to in the given timeframe and how many scrobbles (last.fm’s term for plays) each song received. It then assigns each song a number of points. The song that was scrobbled the most is given 15 points, the next is given 14, and so on until the tenth most scrobbled song earns 6 points. The program only looks at the top ten songs, unless there are ties for last place. If a user has not scrobbled at least ten unique songs, then that user’s data is not counted for the chart.
  
  In the case of ties, the points given are averaged based on placement. For example, if two songs tied for second, then each of those songs will earn 13.5 points (the average of 14 and 13). If three songs tied for second, then each would earn 13 points (the average of 14 and 12).
  
  If multiple songs tie in such a way that the bottom placement is below 10, the points will still be calculated as normal. E.g. if four songs tie for ninth, each song will earn 5.5 points (the average of 7 and 4). Oftentimes, a user will have scrobbled multiple songs just once, resulting in dozens of songs tying for last place. The minimum number of points any song can earn is 1.
  
## Duplicates

  Last.fm is bad at recognizing different titles for the same song. One common example is for songs that have features; for example, last.fm will count “Clean Bandit – Symphony (feat. Zara Larsson)” as a separate song from “Clean Bandit feat. Zara Larsson – Symphony” and “Clean Bandit – Symphony ft. Zara Larsson”. Thankfully, the chart program can be set up to recognize these duplicates and merge their points together.
   
   You need to create a text file containing song duplicates, i.e. different titles that correspond to one song. Each line represents one set of titles, with individual titles separated by the “|” character. Name this file “song_duplicates.txt”.
    
  Some duplicates are automatically corrected. Minor differences in capitalization (“to” vs. “To”) are automatically fixed, as well as common aberrations in features. The program will actually correct the previous examples to “Clean Bandit – Symphony (feat. Zara Larsson)” on its own.
  
  Not all duplicates will be fixed automatically. Additional duplicates can be recorded in the aforementioned file “song_duplicates.txt”. Each line has a different set of duplicates that correspond to the same song, with each title separated by a “|” character. The last title in each line should be the title you wish to set all of the duplicate song titles as. For example, one possible line could be:
 
```
Kali Uchis - Miami|Kali Uchis, Bia - Miami|Kali Uchis - Miami (feat. BIA)
```

  If the program encounters any title in a given line, it will set the title to the last title in the line. For example, if “Kali Uchis – Miami” is found in a user’s songs, the program will change it to “Kali Uchis – Miami (feat. BIA)”. Sometimes a user will scrobble the same song under multiple titles, in which case the program will sum up their plays and distribute points accordingly.
  
  You will likely have to run the program once, then look for duplicates in the resulting chart before adding them to the duplicate file and running the program again. If a song title has the “|” character in it already, replace that character with the phrase “(break)” when recording its duplicate.
  
  See [the song duplicates file](https://github.com/jnlu/groupchart/blob/master/examples/song_duplicates.txt) in the repository for an example. Album duplicates must be stored in a file named "album_duplicates.txt".
  
## Exclusions

  Sometimes you may not want to include a song in your chart, perhaps because it has not yet been officially released. To prevent the song from appearing in the chart, and to prevent it from counting in individual users' top 10 charts, you can use a text file containing songs to exclude.
  
  Each line in this file contains one song title to exclude. Name this file "song_exclusions.txt". For example, some possible lines could be:
  
  ```
  Lady Gaga - Rain On Me (feat. Ariana Grande)
  Lady Gaga - STUPID LOVE_v5 (1.24.19)
  ```
  
  Album exclusions must be stored in a file named "album_exclusions.txt".
 
## Album Charts
 
  The program can also calculate charts for albums instead of songs. To run it for albums, run “python chart.py album” instead. You will need to set the timeframe for albums separately from songs in the settings file; see the github repository for an example. The resulting chart is printed to “album_chart.txt”.
  
  Album duplicates should be recorded in a file titled “album_duplicates.txt”. The album duplicates file follows the same syntax as that for songs; each line corresponds to a set of titles for a unique song, with each title separated by the “|” character. 
  
  Album exclusions should be recorded in a file titled "album_exclusions.txt". Like with the song exclusions file, each line corresponds to a single album that should not be counted for the chart.
  
  You do not need to create a separate username file.

## Duplicate Cleanup

  Having an excessively long duplicates file can increase the runtime. To determine which duplicates can be deleted from the file, run "python chart.py clean". The chart will be created as normal, and another file titled "song_unused_dupes.txt" is created as well. Songs from the duplicate file that do not appear on the chart are displayed at the top, and individual duplicate options for songs that did not appear are displayed afterwards. You can safely remove the rows corresponding to the top songs from your duplicates file.
  
  This function works with the albums setting; run "python chart.py album clean". 

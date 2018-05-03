# Summary

Groupchart was created to replace last.fm’s community functunality, which has not been available for several years. With it, users can create a chart that shows which songs or albums were most popular for a group of users within a certain timeframe. Groupchart is a popular weekly feature in online communities such as ATRL and Reddit, with thousands of users currently being tracked to create weekly song charts.

# Requirements

  - Python 2.7

# Set Up
 
You can find the groupchart program at this github repository. To use the program, you will need to create three additional files:

  - A text file that contains the list of last.fm usernames you wish to include in your chart. Each username should be in its own separate line, with no additional text. Name this file “lastfm.txt”. There is an example with the same name in the github repository.
  - A text file containing song duplicates, i.e. different titles that correspond to one song. Each line represents one set of titles, with individual titles separated by the “|” character. Name this file “song_duplicates.txt”. See [the Duplicates section](https://github.com/jnlu/groupchart/blob/master/README.md#duplicates) for more information and the repository for an example .
  - A Python file containing your last.fm settings. You will need to provide your username, your password, and your two API keys, which you can request at last.fm/api. You will also set your desired timeframe for your chart here, which needs to be given in Unix time. Name this file “lastfmsettings.py”. Look at the example with the same file name in the repository to see how to set these parameters.
    - There are [several websites](https://www.epochconverter.com/) that convert times and dates into Unix time.
 
  These files should be all be saved in the same folder as the chart program. Again, see the github repository for examples of all of these files.
 
# Running & Output
 
  To run this program, open your terminal and navigate to the folder containing the chart program. Run “python chart.py”, and the program should begin. It will display the timeframe (start and end date) it is using to calculate the group chart, as well as the current time. As the program runs, it will display which usernames were rejected and for what reason.
  
  When the program is done running, it will display the current time again, how many usernames were rejected out of how many total, and a percent success rate. 
  
  Rejected usernames are not used to calculate the final chart. Usernames will be rejected if:
  
  - It is a duplicate username
  - The username was not found in the last.fm database
  - The user has not listened to at least ten unique songs in the given time frame

  The program prints to a file titled “song_chart.txt”. There, each song is listed in order of rank, ascending. Each line displays a song’s rank, its title and artist, its total points, its number ones (how many users listened to that song the most in the timeframe), and its total number of listeners (how many users contributed to that song’s placement). 
  
  Songs are ranked by total points, then number of total listeners, then by which song was the most played track by the most listeners. If all of those values are equal, then their ranks are tied and the songs are sorted alphabetically.
  
  Running the program again will override the song chart file, so be sure to save the file elsewhere if you want to preserve it.
 
## Points and Ties

  For each user, the program looks at which songs they listened to in the given timeframe and how many scrobbles (last.fm’s term for plays) each song received. It then assigns each song a number of points. The song that was scrobbled the most is given 15 points, the next is given 14, and so on until the tenth most scrobbled song earns 6 points. The program only looks at the top ten songs, unless there are ties for last place. If a user has not scrobbled at least ten unique songs, then that user’s data is not counted for the chart.
  
  In the case of ties, the points given are averaged based on placement. For example, if two songs tied for second, then each of those songs will earn 13.5 points (the average of 14 and 13). If three songs tied for second, then each would earn 13 points (the average of 14 and 12).
  
  If multiple songs tie in such a way that the bottom placement is below 10, the points will still be calculated as normal. E.g. if four songs tie for ninth, each song will earn 5.5 points (the average of 7 and 4). Oftentimes, a user will have scrobbled multiple songs just once, resulting in dozens of songs tying for last place. The minimum number of points any song can earn is 1.
  
## Duplicates
  Last.fm is bad at recognizing different titles for the same song. One common example is for songs that have features; for example, last.fm will count “Clean Bandit – Symphony (feat. Zara Larsson)” as a separate song from “Clean Bandit feat. Zara Larsson – Symphony” and “Clean Bandit – Symphony ft. Zara Larsson”. Thankfully, the chart program can be set up to recognize these duplicates and merge their points together.
  
  Some duplicates are automatically corrected. Minor differences in capitalization (“to” vs. “To”) are automatically fixed, as well as common aberrations in features. The program will actually correct the previous examples to “Clean Bandit – Symphony (feat. Zara Larsson)” on its own.
  
  Not all duplicates will be fixed automatically. Additional duplicates can be recorded in the aforementioned file “song_duplicates.txt”. Each line has a different set of duplicates that correspond to the same song, with each title separated by a “|” character. The last title in each line should be the title you wish to set all of the duplicate song titles as. For example, one possible line could be:
 
```
Kali Uchis - Miami|Kali Uchis, Bia - Miami|Kali Uchis - Miami (feat. BIA)
```

  If the program encounters any title in a given line, it will set the title to the last title in the line. For example, if “Kali Uchis – Miami” is found in a user’s songs, the program will change it to “Kali Uchis – Miami (feat. BIA)”. Sometimes a user will scrobble the same song under multiple titles, in which case the program will sum up their plays and distribute points accordingly.
  
  You will likely have to run the program once, then look for duplicates in the resulting chart before adding them to the duplicate file and running the program again. If a song title has the “|” character in it already, replace that character with the phrase “(break)” when recording its duplicate.
 
## Album Setting
 
  The program can also calculate charts for albums instead of songs. To run it for albums, run “python chart.py album” instead. You will need to set the timeframe for albums separately from songs in the settings file; see the github repository for an example. The resulting chart is printed to “album_chart.txt”.
  
  Album duplicates should be recorded in a file titled “album_duplicates.txt”. The album duplicates file follows the same syntax as that for songs; each line corresponds to a set of titles for a unique song, with each title separated by the “|” character. You do not need to create a separate username file.

# Future Work

Here are other features that I hope to implement:

  - An online version, letting more people access it
  - More options, such as a way set how many songs the program checks for in each user as opposed to ten, as well as an easy way to set the timeframe, such as by just indicating you would like the chart for last week or last month
  - General runtime improvements, namely with the song sorting and the API calls

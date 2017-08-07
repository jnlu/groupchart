# groupchart
Creates a custom chart based on the last.fm weekly charts for a given group of users.

Requires various text files to run:

- lastfm.txt: holds the usernames in the group, one on each line
- lastfmsettings.py: stores your username, password, API key, and API secret
- song_duplicates.txt: a csv file with "|" as the delimiter; each entry in a row is converted to the last entry in that row
- album_duplicates.txt: a csv file with the same properties as above

Edit the file directly to input different time frames.

If no argument is provided, it will default to song. To run it for albums, add the argument "album".


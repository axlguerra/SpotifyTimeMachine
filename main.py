from bs4 import BeautifulSoup
from urllib.request import urlopen
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth



URI= 'http://example.com'

#Secret information
CLIENT_ID = 'YOUR SPOTIFY APP ID'
CLIENT_SECRET = 'YOUR SPOTIFY SECRET CODE'


#USER INPUT
input_date = input('hat year you would like to travel to in YYY-MM-DD format: ')



date_year = input_date.split('-')[0]
date_month = input_date.split('-')[1]
date_day = input_date.split('-')[2]


URL = f'https://www.billboard.com/charts/hot-100/{date_year}-{date_month}-{date_day}/'


soup = BeautifulSoup(urlopen(URL), 'html.parser')


h3 = soup.find_all('h3', class_='u-letter-spacing-0021')

#top son list
top_songs = []

for song in h3:

    top_songs.append(song.getText().strip())


#Cleaning data
clean_songs = []
for song in top_songs:
    if song != 'Songwriter(s):' and song !='Producer(s):' and song !='Imprint/Promotion Label:':
        clean_songs.append(song)


#Authentication

auth_manager= SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=URI, show_dialog=True,
                                               scope='playlist-modify-public',
                                               cache_path="token.txt"))
uder_id = sp.current_user()['id']


#Searching for songs by title and year in spotify

song_uri = []
for song in clean_songs:
    itemp = sp.search(q=f"track:{song} year:{date_year}", type="track")

    try:
        uri = itemp['tracks']['items'][0]['uri']
        song_uri.append(uri)
    except IndexError:
        #In case the script coulndt find the song
        continue

#Test
# print(uder_id)
# print(song_uri)

#Creating a playlist in spotify with Spotipy

playlist = sp.user_playlist_create(user=uder_id, name=f'Billboard {date_year}',

                        description='playlist made in python',
                        )


playlist_id = playlist['id']


#Addint song to playlist in spotify
sp.playlist_add_items(playlist_id=playlist_id, items=song_uri)



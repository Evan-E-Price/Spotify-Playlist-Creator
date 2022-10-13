import spotipy, os, pandas
from spotipy.oauth2 import SpotifyOAuth

USERNAME=""           # Enter username of spotify account
CLIENT_ID=""          # Enter client ID from developer app
CLIENT_SECRET=""      # Etner client secret ID from developer app
FILE_NAME=".txt"      # Text file name of playlist located in the same directory as this code

SCOPE="playlist-modify-private"
REDIRECT_URI="http://localhost:8080/"

# Authorization
token = spotipy.util.prompt_for_user_token(username=USERNAME,scope=SCOPE,client_id=CLIENT_ID,client_secret=CLIENT_SECRET,redirect_uri=REDIRECT_URI)
sp = spotipy.Spotify(auth=token)

# Create Playlist
playlist_data = pandas.read_csv(FILE_NAME, encoding="utf-16 LE", sep="\t")
playlist_name = os.path.splitext(FILE_NAME)[0]
playlist = sp.user_playlist_create(user=USERNAME, name=playlist_name, public=False)

# Search for songs and add to playlist
couldnt_add=[]
for i in range(len(playlist_data)):
    track = str(playlist_data['Name'][i])
    artist = str(playlist_data['Artist'][i])
    try:
        # For more strict search results use:
        # search = sp.search(q=f"track:{track} artist:{artist}", limit=1, type='track')
        # And remove the line below
        search = sp.search(q=f"{track} {artist}", limit=1, type='track')
        song = search['tracks']['items'][0]['id']
        sp.user_playlist_add_tracks(user=USERNAME, playlist_id=playlist['uri'], tracks=[song])
    except:
        couldnt_add.append([track, artist])
        continue

# Print songs that were not able to be added to the playlist
print("Could not add:")
for j in couldnt_add:
    print(" by ".join(each_song for each_song in j))
import os

from creds.secret import spotify_token
from spotify_client import SpotifyClient
from youtube_client import YoutubeClient


def run():
    # Get a list of playlists form Youtube
    youtube_client = YoutubeClient('creds/client_secret.json')
    spotify_client = SpotifyClient(spotify_token)
    playlists = youtube_client.get_playlist()

    # Ask which playlist we want to get the music videos from
    for index, playlist in enumerate(playlists):
        print(f"{index}: {playlist.title}")

    choice = int(input("\nEnter your choice: "))
    chosen_playlist = playlists[choice]
    print(f"You selected: {chosen_playlist.title}")
    print(f"Playlist Id: {chosen_playlist.id}")

    # For each video in the playlist, get the song information from Youtube
    songs = youtube_client.get_videos_from_playlist(chosen_playlist.id)
    print(f"Attempting to add {len(songs)}")
    for song in songs:
        print(f"Song: {song.artist} - {song.track}")

    # Search for the songs on Spotify
    for song in songs:
        spotify_song_id = spotify_client.search_song(song.artist, song.track)
        if spotify_song_id:
            # If we found the song, add it to our Spotify Liked Songs
            added_song = spotify_client.add_song_to_spotify(spotify_song_id)
            if added_song:
                print(f"Added {song.artist} - {song.track}")
            else:
                print(f"Wasn't able to add {song.artist} - {song.track}")


def run2():
    spotify_client = SpotifyClient(spotify_token)
    spotify_client.search_all_artist_song('Drake')


if __name__ == '__main__':
    run()


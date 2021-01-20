import requests
import urllib.parse


class Song(object):
    def __init__(self, artist, track):
        self.artist = artist
        self.track = track


class SpotifyClient(object):
    def __init__(self, api_token):
        self.api_token = api_token

    def get_browse_categories(self):
        url = f"https://api.spotify.com/v1/browse/categories"
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
            }
        )

        response_json = response.json()
        categories = response_json['categories']['items']

        for item in categories:
            url = item['icons'][0]['url']
            height = item['icons'][0]['height']
            width = item['icons'][0]['width']

            print(item['name'])
            print(f"URL: {url}")
            print(f"Height: {height}, Width: {width}\n")

    def search_all_artist_song(self, artist):
        song_title = []
        names = []
        list_of_song = []
        query = urllib.parse.quote(f'{artist}')
        url = f"https://api.spotify.com/v1/search?q={query}&type=track"
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
            }
        )

        response_json = response.json()

        items = response_json['tracks']['items']

        for item in items:
            song_title.append(item['name'])
            temp = ""
            length = len(item['artists'])
            for index, name in enumerate(item['artists']):
                if index < length-1:
                    temp += name['name'] + ", "
                else:
                    temp += name['name']
            # print(f"{temp} - {item['name']}")
            names.append(temp.strip())
            song_obj = Song(names, song_title)
        list_of_song.append(song_obj)

    def search_all_artist_song_with_featuring(self, artist):
        song_title = []
        names = []
        list_of_song = []
        query = urllib.parse.quote(f'{artist} feat.')
        url = f"https://api.spotify.com/v1/search?q={query}&type=track"
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
            }
        )

        response_json = response.json()

        items = response_json['tracks']['items']
        count = 0
        for item in items:
            song_title.append(item['name'])
            temp = ""
            length = len(item['artists'])
            for index, name in enumerate(item['artists']):
                ++count
                if index < length - 1:
                    temp += name['name'] + ", "
                else:
                    temp += name['name']
            print(f"{temp} - {item['name']}")

            names.append(temp.strip())
            song_obj = Song(names, song_title)
        print(f"Total number of songs found: {count}")
        list_of_song.append(song_obj)

    def search_song(self, artist, track):
        query = urllib.parse.quote(f'{artist} {track}')
        print(query)
        # url = f"https://api.spotify.com/v1/search?q={query}&type=track"
        url = f'https://api.spotify.com/v1/search?q=track:{track}+artist:{artist}&type=track'
        print(url)
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
            }
        )

        response_json = response.json()

        print(response_json)

        results = response_json['tracks']['items']

        if results:
            return results[0]['id']
        else:
            Exception(f"No song found for {artist} = {track}")

    def add_song_to_spotify(self, song_id):
        url = "https://api.spotify.com/v1/me/tracks"
        response = requests.put(
            url,
            json={
                'ids': [song_id]
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_token}"
            }
        )

        return response.ok

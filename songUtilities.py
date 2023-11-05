import yt_dlp
from validators import url as validate_url
import requests

API_KEY = "04003e6048d9a7ad9dfc1755c49f07e5"
SHARED_SECRET = "d3de495af61411c5adb4c4fd3763491e"
API_BASE_URL = "http://ws.audioscrobbler.com/2.0/"

def download_song(window, song, selected_folder, downloaded_songs, total_songs, songs_table):
    window['-COUNTER-'].update(f'{downloaded_songs[0]} / {total_songs}')
    ydl_opts = {
        'outtmpl': f'{selected_folder}/%(title)s.%(ext)s',
        'format': 'bestaduio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        query = song if (validate_url(song) and 'youtube' in song) else f'ytsearch:{song} lyrics'
        songs_table.append([song.strip(), 'Downloading'])

        try:
            info = ydl.extract_info(query, download=False)
            if info is not None and info.get('entries', {}):
                title = info['entries'][0].get('title')
                songs_table[downloaded_songs[0]][0] = title
        except:
            status = 'Failed'
        else:
            window['-TABLE-'].update(songs_table)

            try:
                ydl.download([query])
                status = 'Completed'
            except Exception:
                status = 'Failed'
            else: 
                songs_table[downloaded_songs[0]][1] = status
                window['-TABLE-'].update(songs_table)
                downloaded_songs[0] += 1
                window['-COUNTER-'].update(f'{downloaded_songs[0]} / {total_songs}')

def get_suggested_songs(artists):
    songs = []
    for artist in artists:
        payload = {
            'method': 'artist.gettoptracks',
            'artist': artist,
            'api_key': API_KEY,
            'format': 'json'
        }

        r = requests.get(API_BASE_URL, params=payload)

        r_json = r.json()

        for track in r_json['toptracks']['track']:
            print(track)
            print()
            print()
            songs.append(f'{track["artist"]["name"]} {track["name"]}')

        

    return sorted(songs)

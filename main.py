import os
import PySimpleGUI as sg
import yt_dlp
from validators import url as validate_url
import threading

def get_folders_in_current_dir():
    folders = [folder for folder in os.listdir() if os.path.isdir(folder)]
    return folders

def download_song(window, song, selected_folder, downloaded_songs, total_songs, songs_table):
    window['-COUNTER-'].update(f'{downloaded_songs[0]} / {total_songs}')
    ydl_opts = {
        'outtmpl': f'{selected_folder}/%(title)s.%(ext)s',
        'format': 'bestaduio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'extract_flat': 'in_playlist'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        query = song if (validate_url(song) and 'youtube' in song) else f'ytsearch:{song} lyrics'
        songs_table.append([song.strip(), 'Downloading'])

        try:
            info = ydl.extract_info(query, download=False)
            if 'entries' in info:
                title = info['entries'][0].get('title')
                songs_table[downloaded_songs[0]][0] = title
        except:
            status = 'Failed'
        else:
            window['-TABLE-'].update(songs_table)

            try:
                ydl.download(query)
                status = 'Completed'
            except Exception:
                status = 'Failed'
            else: 
                songs_table[downloaded_songs[0]][1] = status
                window['-TABLE-'].update(songs_table)
                downloaded_songs[0] += 1
                window['-COUNTER-'].update(f'{downloaded_songs[0]} / {total_songs}')

def read_file(filename):
    lines = []
    with open(filename, 'r') as f:
        for line in f:
            lines.append(line.strip())
    return lines

def main():
    layout = [
        [sg.Text('Text:')],
        [sg.InputText(key='-TEXT-', enable_events=True)],
        [sg.Text('Choose folder:')],
        [sg.Listbox(values=get_folders_in_current_dir(), size=(30, 6), key='-FOLDERS-'), sg.Button('Upload txt file')],
        [sg.Button('Download Song')],
        [sg.Text('Downloaded songs / Total songs:'), sg.Text('0 / 0', key='-COUNTER-')],
        [sg.Button('Submit', visible=False, bind_return_key=True)],
        [sg.Table(
            values=[],
            headings=['Song', 'Status'],
            display_row_numbers=False,
            auto_size_columns=False,
            col_widths=[40, 12],
            justification='left',
            num_rows=8,
            key='-TABLE-',
            enable_events=True,
            select_mode=sg.TABLE_SELECT_MODE_BROWSE
        )]
    ]

    window = sg.Window('MelodyFetch', layout)

    downloaded_songs= [0]
    total_songs = 0
    songs_table = []

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break
        elif event in ['Download Song', 'Submit', 'Upload txt file']:
            selected_folders = values['-FOLDERS-']

            if selected_folders: 
                songs = []
                if event == 'Download Song' or event == 'Submit':
                    songs = [values['-TEXT-']]
                else:
                    filepath = sg.popup_get_file('Select a txt file', file_types=(("Text files", "*.txt"),))
                    if filepath:
                        filename = os.path.basename(filepath)
                        lines = read_file(filename)
                        songs = lines

                if songs:
                    total_songs += len(songs)
                    for song in songs:
                        download_thread = threading.Thread(target=download_song, args=(window, song.strip(), selected_folders[0], downloaded_songs, total_songs, songs_table))
                        download_thread.start()
                else:
                    sg.popup('You need to type something in text box or upload a txt file')
            else:
                sg.popup('You need to select a folder')

    window.close()


if __name__ == '__main__':
    main()


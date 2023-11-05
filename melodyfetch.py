import os
import PySimpleGUI as sg
import threading
from systemUtilities import get_folders_in_current_dir, read_file
from songUtilities import download_song, get_suggested_songs

def main():
    layout = [
        [sg.Text('Text:')],
        [sg.InputText(key='-TEXT-', enable_events=True), sg.Button('Download Song')],
        [sg.Text('Choose folder:')],
        [
            sg.Column([
                [sg.Listbox(values=get_folders_in_current_dir(), size=(30, 6), key='-FOLDERS-')],
            ], element_justification='c'),
            sg.Column([
                [sg.Button('Download from txt file')],
                [sg.Button('Get suggestions from txt file')],
            ], element_justification='c'),
        ],
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
        elif event in ['Download Song', 'Submit', 'Download from txt file', 'Get suggestions from txt file']:
            selected_folders = values['-FOLDERS-']

            if selected_folders: 
                songs = []
                if event == 'Download Song' or event == 'Submit':
                    songs = [values['-TEXT-']]
                else:
                    filepath = sg.popup_get_file('Select a txt file', file_types=(("Text files", "*.txt"),))
                    if filepath:
                        filename = os.path.abspath(filepath)
                        lines = read_file(filename)
                        if event == 'Download from txt file':
                            songs = lines
                        else:
                            suggested_songs = get_suggested_songs(lines)

                            layout_selected_songs = [
                                [sg.Text('Select the songs that you want to download')]
                            ]

                            col_layout = []
                            for suggested_song in suggested_songs:
                                col_layout.append([sg.Checkbox(suggested_song, key=suggested_song)])
                            layout_selected_songs.append([sg.Column(col_layout, scrollable=True, vertical_scroll_only=True, size=(300, 300))])
                            layout_selected_songs.append([sg.Button('OK'), sg.Button('Cancel')])

                            window_selected_songs = sg.Window('Select songs', layout_selected_songs, finalize=True, resizable=True)

                            while True:
                                event, values = window_selected_songs.read()

                                if event in (sg.WINDOW_CLOSED, 'Cancel'):
                                    break
                                elif event == 'OK':
                                    songs = [suggested_song for suggested_song in suggested_songs if values.get(suggested_song)]
                                    break

                            window_selected_songs.close()

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


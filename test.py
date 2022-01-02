# def sentence_has_animal(sentence: str) -> bool:
#     return "animal" in sentence

# print(sentence_has_animal('У Ивана есть своя собственная ферма с animals'))
# print(u'У Ивана есть своя собственная ферма с animals')

# import math

# flat = [
#     5.55, 22.19, 7.78, 26.86, 5.55,
#     29.84, 22.19, 5.55, 16.85, 4.52
# ]

# sum_area = math.fsum(flat)
# print(sum_area)
# https://0.30000000000000004.com/

# import PySimpleGUI as sg
# from playsound import playsound
# from time import sleep
# import threading
# import pyglet

# def play_audio(file):
#     if file != '':
#         player = pyglet.media.Player()
#         sound = pyglet.media.load(file)
#         player.queue(sound)
#         player.play()

#         @player.event
#         def on_eos():
#             pyglet.app.exit()

#         pyglet.app.run()

# def play_sound(file):
#     playsound(file)

# layout = [  [sg.Text('Путь к файлу:')],
#             [sg.InputText(key='-IN-'), sg.FilesBrowse('Открыть')],
#             [sg.Button('Play'), sg.Button('Cancel')] ]

# window = sg.Window('Window Title', layout)

# while True:
#     event, values = window.read()
#     if event == sg.WIN_CLOSED or event == 'Cancel':
#         break
#     if event == 'Play':
#         threading.Thread(target=play_sound, args=(values['-IN-'], ), daemon=True).start()
#         sleep(1)
#         threading.Thread(target=play_sound, args=(values['-IN-'], ), daemon=True).start()
#         #playsound(values['-IN-'])
# window.close()

import PySimpleGUI as sg

"""
    Demo - Save previously entered strings for Input and Combo elements by using user_settings calls

    It's literally 1 parameter in the layout to get the list of previously used entries shown.
    Then, when the OK button is clicked, it's one line of code to save the newly added
    name into the saved list.

    Copyright 2020 PySimpleGUI.org
"""

def main():
    sg.user_settings_filename(path='.')         # The settings file will be in the same folder as this program

    layout = [[sg.T('This is your layout')],
              [sg.T('Enter or choose name'),
               sg.Combo(values=sorted(sg.user_settings_get_entry('-names-', [])),
                        default_value=sg.user_settings_get_entry('-last name chosen-', None),
                        size=(20,1), k='-COMBO-')],
              [sg.T('Remembers last value'), sg.In(sg.user_settings_get_entry('-input-', ''), k='-INPUT-')],
              [sg.OK(), sg.Button('Exit')]]

    event, values = sg.Window('Pattern for saving with Combobox', layout).read(close=True)

    if event == 'OK':
        sg.user_settings_set_entry('-names-', list(set(sg.user_settings_get_entry('-names-', []) + [values['-COMBO-'],])))
        sg.user_settings_set_entry('-last name chosen-',  values['-COMBO-'])
        sg.user_settings_set_entry('-input-', values['-INPUT-'])
        sg.popup(f"You chose {values['-COMBO-']} and input {values['-INPUT-']}",
                 'The settions dictionary:', sg.user_settings())


if __name__ == '__main__':
    main()

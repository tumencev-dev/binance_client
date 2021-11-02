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

import PySimpleGUI as sg
from playsound import playsound
from time import sleep
import threading
import pyglet

def play_audio(file):
    if file != '':
        player = pyglet.media.Player()
        sound = pyglet.media.load(file)
        player.queue(sound)
        player.play()

        @player.event
        def on_eos():
            pyglet.app.exit()

        pyglet.app.run()

def play_sound(file):
    playsound(file)

layout = [  [sg.Text('Путь к файлу:')],
            [sg.InputText(key='-IN-'), sg.FilesBrowse('Открыть')],
            [sg.Button('Play'), sg.Button('Cancel')] ]

window = sg.Window('Window Title', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break
    if event == 'Play':
        threading.Thread(target=play_sound, args=(values['-IN-'], ), daemon=True).start()
        sleep(1)
        threading.Thread(target=play_sound, args=(values['-IN-'], ), daemon=True).start()
        #playsound(values['-IN-'])
window.close()

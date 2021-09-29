import PySimpleGUI as sg
from tkinter import Tk
from PySimpleGUI.PySimpleGUI import HorizontalSeparator
from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *
from os import path, getenv
import threading
import requests
import webbrowser
import json

# константы
icon = 'iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAACXBIWXMAAAsTAAALEwEAmpwYAAAAIGNIUk0AAHolAACAgwAA+f8AAIDoAABSCAABFVgAADqXAAAXb9daH5AAAARzSURBVHjafJZLbJRVFMd/9850hvZ7a0ot6SMUSgIkirjDZwgxsTXGqLRVSFiARl6yAFMXSnRpXGjQhQFEIvXRNgqYNhG3uDIKJvKIrDSxNCUBxk4H2pn5vr+LmfJoOz3Jzfe6Of9zzu9+91xTH4ZYGSQeNrAdeAp4AKgDRMUMYIytPCipXOZ8LwE3EL9IHAPOW4SpD0NSMq9IDABZaphNGfK5GAAvTJHEoqYZSorZZtG3pj4IH7Ey56tR1HBuyeeKuJlKClPFBC/MkMTJYiJYab21MrsWc55KWwpTRVCZMyOrODOyClSmMDVDKm1rCwiE2WuBJxYry2RuhqRU5vQ3nWzY5LBhk8PprztJSjGTuRlsyiym8bgF/Jo1v1mCRAyeWMELrwZwIQ8X8rzwWsDgVysgEfmbJWyqZiaeBez8shjyuTIQMzjQTs8Wj/hiAUILoSG5VKBnq8fgQDuQkM8VSaUXzMTOFzAwXYjpaLaMDrTTs9mFv26T6rT07fyXvp1j2JUWrtymZ7PL6Ik2Opot04V4IZKy9wI2xlDIJxRnyjzX5dO1xYexaWg1HNg3weDIdQZHrnNg3wS0GhibpmurR/fzIcWZMoV8gjEGc6+Q40fjjh/JjyLZTCgIBL4c19Pxj5dL0+vVv69VsETgV8cS9b/VJk2v14lDy+V6s+8DmbpQXhTJ8SM5fjSO40fjXhTJpn2Bp9HvO/XBO22CBjlZX90bmwSewNEPRzt08osOgSPw1L2xSW7WFzToYH+bfjrdKYsvm/blhVUBN4jGbTpUYxDq11PLpfIaaXq1Pn2vtRqVK0ugocPtktZKWqvhI+2yBAJX4OvQu63S9GqpvEa//dihpWEomw7lBtF4+j4iSkAlkEGoisfeXdWUqqxmt4lZhALFIBHHMYkMzM65W6JK7UeH2/R+f7PAVUMmVNfTjVUurk4ebtHJoy3VyAN1P9MoJxsKXB18u1kjw20CXzYdzHIYx/GjqwtDDnXsw2bpVof69zTdA7gy+nc3Sbc6dPyjh+S44R3INhPKnwN5rPogN4hEqiKya9tSSa3SpRbpWov272i843z/jkbpWot0sUVSm/ZuX1oJLBXKDe44l+NH46lMtn4/4M1yyGQNBsPE1YROL6HzUcE/4tmXU1z+E9auTHHkszr4O4FlMT8PlvjkSJlC0bCkwdztEBWbMo4fjQHL7t8qYDInSOC7z9P0vgTFK5AOKsBL/4nsKhg+JXreKIMBPzTE8bw/eSINzNvU4zJ4gSF/E/rejKFs6N0M8eUEBNk1YmjY0Lu7stK8kIWcAyRpDJMs0JySGLwI8pPQt0dkjXixVyA4NWTo3Q2kwPMrc2s0nUnj+tFhweu1Gw5MTUFShLNDFU9P9qSwGXDdSra1OhriS+P54boEc27xlgn5nMGpq6RaKBm8UItFDoKkrMcs8Icx9AmKtQSSGLxAFGIoVO9rOq9iNGIL4pzx/BAZQ4LWIbPdVI4tDwJp5iy6OceWuTGXgRvAWYOOIfN7XBb/DwA31yPOSnmqQwAAAABJRU5ErkJggg=='
bg_color = '#282828'
bg_color_light = '#454545'
bg_color_frame = '#ededed'
g_api_key, g_secret_key = "", ""

# проверка ключей API и их подгрузка из файла
homepath = os.getenv('USERPROFILE')
file_path = os.path.normpath(homepath) + "\.BinanceClient\settings_binance.json"
folder_path = os.path.normpath(homepath) + "\.BinanceClient"
if os.path.exists(folder_path) == True:
    if os.path.exists(file_path) == True:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            g_api_key = data['settings']['api_key']
            g_secret_key = data['settings']["secret_key"]
else:
    os.mkdir(folder_path)

# функции
def get_price(symbol):
    response = requests.get(url=f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}")
    return json.loads(response.text)

def get_depth(symbol, price):
    response = requests.get(url=f"https://api.binance.com/api/v3/depth?symbol={symbol}&limit=500")
    data = json.loads(response.text)
    l_bids = data['bids']
    l_asks = data['asks']
    l_depth = l_bids + l_asks
    for list in l_depth:
        if price in list[0]:
            return list[1]

def copy(text):
    r = Tk()
    r.withdraw()
    r.clipboard_clear()
    r.clipboard_append(text)
    r.update()
    r.destroy()

def the_thread_order_by_volume(window, set_price, set_qty, set_quantity, set_long, set_short, set_start, set_stop, set_info):
    if g_api_key == "" and g_secret_key == "":
        window['-info-'].update("Не найдены API ключи. Вам необходимо настроить программу -->")
    else:
        ticker = values['-ticker_orders-'].upper() + "USDT"
        if ticker == "USDT" or len(ticker) < 7:
            window['-info-'].update("Кажется вы неверно заполнили поле «ТИКЕР» (Пример: BTC или btc)")
        else:
            try:
                price = values[set_price].replace(',', '.')
                qty = float(values[set_qty].replace(',', '.'))
                quantity = values[set_quantity].replace(',', '.')
                window[set_start].update(visible=False)
                window[set_stop].update(visible=True)
                window[set_price].update(disabled=True)
                window[set_qty].update(disabled=True)
                window[set_quantity].update(disabled=True)
                while True:
                    current_depth = get_depth(ticker, price)
                    if float(current_depth) < qty:
                        request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
                        if values[set_long] == True:
                            request_client.post_order(symbol=ticker, side=OrderSide.BUY, quantity=quantity, ordertype=OrderType.MARKET)
                        if values[set_short] == True:
                            request_client.post_order(symbol=ticker, side=OrderSide.SELL, quantity=quantity, ordertype=OrderType.MARKET)
                        window[set_info].Update("Код выполнен. Ордера закрыты...")
                        window[set_stop].update(visible=False)
                        window[set_start].update(visible=True)
                        window[set_price].update(disabled=False)
                        window[set_qty].update(disabled=False)
                        window[set_quantity].update(disabled=False)
                        break
                    window[set_info].Update("Текущий объём = " + str('{:.0f}'.format(float(current_depth))).replace('.', ','))
                    window.refresh()
                    if event == set_stop:
                        window[set_stop].update(visible=False)
                        window[set_start].update(visible=True)
                        window[set_price].update(disabled=False)
                        window[set_qty].update(disabled=False)
                        window[set_quantity].update(disabled=False)
                        break
            except:
                window[set_info].Update("Binance вернул ошибку!")
                window[set_stop].update(visible=False)
                window[set_start].update(visible=True)
                window[set_price].update(disabled=False)
                window[set_qty].update(disabled=False)
                window[set_quantity].update(disabled=False)

def the_thread_order_by_price(window, set_price, set_quantity, set_long, set_short, set_start, set_stop, set_info):
    if g_api_key == "" and g_secret_key == "":
        window['-info-'].update("Не найдены API ключи. Вам необходимо настроить программу -->")
    else:
        ticker = values['-ticker_orders-'].upper() + "USDT"
        if ticker == "USDT" or len(ticker)<7:
            window['-info-'].update("Кажется вы неверно заполнили поле «ТИКЕР» (Пример: BTC или btc)")
        else:
            try:
                quantity = float(values[set_quantity].replace(',', '.'))
                price = float(values[set_price].replace(',', '.'))
                current_price = get_price(ticker)['price']
                if float(current_price) > price:
                    window[set_price].update(disabled=True)
                    window[set_quantity].update(disabled=True)
                    window[set_start].update(visible=False)
                    window[set_stop].update(visible=True)
                    while True:
                        current_price = get_price(ticker)['price']
                        if float(current_price) <= price:
                            request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
                            if values[set_long] == True:
                                request_client.post_order(symbol=ticker, side=OrderSide.BUY, quantity=quantity, ordertype=OrderType.MARKET)
                                window[set_stop].update(visible=False)
                                window[set_start].update(visible=True)
                                window[set_price].update(disabled=False)
                                window[set_quantity].update(disabled=False)
                                window[set_info].Update("Код выполнен. Открыт ордер LONG")
                                break
                            if values[set_short] == True:
                                request_client.post_order(symbol=ticker, side=OrderSide.SELL, quantity=quantity, ordertype=OrderType.MARKET)
                                window[set_stop].update(visible=False)
                                window[set_start].update(visible=True)
                                window[set_price].update(disabled=False)
                                window[set_quantity].update(disabled=False)
                                window[set_info].Update("Код выполнен. Открыт ордер SHORT")
                                break
                        window[set_info].update("Текущая цена: " + '{:.4f}'.format(float(current_price)).replace('.', ','))
                        window.refresh()
                        if event == set_stop:
                            window[set_stop].update(visible=False)
                            window[set_start].update(visible=True)
                            window[set_price].update(disabled=False)
                            window[set_quantity].update(disabled=False)
                            break
                elif float(current_price) < price:
                    window[set_start].update(visible=False)
                    window[set_stop].update(visible=True)
                    window[set_price].update(disabled=True)
                    window[set_quantity].update(disabled=True)
                    while True:
                        current_price = get_price(ticker)['price']
                        if float(current_price) >= price:
                            request_client = RequestClient(api_key=g_api_key, secret_key=g_secret_key)
                            if values[set_long] == True:
                                request_client.post_order(symbol=ticker, side=OrderSide.BUY, quantity=quantity, ordertype=OrderType.MARKET)
                                window[set_stop].update(visible=False)
                                window[set_start].update(visible=True)
                                window[set_price].update(disabled=False)
                                window[set_quantity].update(disabled=False)
                                window[set_info].Update("Код выполнен. Открыт ордер LONG")
                                break
                            if values[set_short] == True:
                                request_client.post_order(symbol=ticker, side=OrderSide.SELL, quantity=quantity, ordertype=OrderType.MARKET)
                                window[set_stop].update(visible=False)
                                window[set_start].update(visible=True)
                                window[set_price].update(disabled=False)
                                window[set_quantity].update(disabled=False)
                                window[set_info].Update("Код выполнен. Открыт ордер SHORT")
                                break
                        window[set_info].update("Текущая цена: " + '{:.4f}'.format(float(current_price)).replace('.', ','))
                        window.refresh()
                        if event == set_stop:
                            window[set_price].update(disabled=False)
                            window[set_quantity].update(disabled=False)
                            window[set_stop].update(visible=False)
                            window[set_start].update(visible=True)
                            break
                else:
                    window[set_info].Update("Текущая цена равна цене условия входа")
            except:
                window[set_info].Update("Binance вернул ошибку!")
                window[set_price].update(disabled=False)
                window[set_quantity].update(disabled=False)
                window[set_stop].update(visible=False)
                window[set_start].update(visible=True)

menu_btn = [
    [
        sg.Button('Торговля', border_width=0, pad=((18,1),0), size=(10,2), button_color=bg_color_light, mouseover_colors=bg_color_light, key='-btn_orders-'),
        sg.Button('Скринер', border_width=0, pad=(1,0), size=(10,2), button_color=bg_color, mouseover_colors=bg_color_light, key='-btn_screener-'),
        sg.Button('Объём', border_width=0, pad=(1,0), size=(10,2), button_color=bg_color, mouseover_colors=bg_color_light, key='-btn_volume-'),
        sg.Button('Настройки', border_width=0, pad=(1,0), size=(10,2), button_color=bg_color, mouseover_colors=bg_color_light, key='-btn_settings-'),
        sg.Button('Инструкция', border_width=0, pad=(1,0), size=(10,2), button_color=bg_color, mouseover_colors=bg_color_light, key='-btn_instruction-'),
        sg.Button('Контакты', border_width=0, pad=((1,18),0), size=(10,2), button_color=bg_color, mouseover_colors=bg_color_light, key='-btn_contacts-')
    ]
]

by_volume_layout_1 = [
    [
        sg.Text('Цена с крупным объёмом:', background_color=bg_color_frame, text_color='black', size=(24, 1)),
        sg.Input(default_text='0', key='-price_1-', size=(12, 1))
    ],
    [
        sg.Text('Ордер, если объём меньше:', background_color=bg_color_frame, text_color='black', size=(24, 1), pad=(5, 6)),
        sg.Input(default_text='0', key='-qty_1-', size=(12, 1), pad=(5, 6))
    ],
    [sg.Text('Объём по данной цене:', key='-info_orders_1-', border_width=3, background_color=bg_color, text_color='white', size=(38,1))]
]
by_volume_layout_2 = [
    [
        sg.Radio('LONG', 'SIDE', default=True, background_color=bg_color_frame, text_color='black', key='-long_1-'),
        sg.Radio('SHORT', 'SIDE', background_color=bg_color_frame, text_color='black', key='-short_1-')
    ],
    [sg.Input(default_text='0', key='-quantity_1-', size=(18, 1))],
    [
        sg.Button('Запустить', key='-start1-',  size=(18,1), button_color=bg_color, mouseover_colors=bg_color_light, border_width=0, pad=(5,(5,5))),
        sg.Button('Остановить', key='-stop1-',  size=(18,1), button_color='red', mouseover_colors=bg_color_light, border_width=0, pad=(5,(5,5)), visible=False)
    ]
]
by_volume_layout_3 = [
    [
        sg.Text('Цена с крупным объёмом:', background_color=bg_color_frame, text_color='black', size=(24, 1)),
        sg.Input(default_text='0', key='-price_3-', size=(12, 1))
    ],
    [
        sg.Text('Ордер, если объём меньше:', background_color=bg_color_frame, text_color='black', size=(24, 1), pad=(5, 6)),
        sg.Input(default_text='0', key='-qty_3-', size=(12, 1), pad=(5, 6))
    ],
    [sg.Text('Объём по данной цене:', key='-info_orders_3-', border_width=3, background_color=bg_color, text_color='white', size=(38,1))]
]
by_volume_layout_4 = [
    [
        sg.Radio('LONG', 'SIDE_3', default=True, background_color=bg_color_frame, text_color='black', key='-long_3-'),
        sg.Radio('SHORT', 'SIDE_3', background_color=bg_color_frame, text_color='black', key='-short_3-')
    ],
    [sg.Input(default_text='0', key='-quantity_3-', size=(18, 1))],
    [
        sg.Button('Запустить', key='-start3-',  size=(18,1), button_color=bg_color, mouseover_colors=bg_color_light, border_width=0, pad=(5,(5,5))),
        sg.Button('Остановить', key='-stop3-',  size=(18,1), button_color='red', mouseover_colors=bg_color_light, border_width=0, pad=(5,(5,5)), visible=False)
    ]
]

by_price_layout_1 = [
    [
        sg.Text('Укажите цену для ордера:', background_color=bg_color_frame, text_color='black', size=(24, 1)),
        sg.Input(default_text='0', key='-price_2-', size=(12, 1))
    ],
    [sg.VerticalSeparator(pad=(0,15))],
    [sg.Text('Текущая цена:', key='-info_orders_2-', border_width=3, background_color=bg_color, text_color='white', size=(38,1))]
]
by_price_layout_2 = [
    [
        sg.Radio('LONG', 'SIDE_2', default=True, background_color=bg_color_frame, text_color='black', key='-long_2-'),
        sg.Radio('SHORT', 'SIDE_2', background_color=bg_color_frame, text_color='black', key='-short_2-')
    ],
    [sg.Input(default_text='0', key='-quantity_2-', size=(18, 1))],
    [
        sg.Button('Запустить', key='-start2-',  size=(18,1), button_color=bg_color, mouseover_colors=bg_color_light, border_width=0, pad=(5,(5,5))),
        sg.Button('Остановить', key='-stop2-',  size=(18,1), button_color='red', mouseover_colors=bg_color_light, border_width=0, pad=(5,(5,5)), visible=False)
    ]
]
by_price_layout_3 = [
    [
        sg.Text('Укажите цену для ордера:', background_color=bg_color_frame, text_color='black', size=(24, 1)),
        sg.Input(default_text='0', key='-price_4-', size=(12, 1))
    ],
    [sg.VerticalSeparator(pad=(0,15))],
    [sg.Text('Текущая цена:', key='-info_orders_4-', border_width=3, background_color=bg_color, text_color='white', size=(38,1))]
]
by_price_layout_4 = [
    [
        sg.Radio('LONG', 'SIDE_4', default=True, background_color=bg_color_frame, text_color='black', key='-long_4-'),
        sg.Radio('SHORT', 'SIDE_4', background_color=bg_color_frame, text_color='black', key='-short_4-')
    ],
    [sg.Input(default_text='0', key='-quantity_4-', size=(18, 1))],
    [
        sg.Button('Запустить', key='-start4-',  size=(18,1), button_color=bg_color, mouseover_colors=bg_color_light, border_width=0, pad=(5,(5,5))),
        sg.Button('Остановить', key='-stop4-',  size=(18,1), button_color='red', mouseover_colors=bg_color_light, border_width=0, pad=(5,(5,5)), visible=False)
    ]
]

orders_tab = [
    [
        sg.Text('Укажите тикер монеты и нажмите Enter ', background_color=bg_color_frame, text_color='black', pad=((60,0),20)),
        sg.Input(size=(20,1), border_width=1, pad=((0,60),20), key='-ticker_orders-', enable_events=True)
    ],
    [sg.Text('\nОРДЕРА ПО НАЛИЧИЮ ПЛОТНОСТИ НА ЦЕНОВОМ УРОВНЕ', size=(65,2), pad=(0,0), background_color=bg_color, justification='center', border_width=8)],
    [sg.HorizontalSeparator(color='black')],
    [
        sg.Frame('', by_volume_layout_1, background_color=bg_color_frame, border_width=0),
        sg.Frame('', by_volume_layout_2, background_color=bg_color_frame, border_width=2, element_justification='center')
    ],
    [sg.HorizontalSeparator(color='black')],
    [
        sg.Frame('', by_volume_layout_3, background_color=bg_color_frame, border_width=0),
        sg.Frame('', by_volume_layout_4, background_color=bg_color_frame, border_width=2, element_justification='center')
    ],
    [sg.HorizontalSeparator(color='black')],
    [sg.Text('\nОРДЕРА ПО ДОСТИЖЕНИЮ ЦЕНОВОГО УРОВНЯ', size=(65,2), pad=(0,0), background_color=bg_color, justification='center', border_width=8)],
    [sg.HorizontalSeparator(color='black')],
    [
        sg.Frame('', by_price_layout_1, background_color=bg_color_frame, border_width=0),
        sg.Frame('', by_price_layout_2, background_color=bg_color_frame, border_width=2, element_justification='center')
    ],
    [sg.HorizontalSeparator(color='black')],
    [
        sg.Frame('', by_price_layout_3, background_color=bg_color_frame, border_width=0),
        sg.Frame('', by_price_layout_4, background_color=bg_color_frame, border_width=2, element_justification='center')
    ],
    [sg.HorizontalSeparator(color='black')],
    [sg.VerticalSeparator(pad=(0,14))],
    [sg.Text('Здесь будет выводиться информация о работе программы :)', key='-info-', border_width=8, background_color=bg_color, text_color='white', size=(64,1))]
]
screener_tab = [
    [sg.Text('Функционал в разработке :(', background_color=bg_color_frame, text_color='black', pad=(162,162))]
]
volume_tab = [
    [
        sg.Text('Укажите тикер монеты и нажмите Enter ', background_color=bg_color_frame, text_color='black', pad=((60,0),20)),
        sg.Input(size=(20,1), border_width=1, pad=((0,60),20), key='-ticker_volume-', enable_events=True),
        sg.Button('-submit-', visible=False, bind_return_key=True)
    ],
    [sg.HorizontalSeparator(color='black')],
    [
        sg.Text('Крупный объём 1 = ', background_color=bg_color_frame, text_color='black', pad=((51,0),(20,0))),
        sg.Input(size=(20,1), key='-big_volume_1-', pad=(5,(20,0))),
        sg.Button('Копировать', key='-copy1-', disabled=True, size=(12,1), button_color=bg_color, mouseover_colors=bg_color_light, border_width=0, pad=((0,51),(20,0)))
    ],
    [
        sg.Text('Крупный объём 2 = ', background_color=bg_color_frame, text_color='black', pad=((51,0),(10,20))),
        sg.Input(size=(20,1), key='-big_volume_2-', pad=(5,(10,20))),
        sg.Button('Копировать', key='-copy2-', disabled=True, size=(12,1), button_color=bg_color, mouseover_colors=bg_color_light, border_width=0, pad=((0,51),(10,20)))
    ],
    [sg.HorizontalSeparator(color='black')]
]
settings_tab = [
    [sg.Text('API_KEY:', background_color=bg_color_frame, text_color='black', size=(12,0), pad=((32,5),(25,5)), key='-API_KEY_IN-'), sg.Input(key='-API_KEY-', pad=((5,32),(25,5)), default_text=g_api_key)],
    [sg.Text('SECRET_KEY:', background_color=bg_color_frame, text_color='black', size=(12,0), pad=((32,5),(5,5)), key='-SECRET_KEY_IN-'), sg.Input(key='-SECRET_KEY-', pad=((5,32),(5,5)), default_text=g_secret_key)],
    [
        sg.Text('Изменения сохранены', background_color=bg_color_frame, text_color=bg_color_frame, size=(20,0), pad=(32,(5, 24)), key='-settings_info-'),
        sg.Button('Сохранить', key='-save-', size=(12,1), button_color=bg_color, mouseover_colors=bg_color_light, border_width=0, pad=((152,32),(5,25)))
    ]
]
instruction_tab = [
    [sg.Text('Функционал в разработке :(', background_color=bg_color_frame, text_color='black', pad=(162,162))]
]
contacts_tab = [
    [sg.VerticalSeparator(pad=(0,50))],
    [
        sg.HorizontalSeparator(pad=(8,0)),
        sg.Text('Официальный телеграм-канал:', font=('Arial',14), pad=(0,5), background_color=bg_color_frame, text_color='black'),
        sg.Button('https://t.me/tat_lab', font=('Arial',14), pad=(0,5), button_color=('blue',bg_color_frame), border_width=0, key='-link_chanell-'),
        sg.HorizontalSeparator(pad=(8,0))
    ],
    [sg.Text('Ждите обновлений!', font=('Arial',14), background_color=bg_color_frame, text_color='black')],
    [sg.VerticalSeparator(pad=(0,50))]
]

layout = [
    [sg.Frame('', menu_btn, border_width=0, background_color=bg_color, pad=(0,0), element_justification="center")],
    [
        sg.Frame('', orders_tab, border_width=0, background_color=bg_color_frame, key='-frame_orders-', element_justification="center"),
        sg.Frame('', screener_tab, border_width=0, background_color=bg_color_frame, visible=False, key='-frame_screener-'),
        sg.Frame('', volume_tab, border_width=0, background_color=bg_color_frame, visible=False, key='-frame_volume-'),
        sg.Frame('', settings_tab, border_width=0, background_color=bg_color_frame, visible=False, key='-frame_settings-'),
        sg.Frame('', instruction_tab, border_width=0, background_color=bg_color_frame, visible=False, key='-frame_instruction-'),
        sg.Frame('', contacts_tab, border_width=0, background_color=bg_color_frame, visible=False, key='-frame_contacts-', element_justification="center")
    ]
]

window = sg.Window('Binance Client ver.5.0', layout, font=('Arial',9), background_color=bg_color, use_default_focus=False, size=(492,700), margins=(0,0), icon=icon)

while True:
    event, values = window.read()
    if event == '-btn_orders-':
        window['-btn_orders-'].update(button_color=bg_color_light)
        window['-btn_screener-'].update(button_color=bg_color)
        window['-btn_volume-'].update(button_color=bg_color)
        window['-btn_settings-'].update(button_color=bg_color)
        window['-btn_instruction-'].update(button_color=bg_color)
        window['-btn_contacts-'].update(button_color=bg_color)
        window['-frame_screener-'].update(visible=False)
        window['-frame_volume-'].update(visible=False)
        window['-frame_settings-'].update(visible=False)
        window['-frame_instruction-'].update(visible=False)
        window['-frame_contacts-'].update(visible=False)
        window['-frame_orders-'].update(visible=True)
    if event == '-btn_screener-':
        window['-btn_screener-'].update(button_color=bg_color_light)
        window['-btn_orders-'].update(button_color=bg_color)
        window['-btn_volume-'].update(button_color=bg_color)
        window['-btn_settings-'].update(button_color=bg_color)
        window['-btn_instruction-'].update(button_color=bg_color)
        window['-btn_contacts-'].update(button_color=bg_color)
        window['-frame_orders-'].update(visible=False)
        window['-frame_volume-'].update(visible=False)
        window['-frame_settings-'].update(visible=False)
        window['-frame_instruction-'].update(visible=False)
        window['-frame_contacts-'].update(visible=False)
        window['-frame_screener-'].update(visible=True)
    if event == '-btn_volume-':
        window['-btn_volume-'].update(button_color=bg_color_light)
        window['-btn_orders-'].update(button_color=bg_color)
        window['-btn_screener-'].update(button_color=bg_color)
        window['-btn_settings-'].update(button_color=bg_color)
        window['-btn_instruction-'].update(button_color=bg_color)
        window['-btn_contacts-'].update(button_color=bg_color)
        window['-frame_orders-'].update(visible=False)
        window['-frame_screener-'].update(visible=False)
        window['-frame_settings-'].update(visible=False)
        window['-frame_instruction-'].update(visible=False)
        window['-frame_contacts-'].update(visible=False)
        window['-frame_volume-'].update(visible=True)
    if event == '-btn_settings-':
        window['-btn_settings-'].update(button_color=bg_color_light)
        window['-btn_orders-'].update(button_color=bg_color)
        window['-btn_screener-'].update(button_color=bg_color)
        window['-btn_volume-'].update(button_color=bg_color)
        window['-btn_instruction-'].update(button_color=bg_color)
        window['-btn_contacts-'].update(button_color=bg_color)
        window['-frame_orders-'].update(visible=False)
        window['-frame_screener-'].update(visible=False)
        window['-frame_volume-'].update(visible=False)
        window['-frame_instruction-'].update(visible=False)
        window['-frame_contacts-'].update(visible=False)
        window['-settings_info-'].update(text_color=bg_color_frame)
        window['-frame_settings-'].update(visible=True)
    if event == '-btn_instruction-':
        window['-btn_instruction-'].update(button_color=bg_color_light)
        window['-btn_orders-'].update(button_color=bg_color)
        window['-btn_screener-'].update(button_color=bg_color)
        window['-btn_volume-'].update(button_color=bg_color)
        window['-btn_settings-'].update(button_color=bg_color)
        window['-btn_contacts-'].update(button_color=bg_color)
        window['-frame_orders-'].update(visible=False)
        window['-frame_screener-'].update(visible=False)
        window['-frame_volume-'].update(visible=False)
        window['-frame_settings-'].update(visible=False)
        window['-frame_contacts-'].update(visible=False)
        window['-frame_instruction-'].update(visible=True)
    if event == '-btn_contacts-':
        window['-btn_contacts-'].update(button_color=bg_color_light)
        window['-btn_orders-'].update(button_color=bg_color)
        window['-btn_screener-'].update(button_color=bg_color)
        window['-btn_volume-'].update(button_color=bg_color)
        window['-btn_settings-'].update(button_color=bg_color)
        window['-btn_instruction-'].update(button_color=bg_color)
        window['-frame_orders-'].update(visible=False)
        window['-frame_screener-'].update(visible=False)
        window['-frame_volume-'].update(visible=False)
        window['-frame_settings-'].update(visible=False)
        window['-frame_instruction-'].update(visible=False)
        window['-frame_contacts-'].update(visible=True)
    if event == '-submit-':
        ticker = values['-ticker_volume-'].upper() + "USDT"
        price_1 = values['-price_1-'].replace(",", ".")
        price_2 = values['-price_3-'].replace(",", ".")
        if ticker == "USDT" or len(ticker) < 7:
            window['-info-'].update("Кажется вы неверно заполнили поле «ТИКЕР» (Пример: BTC или btc)")
            window['-copy1-'].update(disabled=True)
            window['-copy2-'].update(disabled=True)
        else:
            try:
                window['-info_orders_1-'].update('Объём по данной цене: ' + '{:.0f}'.format(float(get_depth(ticker, price_1))).replace('.', ','))
                window['-info_orders_3-'].update('Объём по данной цене: ' + '{:.0f}'.format(float(get_depth(ticker, price_2))).replace('.', ','))
                window['-info_orders_2-'].update("Текущая цуна: " + '{:.4f}'.format(float(get_price(ticker)['price'])).replace('.', ','))
                window['-info_orders_4-'].update("Текущая цуна: " + '{:.4f}'.format(float(get_price(ticker)['price'])).replace('.', ','))
                amount1 = 250000 / float(get_price(ticker)['price'])
                amount2 = 1000000 / float(get_price(ticker)['price'])
                window['-big_volume_1-'].update('{:.2f}'.format(amount1).replace('.', ','))
                window['-big_volume_2-'].update('{:.2f}'.format(amount2).replace('.', ','))
                window['-copy1-'].update(disabled=False)
                window['-copy2-'].update(disabled=False)
            except:
                window['-info-'].update("Binance сообщает что такого тикера не существует! Повторите ввод")
                window['-copy1-'].update(disabled=True)
                window['-copy2-'].update(disabled=True)
    if event == '-copy1-':
        copy(values['-big_volume_1-'])
    if event == '-copy2-':
        copy(values['-big_volume_2-'])
    if event == '-ticker_orders-':
        window['-ticker_volume-'].update(values['-ticker_orders-'])
    if event == '-start1-':
        threading.Thread(target=the_thread_order_by_volume, args=(window, '-price_1-', '-qty_1-', '-quantity_1-', '-long_1-', '-short_1-', '-start1-', '-stop1-', '-info_orders_1-'), daemon=True).start()
    if event == '-start2-':
        threading.Thread(target=the_thread_order_by_price, args=(window, '-price_2-', '-quantity_2-', '-long_2-', '-short_2-', '-start2-', '-stop2-', '-info_orders_2-'), daemon=True).start()
    if event == '-start3-':
        threading.Thread(target=the_thread_order_by_volume, args=(window, '-price_3-', '-qty_3-', '-quantity_3-', '-long_3-', '-short_3-', '-start3-', '-stop3-', '-info_orders_3-'), daemon=True).start()
    if event == '-start4-':
        threading.Thread(target=the_thread_order_by_price, args=(window, '-price_4-', '-quantity_4-', '-long_4-', '-short_4-', '-start4-', '-stop4-', '-info_orders_4-'), daemon=True).start()
    if event == '-save-':
        data = {
            'settings': {
                'api_key': values['-API_KEY-'],
                'secret_key': values['-SECRET_KEY-'],
            }
        }
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        window['-settings_info-'].update(text_color='green')
        g_api_key = values['-API_KEY-']
        g_secret_key = values['-SECRET_KEY-']
    if event == '-link_chanell-':
        webbrowser.open("https://t.me/tat_lab")
    if event == sg.WIN_CLOSED:
        break
window.close()

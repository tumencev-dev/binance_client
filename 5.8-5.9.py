import os
import json

# проверка ключей API и их подгрузка из файла
print('Проверка файла конфига программы BinTrade для перехода на версию 5.9...')
homepath = os.getenv('USERPROFILE')
file_path = os.path.normpath(homepath) + "\.BinanceClient\settings_binance.json"
folder_path = os.path.normpath(homepath) + "\.BinanceClient"
if os.path.exists(folder_path) == True:
    print('Папка .BinanceClient найдена в папке пользователя...')
    if os.path.exists(file_path) == True:
        print('Файл конфига программы найден...')
        with open(file_path, 'r') as json_file:
            print('Добавляем в конфиг строку для хранения настроек скринера...')
            data = json.load(json_file)
            g_api_key = data['settings']['api_key']
            g_secret_key = data['settings']["secret_key"]
            new_data = {
                        'settings': {
                            'api_key': g_api_key,
                            'secret_key': g_secret_key,
                        }
                    }
            new_data['tickers'] = {}
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(new_data, f, ensure_ascii=False, indent=4)
        print('Файл конфига программы обновлен...')
    else:
        print('Файл конфига программы НЕ найден...')
        new_data = {
                    'settings': {
                        'api_key': '',
                        'secret_key': '',
                    }
                }
        new_data['tickers'] = {}
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, ensure_ascii=False, indent=4)
        print('Файл конфига УСПЕШНО СОЗДАН...')
else:
    print('Папка .BinanceClient НЕ найдена в папке пользователя...')
    print('Папка .BinanceClient УСПЕШНО СОЗДАНА...')
    os.mkdir(folder_path)
    new_data = {
                    'settings': {
                        'api_key': '',
                        'secret_key': '',
                    }
                }
    new_data['tickers'] = {}
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=4)
    print('Файл конфига добавлен...')
input('Работа программы завершена, нажмите любую клавишу...')
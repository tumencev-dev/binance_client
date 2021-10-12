import os
import json

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
            new_data = {
                        'settings': {
                            'api_key': g_api_key,
                            'secret_key': g_secret_key,
                        }
                    }
            new_data['tickers'] = {}
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(new_data, f, ensure_ascii=False, indent=4)
    else:
        new_data = {
                    'settings': {
                        'api_key': '',
                        'secret_key': '',
                    }
                }
        new_data['tickers'] = {}
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(new_data, f, ensure_ascii=False, indent=4)
else:
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
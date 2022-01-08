import requests, json

ticker = ''
sum = 0

while True:
    old_ticker = ticker
    ticker = input('(Пример: BTC) Введите тикер: ').upper() + 'USDT'
    
    if ticker == 'USDT' and sum == 0:
        print('Не заполнили тикер!')
        continue
    elif ticker == 'USDT' and sum != 0:
        ticker = old_ticker
    elif ticker == 'EXITUSDT':
        break

    try:
        response = requests.get(url=f"https://api.binance.com/api/v3/klines?symbol={ticker}&interval=1h")
        data = json.loads(response.text)
        sum = 0
        for i in range(-1, -169, -1):
            sum += float(data[i][5])
        print('Средний объём последних свечей: ' + '{:.0f}'.format(sum/2016))
    except:
        print('ОШИБКА! Убедитесь что правильно ввели тикер!')

# import asyncio

# async def tcp_echo_client(message):
#     reader, writer = await asyncio.open_connection(
#         'wss://stream.binance.com/', 9443)

#     print(f'Send: {message!r}')
#     writer.write(message.encode())
#     await writer.drain()

#     data = await reader.read(100)
#     print(f'Received: {data.decode()!r}')

#     print('Close the connection')
#     writer.close()
#     await writer.wait_closed()

# asyncio.run(tcp_echo_client('btcusdt@depth'))

# def convert(value):
#     if value >= 1_000_000:
#         value = '{:.1f}'.format(value / 1_000_000) + ' M'
#     elif value >= 1000:
#         value = '{:.1f}'.format(value / 1000) + ' K'
#     return value

# print(convert(123456123))
# print(convert(123152))

# import PySimpleGUI as sg

# # layout the window
# layout = [[sg.Text('A custom progress meter')],
#           [sg.ProgressBar(100, orientation='h', size=(50, 8), key='progressbar')],
#           [sg.Cancel()]]

# # create the window`
# window = sg.Window('Custom Progress Meter', layout)
# progress_bar = window['progressbar']
# # loop that would normally do something useful
# for i in range(1000):
#     # check to see if the cancel button was clicked and exit loop if clicked
#     event, values = window.read(timeout=10)
#     if event == 'Cancel'  or event == sg.WIN_CLOSED:
#         break
#   # update bar with loop value +1 so that bar eventually reaches the maximum
#     progress_bar.UpdateBar(i + 1)
# # done with loop... need to destroy the window as it's still open
# window.close()

# ticker_list = ['BANDUSDT', 'COMPUSDT', 'ENJUSDT', 'MATICUSDT', 'ADAUSDT', 'DOTUSDT', 'XRPUSDT', 'ETHUSDT', 'BNBUSDT', 'DOTUSDT', 'SUSHIUSDT', 'SOLUSDT', 'BCHUSDT', 'EOSUSDT', 'ALGOUSDT', 'ATOMUSDT', 'EGLDUSDT', 'KSMUSDT', 'LUNAUSDT', 'LINAUSDT', 'AXSUSDT', 'ICPUSDT', 'ALICEUSDT', 'LINKUSDT', 'RUNEUSDT', 'UNIUSDT', 'CHZUSDT', 'FILUSDT', 'NEOUSDT', 'IOTAUSDT', 'MKRUSDT', 'ZILUSDT']
# print(len(ticker_list))
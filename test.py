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

def convert(value):
    if value >= 1_000_000:
        value = '{:.1f}'.format(value / 1_000_000) + ' M'
    elif value >= 1000:
        value = '{:.1f}'.format(value / 1000) + ' K'
    return value

print(convert(123456123))
print(convert(123152))
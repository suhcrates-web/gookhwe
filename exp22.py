import websocket

def on_message(ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws,a,b):
    print(a)
    print(b)
    print("### closed ###")

def on_open(ws):
    ws.send('hello, world')

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://smi.webcast.go.kr/socket.io/?EIO=3&transport=websocket&sid=eYKEQg09sreVgH98AAIe",
                                on_message = on_message,
                                on_error = on_error,
                                on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
import socket

a = 'https://smi.webcast.go.kr/socket.io/?EIO=3&transport=polling&t=O9O9Pi3'
b ='https://smi.webcast.go.kr/socket.io/?EIO=3&transport=polling&t=O9O9Pj3&sid=5BphY9_IPxjtsz2sAAr4' #post
c = 'https://smi.webcast.go.kr/socket.io/?EIO=3&transport=polling&t=O9O9Pj4&sid=5BphY9_IPxjtsz2sAAr4'
d = 'https://smi.webcast.go.kr/socket.io/?EIO=3&transport=polling&t=O9O9PjF&sid=5BphY9_IPxjtsz2sAAr4'
e = 'wss://smi.webcast.go.kr/socket.io/?EIO=3&transport=websocket&sid=5BphY9_IPxjtsz2sAAr4Y9_IPxjtsz2sAAr4'

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

clientSocket.connect()
data = clientSocket.recv(1024)
print(data)
import socket

mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mysock.connect(("data.pr4e.org", 80))
cmd = "GET http://data.pr4e.org/intro-short.txt HTTP/1.0\r\n\r\n".encode()
mysock.send(cmd)
rdata = ""
while True:
    data = mysock.recv(512)
    if len(data) < 1:
        break
    rdata += data.decode()

header_text = rdata.split("\r\n\r\n", 1)[0]
"""headers = {}
for l in header_text[1:].split("\r\n"):
    kv = l.split(":",1) if ":" in l else None
    headers[kv[0]] = kv[1]
print(headers)"""
print(header_text)
mysock.close()

from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = input("Enter: ")
pos = input("Enter position: ")
count = input("Enter count: ")

html = urlopen(url, context=ctx).read()
soup = BeautifulSoup(html, "html.parser")

tags = soup("a")
for i in range(int(count) - 1):
    tags = soup("a")
    url = tags[int(pos) - 1].get("href", None)
    html = urlopen(url, context=ctx).read()
    soup = BeautifulSoup(html, "html.parser")
    tags = soup("a")
    summ = [tag.get("href", None) for tag in tags][int(pos) - 1]
    print(summ)

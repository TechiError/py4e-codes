import json
from urllib.request import urlopen

url = input("Enter location: ")
if len(url) < 1:
    url = "http://py4e-data.dr-chuck.net/comments_42.json"

print("Retrieving", url)
uh = urlopen(url)
data = uh.read()

info = json.loads(data)

comms = [item["count"] for item in info.get("comments")]
print("Count:", len(comms))
print("Sum:", sum(comms))

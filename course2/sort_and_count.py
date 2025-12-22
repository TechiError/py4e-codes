"""Module 6 Assignment 1"""

name = input("Enter file:")
if len(name) < 1:
    name = "mbox-short.txt"
dk = {}
handle = open(name, "r")
for lin in handle:
    if lin.startswith("From"):
        line = lin.split(" ")
        if len(line) < 3:
            continue
        hr = (line[6]).split(":")[0]
        dk[hr] = dk.get(hr, 0) + 1

ss = [hr for hr in dk.keys()]
ss.sort()
for h in ss:
    print(h, dk.get(h))

"""Module 5 Assignment 1"""

name = input("Enter file:")
if len(name) < 1:
    name = "mbox-short.txt"
dk = {}
handle = open(name, "r")
for lin in handle:
    if lin.startswith("From"):
        line = lin.split(" ", 2)
        if len(line) < 3:
            continue
        mail = line[1]
        dk[mail] = dk.get(mail, 0) + 1

ss = max(dk, key=dk.get)
print(ss, dk[ss])

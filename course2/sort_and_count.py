"""Write a program to read through the mbox-short.txt and
figure out the distribution by hour of the day for each of the messages.
You can pull the hour out from the 'From ' line by finding the time and
then splitting the string a second time using a colon.
From stephen.marquard@uct.ac.za Sat Jan  5 09:14:16 2008
Once you have accumulated the counts for each hour,
print out the counts, sorted by hour as shown below."""

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

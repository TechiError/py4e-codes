"""Module 4 Assignment 1"""

fname = input("Enter file name: ")
if len(fname) < 1:
    fname = "romeo.txt"
fh = open(fname)
lst = list()
for line in fh:
    lstx = line.split()
    for i in lstx:
        if i in lst:
            continue
        lst.append(i)
lst.sort()
print(lst)

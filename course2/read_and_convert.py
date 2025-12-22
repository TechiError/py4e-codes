# Module 3 Assignment 1
fname = input("Enter file name: ")
if len(fname) < 1:
    fname = "words.txt"
fh = open(fname, "r").read()
txt = fh.strip().upper()
print(txt)

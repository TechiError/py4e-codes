# Use words.txt as the file name
fname = input("Enter file name: ")
fh = open(fname, "r").read()
txt = fh.strip().upper()
print(txt)

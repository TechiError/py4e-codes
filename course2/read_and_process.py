"""Module 3 Assignment 2"""

fname = input("Enter file name: ")
if len(fname) < 1:
    fname = "mbox-short.txt"
ad = 0
srl = 0
fh = open(fname)
for line in fh:
    if not line.startswith("X-DSPAM-Confidence:"):
        continue
    nm = line.find(":")
    nm = float(line[nm + 1 :].strip())
    ad = ad + nm
    srl = srl + 1
print("Average spam confidence:", ad / srl)

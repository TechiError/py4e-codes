"""Module 2 Assignment 1"""

fh = open("romeo.txt", "r")

count = 0
for line in fh:
    print(line.strip())
    count = count + 1

print(count, "Lines")

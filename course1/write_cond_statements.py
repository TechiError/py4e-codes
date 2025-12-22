"""Module 5 Assignment 2"""

score = input("Enter Score: ")

try:
    s = float(score)
except ValueError:
    print("Error: Please enter a numeric value.")
    exit()

if s < 0.0 or s > 1.0:
    print("Error: Score is out of range. Please enter a score between 0.0 and 1.0.")
    exit()
elif s >= 0.9:
    print("A")
elif s >= 0.8:
    print("B")
elif s >= 0.7:
    print("C")
elif s >= 0.6:
    print("D")
else:
    print("F")

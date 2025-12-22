"""Module 6 Assignment 1"""


def computepay(hours, rate):
    if hours > 40:
        regular_pay = 40 * rate
        overtime_pay = (hours - 40) * (rate * 1.5)
        total_pay = regular_pay + overtime_pay
    else:
        total_pay = hours * rate
    return total_pay


# Prompt user for input
hrs = input("Enter Hours: ")
rte = input("Enter Rate per Hour: ")

# Convert input strings to float
h = float(hrs)
r = float(rte)

# Compute pay
p = computepay(h, r)
print("Pay", p)

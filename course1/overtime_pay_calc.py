"""Module 5 Assignment 1"""

hrs = input("Enter Hours:")
h = float(hrs)

rate_str = input("Enter Rate:")
rate = float(rate_str)

if h <= 40:
    pay = h * rate
else:
    regular_pay = 40 * rate
    overtime_hours = h - 40
    overtime_pay = overtime_hours * rate * 1.5
    pay = regular_pay + overtime_pay

print(pay)

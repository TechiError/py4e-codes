import re
from urllib.request import urlretrieve

url = input("Enter the link: ")
f, _ = urlretrieve(url, "regex_sum.txt")
x = open(f, "r").read()

ints = re.findall("[0-9]+", x)

summ = [int(x) for x in ints]
print(sum(summ))

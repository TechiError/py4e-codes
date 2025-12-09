"""Extracting a Number from a Text String"""

text = "X-DSPAM-Confidence:    0.8475"
col_pos = text.find(":")
number_str = text[col_pos + 1 :]
print(float(number_str.strip()))

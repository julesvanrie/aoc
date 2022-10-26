## PART 1

text = """
Le Wagon x Advent of Code
200 110 1110 1211 0212002
11102220 10200200 11011200 10122020 1201020 11111100 10212000 10200200 1201020 11102220 11112210 11010020 1201020 11020010 10202010 1201020 11111100 10212000 10200200 1201020 10202010 10220110 11101110 11102220 11111100 1201020 2220000 2211120 2210010 2201200 2200020 2121210 1201020 10122020 10200200 10120210 10220110 11010020 10110220 11001210 11102220 1201020 11020010 10202010 1201020 11021120 10220110 1201020 11111100 11020010 1201020 11021120 10220110 11001210 11020010 11112210 1201020 11111100 11020010 1201020 10210120 10200200 11111100 1201020 11101110 10200200 11122200 10110220 11101110 10122020
"""
date = text.split("\n")[2]
code = text.split("\n")[3]

# Get the time, and especially the minutes
time = []
for number in date.split(" "):
    time.append(sum([int(num) * 3**index for index, num in enumerate(number[::-1])]))
print(":".join([str(t) for t in time]))
minutes = time[2]

# Get the characters
result = []
for number in code.split(" "):
    result.append(sum([int(num) * 3**index for index, num in enumerate(number[::-1])]))
decoded = []
for number in result:
    decoded.append(int(number / minutes))
print("")
print(min(decoded), max(decoded))
print("".join([chr(d) for d in decoded]))


## PART 2
import math
print(math.pi)

import requests
pi = requests.get("http://newton.ex.ac.uk/research/qsystems/collabs/pi/pi6.txt").text

pi = pi.replace(chr(12),"").replace("\n","").replace(" ", "")

def pi_decimals(pi, length):
    return [int(digit) for digit in pi[2:length+2]]

# quick test
print("".join([str(d) for d in pi_decimals(pi, 5)]))

# the result
print(sum(pi_decimals(pi, 654321)))

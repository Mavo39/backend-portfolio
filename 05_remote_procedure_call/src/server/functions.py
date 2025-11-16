import math

def floor(x):
    return math.floor(x)

def nroot(n, x) -> int:
    return round(x ** (1/n))

def reverse(s):
    return s[::-1]

def validAnagram(str1, str2):
    return sorted(str1) == sorted(str2)

def sort(*strArr):
    return sorted(strArr)
import math
from typing import List

def floor(x: float) -> int:
    return math.floor(x)

def nroot(n: int, x: int) -> int:
    return round(x ** (1/n))

def reverse(s: str) -> str:
    return s[::-1]

def validAnagram(str1: str, str2: str) -> bool:
    return sorted(str1) == sorted(str2)

def sort(strArr: List[str]) -> List[str]:
    return sorted(strArr)
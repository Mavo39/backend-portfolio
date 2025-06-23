import sys
import random

input('Welcome to "Guess the number game"!(Press Enter)')

# 整数を入力するための関数
def get_integer(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid integer.")

# 最小値と最大値の入力
n = get_integer("Input minimum number: ")
m = get_integer("Input maximum number: ")

while n >= m:
   input("Your inputed minimum number was bigger than maximum one. Please input again. (Press Enter)")
   m = get_integer("Input maximum number: ")

answer = random.randint(n,m)


import sys
import random

input("Welcome to 'Guess the number game'!\nFirst, you'll set the minimum and maximum numbers.\nThen, try to guess the number chosen within that range.(Press Enter)")

# 整数を入力するための関数
def get_integer(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid integer.\n")

# 最小値と最大値の入力
n = get_integer("Input minimum number: ")
m = get_integer("Input maximum number: ")
print()

while n >= m:
   input("Your inputed minimum number was bigger than maximum one. Please input again. (Press Enter)")
   m = get_integer("Input maximum number: ")

answer = random.randint(n,m)

# モード選択
mode = 0
while mode not in [1,2]:
    mode = get_integer("Please select integer 1 or 2 (1: Limited attempts 2: Unlimited attempts)\nYour select is: ")

print(f"\nYou can input between {n} to {m}\n")

# メッセージ
msg_congrats = "\nCongratulations!!\nPress Enter to finish the game."
msg_game_over = "\nGame Over... The correct answer was {answer}.\n(Press Enter)"
msg_try_again = "Try again! (Press Enter)\n"
msg_input_number = "Your input number is: "
msg_out_of_range = "Your input is out of range ({n} - {m})!\n"
msg_high = "Too high!\n"
msg_low = "Too low!\n"

# モード1
if mode == 1:
    attempts = get_integer("How many times do you want to challenge???\nAttemps: ")

    for i in range(attempts):
        inputed = int(input("Your input number is: "))

        if(inputed == answer):
            input("\nCongratulations!!\nPress Enter to finish this game")
            break
        elif(attempts == 0):
            input("\nGame Over...(Press Enter)")
            break
        else:
            input("Try again!(Press Enter)\n")

# モード2
else:
    while True:
        inputed = int(input("Your input number is: "))

        if inputed == answer:
            input("\nCongratulations!!\nPress Enter to finish this game")
            break
        elif inputed > answer:
            input("Your inputed number is too large\nTry again!(Press Enter)\n")
        else:
            input("Your inputed number is too small\nTry again!(Press Enter)\n")
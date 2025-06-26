import sys
import random

print("Welcome to 'Guess the number game'!\nFirst, you'll set the minimum and maximum numbers.\nThen, try to guess the number chosen within that range.\n")

# 整数を入力するための関数
def get_integer(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please input a valid integer.\n")

# 最小値と最大値の入力
n = get_integer("Minimum number: ")
m = get_integer("Maximum number: ")
print()

# 入力値エラー
while n >= m:
   input("Your inputed minimum number was bigger than maximum one. Please input again. (Press Enter)")
   m = get_integer("Maximum number: ")
   print()

# ランダム値の生成
answer = random.randint(n,m)

# モード選択
mode = 0
while mode not in [1,2]:
    mode = get_integer("Please select game mode 1 or 2 (1: Limited attempts / 2: Unlimited attempts)\nYour select is: ")
    print()

print(f"You can input between {n} and {m}")

# メッセージ
msg_congrats = "\nCongratulations!!"
msg_game_over = "\nGame Over... The correct answer was {answer}."
msg_try_again = "Try again!"
msg_input_number = "\nYour input number is: "
msg_out_of_range = "Your input is out of range ({n} - {m})!"
msg_high = "Too high!\n"
msg_low = "Too low!\n"

# 予想数字を判定する関数
def check_guess(guess, answer, n, m):
    if guess == answer:
        print(msg_congrats)
        return True
    elif guess < n or guess > m:
        print(msg_out_of_range.format(n=n, m=m))
    elif guess > answer:
        print(msg_high + msg_try_again)
    else:
        print(msg_low + msg_try_again)
    return False

# 予想数字を安全に入力する関数
def get_guess(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please input a valid integer.")

# モード1
if mode == 1:
    attempts = 0
    max_attempts = m - n + 1

    while attempts < 1 or attempts > max_attempts:
        attempts = get_integer(f"How many attempts do you want to try???(Max: {max_attempts})\nAttemps: ")

        if attempts > max_attempts: 
            print(f"You can try up to {max_attempts} attempts.\nPlease input within that range.\n")
        elif attempts < 1:
            print("Please enter at least 1 attempt.\n")

    for i in range(attempts):
        guess = get_guess(msg_input_number)

        if check_guess(guess, answer, n, m):
            break
    
    else:
        print(msg_game_over.format(answer=answer))

# モード2
else:
    while True:
        guess = get_guess(msg_input_number)

        if check_guess(guess, answer, n, m):
            break

        user_continue = input("Do you want to continue? (y/n): ").strip().lower()

        if user_continue == "n":
            print(msg_game_over.format(answer=answer))
            break
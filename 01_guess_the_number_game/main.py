import sys
import random

input("Welcome to 'Guess the number game'!\nFirst, you'll set the minimum and maximum numbers.\nThen, try to guess the number chosen within that range.(Press Enter)\n")

# 整数を入力するための関数
def get_integer(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid integer.\n")

# 最小値と最大値の入力
n = get_integer("Minimum number: ")
m = get_integer("Maximum number: ")
print()

while n >= m:
   input("Your inputed minimum number was bigger than maximum one. Please input again. (Press Enter)")
   m = get_integer("Maximum number: ")

answer = random.randint(n,m)

# モード選択
mode = 0
while mode not in [1,2]:
    mode = get_integer("Please select game mode 1 or 2 (1: Limited attempts / 2: Unlimited attempts)\nYour select is: ")

print(f"\nYou can input between {n} and {m}")

# メッセージ
msg_congrats = "Congratulations!!\nPress Enter to finish the game."
msg_game_over = "Game Over... The correct answer was {answer}.\nPress Enter to finish the game."
msg_try_again = "Try again! (Press Enter)"
msg_input_number = "\nYour input number is: "
msg_out_of_range = "Your input is out of range ({n} - {m})!"
msg_high = "Too high!"
msg_low = "Too low!"

# モード1
if mode == 1:
    attempts = 0
    max_attempts = m - n + 1

    while attempts < 1 or attempts > max_attempts:
        attempts = get_integer(f"How many times do you want to try???(Max: {max_attempts})\nAttemps: ")
        if attempts > max_attempts: 
            print(f"You can try up to {max_attempts} attempts.\nPlease input within that range.\n")
        elif attempts < 1:
            print("Please enter at least 1 attempt.\n")

    for i in range(attempts):
        guess = int(input(msg_input_number))

        if guess == answer:
            print(msg_congrats.format(answer=answer))
            break
        elif guess < n or guess > m:
            print(msg_out_of_range.format(n=n, m=m))
        elif guess > answer:
            print(msg_high)
            print(msg_try_again)
        else:
            print(msg_low)
            print(msg_try_again)

# モード2
else:
    while True:
        guess = int(input(msg_input_number))

        if guess == answer:
            print(msg_congrats.format(answer=answer))
            break
        elif guess < n or guess > m:
            print(msg_out_of_range.format(n=n, m=m))
        elif guess > answer:
            print(msg_high)
            print(msg_try_again)
        else:
            print(msg_low)
            print(msg_try_again)
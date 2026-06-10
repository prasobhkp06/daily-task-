import random

def guessing_game():
    number = random.randint(1, 100)
    attempts = 0

    print("🎯 I've picked a number between 1 and 100. Can you guess it?")

    while True:
        try:
            guess = int(input("Your guess: "))
            attempts += 1

            if guess < number:
                print("📉 Too low! Try higher.")
            elif guess > number:
                print("📈 Too high! Try lower.")
            else:
                print(f"🎉 Correct! You got it in {attempts} attempt{'s' if attempts != 1 else ''}!")
                break
        except ValueError:
            print("Please enter a valid number.")

guessing_game()
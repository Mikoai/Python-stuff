#!/usr/bin/python

import random
import os
import string

clear = lambda: os.system('clear')

#start with menu
print("Welcome to hangman game!")
print("What's yout name?")
username = input()
clear()
print("Hello "+username+"!")
print("Are you ready for a game (Y or N)?:")

while True:
    decision = input().upper()

    if decision == 'Y' or decision == 'N':
        break
    else:
        print("I don't get it, once again please...")

if decision == 'N':
    clear()
    print("Okay then, let's play another time!")
elif decision == 'Y':
    clear()
    print("Let's have some fun then!")

#opponent enters keyphrase
print("Okay, now let someone else enter a phrase and you will guess it!")
keyphrase = list(input("Keyphrase: ").lower())
clear()

#start of the game
health = 12
misses = []
guesses = []

for x in range(len(keyphrase)):
    guesses.append("_")

print("Let's start the game!\n")

#game loop
while True:

    print(" ")
    for i in guesses:
        print(i, end=" ")

    print("\n\nMisses:", end=" ")
    for y in misses:
        print(y, end=", ")

    print("\nNumber of tries left: "+str(health))

    print("\n\nTry to guess any character:")
    guess = input("Your guess: ").lower()
    clear()

    #finding if there is guess in keyphrase
    if guess not in keyphrase:
        if guess in misses:
            print("You have tried '"+guess+"' already, try different one!\n")
        else:
            print("Miss!\n")
            health -= 1
            misses.append(guess)
    else:
        for x in range(len(keyphrase)):
            if keyphrase[x] == guess:
                guesses[x] = guess

    if health == 0:
        clear()
        print("Oops... You are out of tries!")
        print("Wish you luck next time!")
        break

    elif guesses == keyphrase:
        print("You won!")
        print("Thanks for game!")
        break

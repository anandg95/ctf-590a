#!/usr/bin/python2 -u
import os

with open(__file__) as f:
    print(f.read())

with open("flag.txt") as f:
    flag = f.read()

try:
    guess = input("Guess the flag : ")
    if guess == flag:
        print("Correct")
    else:
        print(str(guess) + " was incorrect")
except:
    pass

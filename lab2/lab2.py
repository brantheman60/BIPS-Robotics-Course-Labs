from lab2_questions import question_list
import random

round = 1      # current round
completed = [] # list of the indices of completed questions

# First check that question_list is correct
for question in question_list:
    assert(len(question) == 6)
    assert(question[5] in "ABCD")

# Introduction
print("Welcome to our quiz! To pass, you must correctly answer 15 multiple-choice questions in a row. Let's begin!")

# Repeat for 15 rounds
while(round <= 15):
    # Get a question that hasn't been picked yet
    q = random.randrange(0, len(question_list))
    while(q in completed):
        q = q + 1
        if (q == len(question_list)):
            q = 0

    # Add the question number to the completed list
    completed.append(q)

    # Get the question, choices, and answer from question_list
    question = question_list[q][0]
    choice1  = question_list[q][1]
    choice2  = question_list[q][2]
    choice3  = question_list[q][3]
    choice4  = question_list[q][4]
    answer   = question_list[q][5]

    # Print the round, question, and choices
    print("Round " + str(round))
    print(question)
    print("A. " + choice1)
    print("B. " + choice2)
    print("C. " + choice3)
    print("D. " + choice4)

    # Get player's answer (must be A, B, C, or D)
    a = input("Select A, B, C, or D: ")
    while(a != "A" and a != "B" and a != "C" and a != "D"):
        a = input("Sorry, please enter A, B, C, or D: ")

    # Check if the player's answer was correct
    if(a == answer):
        print("Correct! The correct answer was "+answer)
    else:
        print("Incorrect! The correct answer was "+answer)
        print("You lost at Round " + str(round))
        exit()

    # Prepare for the next round
    round = round + 1
    print()

# If you made it out the while loop, must have completed 15 rounds
print("Congratulations!!! You passed all 15 rounds!!!")

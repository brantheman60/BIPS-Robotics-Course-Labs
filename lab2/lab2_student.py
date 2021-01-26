from lab2_questions import question_list
import random

round = 1      # current round number
completed = [] # list of the indices of completed questions

# TODO: Check that every question has exactly 6 elements,
# and the last element is either "A", "B", "C", or "D"
for question in question_list:
    assert(???)
    assert(???)


# TODO: Write an introduction to the quiz
print(???)


# TODO: Loop for 15 rounds
while(???):
    # TODO: Pick a random index from 0 to (number of questions - 1)
    q = ???

    # TODO: keep finding an index that hasn't been put in completed yet
    while(q in completed):
        q = ???

    # Add the index to the completed list
    completed.append(q)

    # TODO: Get the question, choices, and answer from question_list[q]
    question = ???
    choice1  = ???
    choice2  = ???
    choice3  = ???
    choice4  = ???
    answer   = ???

    # TODO: Print the round, question, and choices
    print(???)      # Round X
    print(???)      # Question
    print(???)      # A. X
    print(???)      # B. X
    print(???)      # C. X
    print(???)      # D. X

    # TODO: Get player's inputted answer
    a = ???

    # TODO: If a isn't A, B, C, or D, tell them to try again
    # and get their next inputted answer
    while(??? and ??? and ??? and ???):
        a = ???

    # TODO: Check if the player's answer was correct
    if ???:
        print("Correct! The correct answer was "+answer)
    else:
        print("Incorrect! The correct answer was "+answer)
        print("You lost at Round " + str(round))
        exit()

    # TODO: Increase the round number
    round = ???
    print()

# TODO: Congratulate the player for winning
print(???)

# CHALLENGE TODO: Rewrite the code (in a new Python file called
# lab2_challenge.py) so that instead of only needing to select 1 of
# 4 options, players need to type out the full answer. Be generous and
# let the player win if they use extra spaces or capitalize/don't
# capitalize their answers. Use a new list of questions (instead of
# the list in lab2_questions.py).

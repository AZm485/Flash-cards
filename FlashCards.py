import random
import sqlite3
import os

def get_length(connection, subject):
    cursor = connection.cursor()
    statement = f"SELECT COUNT(*) FROM [{subject}]"
    cursor.execute(statement)
    count = cursor.fetchone()[0]
    return count

def get_question(connection, subject,ID):
    cursor = connection.cursor()
    statement = f'''SELECT Question FROM [{subject}]
    WHERE Num = ?'''
    cursor.execute(statement, (ID,))
    output = cursor.fetchall()
    for row in output:
        return row[0]
    
def get_answer(connection, subject,ID):
    cursor = connection.cursor()
    statement = f'''SELECT Answer FROM [{subject}]
    WHERE Num = ?'''
    cursor.execute(statement, (ID,))
    output = cursor.fetchall()
    for row in output:
        return row[0]

def get_rand_answer(connection, subject,ID):
    cursor = connection.cursor()
    statement = f'''SELECT Answer FROM [{subject}]
    WHERE Num = ?'''
    cursor.execute(statement, (ID,))
    output = cursor.fetchall()
    for row in output:
        return row[0]

def print_card():
    pass

def get_randNum(length):
    num = random.randint(1,length)
    return num

def get_randAnswerNum(ID, row_count):
    # This makes it where the answer to the question does not become a incorrect multiple choice option
    while True:
        random_num = random.randint(1,row_count)
        if random_num != ID:
            break
    return random_num

def check_answer(user_answer, answer, score):
    if user_answer == answer:
        print("You are correct, Good Job")
        score = add_score(score)
    else:
        print("That was incorrect. The correct answer was " + answer)
    return score

def add_score(score):
    score += 1
    return score

def get_score(score):
    print("Your current score is:", score)
    print("You're doing a great job!")

def get_subject():
    options = ["Searching Alg", "Graph Alg", "Runtime", "Sorting Alg", "Terms"]
    print("these are your subject options.")
    print(options,"\n")
    num = (int(input("what subject would you like? enter 1-5 "))) - 1
    print()
    subject = options[num]
    return subject

def multiple_choice(connection,subject,ID,length):
    question = [get_answer(connection,subject,ID)]
    i = 0
    j = 0
    choice_num = 1
    while i < 3:
        temp = get_rand_answer(connection,subject, get_randAnswerNum(ID, length))
        question.append(temp)
        i+=1
    random.shuffle(question)
    
    while j < 4:
        print(f"{choice_num}: {question[j]}")
        print()
        j+=1
        choice_num+=1
    return question
        

def main(score):
    #Starts connection to db
    database_path = r'C:\python projects\projects\Flash cards\Flash card database.db'
    connection = sqlite3.connect(database_path)
    
    # Gets name of table / subject that user wants to study
    subject = get_subject()
    # Gets number of rows in table 
    length = get_length(connection, subject)
    # Gets random question num ID in table
    ID = get_randNum(length)

    print(get_question(connection, subject, ID),"\n")
    answer = get_answer(connection,subject,ID)

    choices = multiple_choice(connection,subject,ID,length)
    user_answer = choices[int(input("What option is it? Enter 1-4: ")) - 1]

    score = check_answer(user_answer,answer,score)
    get_score(score)

    play_again = int(input("Would you like to play again? (1: yes\n2: no)"))
    if play_again == 1:
        main(score)
    else:
        print("Good Job studying! Come again!")
        connection.close()

score = 0
main(score)


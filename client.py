import threading
import socket
import random

#Connect to the server and choose a name
name = input("Choose a name: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("127.0.0.1", 56789))

score = 0

#Yay math is so fun...
def question():
    global score
    question = input("Would you like a math question? ")
    if (question == "y" or question =="yes"):
        type_of_question = input("What type of question (multiplication - m, addition - a, subtraction - s)? ")
        num1 = random.randint(51, 100)
        num2 = random.randint(1,50)

        if (type_of_question == "m"):
            answer = int(input(f"What is {num1} times {num2}? "))
            if (answer == num1 * num2):
                print("Correct!")
                score += 1
            else:
                print("Sorry that's wrong.")

        elif (type_of_question == "a"):
            answer = int(input(f"What is {num1} plus {num2}? "))
            if (answer == num1 + num2):
                print("Correct!")
                score += 1
            else:
                print("Sorry that's wrong.")

        elif (type_of_question == "s"):
            answer = int(input(f"What is {num1} minus {num2}? "))
            if (answer == num1 - num2):
                print("Correct!")
                score += 1
            else:
                print("Sorry that's wrong.")

        else:
            print("Please enter a valid option.")
    else:
        print("Goodbye!")

#Receive messages from other clients and the server
def client_receive():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "name?":
                client.send(name.encode("utf-8"))
            else:
                print(message)

        except:
            print("Error")
            client.close()
            break

#Send messages to other clients/the server
def client_send():
    while True:
        mensaje = input("")
        message = f'{name}: {mensaje} \n{score}'
        client.send(message.encode("utf-8"))
        if (mensaje == "question" or mensaje == "q"):
            question()

receive_thread = threading.Thread(target = client_receive)
receive_thread.start()

send_thread = threading.Thread(target = client_send)
send_thread.start()
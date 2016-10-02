import socket
import time
import configparser
import json
from Settings import HOST, PORT, RATE, JOKE_DELAY

config = configparser.ConfigParser()
config.read('config.ini')
PASS = config.get('TWITCH', 'PASS')
IDENT = config.get('TWITCH', 'IDENT')
CHANNEL = config.get('TWITCH', 'CHANNEL')

def open_socket():
    s = socket.socket()
    s.connect((HOST, PORT))
    s.send("PASS " + PASS + "\r\n")
    s.send("NICK " + IDENT + "\r\n")
    s.send("JOIN #" + CHANNEL + "\r\n")
    return s

def send_message(s, message, joke = False):
    #magic nums
    if(message.count("\n") > 3 and message.count("\n") < 7):
        message = message.replace("\n", " ")
    lines_in_message = message.split("\n")
    for i, line in enumerate(lines_in_message):
        if line:
            chat_msg = "PRIVMSG #" + CHANNEL + " :" + line
            s.send(chat_msg.encode('utf-8').strip() + "\r\n")
            print("Sent: " + chat_msg)
            if(joke and i != (len(lines_in_message)-1)):
                time.sleep(JOKE_DELAY)
            else:
                time.sleep(RATE)

def send_menu(s, user, message):
    lines_in_message = message.split("\n")
    for line in lines_in_message:
        if line:
            private_msg = "PRIVMSG #" + CHANNEL + " :.w " + user + " " + line
            s.send(private_msg.encode('utf-8').strip() + "\r\n")
            time.sleep(RATE/2)
            print("Sent: " + private_msg)

def send_dictionary(s, dictionary):
    string_rep = [str(key) + " " + str(dictionary[key]) for key in dictionary.iterkeys()]
    for string in string_rep:
        chat_msg = "PRIVMSG #" + CHANNEL + " :" + string
        s.send(chat_msg + "\r\n")
        time.sleep(RATE)


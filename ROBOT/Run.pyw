import string
import time
import threading
import configparser
import random

#retrieves jokes through database or reddit webscraping
from getRandomJoke import get_random_joke
from getTopJokes import get_top_jokes
from get_world_news import get_world_news
from get_random_riddle import get_random_riddle

#used in conjuction with the typeracer option in the bot
from getTranscription import get_transcription, latin_to_mathematical

#imports method that returns a json file
from TwitchEmotes import generate_emotes

#imports from twitch_bot necessary components
from Settings import RATE
from Read import get_user, get_message
from Socket import open_socket, send_message, send_dictionary, send_menu
from Initialize import join_room

#retrieve config variables
config = configparser.ConfigParser()
config.read('config.ini')
IDENT = config.get('TWITCH', 'IDENT')

MENU_DELAY_TIMER_IN_SECONDS = 120
PRINT_FREQ_DELAY_IN_SECONDS = 60
PRINT_JOKE_DELAY_IN_SECONDS = 120
NUMBER_OF_HOURLY_JOKES = 6

#phrases that command the bot
TYPE_RACE_ACTIVATION_PHRASE = "!typerace"
JOKE_ACTIVATION_PHRASE = "!jokes"
EMOTE_ACTIVATION_PHRASE = "!emotepulse"
RIDDLE_ACTIVATION_PHRASE = "!riddle"
NEWS_ACTIVATION_PHRASE = "!news"
LEADERBOARD_PHRASE = "!leaderboard"
MENU_COMMAND = "!menu"

#bools in charge of threads
JOKES_ON = False
PULSE_ON = False
RIDDLE_ON = False

#initializes the twitch bot and enables communication to chat
s = open_socket()
join_room(s)
readbuffer = ""

#instantiates a list of emotes, then creates a dict using emotes and a parallel zero list
emotes = generate_emotes()
frequencies = [0]*len(emotes)
emote_frequencies = dict(zip(emotes, frequencies))

jokes = get_top_jokes(posts = NUMBER_OF_HOURLY_JOKES)    
leaderboard = {}

#prints the emote with the max frequency
def print_max_freq():
    global PULSE_ON
    if PULSE_ON:
        global emote_frequencies
        key_index = max(emote_frequencies.iterkeys(), key=lambda k: emote_frequencies[k])
        if(emote_frequencies[key_index] != 0):
            send_message(s, "The most popular emote: " + key_index + " with "
                         + str(emote_frequencies[key_index]) + " occurencess in "
                         + str(PRINT_FREQ_DELAY_IN_SECONDS/60) + " minutes")
        else:
            send_message(s, "No emote was entered in the past "
                         + str(PRINT_FREQ_DELAY_IN_SECONDS/60) + " minutes")
            
        emote_frequencies = {key:0 for key in emote_frequencies}
        #thread that calls the print_max_freq once the timer ends
        threading.Timer(PRINT_FREQ_DELAY_IN_SECONDS,
                        print_max_freq).start()
    
#periodically prints the top joke from jokes subreddit every joke delay seconds
def print_top_joke(jokes):
    global JOKES_ON
    if JOKES_ON:
        #check if the joke list is empty, then update
        if not jokes:
            jokes = get_top_jokes(posts = NUMBER_OF_HOURLY_JOKES)
        send_message(s, jokes.pop(), True)

        #thread that calls the print_top_joke once the timer ends
        threading.Timer(PRINT_JOKE_DELAY_IN_SECONDS,
                        print_top_joke, [jokes]).start()
      

def print_menu():
    send_message(s, "Type !menu for bot info")
    threading.Timer(MENU_DELAY_TIMER_IN_SECONDS, print_menu).start()

print_menu()

#starts the type race
def initiateTypeRace():
    global leaderboard
    phrase_index = int(random.random()*10)
    transcription = get_transcription(phrase_index)
    phrase = transcription[0]
    send_message(s, "3\n2\n1")
    send_message(s, "Type the phrase\n" + transcription[1].lower())
    race_ongoing = True
    start = time.clock()
    #race goes on until someone types in the correct phrase
    while race_ongoing:
        temp = record_user_input()
        for line in temp:
            user = get_user(line)
            message = get_message(line)
            if user != IDENT:
                print user + " typed: " + message
                #removes any trailing whitespaces, then compares
                #user message to chat to the typerace phrase
                if message.strip().lower() == phrase.strip().lower():
                    time_elapsed = time.clock() - start
                    send_message(s, user + " has won! with a time of "
                                 + str(time_elapsed))
                    #adjust leaderboards according to PHRASES
                    capped_phrase = phrase[:30] + "..."
                    leaderboard[capped_phrase] = (user, time_elapsed)
                    race_ongoing = False
        
def record_user_input():
    global readbuffer
    readbuffer = readbuffer + s.recv(1024)
    #reads and separates input by newline, then removes the the last item in the stack
    temp = string.split(readbuffer, "\n")
    readbuffer = temp.pop()
    return temp

   
#keep waiting and reading user input
while True:

    temp = record_user_input()
        
    #if the line in temp contains a command,
    #send a chat message accordingly
    for line in temp:
        
        user = get_user(line)
        message = get_message(line)

        #checks if the user isn't the bot
        if user != IDENT:
            print user + " typed: " + message

            #if bot is inactive, make sure to respond to when twitch pings the bot
            #so that it does not get kicked out for being afk
            if message == "PING :tmi.twitch.tv\r\n":
                s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))

            if message.strip() == RIDDLE_ACTIVATION_PHRASE:
                RIDDLE_ON = not RIDDLE_ON
                if RIDDLE_ON:
                    RIDDLE = get_random_riddle()
                    send_message(s, RIDDLE[0])
                    
            if RIDDLE_ON:
                #if message equals the riddle's answer
                print RIDDLE
                if RIDDLE[1].strip().lower() in message.strip().lower():
                    send_message(s, user + " got the correct answer!")
                    RIDDLE_ON = False

            if message.strip() == NEWS_ACTIVATION_PHRASE:
                send_message(s, get_world_news()[0])
                
            if message.strip() == MENU_COMMAND:
                menu = "List of commands " \
                       + "\n" + TYPE_RACE_ACTIVATION_PHRASE \
                       + "\n" + JOKE_ACTIVATION_PHRASE \
                       + "\n" + "joke (only if !jokes)" \
                       + "\n" + EMOTE_ACTIVATION_PHRASE \
                       + "\n" + LEADERBOARD_PHRASE \
                       + "\n" + RIDDLE_ACTIVATION_PHRASE \
                       + "\n" + NEWS_ACTIVATION_PHRASE
                send_menu(s, user, menu)
                
            if message.strip() == LEADERBOARD_PHRASE:
                send_dictionary(s, leaderboard)
                
            if message.strip() == TYPE_RACE_ACTIVATION_PHRASE:
                send_message(s, "TYPE RACE ACTIVATED, EVERYTHING"
                             + " ELSE IS DEACTIVATED UNTIL THE "
                             + " RACE IS OVER OR CANCELLED")
                JOKES_ON = False
                EMOTE_PULSE = False                
                initiateTypeRace()

            #turns on jokes functionality
            if message.strip() == JOKE_ACTIVATION_PHRASE:
                JOKES_ON = not JOKES_ON
                send_message(s, "Type !jokes to turn off jokes"
                             if JOKES_ON else "Type !jokes to turn on jokes")
                if JOKES_ON:
                    print_top_joke(jokes)

            #enables requesting of a random joke by the "joke" command
            if JOKES_ON and message.strip() == "joke":
                send_message(s, get_random_joke(), joke=True)
                                    
            #turns on emotepulse functionality
            if message.strip() == EMOTE_ACTIVATION_PHRASE:
                PULSE_ON = not PULSE_ON
                send_message(s, "Type !emotepulse to turn off emoji pulse"
                             if PULSE_ON else "Type !emotepulse to turn on emoji pulse")
                if PULSE_ON:
                    print_max_freq()
                
            #increment according values of keys in dictionary that
            #have been mentioned
            if PULSE_ON:
                for emote in emotes:
                    if emote in message:
                        #increment frequency of emote that is shown
                        emote_frequencies[emote] += 1
                        print emote, emote_frequencies[emote]
    

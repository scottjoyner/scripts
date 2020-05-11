# importing speech recognition package from google api
import speech_recognition as sr
import playsound # to play saved mp3 file
from gtts import gTTS # google text to speech
import os # to save/open files
import wolframalpha # to calculate strings into formula
from selenium import webdriver # to control browser operations
import logging



# Create a custom logger

logger = logging.getLogger(__name__)
stenographer = logging.FileHandler('script.log')
stenographer.setLevel(logging.ERROR)
stenographer_format = logging.Formatter('%(asctime)s :  %(message)s')
stenographer.setFormatter(stenographer_format)
logger.addHandler(stenographer)



logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y%H:%M:%S')

def process_text(input):
    try:
        if 'light' in input or 'lights' in input:
            # Creating client
            client = mqtt.Client(client_id='macbook')

            # Connecting callback functions
            client.on_connect = connect_msg
            client.on_publish = publish_msg

            # Connect to broker
            client.connect("192.168.1.73",1883)

            if 'on' in input:
                # print("Lights are on")
                # Publish a message with topic
                ret= client.publish("house/closet-light","on")
                speak = '''The lights are on'''
            if 'off' in input:
                # print("Lights are off")
                # Publish a message with topic
                ret= client.publish("house/closet-light","off")
                speak = '''The lights are off'''
                
            # Run a loop
            client.loop()
            assistant_speaks(speak)
        
        elif 'search' in input or 'play' in input:
            # a basic web crawler using selenium
            search_web(input)
            return

        elif "who are you" in input or "define yourself" in input:
            speak = '''Hello, I am Person. Your personal Assistant.
            I am here to make your life easier. You can command me to perform
            various tasks such as calculating sums or opening applications etcetra'''
            assistant_speaks(speak)
            return

        elif "who made you" in input or "created you" in input:
            speak = "I have been created by Sheetansh Kumar."
            assistant_speaks(speak)
            return

        elif "geeksforgeeks" in input:# just
            speak = """Geeks for Geeks is the Best Online Coding Platform for learning."""
            assistant_speaks(speak)
            return

        elif "calculate" in input.lower():

            # write your wolframalpha app_id here
            app_id = "WOLFRAMALPHA_APP_ID"
            client = wolframalpha.Client(app_id)

            indx = input.lower().split().index('calculate')
            query = input.split()[indx + 1:]
            res = client.query(' '.join(query))
            answer = next(res.results).text
            assistant_speaks("The answer is " + answer)
            return

        elif 'open' in input:

            # another function to open
            # different application availaible
            open_application(input.lower())
            return

        else:

            assistant_speaks("I can search the web for you, Do you want to continue?")
            ans = get_audio()
            if 'yes' in str(ans) or 'yeah' in str(ans):
                search_web(input)
            else:
                return
    except :

        assistant_speaks("I don't understand, I can search the web for you, Do you want to continue?")
        ans = get_audio()
        if 'yes' in str(ans) or 'yeah' in str(ans):
            search_web(input)




num = 1
def assistant_speaks(output):
    global num

    # num to rename every audio file
    # with different name to remove ambiguity
    num += 1
    print("PerSon : ", output)

    toSpeak = gTTS(text = output, lang ='en', slow = False)
    # saving the audio file given by google text to speech
    file = str(num)+".mp3"
    toSpeak.save(file)

    # playsound package is used to play the same file.
    playsound.playsound(file, True)
    os.remove(file)



def get_audio():

    rObject = sr.Recognizer()
    audio = ''

    with sr.Microphone() as source:
        print("Listening")

        # recording the audio using speech recognition
        audio = rObject.listen(source, phrase_time_limit = 5)
        
    print("Stop.") # limit 5 secs

    try:

        text = rObject.recognize_google(audio, language ='en-US')
        if text != 0:
            logger.error('%s', text)
            print("You : ", text)
            return text

    except:
        
        return 0


# Driver Code
if __name__ == "__main__":
    #assistant_speaks("What's your name, Human?")
    #name ='Human'
    #name = get_audio()
    #assistant_speaks("Hello, " + name + '.')

    while(1):
        logger.error("Dictation Started")
        #assistant_speaks("What can i do for you?")
        text = get_audio().lower()

        if text != 0:
            if "exit" in str(text) or "bye" in str(text) or "sleep" in str(text):
                logger.error("Dictation Ended")
                break

        # calling process text to process the query
        #process_text(text)
        
        

import speech_recognition as sr
import os # to save/open files
import logging


# set up logging to file - see previous section for more details
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='/temp/myapp.log',
                    filemode='w')

logger1 = logging.getLogger('myapp.area1')
logger2 = logging.getLogger('myapp.area2')

def process_text(input):
    try:

    except :


def log_speech(input):
    try:
        logger1.info(input)

def get_audio():

	rObject = sr.Recognizer()
	audio = ''

	with sr.Microphone() as source:
		print("on")

		# recording the audio using speech recognition
		audio = rObject.listen(source, phrase_time_limit = 5)
	print("off") # limit 5 secs

	try:

		text = rObject.recognize_google(audio, language ='en-US')
		return text 

	except:
        # Failed to translate text
		return 0



# Driver Code
if __name__ == "__main__":

	while(1):
		text = get_audio()

		if text == 0:
			continue

		if "exit" in str(text) or "bye" in str(text) or "sleep" in str(text):
			print("Not Listening anymore")
			break

		# calling process text to process the query
        log_speech(text)
		process_text(text)

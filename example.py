import speech_recognition as sr
import threading, queue
import logging


# Pipeline for communication between the threads
class Pipeline:
    """
    Class to allow a single element pipeline between producer and consumer.
    """
    def __init__(self):
        self.message = 0
        self.producer_lock = threading.Lock()
        self.consumer_lock = threading.Lock()
        self.consumer_lock.acquire()

    def get_message(self, name):
        logging.debug("%s:about to acquire getlock", name)
        self.consumer_lock.acquire()
        logging.debug("%s:have getlock", name)
        message = self.message
        logging.debug("%s:about to release setlock", name)
        self.producer_lock.release()
        logging.debug("%s:setlock released", name)
        return message

    def set_message(self, message, name):
        logging.debug("%s:about to acquire setlock", name)
        self.producer_lock.acquire()
        logging.debug("%s:have setlock", name)
        self.message = message
        logging.debug("%s:about to release getlock", name)
        self.consumer_lock.release()
        logging.debug("%s:getlock released", name)
        
def worker():
    while True:
        audio = q.get()
        try:
            text = rObject.recognize_google(audio, language ='en-US')
            logger.error('%s', text)
            print(text)
        except sr.UnknownValueError:
            logger.info("Unkown Value Error")
        except sr.RequestError as e:
            logger.info("Request Error")
        q.task_done()
        logger.info('%i items in queue', q.qsize())



# Location of the main method
if __name__ == "__main__":
    # Create a custom logger

    logger = logging.getLogger(__name__)
    stenographer = logging.FileHandler('script.log')
    stenographer.setLevel(logging.ERROR)
    stenographer_format = logging.Formatter('%(asctime)s :  %(message)s')
    stenographer.setFormatter(stenographer_format)
    logger.addHandler(stenographer)
    
    console = logging.StreamHandler()
    console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console.setFormatter(console_format)
    console.setLevel(logging.ERROR)
    logger.addHandler(console)
    

    # Initalize the Queue
    q = queue.Queue()
    
    # turn-on the worker thread
    threading.Thread(target=worker, daemon=True).start()
    
#    rObject = sr.Recognizer()
#    m = sr.Microphone()
#    with m as source:
#        rObject.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening
#        stop_listening = rObject.listen_in_background(m, callback)
#
#    q.put(audio)
    while(1):
        rObject = sr.Recognizer()
        audio = ''
        with sr.Microphone() as source:
            rObject.adjust_for_ambient_noise(source)
            logger.error("listening")
            # recording the audio using speech recognition
            audio = rObject.listen(source)
            logger.error("Audio Generated")
        q.put(audio)

# block until all tasks are done
q.join()




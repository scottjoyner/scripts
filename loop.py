import threading
import time
import logging
import speech_recognition as sr
import concurrent.futures





def producer(pipeline):
    logging.info("Producer got message: %s", message)

    rObject = sr.Recognizer()
    audio = ''

    with sr.Microphone() as source:
        print("Listening")

        # recording the audio using speech recognition
        audio = rObject.listen(source, phrase_time_limit = 5)
    
    pipeline.set_message(audio, "Producer")


def consumer(pipeline):
    """Pretend we're saving a number in the database."""
    message = 0
    while message is not audio:
        message = pipeline.get_message("Consumer")
        if message is not audio:
            
            logging.info("Consumer storing message: %s", message)




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
    
    
    
    
    
    
    


    print("Start")
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    logging.getLogger().setLevel(logging.DEBUG)

    pipeline = Pipeline()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        while(1):
            executor.submit(producer, pipeline)
            executor.submit(consumer, pipeline)

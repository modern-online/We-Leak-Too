# Leon Eckert / Vytas Jankauskas
# 2k20 
# Sniffo da Sniff 
# If voice-assistant is available
# Takes files sniffed from the internetz
# leaves images and .html, dumps the rest 
# gets voice-assistant to say latest html file's content
# gets some lights to flash
# cleans up

import os 
from os import path
import subprocess
import re 
import serial
import random
from time import sleep
import requests
from threading import Thread
import html2text
from mycroft_bus_client import MessageBusClient, Message
from mycroft.audio import wait_while_speaking
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# where the sniffed files and tts voice files are
folder_paths = ["/tmp/mycroft/cache/tts/Mimic", "/home/caclab/Desktop/sniff/packets"]
# folder_path = "/home/caclab/Desktop/sniff/packets"

# Insert server to connect to
api="XXXXXXXX"

# connect to arduino serial 
arduino = serial.Serial('/dev/ttyACM0', 115200, timeout=.1) # serial comms with LED ring
sleep(1)

# connect to Mycroft
client = MessageBusClient()
client.run_in_thread()

# html content parser
reader = html2text.HTML2Text()
reader.ignore_links = True
reader.ignore_images = True

# Class for uploading files to server in thread
class ThreadyThread:
    def __init__(self):
        self.running = True

    def terminate(self):
        self.running = False    

    # Upload file to server
    def send_to_server(self, filepath, api=api):
                
        with open(filepath, "rb") as upload:
            try:
                print(f"Uploading {filepath} to server")
                response = requests.post(api, files={"file": upload})
                print(response)
            except Exception:
                pass
            
            # Remove file
            try:
                os.remove(filepath)
            except OSError as e:
                 pass     

        self.terminate()

    # Mycroft will speak and set appropriate LEDs on Arduino
    def say_something(self, text):

        # turn lights on arduino
        confess()

        # speak on mycroft
        client.emit(Message('speak', data = {'utterance': text}))

        # wait while Mycroft is saying something
        wait_while_speaking() 

        # cleanup 
        clean_tts_cache()

        # change lights on arduino
        thinking()

        self.terminate()   


# Class for dealing with newly sniffed files
class SniffHandler(FileSystemEventHandler):
    
    # If new file is sniffed
    def on_created(self, event):
        print("sniffed ", event.src_path)
        
        try:
            if path.exists(event.src_path):
            
                # If text based file
                if event.src_path.endswith('.html') or event.src_path.endswith('.txt'):
                    handle_text(event.src_path)

                # If image or sound
                elif event.src_path.endswith('.jpeg') or event.src_path.endswith('.png') or event.src_path.endswith('.jpg') or event.src_path.endswith('.mp3'):
                
                    # send to server
                    t = Thread(target=thready.send_to_server, args=(event.src_path, ))
                    t.start()

                # If wav audio we need to compress to mp3 before uploading to server
                elif event.src_path.endswith('.wav'):

                    print("converting to mp3")

                    output_file= " /home/caclab/Desktop/sniff/packets/" + path.splitext(path.basename(event.src_path))[0] + '.mp3'
                    mp3 = event.src_path + output_file
                    cmd = 'lame --preset insane %s' % mp3                    
                    
                    # we need to wait a bit for the .wav file to be properly generated, otherwise conversion results empty
                    sleep(2)

                    # Call LAME codec to convert wav into mp3 
                    subprocess.call(cmd, shell=True)

                else:
                    try:
                        os.remove(event.src_path)
                    except OSError as e:
                        pass                        
        
        except OSError as e:
            pass

# Text message processing
def handle_text(text_file):
    
    # parse html
    source = open(text_file).read()
    text = reader.handle(source)

    # save parsed html copy for server upload
    text_filepath = "/home/caclab/Desktop/sniff/tmp/tmp.txt"
    with open(text_filepath, "w") as temp:
        temp.write(text)

    # upload parsed html to server
    t = Thread(target=thready.send_to_server, args=(text_filepath, ))
    t.start()

    # clean bad symbols
    trashy_vocab = ['*', '/', '_', '#', '[', ']', '{', '}']
    for symbol in trashy_vocab:
        if symbol in text:
            text = text.replace(symbol, '')


    # filter out floats (This will need to be modified in the futch)
    text = re.sub(r'\d+(?:\.\d*)', '', text)
                
    # remove empty lines
    text = text.strip()
    
    # Pick some random lines instead of the whole text
    #text = pick_random_lines(text)
    text = ''.join([i for i in text if not i.isdigit()])

    print(text)
    if text:
        # Speak text on Mycroft
        u = Thread(target=thready.say_something, args=(text, ))
        u.start()

# Random line picker
def pick_random_lines(text):
    
    # picks 10 consequential lines / Adjust according to your liking
    number_of_lines = 2

    chosen_lines=''
    lines = text.splitlines()
    lines = list(filter(None, lines))

    if len(lines) > 1:
        random_line_index  = random.randint(1, len(lines))
        for i in range(number_of_lines): 
            if random_line_index + i < len(lines):
                chosen_lines +=  str(lines[random_line_index+i])
            else: 
                break
    else: 
        chosen_lines = text

    text = chosen_lines
    return text


# ARDUINO: LED ring interaction lights
# Get data from arduino
def get_arduino():
    while True:
        data = arduino.readline().strip().decode("utf-8") 
        sleep(.1)
        if data == "1":
            break

def confess():
    print("CONFESSING")
    get_arduino()
    arduino.write('2'.encode()) # put LED in 'CONFESS' state
    arduino.flushOutput()
    sleep(.1)

# Set lights for remaining interactions
def wakeword(message):
    print("LISTENING")
    get_arduino()
    arduino.write('3'.encode()) # put LED in 'LISTENING" state
    arduino.flushOutput()
    sleep(.1)

def replying(message):
    print("REPLYING")
    get_arduino()
    arduino.write('4'.encode()) # put LED in 'REPLYING" state
    arduino.flushOutput()
    sleep(.1)
    wait_while_speaking() 
    thinking()

def pausing(message):
    thinking()

def thinking():
    print("THINKING")
    get_arduino()
    arduino.write('1'.encode()) # put LED in 'THINKING state
    arduino.flushOutput()
    sleep(.1)


def clean_tts_cache():
    # Clean oldest wavs and phos from cache
    sleep(2)
    list_of_files = os.listdir('/tmp/mycroft/cache/tts/Mimic')
    full_path = ["/tmp/mycroft/cache/tts/Mimic/{0}".format(x) for x in list_of_files]
    full_path.sort(key=path.getctime)

    if len(full_path) > 1:    
        for x, y in zip(full_path, full_path[1:]):
            time_difference = path.getctime(y) - path.getctime(x) 
            if time_difference > 1:
                full_path.remove(y)

    for pathy in full_path:
        try:
            os.remove(pathy)
        except OSError as e:
            pass 


# Threaded functions
thready = ThreadyThread()

# Mycroft is ready to go (This also starts the tts engine so that appropriate cache folders are created)
hello_phrase = "Hello folks, I am ready to sniff"
u = Thread(target=thready.say_something, args=(hello_phrase, ))
u.start()

# wait for Mycroft's tts engine to initialize properly
sleep(5)

# Check for new packets
observer = Observer()

# Directory monitoring
for folder_path in folder_paths:
    event_handler = SniffHandler()
    observer.schedule(event_handler, path=folder_path, recursive=False)
observer.start()

# Mycroft event listeners
client.on('recognizer_loop:wakeword', wakeword) # if wakeword detected
client.on('recognizer_loop:record_end', pausing) # if recording of user's message has ended
client.on('recognizer_loop:utterance', replying) # if user has finished speaking

while True:
    try:
        # better keep clean here
        pass
    except KeyboardInterrupt:
        observer.stop()
        observer.join()
    
    observer.join()

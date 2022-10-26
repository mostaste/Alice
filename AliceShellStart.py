import time
import requests
import json
import datetime
import os
import sys
import random
import pygame
import threading
import vlc 
import pafy
import wikipedia
import webbrowser


from pprint import pprint
from os import listdir
from os.path import isfile, join

import speech_recognition as sr
import pyttsx3

#import pocketsphinx
from youtubesearchpython import SearchVideos



##################################################################################################################################################################################################################



###############################  Initializer ###############################
    
Lisa = "Lisa: "

# Initialize the Speech Engine
voiceRate = 210
voiceID = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
engine = pyttsx3.init()
engine.setProperty('voice', voiceID)
engine.setProperty('rate', voiceRate)

stop_event = threading.Event()

############################################################################

# Function to convert text to speech 
def SpeakText(command): 
    engine.say(command) 
    engine.runAndWait()


def TopHeader():
    print("\n-------------------------------\n")
    print(" Conversational Shell Started\n")
    print("-------------------------------\n")
    SpeakText("Conversational Shell Started")

def WelcomeBack():
    TopHeader()
    print('\n' + Lisa + 'Welcome back to Conversation Shell\n')

def StartMessage():
    TopHeader()
    Date()
    Time()
    Weather()

    print(Lisa, end = '')
    
    i = random.randint(1, 4);

    if(i == 1):
        print("Good Morning ~ \n")
        SpeakText('Good Morning')
    if(i == 2):
        print("Have a Nice Day ~ \n")
        SpeakText('Have a Nice Day')
    if(i == 3):
        print("Rise and Shine ~ \n")
        SpeakText('Rise and Shine')
    if(i == 4):
        print("Time for Work ~ \n")
        SpeakText('Time for Work')
    if(i == 5):
        print("Go getter ~ \n")
        SpeakText('Go getter')


#Speech Input Function
# Sphinx Speech
def UserSpeechInput2():
    while True:
        try:
            # Use the Microphone as source for input.
            print("Listening...\n")
            with sr.Microphone() as source2:
                # Wait for a second to let the recognizer adjust the energy threshold based on the surrounding noise level
                r.adjust_for_ambient_noise(source2, duration=0.2)
            
                # Listens for the User's Input 
                audio2 = r.listen(source2)
            
                # Using Google to Recognize Audio
                # Google Recognizer(Requires Active Internet Connection)
                MyText = r.recognize_sphinx(audio2)
                MyText = MyText.lower()
                return MyText
                break
                    
        except sr.RequestError as e:
            #return str("Could not Request Results; {0}".format(e))
            print("Could not request results; {0}".format(e))
            continue
                    
        except sr.UnknownValueError:
            #return str("Unknown Sound")
            print("Unknown Sound")
            continue

# Google Speech
def UserSpeechInput():
    while True:
        if stop_event.is_set():
            print("Break Event")
            break
        # Use the Microphone as source for input.
        with sr.Microphone() as source2:
            r = sr.Recognizer()
            # Wait for a second to let the recognizer adjust the energy threshold based on the surrounding noise level
            r.adjust_for_ambient_noise(source2, duration=0.2)
            print("Listening...\n")
            # Listens for the User's Input 
            audio2 = r.listen(source2, phrase_time_limit = 10)
            print("Done Listening..\n")
            try:
                # Using Google to Recognize Audio
                # Google Recognizer(Requires Active Internet Connection)
                print("Recognizing Audio.\n")
                MyText = r.recognize_google(audio2)
                MyText = MyText.lower()
                print("Input: " + MyText, end='\n\n')
                return MyText
                        
            except sr.RequestError as e:
                #return str("Could not Request Results; {0}".format(e))
                print("Could not request results; {0}".format(e), end='\n\n')
                continue
                        
            except sr.UnknownValueError:
                #return str("Unknown Sound")
                print("Unknown Sound\n\n")
                continue
	

def StartFirstTime():
    print(Lisa, end='')
    print('Hello, I am Lisa.  What is your name?')
    name = input(Me)
    file = open("name.txt", "w") 
    file.write(name) 
    file.close()  
    print(Lisa + 'Hello, ' + name)
    time.sleep(2)
    print(Lisa + 'It is nice to meet you. ')

    
def Date():
    now = datetime.datetime.now()
    dateText = 'Date is {:d}/{:d}/{:d}'.format(now.day, now.month, now.year)
    print(dateText)
    #dateSpeak = 'Today is ' + str(now.month) + str(now.day) + str(now.year) 
    #SpeakText(dateSpeak)
    
def Time():
    now = datetime.datetime.now()
    timeText = 'Time is {:d}:{:02d}'.format(now.hour, now.minute)
    print(timeText)
    #SpeakText(timeText)


def Weather():
    cityWeather = 'Bangkok'
    apiWeather = '0ccef92205ec3f8d935db746408d8245'
    res = requests.get('https://api.openweathermap.org/data/2.5/weather?q=' + cityWeather + '&APPID=' + apiWeather + '&units=metric')
    weather = str(res.json()['weather'][0]['main'])
    temperature = str(res.json()['main']['temp'])
    weatherText = 'Weather - ' + weather
    temperatureText = 'Temperature - ' + temperature + '°C\n'
    print(weatherText)
    print(temperatureText)
    #weatherText = 'Weather is ' + weather
    #temperatureText = 'Temperature is ' + temperature + '°C'
    #SpeakText(weatherText)
    #SpeakText(temperatureText)


def Reminder(temp):
    bReminder = False
    print("\n\n  Reminder Protocol Initiated !\n\n")
    while not bReminder:
        if "read" in temp:
            print("\nReading Reminders...")
            with open('Reminder.txt', 'r', errors = 'ignore') as reader:
                data = reader.read()
                if data == '':
                    print("No Reminders Found")
                    SpeakText("No Reminders Found")
                else:
                    print(data)
                    SpeakText(data)
                reader.close()
                bReminder = True
                break
        elif "write" in temp:
            with open('Reminder.txt', 'a', errors = 'ignore') as reader:
                SpeakText("Writing Reminders")
                newReminder = UserSpeechInput()
                reader.write(newReminder)
                reader.close()
                bReminder = True
                break
        elif "clear" in temp:
            print("\nClearing Reminders...")
            SpeakText("Clearing Reminders")
            open('Reminder.txt', 'w', errors = 'ignore').close()
            bReminder = True
            break

        else:
            print("No Reminder Options Found")
            SpeakText("No Reminder Options Found")
            bReminder = True
            break
        
    print()
    print("\n\n  Exiting Reminder Protocol ! ")
    SpeakText("Exiting Reminder Protocol!")
    TopHeader()
    print('\nWelcome back to Conversational Shell ~~~\n')
        
    '''
    print("Remember to wear a Mask")
    SpeakText("Remember to wear a Mask")
    print("\n-----------------------------------\n")
    print(" Reminder Protocol Options ")
    print("\n-----------------------------------\n")
    print("1. Read Reminders")
    print("2. Add Reminders")
    print("3. Clear Reminders")
    print("4. Exit Reminders\n")
    
    option = input("Reminder: ")
    

    if str(option) == '1':
        print("\nReading Reminders...")
        with open('Reminder.txt', 'r', errors = 'ignore') as reader:
            print(reader.read())
            reader.close()
        print()
    elif str(option) == '2':
        print("\nAdding Reminders...")
        with open('Reminder.txt', 'a', errors = 'ignore') as access:
            newReminder = input()
            access.write("\n")
            access.write(newReminder)
            access.close()
    elif str(option) == '3':
        print("\nClearing Reminders...")
        open('Reminder.txt', 'w', errors = 'ignore').close()
    elif str(option) == '4':
        print("\n\n  Exiting Reminder Protocol ! ")
        SpeakText("Exiting Reminder Protocol!")
        TopHeader()
        print('\nWelcome back to Conversational Shell ~~~\n')
        return False
    else:
        print("\nNo Such Option Found ! ")
        continue
    '''


def MusicPlayer():
    print("\n\n~~~~~~~~~  Music Protocol Initiated  ~~~~~~~~~\n\n")
    SpeakText("Music Protocol Initiated")

# Reading Music Files  
    filedir = os.path.dirname(r"C:\Users\mosta\Desktop\Deep Learning Projects\Projects\Lib\New Project")
    dirPath = os.path.join(filedir, "New Project")
    dirListing = os.listdir(dirPath)
    
    playlist = list()
    itemlist = list()
    for item in dirListing:
        if ".mp3" in item:
            playlist.append(dirPath+'\\'+item)
            itemlist.append(item)
    nSongs = len(playlist)
    print("Playlist:", nSongs, "Songs", end="\n\n")
    for item in itemlist:
        print(item)
    print()


# Music Settings
    nLoop = 1
    fVolume = 0.8
    bMusicRunning = True
    bOnCreate = True
    bThreadJoin = False
    bPaused = False
    bLoop = False
    
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.set_volume(fVolume)
    NEXT_SONG = pygame.USEREVENT + 1
    pygame.mixer.music.set_endevent(NEXT_SONG)

# Music Loader
    nCurrentIndex = random.randint(0, nSongs - 1)
    sCurrentSong = playlist[nCurrentIndex]
    pygame.mixer.music.load(sCurrentSong)
    pygame.mixer.music.play()
    print("\nPlaying", itemlist[nCurrentIndex], end='\n\n')

    def PlayNext():
        nCurrentIndex = random.randint(0, nSongs - 1)
        sCurrentSong = playlist[nCurrentIndex]
        pygame.mixer.music.load(sCurrentSong)
        pygame.mixer.music.play()
        print("\nPlaying", itemlist[nCurrentIndex], end='\n\n')

    def AutoNext():
        while True:
            if not bThreadJoin:
                if not bLoop:
                    for event in pygame.event.get():
                        if event.type == NEXT_SONG:
                            PlayNext()
                            break
            else:
                break
                    

    def MusicOptions():
        print("-----------------------------")
        print(" Music Protocol Options")
        print("-----------------------------")
        print("'Play/Pause' to ⏯️")
        print("'Next/Forward' to ⏭")
        print("'Loop' for 🔁")
        print("'Random' for 🔀")
        print("'Volume' for 🔊")
        print("'Exit' to Exit")
        print("-----------------------------")
        print("Music: ", end=' ')
        return UserSpeechInput()
           

    while bMusicRunning:
        if bOnCreate:
            musicPlayThread = threading.Thread(target=AutoNext)
            musicPlayThread.start()
            bOnCreate = False

        ch = MusicOptions()
        
        if ch == "p" or ch == "pause" or ch == "play":
            if not pygame.mixer.music.get_busy():
                if ch == "play":
                    pygame.mixer.music.play()
            else:
                if bPaused:
                    if (ch == "pause"):
                        print("Music is already Paused ! \n")
                    else:
                        print("\nPlaying", itemlist[nCurrentIndex], end='\n')
                        pygame.mixer.music.unpause()
                        bPaused = False
                else:
                    if (ch == "play"):
                        print("Music is already Playing ! \n")
                    else:
                        print("\nPausing", itemlist[nCurrentIndex], end='\n')
                        pygame.mixer.music.pause()
                        bPaused = True
    
        elif ch == "s" or ch == "stop":
            pygame.mixer.music.fadeout(10000)
            print("Music will be fading out in 10 seconds\n")

        elif ch == "next song" or ch == "forward" or ch == "next":
            PlayNext()
            
        elif ch == "lou" or ch == "loop":
            if not bLoop:
                nLoop = -1
                bLoop = True
                print("Music is on Loop ! \n")
            else:
                nLoop = 1
                bLoop = False
                print("Music is off Loop ! \n")
            pygame.mixer.music.play(nLoop)

        elif ch == "rewind" or ch == "restart":
            pygame.mixer.music.rewind()
        
        elif ch == "r" or ch == "random":
            nCurrentIndex = random.randint(0, nSongs - 1)
            sCurrentSong = playlist[nCurrentIndex]
            print("Playlist has been Randomized ! \n")

        elif ch == "volume":
            print("Volume is at %.1f" %(fVolume))
            print(pygame.mixer.music.get_busy())
            
        elif ch == "increase volume":
            if fVolume < 1.0:
                fVolume += 0.2
                pygame.mixer.music.set_volume(fVolume)
                print("Setting Volume at %.1f" % (fVolume))
            else:
                print("Volume is already at the maximum!")

        elif ch == "decrease volume":
            if fVolume > 0.0 and fVolume <= 1.0:
                fVolume -= 0.2
                pygame.mixer.music.set_volume(fVolume)
                print("Setting Volume at %.1f" % (fVolume))
            else:
                print("Volume is already at the minimum!")
            
        elif ch == "exid" or ch == "exit" or ch == "quit":
            bThreadJoin = True
            musicPlayThread.join()
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.quit()
            pygame.quit()
            print("\n\n~~~~~~~~~  Exiting Music Protocol  ~~~~~~~~~\n\n")
            SpeakText("Exiting Music Protocol")
            bMusicRunning = False
            time.sleep(1)
        else:
            print("No Such Option Found ! \n")

        ch = ''
        time.sleep(2)
        continue


def YoutubePlayer():
    print("\n\n~~~~~~~~~  Youtube Protocol Initiated  ~~~~~~~~~\n\n")
    SpeakText("Youtube Protocol Initiated!")
    bQuery = True
    bMusicConfirm = False
    
    while True:
        while bQuery:
            print("Searching... ", end='\n')
            SpeakText("Ask for a Song ~")
            videoQuery = UserSpeechInput()
            search = SearchVideos(videoQuery, offset = 1, mode = "json", max_results = 1)
            res = json.loads(search.result())
            res1 = res['search_result']
            res2 = res1[0]
            url = res2['link']
            #res = json.loads('https://www.youtube.com/watch?v=Ec3TCNaHU04&list=RDEc3TCNaHU04&index=1&ab_channel=ZaadOatStudio')
            #url = "https://www.youtube.com/watch?v=Ec3TCNaHU04&list=RDEc3TCNaHU04&index=1&ab_channel=ZaadOatStudio"
            #url = "https://www.youtube.com/watch?v=Zi_XLOBDo_Y&ab_channel=michaeljacksonVEVO"
            #url = "https://www.youtube.com/watch?v=djV11Xbc914&ab_channel=a-ha"
            #url = "https://www.youtube.com/watch?v=7FhbKx4Xr60&ab_channel=ZaadOatStudio"
            #url = "https://www.youtube.com/watch?v=BGPVS4xNIC0&list=PLGkKtx7nj1DaTfi9EfCECYrZOUjz14-J6&index=33&ab_channel=ZaadOatStudio"
            #SpeakText("Playing Ice Songs")
            #url = "https://www.youtube.com/watch?v=J3R5c2arFhY&ab_channel=ZaadOatStudio"
            video = pafy.new(url)
            media = vlc.MediaPlayer(video.getbest().url)
            media.play()
            print("Playing: %s" %videoQuery)
            print(url)
            time.sleep(5)
            videoQuery = ''
            bQuery = False
            break
    
        if not media.is_playing():
            bQuery = True
            bMusicConfirm = False


def Wikipedia(statement):
    SpeakText("Searching Wikipedia...")
    statement = statement.replace("Wikipedia", "")
    results = wikipedia.summary(statement, sentences=3)
    SpeakText("According to Wikipedia")
    print(results, end='\n\n')
    SpeakText(results)
            


def Google():
    SpeakText("Opening Google")
    webbrowser.open_new_tab("https://www.google.com")

def News():
    SpeakText("Opening News")
    webbrowser.open_new_tab("https://www.bbc.com/news/world")

def Mail():
    SpeakText("Opening Mail")
    webbrowser.open_new_tab("https://mail.google.com/")
            

##################################################################################################################################################################################################################

'''

if not media.is_playing():
                    media = vlc.MediaPlayer(video.getbestaudio().url)
                    media.play()
                    time.sleep(3)

stop_event.set()
stop_event.clear()
def MediaPlay():
            while not bThreadJoin:
                ch = UserSpeechInput()
                if ch == "stop" or ch == "exit":
                    bMediaLoop = False
                    media.stop()
                    print("Thread Stopping...\n")
                    break
print("Do you want to quit Youtube Protocol? ")
                if UserSpeechInput() in ("exit", "quit"):
                    break

        if not media.is_playing():
            if bMediaLoop:
                media = vlc.MediaPlayer(video.getbestaudio().url)
                media.play()
                time.sleep(5)
            else:
                print("Media has stopped playing\n")
                SpeakText("Media has stopped playing")
                bThreadJoin = True
                stop_event.set()
                musicInputThread.join()
                print("Thread Stopped..\n")
                bQuery = True
                bMusicConfirm = False
                time.sleep(4)
                stop_event.clear()


while True:
       for event in pygame.event.get():
          if event.type == pygame.USEREVENT:    
             if len ( playlist ) > 0:
                mixer.music.queue ( playlist.pop() )
                # musicpath = os.path.join(filedir, "New Project\Aeris.mp3")
    for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if len ( playlist ) > 0:
                    mixer.music.queue (playlist.pop())

    with open('Playlist.txt', 'r', errors = 'ignore') as reader:
        print(reader.read())
    playlist = list()
    playlist.append ( os.path.join(filedir, "New Project\Aeris.mp3") )
    playlist.append ( os.path.join(filedir, "New Project\Love.mp3") )

    # mixer.pre_init(44100, 16, 2, 4096)
    # musicPath = os.path.join(filedir, "New Project\Love.mp3")
    # musicPlaylist = os.path.join(filedir, "New Project")



    if mixer.music.get_busy():
            if nCounter < nSongs:
                nCurrentIndex = random.randint(0, nSongs-1)
                sCurrentSong = playlist[nCurrentIndex]
                nNextIndex = random.randint(0, nSongs-1)
                sNextSong = playlist[nNextIndex]

                mixer.music.queue(sCurrentSong)
                mixer.music.load(sCurrentSong)
                mixer.music.play()
                print("\nPlaying", itemlist[nCurrentIndex])

                nCounter += 1


    # print("Song Will Come to an AutoStop")
            # if mixer.music.get_busy():
                #if nCounter > nSongs:
                    #mixer.music.stop()
                    #bStop = True

                        
    try:
        # Use the microphone as source for input. 
        with sr.Microphone() as source2:
            # Wait for a second to let the recognizer adjust the energy threshold based on the surrounding noise level
            r.adjust_for_ambient_noise(source2, duration=0.2)
        
            # Listens for the user's input 
            audio2 = r.listen(source2)
        
            # Using Google to recognize audio
            # Google Recognizer(Requires Active Internet Connection)
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
            if MyText:
                tempInput = MyText
                print(tempInput)
                source2 = None
                audio2 = None
                MyText = None
                inConversationShell = False
            
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e)) 
                
    except sr.UnknownValueError:
        print("unknown error occured")



    musicInputThread = threading.Thread(target=UserSpeechInput)
    import concurrent.futures
    with concurrent.futures.ThreadPoolExecutor() as executor:
    future = executor.submit(foo, 'world!')
    return_value = future.result()
    print(return_value)

    concurrent.futures.ThreadPoolExecutor().submit(UserSpeechInput)
    
    for event in pygame.event.get():
            if event.type == NEXT_SONG:
                nCurrentIndex = random.randint(0, nSongs - 1)
                sCurrentSong = playlist[nCurrentIndex]
                pygame.mixer.music.load(sCurrentSong)
                pygame.mixer.music.play()
                print("\nPlaying", itemlist[nCurrentIndex], end='\n\n')
                MusicOptions()
            else:
                ch = str(musicInput.result())
                print(ch)
    musicInput = concurrent.futures.ThreadPoolExecutor().submit(UserSpeechInput)

    if bThreadJoin:
    ch = MusicOptions()
    bThreadJoin = False

        def VolumeInput():
        while True:
            try:
                fVolume = float(input("Enter Volume(0 to 1): "))
                pygame.mixer.music.set_volume(fVolume)
                print("Volume has been set to", fVolume)
                break
            except:
                print("Unknown Value for Volume")
                continue

        voices = engine.getProperty('voices')

    for voice in voices: 
        # to get the info. about various voices in our PC  
        print("Voice:") 
        print("ID: %s" %voice.id) 
        print("Name: %s" %voice.name) 
        print("Age: %s" %voice.age) 
        print("Gender: %s" %voice.gender) 
        print("Languages Known: %s" %voice.languages)



    r = search.result()
    print(r)
    res = json.loads(r)
    res1 = res['search_result']
    res2 = res1[0]
    res_fin = res2['link']
    print(res1)
    
    # best = video.getbest()

        #best = video.getbestaudio()
        #media = vlc.MediaPlayer(pafy.new(url).getbestaudio().url)
        
        def MediaPlay():
            while not bThreadJoin:
                ch = UserSpeechInput()
                if ch == "stop" or ch == "exit":
                    media.stop()
                    print("Thread Stoppingg")







    Youtube Query Request:
            #if bQuery:
            #while not bMusicConfirm:

                # Youtube Query
                print("Searching... ", end='\n')
                SpeakText("Ask for a Song ~")
                videoQuery = UserSpeechInput()
                repeatQuery = "Do you want me to Play" + videoQuery + "?"
                print("Play", videoQuery, "?")
                SpeakText(repeatQuery)
                #Ask for confirmation
                confirmation = UserSpeechInput()
                if confirmation == "yes":
                    bMusicConfirm = True
                else:
                    continue
                    

            
            
'''

##################################################################################################################################################################################################################

                        



####################  Main Code  ####################

StartMessage()
while True:
    SpeakText("What can I do for you?")
    tempInput = UserSpeechInput()

    if 'reminder' in tempInput:
        Reminder(tempInput)
    if 'music' in tempInput:
        MusicPlayer()
    if 'wikipedia' in tempInput:
        Wikipedia(tempInput)
    if 'google' in tempInput:
        Google()
    if 'news' in tempInput:
        News()
    if 'mail' in tempInput:
        Mail()
        

    tempInput = ''
    continue



    '''
    if (tempInput == "date" or tempInput == "d"):
        Date()
    elif (tempInput == "time" or tempInput == "t"):
        Time()
    elif (tempInput == "weather" or tempInput == "w"):
        Weather()
    elif (tempInput == "datetime" or tempInput == "dt"):
        Date()
        Time()
    elif (tempInput == "dateweather" or tempInput == "dw"):
        Date()
        Weather()
    elif (tempInput == "timeweather" or tempInput == "tw"):
        Time()
        Weather()
    elif (tempInput == "reminder" or tempInput == "remind" or tempInput == "going out" or tempInput == "i'm going out" or tempInput == "i;m going off" or tempInput == "going off"):
        Reminder()
    elif (tempInput == "music" or tempInput == "play music"):
        MusicPlayer()
        WelcomeBack()
    elif (tempInput == "youtube" or tempInput == "play youtube" or tempInput == "play ice"):
        YoutubePlayer()
        WelcomeBack()
        
    elif (tempInput == "exit" or tempInput == "exid" or tempInput == "goodbye"):
        print("\n" + Lisa + "Goodbye...")
        time.sleep(5)
        sys.exit()
    else:
        YoutubePlayer()
    else:
        print("No Such Option Found ! \n")
        SpeakText("No Such Option Found!")
    '''

    


##################################################################################################################################################################################################################




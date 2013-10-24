import time
import mp3play
from settings import Settings


# Thread that handles the display of messages and the clock!
def DisplayThread(displayQ, startTime, communicationQ):
    """

    @param displayQ:
    @param startTime:
    @param communicationQ:
    """
    secondsPrinted = 0
    run = True
    while run:
        time.sleep(.1)

        # Check if we need to display the clock:
        now = time.time()
        minute, seconds = divmod(now - startTime, 60)
        seconds = int(seconds)
        if seconds != secondsPrinted:
            secondsPrinted = seconds
            print '%02d:%02d' % (minute, seconds)

        # Check if the display queu needs processing:
        if len(displayQ) > 0:
            (msg, callBack) = displayQ.popleft()
            print msg
            if not callBack is None:
                callBack()

        #Check for signals in the communication thread
        if len(communicationQ) >0:
            for msg in communicationQ:
                if msg == 'DISPLAY-STOP':
                    run = False

# Thread that handles the audioQueue and playback.
def AudioThread(audioQ, communicationQ):
    """

    @param audioQ:
    @param communicationQ:
    """
    run = True
    while run:
        # If there is no audio to play, we make some random noise
        if len(audioQ) == 0:
            siren = randomSiren()
            siren.play()

            while len(audioQ) == 0 and siren.isplaying():
                time.sleep(.1)

        #Check if the audio queu needs processing
        if len(audioQ) > 0:
            (sound, duration, callBack) = audioQ.popleft()
            clip = mp3play.load(Settings.soundsDir + sound)
            if duration > 0:
                timer = time.time() + duration
                while time.time() < timer:
                    if not clip.isplaying():
                        clip.play()
                    time.sleep(.1)
                clip.stop()
            else:
                clip.play()
                while clip.isplaying():
                    time.sleep(.1)

            if not callBack is None:
                callBack()

        #Check for signals in the communication thread
        if len(communicationQ) >0:
            for msg in communicationQ:
                if msg == 'AUDIO-STOP':
                    run = False

def randomSiren():
    """


    @return:
    """
    from random import randint
    rnd = randint(0,3)
    if rnd == 0:
        siren = mp3play.load(Settings.soundsDir + Settings.sound['siren1'])
    elif rnd == 1:
        siren = mp3play.load(Settings.soundsDir + Settings.sound['siren1'])
    elif rnd == 2:
        siren = mp3play.load(Settings.soundsDir + Settings.sound['siren2'])
    elif rnd == 3:
        siren = mp3play.load(Settings.soundsDir + Settings.sound['siren3'])
    else:
        print "Error in random int, it retrns: " + str(rnd)
        exit()

    return siren

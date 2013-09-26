import time
import mp3play
from settings import Settings


# Thread that handles the display of messages and the clock!
def DisplayThread(displayQ, startTime):
    secondsPrinted = 0
    while True:
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

# Thread that handles the audioQueue and playback.
def AudioThread(audioQ):
    while True:
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

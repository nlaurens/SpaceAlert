# Requires mp3play (easy_install mp3play from pipy)
import time
import sys
import mp3play
from collections import deque
from threading import Thread
from settings import Settings

#TODO;
# - add second phase begins (no event is spawned for this. Should be directly
# after 1st phase ends.).
# - Refactor audio/display threads to proper state machine's (that just get a
# state and decide what to do).
# - Give audio/display threads access to audio/display queue's
# - Add the german language pack into the settings and make a 1 line languag
# eswitch!


# Thread that handles the audioQueue and playback.
def AudioThread(audioQ):
    while True:
        time.sleep(.1)

        #Check if the audio queu needs processing
        if len(audioQ) > 0:
            sound = audioQ.popleft()

            # Communication Systems Down is a special case:
            if sound.startswith('CS'):
                duration = int(sound[2: sound.index('-') ])
                sound = sound[sound.index('-') + 1:]
                clip = mp3play.load(Settings.soundsDir + sound)
                clip.play()
                timer = time.time() + duration

                # First play the communications down
                print 'DEBUG playing audio: ' + sound
                clip.play()
                while clip.isplaying():
                    time.sleep(.1)

                # then play the white noise till the timer runs out
                sound = (Settings.soundsDir + Settings.sound['noise'])
                clip = mp3play.load(sound)
                while time.time() < timer:
                    if not clip.isplaying():
                        print 'DEBUG playing audio: ' + sound
                        clip.play()
                    time.sleep(.1)
                clip.stop()

                #Last play the communicatoins restored
                sound = (Settings.soundsDir + Settings.sound['CSRestored'])
                clip = mp3play.load(sound)
                print 'DEBUG playing audio: ' + sound
                clip.play()
                while clip.isplaying():
                    time.sleep(.1)

            else:
                clip = mp3play.load(Settings.soundsDir + sound)
                print 'DEBUG playing audio: ' + sound
                clip.play()
                while clip.isplaying():
                    time.sleep(.1)


# Thread that handles the display of messages and the clock!
def DisplayThread(displayQ):
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
            msg = displayQ.popleft()
            print msg


#Split the timeString (mmss) from the EventString (xxx)
def splitEvent(event):
    i = 0
    while event[i].isdigit():
        i = i + 1
    return (event[0:i], event[i:])


#Returns the time
def convertTime(timeStr):

    if len(timeStr) == 3:
        return int(timeStr[0]) * 60 + int(timeStr[1:3])
    elif len(timeStr) == 4:
        return int(timeStr[0:2]) * 60 + int(timeStr[2:4])

    print 'Error in time of timeStr: ' + timeStr
    sys.exit(1)


def processEvent(event, audioQ, displayQ):
    if event['type'] == 'AL':
        phase = event['params'][0]
        zone = event['params'][-1]
        threat = event['params'][1:len(event['params']) - 1]

        # queue all messages:
        displayQ.append(Settings.messg['AL'] + ' - ' + Settings.messg['ALP'] % (phase) + ' - ' +  Settings.messg['ALT' + threat] + ' - ' + Settings.messg['ALZ' + zone])

        # queue all audio:
        audioQ.append(Settings.sound['AL'])
        audioQ.append(Settings.sound['ALP'] % (phase))
        audioQ.append(Settings.sound['ALT' + threat])
        audioQ.append(Settings.sound['ALZ' + zone])
        audioQ.append(Settings.sound['repeat'])
        audioQ.append(Settings.sound['ALP'] % (phase))
        audioQ.append(Settings.sound['ALT' + threat])
        audioQ.append(Settings.sound['ALZ' + zone])
    elif event['type'] == 'UR':
        phase = event['params'][0]
        zone = event['params'][-1]
        threat = event['params'][1:len(event['params']) - 1]

        # queue all messages:
        displayQ.append(Settings.messg['UR'] + ' - ' + Settings.messg['ALP'] % (phase) + ' - ' +  Settings.messg['ALT' + threat] + ' - ' + Settings.messg['ALZ' + zone])

        # queue all audio:
        audioQ.append(Settings.sound['UR'])
        audioQ.append(Settings.sound['ALP'] % (phase))
        audioQ.append(Settings.sound['ALT' + threat])
        audioQ.append(Settings.sound['ALZ' + zone])
        audioQ.append(Settings.sound['repeat'])
        audioQ.append(Settings.sound['UR'])
        audioQ.append(Settings.sound['ALP'] % (phase))
        audioQ.append(Settings.sound['ALT' + threat])
        audioQ.append(Settings.sound['ALZ' + zone])
    elif event['type'] == 'CS':
        displayQ.append(Settings.messg['CS'])
        audioQ.append(Settings.sound['CS'] % (event['params']))
    else:
        displayQ.append(Settings.messg[event['type'] + event['params']])
        audioQ.append(Settings.sound[event['type'] + event['params']])

    return event

script = '010CS5,020DT,040AL3STB,060ID,140PE1,250PE2'

lijst = script.split(',')

eventList = []
for eventStr in lijst:
    event = {}
    (timeStr, eventStr) = splitEvent(eventStr)
    event['time'] = convertTime(timeStr)
    event['type'] = eventStr[0:2]
    event['params'] = eventStr[2:]
    eventList.append(event)

#spawn t-1m, t-20s, phase events for end of phase:
for event in eventList:
    if event['type'] == 'PE' and event['params'] == '1' or event['params'] == '2':

        #add the 1 min warning
        tmpEvent = {}
        tmpEvent['time'] = event['time'] - 63
        tmpEvent['type'] = 'PE'
        tmpEvent['params'] = event['params'] + '1M'
        eventList.append(tmpEvent)

        #add the 20s warning
        tmpEvent2 = {}
        tmpEvent2['time'] = event['time'] - 23
        tmpEvent2['type'] = 'PE'
        tmpEvent2['params'] = event['params'] + '20S'
        eventList.append(tmpEvent2)

        # correct for the length of the mp3 10s and the actual end sound in the
        # mp3 (3 seconds before end).
        event['time'] = event['time'] - 7  # adjust for the length of the mp3 (10s)

#Sort the list after the inserts
eventList = sorted(eventList, key=lambda k: k['time'])

# Initilaize the audio & display queu:
audioQ = deque([])
displayQ = deque([])

# Spawn the audio thread:
audioThread = Thread(target = AudioThread, args = (audioQ, ))
audioThread.setDaemon(True)
audioThread.start()

# Spawn the display thread:
displayThread = Thread(target = DisplayThread, args = (displayQ,))
displayThread.setDaemon(True)
displayThread.start()

# Run the game!
startTime = time.time()
audioQ.append(Settings.sound['begin'])
displayQ.append(Settings.messg['begin'])

for event in eventList:

    # Set the timer for the next event.
    timer = startTime + event['time']

    # Wait for next event.
    while time.time() < timer:
        # go easy on the CPU:
        time.sleep(.1)

    # Process & run the event
    event = processEvent(event, audioQ, displayQ)

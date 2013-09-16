# Requires mp3play (easy_install mp3play from pipy)
import time
import sys
import mp3play
from collections import deque
from threading import Thread


#TODO;
# Vertaal tabel voor de threats -> text & mp3!


# Thread that handles the audioQueue and playback.
def AudioThread(audioQ):
    while True:
        time.sleep(.1)

        #Check if the audio queu needs processing
        if len(audioQ) > 0:
            sound = audioQ.popleft()
            print 'playing audio: ' + sound
            clip = mp3play.load('sounds/' + sound + '.mp3')
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
    if event['type'] == 'PE':
        print 'TODO Phase ends - ' + event['params']
    elif event['type'] == 'AL':
        phase = event['params'][0]
        zone = event['params'][-1]
        threat = event['params'][1:len(event['params']) - 1]
        msg = 'Alert - T%d - threat: %s - zone:%s' % (int(phase), threat, zone)
        displayQ.append(msg)
        audioQ.append('alert')
        audioQ.append('time_t_plus_'+ phase)
        audioQ.append('threat')
        audioQ.append('zone_'+ zone)
        audioQ.append('repeat')
        audioQ.append('time_t_plus_'+ phase)
        audioQ.append('threat')
        audioQ.append('zone_'+ zone)
    elif event['type'] == 'UR':
        print 'TODO Unconfirmed Report - ' + event['params']
    elif event['type'] == 'ID':
        print 'TODO Incoming Data' + event['params']
    elif event['type'] == 'DT':
        print 'TODO Data Transfer' + event['params']
    elif event['type'] == 'CS':
        print 'TODO Communications Down' + event['params']

    return event

script = '015AL1STB,100AL2TB,215DT,300DT,310AL3TR,320ID,410PE1,425DT,630ID,720PE2'

filename = r'sounds\alert.mp3'

lijst = script.split(',')

eventList = []
for eventStr in lijst:
    event = {}
    (timeStr, eventStr) = splitEvent(eventStr)
    event['time'] = convertTime(timeStr)
    event['type'] = eventStr[0:2]
    event['params'] = eventStr[2:]
    event['sounds'] = []
    eventList.append(event)

#spawn t-1m, t-20s events for end of phase:
for event in eventList:
    if event['type'] == 'PE' and event['params'] == '1' or event['params'] == '2':
        event['time'] = event['time'] - 10  # adjust for the length of the mp3 (10s)

        #add the 1 min warning
        tmpEvent = {}
        tmpEvent['time'] = event['time'] - 63
        tmpEvent['type'] = 'PE'
        tmpEvent['params'] = event['params'] + 'm'
        eventList.append(tmpEvent)

        #add the 20s warning
        tmpEvent2 = {}
        tmpEvent2['time'] = event['time'] - 23
        tmpEvent2['type'] = 'PE'
        tmpEvent2['params'] = event['params'] + 's'
        eventList.append(tmpEvent2)

#Sort the list after the inserts
eventList = sorted(eventList, key=lambda k: k['time'])

# Initilaize the audio & display queu:
audioQ = deque(['begin_first_phase'])
displayQ = deque(['Alert, enemy activity detected! Please begin first phase!'])

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
for event in eventList:

    # Set the timer for the next event.
    timer = startTime + event['time']
    now = time.time()

    # Wait for next event.
    while now < timer:
        # go easy on the CPU:
        time.sleep(.1)
        now = time.time()

    # Process & run the event
    event = processEvent(event, audioQ, displayQ)

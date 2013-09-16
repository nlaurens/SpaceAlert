# Requires mp3play (easy_install mp3play from pipy)
import time
import sys
import mp3play

#TODO;
# Vertaal tabel voor de zones, threats -> text & mp3!

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


def processEvent(event):
    if event['type'] == 'PE':
        print 'Phase ends - ' + event['params']
    elif event['type'] == 'AL':
        phase = event['params'][0]
        zone = event['params'][-1]
        threat = event['params'][1:len(event['params']) - 1]
        event['text'] = 'Alert - T%d - threat: %s - zone:%s' % (int(phase), threat, zone)
        event['sound'] = r'sounds\alert.mp3'
    elif event['type'] == 'UR':
        print 'Unconfirmed Report - ' + event['params']
    elif event['type'] == 'ID':
        print 'Incoming Data' + event['params']
    elif event['type'] == 'DT':
        print 'Data Transfer' + event['params']
    elif event['type'] == 'CS':
        print 'Communications Down' + event['params']

    return event

script = '002AL1STB,005AL2TB,215DT,300DT,310AL3TR,320ID,410PE1,425DT,630ID,720PE2'

filename = r'sounds\alert.mp3'

lijst = script.split(',')
print script

eventList = []
for eventStr in lijst:
    event = {}
    (timeStr, eventStr) = splitEvent(eventStr)
    event['time'] = convertTime(timeStr)
    event['type'] = eventStr[0:2]
    event['params'] = eventStr[2:]
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


# Run the game!
startTime = time.time()
for event in eventList:
    timer = startTime + event['time']
    now = time.time()
    while now < timer:
        time.sleep(1)
        now = time.time()
        minute, seconds = divmod(now - startTime, 60)
        print '%02d:%02d' % (minute, seconds)
    event = processEvent(event)
    print event['text']
    mp3 = mp3play.load(event['sound'])
    mp3.play()

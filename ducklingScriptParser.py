import time
import sys
import mp3play
from collections import deque
from threading import Thread
from settings import Settings


class ducklingScriptParser(script):

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

    def __init__(self, script):
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

#ADD THE START GAME EVENT CLASS to LIST

#Sort the list after the inserts
        eventList = sorted(eventList, key=lambda k: k['time'])

        return eventList

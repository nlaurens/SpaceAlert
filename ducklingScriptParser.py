import sys
import event


class ducklingScriptParser():
    #Split the timeString (mmss) from the EventString (xxx)
    """

    """

    def __init__(self):
        pass

    @staticmethod
    def splitEvent(strEvent):
        """

        @param strEvent:
        @return:
        """
        i = 0
        while strEvent[i].isdigit():
            i += 1
        return strEvent[0:i], strEvent[i:]


    #Returns the time
    @staticmethod
    def convertTime(timeStr):

        """

        @param timeStr:
        @return:
        """
        if len(timeStr) == 3:
            return int(timeStr[0]) * 60 + int(timeStr[1:3])
        elif len(timeStr) == 4:
            return int(timeStr[0:2]) * 60 + int(timeStr[2:4])

        print 'Error in time of timeStr: ' + timeStr
        sys.exit(1)

    @staticmethod
    def strThreatToEventThreat(strThreat):
        """

        @param strThreat:
        @return:
        """
        if strThreat == 'T':
            return 'threat_normal'
        elif strThreat == 'ST':
            return 'threat_serious'
        elif strThreat == 'IT':
            return 'internal_normal'
        elif strThreat == 'SIT':
            return 'internal_serious'
        else:
            print "ERROR unkown threat code, make it a proper exception!"
            print "threatstr: " + strThreat

    @staticmethod
    def strZonetoEventZone(strZone):
        """

        @param strZone:
        @return:
        """
        if strZone == 'R':
            return 'zone_red'
        elif strZone == 'W':
            return 'zone_white'
        elif strZone == 'B':
            return 'zone_blue'
        else:
            print "ERROR unkown zone code, make it a proper exception!"
            print "threatstr: " + strZone

    def parseEventStr(self, eventStr):
        """

        @param eventStr:
        @return:
        """
        eventList = []
        (timeStr, eventStr) = self.splitEvent(eventStr)
        time = self.convertTime(timeStr)
        strType  = eventStr[0:2]
        strParams = eventStr[2:]

        if strType == "PE":
            eventList.append((time - 60, event.phaseEnds(int(strParams), '1min')))
            eventList.append((time - 20, event.phaseEnds(int(strParams), '20s')))
            eventList.append((time - 7, event.phaseEnds(int(strParams), 'now')))
        elif strType == "AL":
            turn = int(strParams[0])
            threat = self.strThreatToEventThreat(strParams[1:len(strParams) - 1])
            zone = self.strZonetoEventZone(strParams[-1])
            eventList.append((time, event.alert(turn, threat, zone)))
            pass
        elif strType == "UR":
            turn = int(strParams[0])
            threat = self.strThreatToEventThreat(strParams[1:len(strParams) - 1])
            zone = self.strZonetoEventZone(strParams[-1])
            eventList.append((time, event.alert(turn, threat, zone, True)))
        elif strType == "ID":
            eventList.append((time, event.incomingData()))
        elif strType == "DT":
            eventList.append((time, event.dataTransfer()))
        elif strType == "CS":
            eventList.append((time, event.communicationSystemsDown(int(strParams))))
        else:
            print 'error unkown eventtype in script. TODO: make a proper exception from this.'
            print 'eventtyp: ' + strType

        #return the events
        return eventList

    def convertScript(self, script):
        """

        @param script:
        @return:
        """
        lijst = script.split(',')

        eventList = [(0, event.start())]
        for eventStr in lijst:
            events = self.parseEventStr(eventStr)
            eventList.extend(events)

        #Replace the last phase ends with mission ends
        lastEvent = eventList[-1][1]
        if isinstance(lastEvent,event.phaseEnds):
            lastPhaseNumber = lastEvent.getPhaseNumber()
            for time, eventItem in eventList:
                if isinstance(eventItem, event.phaseEnds):
                    if eventItem.getPhaseNumber() == lastPhaseNumber:
                        eventItem.convertToEndMission()

        else:
            print 'ERROR, the last event is not a phase end!'


        return eventList

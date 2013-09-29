import time
from collections import deque
from threading import Thread
from settings import Settings
import event
import threads

def main():
    #load all chapters and missions
    from missionList import missionList
    missionList = missionList()

    #run the menu to make a selection from the available missions
    from SpaceAlertMenu import SpaceAlertMenu
    menu = SpaceAlertMenu()
    chapter, mission = menu.main(missionList)

    if chapter == None and mission == None:
        return False
    else:
        script = missionList.getScript(chapter, mission)
        runGame(script)
        return True

def runGame(script):
    global audioQ, displayQ, eventList, startTime, audioThread, displayThread, timeEvent, event, timer

    # Initilaize the audio & display queu:
    audioQ = deque([])
    displayQ = deque([])

    #parse the duckling script
    eventList = ducklingScriptParser(script)
    #Simple testing mission:
    eventList = []
    eventList.append((0, event.start()))
    eventList.append((10, event.alert(1, 'threat_normal', 'zone_red')))
    eventList.append((25, event.phaseEnds(1, '1min')))
    eventList.append((40, event.communicationSystemsDown(5)))
    eventList.append((55, event.phaseEnds(1, '20s')))
    eventList.append((75 - 7, event.phaseEnds(1, 'now')))
    eventList.append((90, event.alert(1, 'threat_serious', 'zone_white')))
    eventList.append((105, event.dataTransfer()))
    eventList.append((125, event.incomingData()))

    # Start the game NOW:
    startTime = time.time()

    # Spawn the audio thread:
    audioThread = Thread(target=threads.AudioThread, args=(audioQ,))
    audioThread.setDaemon(True)
    audioThread.start()

    # Spawn the display thread:
    displayThread = Thread(target=threads.DisplayThread, args=(displayQ, startTime))
    displayThread.setDaemon(True)
    displayThread.start()

    for timeEvent, event in eventList:

        # Set the timer for the next event.
        timer = startTime + timeEvent

        # Wait for next event.
        while time.time() < timer:
            # go easy on the CPU:
            time.sleep(.1)

        # Add the que's to the event and run the event
        event.setQs(audioQ, displayQ)

if __name__ == "__main__":
    #play the main until it quits
    play = True
    while play:
        play = main()

    print "Byebye space cadet!"

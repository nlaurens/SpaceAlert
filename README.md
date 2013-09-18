#Little Duckling Player
This is an interpreter for scripted missions of the board game Space Alert
(Vlaada Chvatil). Made to work with the missions in the little duckling
expansion.

Rule book, missions, sounds available at:

- http://czechgames.com/en/space-alert/
- http://boardgamegeek.com/boardgame/38453/space-alert
- http://boardgamegeek.com/boardgameexpansion/90133/little-duckling-fan-expansion-for-space-alert

##Todo

- add ability to read from mission files
- add menu to browse through the different mission files and select one to play
- add second phase begins (no event is spawned for this. Should be directly  after 1st phase ends.).
- Refactor audio/display threads to proper state machine's (that just get a state and decide what to do).
- Give audio/display threads access to audio/display queue's
- Add the german language pack into the settings and make a 1 line languag eswitch!
- make it stop after a mission ends (or give an error if the event queue is empty).
- Make a build script that compiles the script to a windows binary.

##Scripted events format
 All events have the following format:
 
 mmss...
 
 * mm = minute the event occurs. The first digit can be ommited;
 * ss = second the event occurs;
 * ... = the event that happens (can be between 2 and 5 characters).
 
 ###Phase events:
 PE#
 Time the events ends. Note you get a 1 min warning and 20 second warning before the end of the phase.
 
 * \# = the number of phase that is ending.
 
 
 ###Alerts
 AL#TZ
 
 * \# = the phase the threat enters the game;
 * T = threat code:
   * T = threat;
   * ST = serious threat;
   * IT - internal threat;
   * SIT - serious internal threat;
 * Z - zone where the alert occurs:
   * R - Red zone;
   * W - White zone;
   * B - Blue zone.
 
 ###Unconfirmed Reports 
 UR#TZ
 
 See Alerts for parameters.
 
 ###Incoming Data
 ID
 
 ###Data Transfers
 DT
 
 ###Communications System Down 
 CS#
 
 * \# - Duration of the system downs (in seconds).

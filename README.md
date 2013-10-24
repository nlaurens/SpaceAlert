#Little Duckling Player
This is an interpreter for scripted missions of the board game Space Alert
(Vlaada Chvatil). Made to work with the missions in the little duckling
expansion.

Rule book, missions, sounds available at:

- http://czechgames.com/en/space-alert/
- http://boardgamegeek.com/boardgame/38453/space-alert
- http://boardgamegeek.com/boardgameexpansion/90133/little-duckling-fan-expansion-for-space-alert

##Installation

- Install requirements (in a Python virtualenv, if you like):
    `$ pip install -r requirements.txt`

##Todo


- make the length of the noise in the communications down event depending on
  the real starttime of the event. Not on the time it starts playing (only
  happens when there are events spawning to close for the mp3 to finish playing)
- add an 'enumerate' to the phase ends constructor instead of strings.
- add a 'begin second phase' after the first phase has ended message has ended.
- make the offsets in the mp3s (for example in first phase ends in 5.4.3.) to
  the settigns file, as this might be different for different sounds.
- Add the german language pack into the settings and make a 1 line languag eswitch!
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

## Mission config files

The 2.7 python reader for config files does not keep the order in the config
file when parsing. Therefore the missions in each chapter are sorted by
alphabetical order in the parser. It is thus highly recommended to keep a name
convention such as "mission1", "missoin2" etc.

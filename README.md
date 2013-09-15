This is an interpreter for scripted missions of the board game Space Alert (Vlaada Chvatil).

#Script format.
All events have the following format:

mmss...

* mm = minute the event occurs. The first digit can be ommited;
* ss = second the event occurs;
* ... = the event that happens (can be between 2 and 5 characters).

##Phase events:
PE#
Time the events ends. Note you get a 1 min warning and 20 second warning before the end of the phase.

* \# = the number of phase that is ending.


##Alerts
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

##Unconfirmed Reports 
UR#TZ

See Alerts for parameters.

##Incoming Data
ID

##Data Transfers
DT

##Communications System Down 
CS#

* \# - Duration of the system downs (in seconds).

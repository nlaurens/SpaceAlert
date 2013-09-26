from settings import Settings
#
#
## event masterClass
class event(object):
    settingsTag = None

    def setQs(self, audioQ, displayQ):
        self.audioQ = audioQ
        self.displayQ = displayQ

    # The standard implementation is to queue the sound and message in the
    # settings.
    def execute(self):
        if self.settingsTag is None:
            raise NotImplementedError("Settings tag is not implemented")
        else:
            self.audioQ.append( (Settings.sound[self.settingsTag], -1, None) )
            self.displayQ.append ( (Settings.messg[self.settingsTag], None) )

class start(event):
    settingsTag = 'begin'

class phaseEnds(event):
    def __init__(self, phaseNumber, warning):
        self.settingsTag = 'phase_' + str(phaseNumber) + '_ends_in_' + warning

class alert(event):

    # use: threat = 'threat_normal', 'threat_serious', 'internal_normal', 'internal_serious'
    # zone = 'zone_blue', 'zone_red', 'zone_white'
    def __init__(self, turn, threat, zone, unconfirmed=False):
        self.turn = turn
        self.threat = threat
        self.zone = zone

    def createMessg(self, repeat):
        if repeat:
            messg = Settings.messg['repeat']
        else:
            messg = ''

        messg = messg + Settings.messg['alert']
        messg += ' - '
        messg = messg + Settings.messg['time_t'] % self.turn
        messg += ' - '
        messg = messg + Settings.messg[self.threat]
        messg += ' - '
        messg = messg + Settings.messg[self.zone]
        return messg

    def execute(self):
        self.displayQ.append( (self.createMessg(False), None))
        self.audioQ.extend ( [(Settings.sound['alert'], -1, None), ( Settings.sound['time_t'] % self.turn, -1, None), (Settings.sound[self.threat], -1, None), (Settings.sound[self.zone], -1, self.executeRepeat)] )

    def executeRepeat(self):
        self.displayQ.append( (self.createMessg(True), None))
        self.audioQ.extend( [(Settings.sound['repeat'], -1, None), ( Settings.sound['time_t'] % self.turn, -1, None), (Settings.sound[self.threat], -1, None), (Settings.sound[self.zone], -1, None)] )


class incomingData(event):
    settingsTag = 'incoming_data'

class dataTransfer(event):
    settingsTag = 'data_transfer'

class communicationSystemsDown(event):
    def __init__(self, noiseDuration):
        self.noiseDuration = noiseDuration

    def execute(self):
        self.audioQ.append((Settings.sound['communication_systems_down'], -1, self.execute2))
        self.displayQ.append((Settings.messg['communication_systems_down'], None))

    def execute2(self):
        self.audioQ.append((Settings.sound['noise'], self.noiseDuration, self.execute3))

    def execute3(self):
        self.audioQ.append((Settings.sound['communication_systems_restored'], -1, None))
        self.displayQ.append((Settings.messg['communication_systems_restored'], None))

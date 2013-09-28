import ConfigParser


class missionList():

    def __init__(self):
        #TODO
        #Scan for all cfg files in the mission dir
        #TMP solution, should be replaced with all .cfg files from 'mission' dir.
        self.missionConfigs = ['duckling.cfg']

    def parseConfigFiles(self):
        missionList = []

        config = ConfigParser.RawConfigParser()
        config.read('missions/duckling.cfg')

        for section in config.sections():
            options = config.options(section)
            missions = []
            for option in options:
                missions.append({option: config.get(section, option)})
            missionList.append({section: missions})

        #TODO: CHECK IF ALL MISSIONS ARE PLAYBLE.
        return missionList

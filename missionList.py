import ConfigParser


class missionList():

    def __init__(self):
        self.chapter = {}
        #TODO
        #Scan for all cfg files in the mission dir
        #TMP solution, should be replaced with all .cfg files from 'mission' dir.
        missionConfigs = ['duckling.cfg', 'LittleDuckling.cfg']

        for file in missionConfigs:
            self.parseConfigFile('missions/'+file)

        #TODO: CHECK IF ALL MISSIONS ARE PLAYBLE.

    def parseConfigFile(self, file):
        chapter = {}
        config = ConfigParser.RawConfigParser()
        config.read(file)

        for section in config.sections():
            options = config.options(section)
            mission = {}
            for option in options:
                mission[option] = config.get(section, option)

            chapter[section] = mission

        self.chapter.update(chapter)

    def getChapters(self):
        chapterList = []
        for chapter, missions in self.chapter.iteritems():
            chapterList.append(chapter)

        chapterList.sort()
        return chapterList

    def getMissions(self, chapter):
        missionList = []
        for mission, missionScript in self.chapter[chapter].iteritems():
            missionList.append(mission)

        missionList.sort()
        return missionList

    def getScript(self, chapter, mission):
        return self.chapter[chapter][mission]

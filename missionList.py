import ConfigParser


class missionList():

    def __init__(self):
        #TODO
        #Scan for all cfg files in the mission dir
        #TMP solution, should be replaced with all .cfg files from 'mission' dir.
        self.missionConfigs = ['duckling.cfg']

        self.loadMissionFiles()

    def loadMissionFiles(self):
        chapter = {}

        config = ConfigParser.RawConfigParser()
        config.read('missions/duckling.cfg')

        for section in config.sections():
            options = config.options(section)
            mission = {}
            for option in options:
                mission[option] = config.get(section, option)

            chapter[section] = mission

        #TODO: CHECK IF ALL MISSIONS ARE PLAYBLE.
        self.chapter = chapter

    def getChapters(self):
        chapterList = []
        for chapter, missions in self.chapter.iteritems():
            chapterList.append(chapter)

        return chapterList

    def getMissions(self, chapter):
        missionList = []
        for mission, missionScript in self.chapter[chapter].iteritems():
            missionList.append(mission)
        return missionList


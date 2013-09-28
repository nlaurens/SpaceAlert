class SpaceAlertMenu():
    def quit(self):
        print 'Byebye Space Cadette!'
        exit()

    def selectChapter(self):
        chapterMenuText = "Select a chapter to play:\n"
        i = 1
        chapters = self.missionList.getChapters()
        for chapter in chapters:
            chapterMenuText += str(i) + ") " + chapter + "\n"
            i += 1

        while True:
            print chapterMenuText
            selection = raw_input("Select chapter: ")
            selection = int(selection)
            if 0 < selection < i:
                return chapters[selection - 1]

    def selectMission(self, chapter):
        missionMenuText = "Select a mission to play:\n"
        i = 1
        missions = self.missionList.getMissions(chapter)
        for mission in missions:
            missionMenuText += str(i) + ") " + mission + "\n"
            i += 1

        while True:
            print missionMenuText
            selection = raw_input("Select mission: ")
            selection = int(selection)
            if 0 < selection < i:
                return missions[selection - 1]


    def noAction(self):
        print 'Say what Cadette?'

    def main(self):
        from missionList import missionList
        self.missionList = missionList()

        mainMenuText = "\n Main Menu.\n (s)elect chapter\n (q)uit"

        while True:
            print mainMenuText
            selection = raw_input("Your selection: ")
            if selection == "q":
                self.quit()
            elif selection == "s":
                chapter = self.selectChapter()
                mission = self.selectMission(chapter)
                return chapter, mission

if __name__ == "__main__":
    SA = SpaceAlertMenu()
    print SA.main()

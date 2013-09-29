class SpaceAlertMenu():

    def subMenu(self, menuItems, menuText):
        i = 1
        for option in menuItems:
            menuText += str(i) + ") " + option + "\n"
            i += 1

        menuText += "0) Back"
        while True:
            print menuText
            selection = raw_input("Make your choice: ")
            if selection.isdigit():
                selection = int(selection)
                if selection == 0:
                    return
                elif 0 < selection < i:
                    return menuItems[selection - 1]

            self.noAction()

    def selectChapter(self):
        menuText = "Select a chapter to play:\n"
        menuOptions = self.missionList.getChapters()
        chapter = self.subMenu(menuOptions, menuText)
        return chapter

    def selectMission(self, chapter):
        menuText = "Select a mission to play:\n"
        missions = self.missionList.getMissions(chapter)
        mission = self.subMenu(missions, menuText)
        return mission

    def noAction(self):
        print 'Say what Cadette?'

    def main(self, missionList):
        self.missionList = missionList

        mainMenuText = "\n Main Menu.\n (s)elect chapter\n (q)uit"

        while True:
            print mainMenuText
            selection = raw_input("Your selection: ")
            if selection == "q":
                return None, None
            elif selection == "s":
                chapter = self.selectChapter()
                if chapter != None:
                    mission = self.selectMission(chapter)
                    if mission != None:
                        return chapter, mission


if __name__ == "__main__":
    SA = SpaceAlertMenu()
    print SA.main()

class SpaceAlertMenu():

    """

    @param missionList:
    """

    def __init__(self, missionList):
        self.missionList = missionList

    def subMenu(self, menuItems, menuText):
        """

        @param menuItems:
        @param menuText:
        @return:
        """
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
        """


        @return:
        """
        menuText = "Select a chapter to play:\n"
        menuOptions = self.missionList.getChapters()
        chapter = self.subMenu(menuOptions, menuText)
        return chapter

    def selectMission(self, chapter):
        """

        @param chapter:
        @return:
        """
        menuText = "Select a mission to play:\n"
        missions = self.missionList.getMissions(chapter)
        mission = self.subMenu(missions, menuText)
        return mission

    @staticmethod
    def noAction():
        """


        """
        print 'Say what Cadette?'

    def main(self):

        """


        @return:
        """
        mainMenuText = "\n Main Menu.\n (s)elect chapter\n (q)uit"

        while True:
            print mainMenuText
            selection = raw_input("Your selection: ")
            if selection == "q":
                return None, None
            elif selection == "s":
                chapter = self.selectChapter()
                if chapter is not None:
                    mission = self.selectMission(chapter)
                    if mission is not None:
                        return chapter, mission

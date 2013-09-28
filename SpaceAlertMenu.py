def quit():
    print 'Quiting Space Alert'
    exit()

def selectChapter():
    print 'playing'

def no_such_action():
    print 'no such action'

def print_menu():
    print '\n'
    print 'Space Alert Menu'
    print '(s)elect chapter'
    print '(q)uit`'

def main():
    # Get all missions:
    from missionList import missionList
    missionList = missionList()

    missionList.getChapters()

    actions = {"s": selectChapter, "q": quit, "Q": quit}
    while True:
        print_menu()
        selection = raw_input("Your selection: ")
        toDo = actions.get(selection, no_such_action)
        toDo()

if __name__ == "__main__":
    main()
import parse
import time

commands = ['u','c','s','i','m', 'w', 't']

class Command:

    def __init__(self, t, c, b):
        '''
        Create a command object from a type and command
        also a browser object
        '''
        self.__type = t
        self.__cmd = c
        self.__browser = b

    def execute(self):
        '''
        Executes whatever the command stored in this object is
        t: The type of command
        c: The command argument
        b: The browser object to execute on
        '''
        if self.__type == 'u':
            if not self.__cmd.startswith("http://"):
                self.__cmd = "http://" + self.__cmd
            self.__browser.get(self.__cmd)
        elif self.__type == 'm':
            self.__browser.maximize_window()
        elif self.__type == 'w':
            sleepMs = int(self.__cmd)
            time.sleep(sleepMs / 1000)
        elif self.__type == 'c':
            c = self.__splitCommand(',')
            target, num = self.__searchFor(c)
            if target and len(target) > num:
                target[num].click()
        elif self.__type == 't':
            c = self.__splitCommand(',')
            if len(c) > 3:
                target, num = self.__searchFor(c)
                text = c[3]
                if target and len(target) > num:
                    target[num].send_keys(text)
        elif self.__type == 's':
            self.__browser.execute_script(self.__cmd)

    def __splitCommand(self, delim):
        c = self.__cmd.split(delim)
        for i in range(len(c)):
            c[i] = c[i].lstrip()
            c[i] = c[i].rstrip()

        return c

    def __searchFor(self, cmd):
        if len(cmd) > 1:
            searchBy = cmd[0]
            pattern = cmd[1]
            avail = 0
            if len(cmd) > 2:
                avail = int(cmd[2])

            searchFunc = self.__getSearchFunc(searchBy)
            if searchFunc:
                res = searchFunc(pattern)
                return res, avail

        return None

    def __getSearchFunc(self, searchBy):
        func = None

        if "class" in searchBy:
            func = self.__browser.find_elements_by_class_name
        elif "css" in searchBy:
            func = self.__browser.find_elements_by_css_selector
        elif "id" in searchBy:
            func = self.__browser.find_elements_by_id
        elif "partial" in searchBy:
            func = self.__browser.find_elements_by_partial_link_text
        elif "link" in searchBy:
            func = self.__browser.find_elements_by_link_text
        elif "name" in searchBy:
            func = self.__browser.find_elements_by_name
        elif "xpath" in searchBy:
            func = self.__browser.find_elements_by_xpath
        elif "tag" in searchBy:
            func = self.__browser.find_elements_by_tag_name

        return func

    def __str__(self):
        return self.__type + "(" + self.__cmd + ")"

class Commands:

    def __init__(self, b):
        '''
        Create a commands container with an attached browser object
        b: a selenium browser object
        '''
        self.__browser = b
        self.__cmds = []
        self.__cursor = 0

    def readCommands(self, openfile):
        '''
        Read all valid commands in a file and store them in this object
        openfile: An open file object
        Note: This function resets its commands / current command
              only if openfile could not be read
        '''

        if not openfile: return

        self.__cmds = []
        self.__cursor = 0

        results = parse.GetCommands(openfile)
        for val in results:
            cmd = self.__parseCommand(val)
            if cmd:
                self.__cmds.append(cmd)

    def executeNext(self):
        '''
        Execute the next command in the container
        Returns true as long as there is a command to execute
        '''

        if self.__cursor < len(self.__cmds):
            print "Executing", self.__cmds[self.__cursor]
            self.__cmds[self.__cursor].execute()
            self.__cursor += 1
            return True
        return False

    def currentCommand(self):
        if self.__cursor < len(self.__cmds):
            return self.__cmds[self.__cursor]
        return ""

    def __parseCommand(self, cmd):
        t = cmd[0]
        c = cmd[2:-1]

        if t in commands:
            return Command(t,c,self.__browser)
        return None

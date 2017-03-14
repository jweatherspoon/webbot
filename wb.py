#!/usr/bin/python

import sys

from selenium import webdriver
from selenium.webdriver.common import keys

from commands import Commands

def main():
    if len(sys.argv) < 2:
        print "Error: Missing commands file input!"
        return -1

    b = webdriver.Chrome()

    f = open(sys.argv[1])
    c = Commands(b)
    c.readCommands(f)

    try:
        while c.executeNext():
            pass
    except Exception as e:
        print "Failed while executing command: "
        print "\t", c.currentCommand()
        print "\n" * 2, "Error Message Given: "
        print e

    raw_input("Waiting to close and exit...")
    b.close()
    c = None

if __name__ == '__main__':
    main()

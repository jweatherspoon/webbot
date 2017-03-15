#!/usr/bin/python

import sys

from selenium import webdriver
from selenium.webdriver.common import keys
from selenium.webdriver.remote.command import Command

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

    if IsOpen(b):
        raw_input("Waiting to close and exit...")
        try:
            b.close()
        except: pass

    c = None

def IsOpen(browser):
    try:
        browser.get_window_position()
        return True
    except:
        return False


if __name__ == '__main__':
    main()

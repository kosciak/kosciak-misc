#!/usr/bin/env python

import curses

import os
os.putenv("ESCDELAY", "25") # no delay after pressing ESC key


def main(scrn):
    
    curses.raw() # disable Ctrl-C, Ctrl-Z
    
    scrn.addstr(0,0, "Press any key... please!")
    while True:
        ch = scrn.getch()
        scrn.addstr(2,0, "                      ")
        scrn.addstr(2,0, "Key code: " + str(ch))
        scrn.addstr(3,0, "                      ")
        scrn.addstr(3,0, "Key name: " + curses.keyname(ch))


if __name__ == "__main__":
    curses.wrapper(main)

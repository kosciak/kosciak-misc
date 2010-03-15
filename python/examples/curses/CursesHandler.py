#!/usr/bin/env python

import curses
import logging


class CursesHandler(logging.Handler):
    
    def __init__(self, win, level=logging.DEBUG):
        logging.Handler.__init__(self, level)
        self.win = win
        maxy, maxx = win.getmaxyx()
        self.height = maxy
        self.formatter = logging.Formatter("%(levelname)s")
    
    def emit(self, record):
        attr = {"DEBUG":curses.A_NORMAL, 
                "INFO":curses.A_NORMAL, 
                "WARNING":curses.A_BOLD, 
                "ERROR":curses.A_BOLD, 
                "CRITICAL":curses.A_STANDOUT}
        
        y,x = self.win.getyx()
        if x != 0:
            #self.win.move(y+1,0)
            y += 1
        if y+1 >= self.height:
            self.win.addstr(self.height-1,0, "--more--")
            self.win.getch()
            self.win.erase()
            y = 0
        
        self.win.addstr(y,0, record.getMessage(), attr[self.format(record)])
        self.win.refresh()


def main(scrn):
    
    ch = CursesHandler(scrn.subwin(5,80, 19,0))
    ch.setLevel(logging.INFO)
    logging.getLogger().addHandler(ch)
    logging.getLogger().setLevel(logging.DEBUG)
    
    logging.debug("debug")
    logging.info("info")
    logging.warning("warning")
    logging.error("error")
    logging.critical("critical")
    
    win = scrn.subwin(10,80, 0,0)
    
    for i in range(0,10):
        win.addstr(i,0, str(i))
        logging.info("Now i = " + str(i))
        win.refresh()
        
    win.getch()


if __name__ == "__main__":
    curses.wrapper(main)

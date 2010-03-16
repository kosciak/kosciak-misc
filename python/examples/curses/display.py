#!/usr/bin/env python

import curses


def main(scrn):
    box = scrn.subwin(3,5, 0,0)
    box.box()
    box.addstr(1,1, "box")
    
    border = scrn.subwin(3,8, 0,6)
    border.border()
    border.addstr(1,1, "border")
    
    background = scrn.subwin(3,14, 0,15)
    background.bkgd("#")
    background.addstr(1,2, "background", curses.A_NORMAL)
    background.refresh
    
    lines = scrn.subwin(3,11, 0,30)
    lines.hline(1,0, curses.ACS_HLINE, 11)
    lines.vline(0,2, curses.ACS_VLINE, 3)
    lines.vline(0,8, curses.ACS_VLINE, 3)
    lines.addstr(0,3, "lines")
    lines.addch(1,2, curses.ACS_SSSS)
    lines.addch(1,8, curses.ACS_SSSS)
    
    text = scrn.subwin(7,9, 3,0)
    text.addstr(0,0, "dim", curses.A_DIM)
    text.addstr(1,0, "normal", curses.A_NORMAL)
    text.addstr(2,0, "underline", curses.A_UNDERLINE)
    text.addstr(3,0, "bold", curses.A_BOLD)
    text.addstr(4,0, "standout", curses.A_STANDOUT)
    text.addstr(5,0, "blink", curses.A_BLINK)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    text.move(6,0)
    text.addch("c", curses.color_pair(1) | curses.A_BOLD)
    text.addch("o", curses.color_pair(2) | curses.A_BOLD)
    text.addch("l", curses.color_pair(3) | curses.A_BOLD)
    text.addch("o", curses.color_pair(2) | curses.A_BOLD)
    text.addch("r", curses.color_pair(1) | curses.A_BOLD)
    
    scrn.addstr(11,0, curses.termname())
    scrn.addstr(": " + curses.longname())
    
    scrn.getch()
    curses.flash()
    scrn.getch()



if __name__ == "__main__":
    curses.wrapper(main)

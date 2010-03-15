#!/usr/bin/env python

import curses


def main(scrn):
    curses.init_pair(1,curses.COLOR_RED,curses.COLOR_BLACK)     # 1
    curses.init_pair(2,curses.COLOR_GREEN,curses.COLOR_BLACK)     # 1
    for i in range(32, 256):
        scrn.addstr(str(i) + ": ", curses.color_pair(2))
        scrn.addstr(chr(i))
        scrn.addstr(chr(i), curses.A_ALTCHARSET | curses.color_pair(1))
        scrn.addch(32)
    
    scrn.getch()


if __name__ == "__main__":
    curses.wrapper(main)

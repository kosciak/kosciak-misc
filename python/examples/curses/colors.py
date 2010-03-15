#!/usr/bin/env python

import curses


def init_color_pairs():
    for background in range(0,8):
        for foreground in range(0,8):
            if foreground == 0:
                pair = 7|background<<3
            elif foreground == 7:
                pair = 0|background<<3
            else:
                pair = foreground|background<<3
            if pair != 0:
                curses.init_pair(pair, foreground, background)

def main(scrn):
    init_color_pairs()
    
    for background in range(0,8):
        scrn.move(background, 0)
        for foreground in range(0,8):
            scrn.addstr("##", curses.color_pair(foreground|background<<3))
            scrn.addstr("##", curses.color_pair(foreground|background<<3) | curses.A_BOLD)
        scrn.move(background+9, 0)
        for foreground in range(0,8):
            scrn.addstr("##", curses.color_pair(foreground|background<<3) | curses.A_STANDOUT)
            scrn.addstr("##", curses.color_pair(foreground|background<<3) | curses.A_BOLD | curses.A_STANDOUT)
            
    scrn.getch()


if __name__ == "__main__":
    curses.wrapper(main)

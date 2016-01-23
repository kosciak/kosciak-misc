# Introduction #

When using Firefox flash objects steal the focus and keyboard input. If you are used to keyboard shortcuts (or use excellent [Vimperator](http://vimperator.org/vimperator) extension) it can be real pain in the ass. The script simulates mouse click in the upper-left corner of the window so you can get focus out of the flash object back to the browser.


# Download #

Script can be found in the SVN repository: http://code.google.com/p/kosciak-misc/source/browse/bash/escape_flash.sh


# Requirements #

You need [xdotool](http://www.semicomplete.com/projects/xdotool/) (I was using version 20080720-1 from Ubuntu Intrepid repository) and x11-utils package (for xwininfo to work).

Script was tested in GNOME window Manager


# Usage #

Download the script and set the keyboard shortcut to run it.

If you are using Compiz run Compiz Config Settings Manager → go to _General Settings_ → _Commands_ tab → set path to the script in _Commands_ section and set key binding in _Key bindings_ section


# Changelog #

0.1
  * initial release
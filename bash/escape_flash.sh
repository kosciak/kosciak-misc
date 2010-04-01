#!/bin/bash

#
# author: Wojciech 'Kosciak' Pietrzok <kosciak@kosciak.net>
# version: 0.1
#

# Get current window's ID
wid=$(xdotool getactivewindow) 

# Focus window (just for sure)
xdotool windowfocus $wid 

# Get window's position
x=$(xwininfo -id $wid | grep "Absolute upper-left X")
x=$((${x:25}+1))
y=$(xwininfo -id $wid | grep "Absolute upper-left Y")
y=$((${y:25}+1))

# Get initial cursor's position
mousexy=$(xdotool getmouselocation)
mousex=$(echo $mousexy | awk '{ print $1 }')
mousey=$(echo $mousexy | awk '{ print $2 }')

# Move cursor to upper-left corner of the window and click
xdotool mousemove $x $y
xdotool click 1

# Move cursor back to the initial position
xdotool mousemove ${mousex:2} ${mousey:2}

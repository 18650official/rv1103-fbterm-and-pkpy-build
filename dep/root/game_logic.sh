#!/bin/sh

# ==========================================================
# == Main Boot Tasks (Will only run on the 2nd execution)
# ==========================================================
# Close the GUI launcher (Executed in father script)
# /etc/init.d/S99lvgl stop
# /etc/init.d/S99fbterm start_with_input

# Prepare to launch the game
echo "Starting Main Boot Tasks..."
sleep 0.3

# 1. Auto update
# The output is redirected to /dev/console to be visible on the LCD screen.
/usr/local/bin/copy_file.sh
# Show the update log
sleep 2

# 2. Start Color test
/usr/bin/color_test_c
# Show color test information
sleep 2
clear

# 3. Game
echo "Start game file..."

# Stuck process, e.g. the main game file
cd /oem/brogue-rpg
pocketpy ./main.py
# evtest /dev/input/event1
# stdio_test

# Exit the son-script, and wait to restart the GUI
echo "Game program exited..."
sleep 2
cd $HOME
exit 0

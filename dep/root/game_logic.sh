#!/bin/sh

# ==========================================================
# == Main Launcher Script (term_start_all.sh)
# == Launched by LVGL (non-TTY)
# ==========================================================

# 1. Stop LVGL (this frees /dev/input/event1)
/etc/init.d/S99lvgl stop

# 2. Unbind vtcon1 (clean up tty1)
if [ -e /sys/class/vtconsole/vtcon1/bind ]; then
     echo 0 > /sys/class/vtconsole/vtcon1/bind 2>/dev/null
fi
# Switch to tty1 to ensure fbterm binds to the foreground screen
chvt 1
usleep 100000

# 3. --- Core: Launch FBTERM the correct way ---
#
# setsid: Create a new session, detached from LVGL
# sh -c: Run a shell
# exec fbterm: Replace the shell with fbterm
# -- /root/game_logic.sh: Tell fbterm what program to run after starting
# </dev/tty1 >/dev/tty1 2>&1: Bind fbterm's own I/O to tty1
#
# This command will "block" until fbterm and game_logic.sh have exited.
setsid sh -c "exec fbterm -- /root/game_logic.sh </dev/tty1 >/dev/tty1 2>&1"

# 4. --- Flow has returned ---
# game_logic.sh has exited, fbterm has exited.
echo "fbterm session finished. Restoring TTY1..."

# 5. Restore tty1
if [ -e /sys/class/vtconsole/vtcon1/bind ]; then
     echo 1 > /sys/class/vtconsole/vtcon1/bind 2>/dev/null
fi

# 6. Restart LVGL
/etc/init.d/S99lvgl start

exit 0
[root@luckfox ]# cat root/game_logic.sh
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

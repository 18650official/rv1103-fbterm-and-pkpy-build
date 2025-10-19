#!/bin/sh

# ==========================================================
# == Execution Guard
# ==========================================================
# This script should only run during the initial system boot on the main console,
# not in remote login shells like ADB (which typically use /dev/pts/*).
# The 'tty' command identifies the current terminal.

case "$(tty 2>/dev/null)" in
    /dev/pts/*)
        # This is an ADB or other remote pseudo-terminal. Exit silently.
        exit 0
        ;;
    *)
        # This is a console TTY, proceed with the boot tasks.
        ;;
esac

# ==========================================================
# == Original Boot Tasks
# ==========================================================
clear > /dev/console
echo "Starting..." > /dev/console
sleep 1.5

# 1. Auto update
# The output is redirected to /dev/console to be visible on the LCD screen.
/usr/local/bin/copy_file.sh > /dev/console

# 2. Start Color test
sleep 1
clear > /dev/console
/usr/bin/color_test_c > /dev/console

# 3. Game
echo "Start game file..." > /dev/console

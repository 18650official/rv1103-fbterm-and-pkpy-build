#!/bin/sh

# ===================================================
#  Miku's Emoji Transparency (Color Keying) Final Test
# ===================================================
# This script will verify if the emoji renderer correctly handles
# transparency on a non-black background.

printf "\n--- Emoji Transparency Final Test ---\n\n"
sleep 1

# --- Test 1: Cat on a Blue Background ---
# We will set a bright blue background (ANSI code 104) for the whole line.
printf "Cat on a BLUE background:\n"
printf "\x1b[104m This line has a blue background >^.^< and a cat emoji -> 😺 <- inside! \x1b[0m\n\n"
sleep 1

# --- Test 2: Thumb on a Green Background ---
printf "Thumbs up on a GREEN background:\n"
# Set background to green (code 42)
printf "\x1b[42m This is a test -> 👍 <- on a green background. \x1b[0m\n\n"
sleep 1


printf "--- Test Complete ---\n\n"
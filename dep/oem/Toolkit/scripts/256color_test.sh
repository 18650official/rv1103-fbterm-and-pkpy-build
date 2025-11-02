#!/bin/sh

# ===================================================
#  16 & 256 Color ANSI Terminal Test Script
#  Uses standard xterm escape sequences.
# ===================================================

# --- 16 Colors ---
printf "\n--- 16 ANSI Colors ---\n"
# Standard foreground colors (30-37)
printf "FG: "
for i in $(seq 30 37); do
    printf "\x1b[%sm %s \x1b[0m" "$i" "$i"
done
printf "\n"

# Bright foreground colors (1;30-37 or 90-97)
printf "    "
for i in $(seq 30 37); do
    printf "\x1b[1;%sm %s \x1b[0m" "$i" "$((i+60))" # Show the 9x code
done
printf "\n\n"

# Standard background colors (40-47)
printf "BG: "
for i in $(seq 40 47); do
    printf "\x1b[%sm %s \x1b[0m" "$i" "$i"
done
printf "\n"

# Bright background colors (100-107)
printf "    "
for i in $(seq 100 107); do
    printf "\x1b[%sm %s \x1b[0m" "$i" "$i"
done
printf "\n"


# --- 256 Colors ---

# Helper to print a 256-color swatch
# We'll print the color code on a background of that color.
print_256_swatch() {
    code=$1
    # Use black text for light colors, white for dark colors for readability
    if [ "$code" -ge 244 ] || { [ "$code" -ge 10 ] && [ "$code" -le 14 ]; } || [ "$code" -ge 142 ] && { [ "$code" -le 159 ] || [ "$code" -ge 178 ]; }; then
        fg_color=0 # Black
    else
        fg_color=15 # White
    fi
    printf "\x1b[48;5;%sm\x1b[38;5;%sm %3d \x1b[0m" "$code" "$fg_color" "$code"
}

# System Colors (0-15) as part of the 256-color palette
printf "\n\n--- 256 ANSI Colors ---\n"
printf "System Colors (0-15):\n"
for i in $(seq 0 15); do
    print_256_swatch "$i"
    if [ "$i" = 7 ]; then
        printf "\n"
    fi
done
printf "\n"

# 6x6x6 Color Cube (16-231)
printf "\nColor Cube (16-231):\n"
for i in $(seq 16 231); do
    print_256_swatch "$i"
    # Create rows of 6 for the cube effect
    if [ $((($i - 16) % 6)) -eq 5 ]; then
        printf "\n"
        # Add an extra newline every 36 colors (end of a cube face)
        if [ $((($i - 16) % 36)) -eq 35 ]; then
            printf "\n"
        fi
    fi
done

# Grayscale Ramp (232-255)
printf "\nGrayscale Ramp (232-255):\n"
for i in $(seq 232 255); do
    print_256_swatch "$i"
done
printf "\n\nTest Complete.\n"

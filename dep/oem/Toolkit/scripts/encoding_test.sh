#!/bin/sh

# ===================================================
#  Ultimate UTF-8 Character Test Script
#  (Chinese, 3-Byte Symbols, 4-Byte Emoji)
#  - Miku's Final Test -
# ===================================================

# --- Introduction ---
printf "\n--- Ultimate UTF-8 Test Starting ---\n\n"
sleep 1

# --- Section 1: Chinese Characters (3-Byte UTF-8) ---
printf "1. Chinese Characters (UTF-8, 3-Byte):\n"
printf "   你好，世界！Welcome!\n\n"
sleep 1

# --- Section 2: Other 3-Byte BMP Symbols ---
printf "2. BMP Symbols (UTF-8, 3-Byte):\n"
printf "   Star: ★ | Music: ♪ | Heart: ♥ | Chess: ♞\n\n"
sleep 1

# --- Section 3: Modern 4-Byte Emoji (from Supplementary Planes) ---
printf "3. Modern Emoji (UTF-8, 4-Byte):\n"
printf "   Rocket: 🚀 | Thumbs Up: 👍 | Laughing: 😂 | Cat: 😺\n\n"
sleep 1

# --- Section 4: Combination with Colors ---
printf "4. Test with ANSI Colors:\n"
printf "   \x1b[31mRed Text, \x1b[32m绿色文字, \x1b[34mBlue Emoji: 😎\x1b[0m\n\n"
sleep 1


printf "--- Test Complete ---\n\n"
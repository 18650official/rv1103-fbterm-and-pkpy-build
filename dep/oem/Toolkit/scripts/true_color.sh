#!/bin/sh

# ===================================================
#  24-bit True Color (RGB) ANSI Test Script
# ===================================================

# 一个小函数，用来打印带特定RGB背景色的文字
# 用法: print_block <R> <G> <B> "要显示的文字"
print_block() {
    R=$1
    G=$2
    B=$3
    TEXT=$4
    # 设置背景色为 R;G;B，前景色为亮白色，打印文字，然后重置
    printf "\x1b[48;2;%s;%s;%sm\x1b[38;2;255;255;255m %s \x1b[0m" "$R" "$G" "$B" "$TEXT"
}

printf "\n--- 24-bit True Color Test ---\n\n"
sleep 1

# --- 两个单色 ---
printf "Solid Colors:\n"
print_block 60 120 255 "--Blue--"
printf "\n"
# sleep 1
# printf "\n"
# sleep 1
print_block 255 165 1 "--Orange--"
printf "\n\n"
sleep 1

# --- 一个渐变色 ---
printf "Gradient (Blue to Cyan):\n"
# 我们将 R 固定为0, B 固定为255, 让 G 从 0 变化到 255
# seq 0 10 255 的意思是：从0开始，每次加10，直到255
for G_VAL in $(seq 0 10 255); do
    # 打印一个空格作为渐变色块的一个像素点
    printf "\x1b[48;2;0;%s;255m \x1b[0m" "$G_VAL"
done
printf "\n\n"
sleep 1

printf "Test Complete.\n\n"

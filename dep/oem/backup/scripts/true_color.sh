#!/bin/sh

# ===================================================
#  24-bit True Color (RGB) ANSI Test Script
# ===================================================

# һ��С������������ӡ���ض�RGB����ɫ������
# �÷�: print_block <R> <G> <B> "Ҫ��ʾ������"
print_block() {
    R=$1
    G=$2
    B=$3
    TEXT=$4
    # ���ñ���ɫΪ R;G;B��ǰ��ɫΪ����ɫ����ӡ���֣�Ȼ������
    printf "\x1b[48;2;%s;%s;%sm\x1b[38;2;255;255;255m %s \x1b[0m" "$R" "$G" "$B" "$TEXT"
}

printf "\n--- 24-bit True Color Test ---\n\n"
sleep 1

# --- ������ɫ ---
printf "Solid Colors:\n"
print_block 60 120 255 "--Blue--"
printf "\n"
# sleep 1
# printf "\n"
# sleep 1
print_block 255 165 1 "--Orange--"
printf "\n\n"
sleep 1

# --- һ������ɫ ---
printf "Gradient (Blue to Cyan):\n"
# ���ǽ� R �̶�Ϊ0, B �̶�Ϊ255, �� G �� 0 �仯�� 255
# seq 0 10 255 ����˼�ǣ���0��ʼ��ÿ�μ�10��ֱ��255
for G_VAL in $(seq 0 10 255); do
    # ��ӡһ���ո���Ϊ����ɫ���һ�����ص�
    printf "\x1b[48;2;0;%s;255m \x1b[0m" "$G_VAL"
done
printf "\n\n"
sleep 1

printf "Test Complete.\n\n"

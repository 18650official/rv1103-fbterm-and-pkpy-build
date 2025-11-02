#!/bin/sh

# 脚本名称: /root/nes_start.sh
# 用途: 停止LVGL, 运行NES模拟器, 然后重启LVGL

# 1. 从第一个参数获取游戏文件的绝对路径
GAME_PATH="$1"

# 2. 检查路径是否为空
if [ -z "$GAME_PATH" ]; then
    # 如果为空，向内核日志输出错误 (你可以通过 dmesg 查看)
    echo "nes_start.sh: Error - No game path provided." > /dev/kmsg
    exit 1
fi

# 3. 停止 LVGL 进程
sleep 0.5
echo "nes_start.sh: Stopping LVGL..." > /dev/kmsg
/etc/init.d/S99lvgl stop

# (可选) 短暂暂停，确保进程完全退出
sleep 0.1

# 4. 运行你的NES模拟器
# 这一步是 *阻塞* 的。脚本会在这里等待，直到 nesemu_rv1103 进程退出
echo "nes_start.sh: Starting game: $GAME_PATH" > /dev/kmsg
echo "Executed command:"
echo "/usr/bin/nesemu_rv1103 $GAME_PATH"
/bin/sh -c "/usr/bin/nesemu_rv1103 $GAME_PATH"

# 5. 当游戏结束后 (nesemu_rv1103 退出), 重启 LVGL
echo "nes_start.sh: Game exited. Restarting LVGL." > /dev/kmsg
/etc/init.d/S99lvgl restart


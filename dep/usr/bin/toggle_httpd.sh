#!/bin/sh

# 定义 busybox httpd 可执行文件
HTTPD_EXEC="/bin/busybox"

# 定义 RNDIS 网卡的 IP 地址
RNDIS_IP="172.32.0.93"
PORT="80"

# 定义 httpd 的参数
# -h /var/www   = 指定网页根目录 (index.html 在这里)
# -f            = 在前台运行 (start-stop-daemon 会负责将其转入后台)
# -p IP:PORT    = 绑定到指定的 IP 和端口 (这是根据您的 help-text 修正的)
HTTPD_ARGS="httpd -f -h /var/www -p ${RNDIS_IP}:${PORT}"

# PID 文件的标准路径，用于跟踪进程
PID_FILE="/var/run/httpd.pid"

# 脚本的核心逻辑
case "$1" in
    start)
        echo "Starting web server on ${RNDIS_IP}:${PORT}..."
        
        if [ -e $PID_FILE ]; then
            echo "Web server is already running (PID: $(cat $PID_FILE))."
            exit 1
        fi

        # 使用 start-stop-daemon 启动进程
        start-stop-daemon --start --quiet --background \
            --pidfile $PID_FILE --make-pidfile \
            --exec $HTTPD_EXEC -- $HTTPD_ARGS
        
        if [ $? -eq 0 ]; then
            echo "Web server started successfully."
            echo "Access at: http://${RNDIS_IP}"
        else
            echo "Error: Web server failed to start."
            # 启动失败时清除残留的 pid 文件
            rm -f $PID_FILE
        fi
        ;;
        
    stop)
        echo "Stopping web server..."
        
        start-stop-daemon --stop --quiet --pidfile $PID_FILE
        
        if [ $? -eq 0 ]; then
            rm -f $PID_FILE
            echo "Web server stopped."
        else
            echo "Web server could not be stopped (or was not running)."
            rm -f $PID_FILE
        fi
        ;;
        
    restart)
        $0 stop
        sleep 1
        $0 start
        ;;
        
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
        ;;
esac

exit 0



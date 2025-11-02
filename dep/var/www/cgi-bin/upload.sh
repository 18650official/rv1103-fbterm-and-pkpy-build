#!/bin/sh

# CGI 脚本必须先输出一个 HTTP 头部！
echo "Content-Type: text/plain"
echo "" # 头部结束的空行

echo "Start update service..."
echo "Receiving TAR file..."

# 1. 定义临时文件路径
UPLOAD_FILE_DIRTY="/tmp/firmware_upload_dirty.tar"
UPLOAD_FILE_CLEAN="/tmp/firmware_fixed.tar"

# 2. 接收被污染的文件
cat > $UPLOAD_FILE_DIRTY

if [ ! -s "$UPLOAD_FILE_DIRTY" ]; then
    echo "[ERROR] File not exist or empty!"
    exit 1
fi

echo "Received: $UPLOAD_FILE_DIRTY"
echo "Size: $(ls -lh $UPLOAD_FILE_DIRTY | awk '{print $5}')"
echo "-----------------------------------"
echo "Cleaning uploaded file..."

# 3. 【新步骤】调用 Python 脚本进行清洗
# 假设你的 python 解释器在 /usr/bin/python
/usr/bin/python /usr/local/bin/fix_upload.py $UPLOAD_FILE_DIRTY $UPLOAD_FILE_CLEAN

# 检查清洗是否成功
if [ $? -ne 0 ] || [ ! -s "$UPLOAD_FILE_CLEAN" ]; then
    echo "[ERROR] Python script failed to clean the file!"
    rm -f $UPLOAD_FILE_DIRTY
    exit 1
fi

echo "File cleaned successfully."
echo "-----------------------------------"
echo "Updating..."

# 4. 【重要】让 ota.sh 使用 *干净的* 文件
/usr/local/bin/ota.sh $UPLOAD_FILE_CLEAN

echo "Cleaning temp files..."
rm -f $UPLOAD_FILE_DIRTY
rm -f $UPLOAD_FILE_CLEAN

echo "All update finished!"
echo "Device will restart in 5 seconds."
sleep 5

# 安全重启
reboot
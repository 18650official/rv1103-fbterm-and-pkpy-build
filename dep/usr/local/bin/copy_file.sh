IMAGE_FILE="/root/mass.img"
MOUNT_POINT="/mnt/mass"
UPDATE_FILE="update.tar"

# 2. Mount the image file to the filesystem for read/write access
echo "Mounting image file for read access..."
# Release loop device
losetup -d /dev/loop0
losetup /dev/loop0 $IMAGE_FILE
mkdir -p "$MOUNT_POINT"
mount -t vfat /dev/loop0 "$MOUNT_POINT"

# Check if mounting was successful
if [ $? -ne 0 ]; then
    echo "Error: Failed to mount image file. Exiting."
    exit 1
fi

# 3. Copy the update file if it exists
if [ -f "$MOUNT_POINT/$UPDATE_FILE" ]; then
    echo "Found update file. Copying to internal storage..."
    rm -rf /oem/update
    mkdir -p /oem/update
    cp "$MOUNT_POINT/$UPDATE_FILE" "/oem/update"

    if [ $? -eq 0 ]; then
        echo "File copied successfully. Starting update..."
        # Add your post-copying logic here, e.g., decompressing, installing, etc.
        tar xvf /oem/update/$UPDATE_FILE -C /oem/update/
        rm /oem/update/$UPDATE_FILE 
        echo "Update file unpacked!"
    else
        echo "Error: Failed to copy file."
    fi
else
    echo "No update file '$UPDATE_FILE' found on U-disk."
fi

# 4. Unmount the image file
echo "Unmounting image file..."
umount "$MOUNT_POINT"
if [ $? -ne 0 ]; then
    echo "Error: Failed to unmount image file."
else
    rmdir "$MOUNT_POINT"
fi

# 5.Execute the update-script
echo "Excuting..."
/oem/update/meta.sh
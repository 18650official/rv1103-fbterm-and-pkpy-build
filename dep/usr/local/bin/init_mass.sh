#!/bin/sh

GADGET_DIR="/sys/kernel/config/usb_gadget/rockchip"
MASS_FUNCTION_DIR="$GADGET_DIR/functions/mass_storage.0"
CONFIG_DIR="$GADGET_DIR/configs/b.1"
IMAGE_FILE="/root/mass.img"

if [ ! -d "$MASS_FUNCTION_DIR" ]; then
    echo "Error: 'mass_storage.0' function not found."
    exit 1
fi

if [ ! -f "$IMAGE_FILE" ]; then
    echo "Error: Image file '$IMAGE_FILE' not found."
    exit 1
fi

echo "Configuring mass_storage function for 'rockchip' gadget..."

echo "$IMAGE_FILE" > "$MASS_FUNCTION_DIR/lun.0/file"

if [ ! -L "$CONFIG_DIR/mass_storage.0" ]; then
    echo "Creating symbolic link to mass_storage.0..."
    ln -s "$MASS_FUNCTION_DIR" "$CONFIG_DIR/"
fi

UDC_NAME=$(cat "$GADGET_DIR/UDC")
if [ -n "$UDC_NAME" ]; then
    echo "Rebinding UDC to apply changes..."
    echo "" > "$GADGET_DIR/UDC"
    echo "$UDC_NAME" > "$GADGET_DIR/UDC"
fi

echo "Mass storage image configured successfully."
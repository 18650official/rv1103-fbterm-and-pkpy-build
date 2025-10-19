#!/bin/bash

# =================================================================
# Luckfox Pico Project Deployment Package Generation Script (v3 - with auto permissions)
#
# This script performs the following actions:
# 1. Creates a temporary root filesystem directory.
# 2. Merges the contents of the 'dep' and 'output' directories into it.
# 3. Intelligently sets +x permissions for all executables and scripts before packaging.
# 4. Packages the temporary directory into an 'update.tar' file that preserves permissions.
# 5. Generates a smart installation script 'install.sh' with permission checks to be run on the target device.
# 6. Places the final artifacts into the 'install/' directory.
# =================================================================

set -eu

# --- Variable Definitions ---
BUILD_DIR=$(pwd)
OUTPUT_DIR="${BUILD_DIR}/output"
DEP_DIR="${BUILD_DIR}/dep"
PACKAGE_DIR="${BUILD_DIR}/install"
PACKAGE_ROOT="${BUILD_DIR}/package_root" # Temporary directory for merging files
TAR_FILE="${PACKAGE_DIR}/update.tar"
INSTALL_SCRIPT="${PACKAGE_DIR}/install.sh"

# --- Check if source directories exist ---
if [ ! -d "${OUTPUT_DIR}" ]; then
    echo "Error: 'output' directory not found. Please run the build script first."
    exit 1
fi
if [ ! -d "${DEP_DIR}" ]; then
    echo "Error: 'dep' directory not found."
    exit 1
fi


# --- 1. Clean and create packaging directories ---
echo "====== 1. Preparing packaging environment... ======"
rm -rf "${PACKAGE_ROOT}" "${PACKAGE_DIR}"
mkdir -p "${PACKAGE_ROOT}"
mkdir -p "${PACKAGE_DIR}"
echo "Temporary directory '${PACKAGE_ROOT}' and output directory '${PACKAGE_DIR}' are ready."
echo ""


# --- 2. Merge files ---
echo "====== 2. Merging 'dep' and 'output' directories... ======"
rsync -a "${DEP_DIR}/" "${PACKAGE_ROOT}/"
rsync -a "${OUTPUT_DIR}/" "${PACKAGE_ROOT}/"
echo "File merge complete."
echo ""


# --- 3. Pre-set file permissions before packaging ---
echo "====== 3. Pre-setting executable permissions... ======"
# Grant executable permissions to our main compiled programs
chmod +x "${PACKAGE_ROOT}/usr/bin/fbterm"
chmod +x "${PACKAGE_ROOT}/usr/bin/pocketpy"
chmod +x "${PACKAGE_ROOT}/usr/bin/fc-"*

# Recursively find all .sh scripts and grant them executable permissions
find "${PACKAGE_ROOT}" -type f -name "*.sh" -exec chmod +x {} \;
echo "Permissions pre-set."
echo ""


# --- 4. Package into a Tar file ---
echo "====== 4. Packaging merged files into ${TAR_FILE}... ======"
# Use the -p flag to ensure file permissions are fully preserved
tar -cpf "${TAR_FILE}" -C "${PACKAGE_ROOT}" .
echo "Packaging complete."
echo ""


# --- 5. Clean up temporary directory ---
echo "====== 5. Cleaning up temporary files... ======"
rm -rf "${PACKAGE_ROOT}"
echo "Cleanup complete."
echo ""


# --- 6. Generate one-click installation script (install.sh) ---
echo "====== 6. Generating target device installation script (install.sh)... ======"
cat << 'EOF' > "${INSTALL_SCRIPT}"
#!/bin/sh
# =================================================
# System Update & Setup Script (v2)
# To be executed on the target device.
# =================================================
set -e

# --- Configuration ---
SWAPFILE_PATH="/root/swapfile"
SWAPFILE_SIZE_MB=128
DISK_IMG_PATH="/root/mass.img"
DISK_IMG_SIZE_MB=64

echo "====== Starting System Update & Setup ======"

if [ ! -f "update.tar" ]; then
    echo "Error: update.tar not found! Please place this script in the same directory as update.tar."
    exit 1
fi

# 1. Special handling for specified /etc subdirectories
echo "--> Preparing /etc directories..."
rm -rf /etc/init.d
rm -rf /etc/profile.d
echo "Old /etc directories removed."

# 2. Extract the archive to the root filesystem
echo "--> Extracting update.tar to root filesystem (preserving permissions)..."
# Use the -p flag to ensure permissions are restored from the archive
tar -xpf update.tar -C /
echo "Extraction complete."

# 3. Failsafe: Ensure all shell scripts are executable
echo "--> Verifying executable permissions for shell scripts..."
# Iterate through key directories and ensure +x permission for all .sh files again
find /etc /oem /root /usr -type f -name "*.sh" -exec chmod +x {} \; 2>/dev/null || true
echo "Permissions verified."

# 4. Check for and create swapfile if it doesn't exist
echo "--> Checking for swapfile at ${SWAPFILE_PATH}..."
if [ ! -f "${SWAPFILE_PATH}" ]; then
    echo "Swapfile not found. Creating a ${SWAPFILE_SIZE_MB}MB swapfile..."
    dd if=/dev/zero of="${SWAPFILE_PATH}" bs=1M count=${SWAPFILE_SIZE_MB}
    chmod 600 "${SWAPFILE_PATH}"
    mkswap "${SWAPFILE_PATH}"
    echo "Swapfile created successfully."
    echo "NOTE: To activate it on boot, add '/root/swapfile none swap sw 0 0' to /etc/fstab."
else
    echo "Swapfile already exists. Skipping creation."
fi

# 5. Check for and create mass storage image if it doesn't exist
echo "--> Checking for disk image at ${DISK_IMG_PATH}..."
if [ ! -f "${DISK_IMG_PATH}" ]; then
    echo "Disk image not found. Creating a ${DISK_IMG_SIZE_MB}MB image..."
    dd if=/dev/zero of="${DISK_IMG_PATH}" bs=1M count=${DISK_IMG_SIZE_MB}
    mkfs.fat "${DISK_IMG_PATH}"
    echo "Disk image created and formatted as FAT successfully."
else
    echo "Disk image already exists. Skipping creation."
fi

# 6. Cleanup
echo "--> Cleaning up installation files..."
rm update.tar
echo "Update process finished! This script will now self-destruct."
rm -- "$0"

echo "====== System Update & Setup Complete! A reboot is recommended. ======"
EOF

chmod +x "${INSTALL_SCRIPT}"
echo "Installation script 'install.sh' generated."
echo ""


# --- 7. Print final deployment instructions ---
echo "================================================================="
echo "✅ Deployment package created successfully!"
echo ""
echo "Next, please follow these steps to deploy on your Luckfox Pico board:"
echo ""
echo "1. Upload all files from the 'install' directory (update.tar and install.sh) to a temporary directory on the board (e.g., /tmp) using scp or another method:"
echo ""
echo "   Example scp command (please replace <board_ip> with the board's actual IP):"
echo "   scp install/* root@<board_ip>:/tmp/"
echo ""
echo "2. SSH into your board, then execute the following commands:"
echo "   cd /tmp"
echo "   ./install.sh"
echo ""
echo "3. The script will automatically handle all deployment tasks and clean up after itself. A reboot is recommended upon completion."
echo "================================================================="

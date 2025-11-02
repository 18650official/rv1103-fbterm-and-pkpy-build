#!/bin/sh

# 1. Get the update file path from the command line argument
SOURCE_UPDATE_FILE="$1"
UPDATE_DIR="/oem/update"

# Check if the argument is provided
if [ -z "$SOURCE_UPDATE_FILE" ]; then
    echo "Error: No update file path provided."
    echo "Usage: $0 /path/to/update.tar"
    exit 1
fi

# Check if the file exists
if [ ! -f "$SOURCE_UPDATE_FILE" ]; then
    echo "Error: File not found: $SOURCE_UPDATE_FILE"
    exit 1
fi

# 2. Prepare the update directory and copy the file
echo "Found update file: $SOURCE_UPDATE_FILE"
echo "Copying to internal storage..."
rm -rf "$UPDATE_DIR"
mkdir -p "$UPDATE_DIR"

# Extract the filename from the source path
UPDATE_FILENAME=$(basename "$SOURCE_UPDATE_FILE")

cp "$SOURCE_UPDATE_FILE" "$UPDATE_DIR/$UPDATE_FILENAME"

# 3. Check copy success, then extract and clean up
if [ $? -eq 0 ]; then
    echo "File copied successfully. Starting update..."

    # Extract the archive
    echo "Attempting to extract $UPDATE_DIR/$UPDATE_FILENAME ..."
    
    # Capture STDOUT and STDERR to a variable
    TAR_OUTPUT=$(/bin/tar xvf "$UPDATE_DIR/$UPDATE_FILENAME" -C "$UPDATE_DIR/" 2>&1)
    TAR_EXIT_CODE=$? # Save the exit code immediately

    echo "--- Begin tar command output (stdout + stderr) ---"
    echo "$TAR_OUTPUT"
    echo "--- End tar command output (exit code: $TAR_EXIT_CODE) ---"

    # Check if extraction was successful
    if [ $TAR_EXIT_CODE -ne 0 ]; then
        echo "Error: Failed to extract $UPDATE_FILENAME."
        exit 1
    fi

    # Remove the original tar file
    rm "$UPDATE_DIR/$UPDATE_FILENAME"
    echo "Update file unpacked!"
else
    echo "Error: Failed to copy file."
    exit 1
fi

# 4. Execute the update script
if [ -f "$UPDATE_DIR/meta.sh" ]; then
    echo "Executing update script..."
    chmod +x "$UPDATE_DIR/meta.sh" # Ensure the script is executable
    "$UPDATE_DIR/meta.sh"
    echo "Update script execution finished."
else
    echo "Error: 'meta.sh' script not found in the package."
    exit 1
fi

echo "Update process finished."

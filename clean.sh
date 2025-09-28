#!/bin/bash

# =================================================================
# Clean Script for RV1103 FbTerm Project
#
# This script removes all generated files and directories, including:
# - Staging, output, install, and toolchain directories
# - Build artifacts inside each source directory (e.g., pocketpy/build)
# =================================================================

set -e

echo "====== Starting project cleanup... ======"

# 1. Remove top-level generated directories and files
echo "--> Removing top-level build artifacts..."
rm -rf staging
rm -rf output
rm -rf install
rm -rf luckfox_toolchain
rm -rf build_temp
rm -f toolchain.cmake
echo "Top-level directories and files removed."

# 2. Clean Autotools-based projects
AUTOTOOLS_DIRS="zlib-1.3.1 expat-2.7.1 libiconv-1.7 freetype-2.10.0 fontconfig-2.16.0 fbterm-truecolor"
echo ""
echo "--> Cleaning individual Autotools project directories..."
for dir in $AUTOTOOLS_DIRS; do
  if [ -d "$dir" ]; then
    echo "  - Cleaning $dir"
    # Use a subshell to avoid manually changing back
    # The '|| true' prevents the script from exiting if 'make clean' fails (e.g., not configured yet)
    (cd "$dir" && make clean &> /dev/null) || true
  else
    echo "  - Skipping $dir (not found)"
  fi
done
echo "Autotools projects cleaned."

# 3. Clean CMake-based projects
echo ""
echo "--> Cleaning individual CMake project directories..."
if [ -d "pocketpy/build" ]; then
  echo "  - Cleaning pocketpy"
  rm -rf "pocketpy/build"
else
  echo "  - Skipping pocketpy (build directory not found)"
fi
echo "CMake projects cleaned."

echo ""
echo "✅ Project cleanup complete!"

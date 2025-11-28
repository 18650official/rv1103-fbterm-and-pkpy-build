#!/bin/bash

# =================================================================
# Fbterm & PocketPy Full Cross-Compile Script (Final - with fbterm fix)
# =================================================================

set -eu

# =================================================================
# Part 1: Install all required dependencies on the host machine
# =================================================================
echo "====== 1.1 Installing all host dependencies (sudo password may be required) ======"
sudo apt-get update
sudo apt-get install -y \
    git ssh make gcc gcc-multilib g++-multilib module-assistant expect g++ \
    gawk texinfo libssl-dev bison flex fakeroot cmake unzip gperf autoconf \
    device-tree-compiler libncurses5-dev pkg-config bc python-is-python3 \
    openssl openssh-server openssh-client vim file cpio rsync \
    build-essential automake libtool uuid-dev wget xz-utils
echo "====== Host base dependencies installed. ======"
echo ""

# --- Final fix: Create symlinks for aclocal and automake to be compatible with fontconfig ---
echo "====== 1.2 Creating aclocal/automake compatibility symlinks... ======"
# Check if aclocal exists
if command -v aclocal &> /dev/null
then
    ACLOCAL_PATH=$(which aclocal)
    # Create aclocal-1.17 symlink
    sudo ln -sf "$ACLOCAL_PATH" /usr/bin/aclocal-1.17
    echo "Symbolic link 'aclocal-1.17' -> '${ACLOCAL_PATH}' created."
else
    echo "Warning: 'aclocal' command not found, skipping symlink creation."
fi
# Check if automake exists
if command -v automake &> /dev/null
then
    AUTOMAKE_PATH=$(which automake)
    # Create automake-1.17 symlink
    sudo ln -sf "$AUTOMAKE_PATH" /usr/bin/automake-1.17
    echo "Symbolic link 'automake-1.17' -> '${AUTOMAKE_PATH}' created."
else
    echo "Warning: 'automake' command not found, skipping symlink creation."
fi
echo ""


# =================================================================
# Part 2: Automatically download and set up the cross-compile toolchain
# =================================================================
BUILD_DIR=$(pwd)
TOOLCHAIN_PARENT_DIR="${BUILD_DIR}/luckfox_toolchain"
TOOLCHAIN_DIR="${TOOLCHAIN_PARENT_DIR}/tools/linux/toolchain/arm-rockchip830-linux-uclibcgnueabihf"
TOOLCHAIN_BIN_PATH="${TOOLCHAIN_DIR}/bin"

echo "====== 2.1 Checking cross-compile toolchain... ======"
if [ ! -d "${TOOLCHAIN_BIN_PATH}" ]; then
    echo "Toolchain not found or incomplete. Cleaning and re-cloning..."
    rm -rf "${TOOLCHAIN_PARENT_DIR}"
    echo "Cloning from Gitee (using HTTPS)..."
    git clone --depth 1 https://gitee.com/LuckfoxTECH/luckfox-pico.git "${TOOLCHAIN_PARENT_DIR}"
    echo "Toolchain cloned."
else
    echo "Toolchain verified and exists at: ${TOOLCHAIN_PARENT_DIR}"
fi
echo ""


# =================================================================
# Part 3: Automatically check and upgrade Autoconf
# =================================================================
echo "====== 3.1 Checking Autoconf version... ======"
AUTOCONF_REQUIRED_VERSION="2.71"
INSTALLED_AUTOCONF_VERSION=$(autoconf --version | head -n 1 | awk '{print $NF}' || echo "0")
LOWEST_VERSION=$(printf '%s\n' "$AUTOCONF_REQUIRED_VERSION" "$INSTALLED_AUTOCONF_VERSION" | sort -V | head -n1)

if [ "$LOWEST_VERSION" != "$AUTOCONF_REQUIRED_VERSION" ]; then
    echo "Warning: Current Autoconf version ($INSTALLED_AUTOCONF_VERSION) is too old, requires >= $AUTOCONF_REQUIRED_VERSION."
    echo "====== Automatically downloading and compiling new Autoconf 2.72 ======"
    
    TEMP_BUILD_DIR=${BUILD_DIR}/build_temp
    mkdir -p "$TEMP_BUILD_DIR"
    cd "$TEMP_BUILD_DIR"
    wget -q --show-progress https://ftp.wayne.edu/gnu/autoconf/autoconf-2.72.tar.gz
    tar -xzf autoconf-2.72.tar.gz
    cd autoconf-2.72
    echo "Configuring Autoconf..."
    ./configure --prefix=/usr/local
    echo "Compiling Autoconf..."
    make -j$(nproc)
    echo "Installing Autoconf to /usr/local/bin with sudo (password required)..."
    sudo make install
    cd ../..
    rm -rf "$TEMP_BUILD_DIR"
    hash -r
    echo "====== Autoconf upgrade complete. ======"
else
    echo "Current Autoconf version ($INSTALLED_AUTOCONF_VERSION) meets requirements, no upgrade needed."
fi
echo "Confirming final Autoconf version:"
which autoconf
autoconf --version
echo ""


# --- Core compilation environment variables ---
TOOLCHAIN_PREFIX="arm-rockchip830-linux-uclibcgnueabihf-"
TARGET_HOST="arm-linux"
INSTALL_DIR="${BUILD_DIR}/staging"

export PATH="${TOOLCHAIN_BIN_PATH}:${PATH}"
export CC="${TOOLCHAIN_PREFIX}gcc"
export CXX="${TOOLCHAIN_PREFIX}g++"
export LD="${TOOLCHAIN_PREFIX}ld"
export AR="${TOOLCHAIN_PREFIX}ar"
export AS="${TOOLCHAIN_PREFIX}as"
export NM="${TOOLCHAIN_PREFIX}nm"
export RANLIB="${TOOLCHAIN_PREFIX}ranlib"
export STRIP="${TOOLCHAIN_PREFIX}strip"
# --- UPDATED PATHS for standard staging layout ---
export PKG_CONFIG_PATH="${INSTALL_DIR}/usr/lib/pkgconfig"
export CPPFLAGS="-I${INSTALL_DIR}/usr/include"
export CXXFLAGS="-g -O2"
export LDFLAGS="-L${INSTALL_DIR}/usr/lib"
# --- END UPDATE ---


# =================================================================
# Part 4: Automatically generate CMake toolchain file
# =================================================================
echo "====== 4.1 Generating CMake toolchain file (toolchain.cmake)... ======"
TOOLCHAIN_CMAKE_FILE="${BUILD_DIR}/toolchain.cmake"
TOOLCHAIN_SYSROOT="${TOOLCHAIN_DIR}/arm-rockchip830-linux-uclibcgnueabihf/sysroot"

cat > "${TOOLCHAIN_CMAKE_FILE}" << EOF
# CMake arm-linux Cross-Compile Toolchain File
set(CMAKE_SYSTEM_NAME Linux)
set(CMAKE_SYSTEM_PROCESSOR arm)
set(CMAKE_C_COMPILER   "${CC}")
set(CMAKE_CXX_COMPILER "${CXX}")
set(CMAKE_SYSROOT "${TOOLCHAIN_SYSROOT}")
set(CMAKE_FIND_ROOT_PATH "${INSTALL_DIR}" "\${CMAKE_SYSROOT}")
set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)
EOF
echo "====== CMake toolchain file generated. ======"
echo ""


# =================================================================
# Part 5: Compile all dependencies and main programs in order
# =================================================================
rm -rf "${INSTALL_DIR}"
mkdir -p "${INSTALL_DIR}"

echo "================================================================="
echo "Cross-compile environment is set:"
echo "  - Install directory: ${INSTALL_DIR}"
echo "  - C Compiler: $(which ${CC})"
echo "================================================================="

# --- Compile zlib ---
echo ""
echo "======== 5.1 Compiling zlib-1.3.1 ========"
cd "${BUILD_DIR}/zlib-1.3.1"
make clean &> /dev/null || true
# --- UPDATED: Use standard prefix and DESTDIR ---
./configure --prefix=/usr --static
make -j$(nproc)
make install DESTDIR="${INSTALL_DIR}"
cd "${BUILD_DIR}"
echo "======== zlib compilation finished. ========"

# --- Compile expat ---
echo ""
echo "======== 5.2 Compiling expat-2.7.1 ========"
cd "${BUILD_DIR}/expat-2.7.1"
make clean &> /dev/null || true
# --- UPDATED: Add --disable-docs to skip building documentation ---
./configure --prefix=/usr \
            --host="${TARGET_HOST}" \
            --enable-static \
            --disable-shared \
            --without-docbook \
            --disable-docs
make -j$(nproc) SUBDIRS="lib xmlwf"
make install DESTDIR="${INSTALL_DIR}" SUBDIRS="lib xmlwf"
cd "${BUILD_DIR}"
echo "======== expat compilation finished. ========"

# --- Compile libiconv ---
echo ""
echo "======== 5.3 Compiling libiconv-1.7 ========"
cd "${BUILD_DIR}/libiconv-1.7"
make clean &> /dev/null || true
# --- UPDATED: Use standard prefix and DESTDIR ---
./configure --prefix=/usr --host="${TARGET_HOST}" --enable-static --disable-shared
make -j$(nproc)
make install DESTDIR="${INSTALL_DIR}"
cd "${BUILD_DIR}"
echo "======== libiconv compilation finished. ========"

# --- Compile freetype ---
echo ""
echo "======== 5.4 Compiling freetype-2.14.1 ========"
cd "${BUILD_DIR}/freetype-2.14.1"
make clean &> /dev/null || true
# --- UPDATED: Use standard prefix and DESTDIR ---
./configure --prefix=/usr --host="${TARGET_HOST}" --with-zlib=yes --enable-static --disable-shared
make -j$(nproc)
make install DESTDIR="${INSTALL_DIR}"
cd "${BUILD_DIR}"
echo "======== freetype compilation finished. ========"

# --- Compile fontconfig ---
( # Use a subshell to isolate the CPPFLAGS change for fontconfig
    echo ""
    echo "======== 5.5 Compiling fontconfig-2.16.0 ========"
    cd "${BUILD_DIR}/fontconfig-2.16.0"
    make clean &> /dev/null || true

    # --- CRITICAL FIX for freetype headers ---
    # Explicitly add the freetype2 include path to CPPFLAGS for fontconfig's configure script
    export CPPFLAGS="${CPPFLAGS} -I${INSTALL_DIR}/usr/include/freetype2"
    echo "Temporarily adding FreeType include path for fontconfig: ${CPPFLAGS}"
    # --- END FIX ---

    # Use standard prefix and DESTDIR for a robust build
    ./configure --prefix=/usr \
                --host="${TARGET_HOST}" \
                --enable-static \
                --disable-shared \
                --disable-docs \
                --sysconfdir=/etc \
                --localstatedir=/var
    make -j$(nproc)
    make install DESTDIR="${INSTALL_DIR}"
    cd "${BUILD_DIR}"
    echo "======== fontconfig compilation finished. ========"
)

# --- Compile PocketPy ---
echo ""
echo "======== 5.6 Compiling PocketPy (using manual CMake) ========"
cd "${BUILD_DIR}/pocketpy"
rm -rf build
mkdir build
cd build
cmake .. \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_TOOLCHAIN_FILE="${TOOLCHAIN_CMAKE_FILE}" \
    -DPK_BUILD_STATIC_MAIN=ON \
    -DPK_ENABLE_DETERMINISM=ON \
    -DPK_BUILD_MODULE_LZ4=ON \
    -DPK_BUILD_MODULE_CUTE_PNG=ON \
    -DPK_BUILD_MODULE_MSGPACK=ON \
    -DPK_GC_MIN_THRESHOLD=10000
make -j$(nproc)
echo "PocketPy executable is at: ${BUILD_DIR}/pocketpy/build/main"
cd "${BUILD_DIR}"
echo "======== PocketPy compilation finished. ========"

# --- Compile fbterm ---
( # Use a subshell to isolate fbterm's special environment variables
    echo ""
    echo "======== 5.7 Compiling fbterm-truecolor ========"
    cd "${BUILD_DIR}/fbterm-truecolor"
    make clean &> /dev/null || true

    # --- Final fix: Run autoreconf for fbterm ---
    echo "--> Regenerating build system for fbterm..."
    autoreconf -fiv
    echo "--> Build system generated."
    
    # --- CRITICAL FIX for freetype headers ---
    # Explicitly add the freetype2 include path for fbterm's configure and make steps
    export CPPFLAGS="${CPPFLAGS} -I${INSTALL_DIR}/usr/include/freetype2"
    echo "Temporarily adding FreeType include path for fbterm: ${CPPFLAGS}"
    # --- END FIX ---

    export CXXFLAGS="${CXXFLAGS} -Wno-narrowing -fpermissive"
    export LIBS="-liconv -lexpat -lz"
    echo "Applying special compile flags for fbterm: CXXFLAGS='${CXXFLAGS}' LIBS='${LIBS}'"

    # The --prefix here doesn't affect the final output, but we set it for consistency
    ./configure --prefix=/usr --host="${TARGET_HOST}"
    make -j$(nproc)

    echo "fbterm executable is at: ${BUILD_DIR}/fbterm-truecolor/src/fbterm"
    cd "${BUILD_DIR}"
    echo "======== fbterm compilation finished. ========"
)

# --- Compile lvgl_menu ---
echo ""
echo "======== 5.8 Compiling lvgl_menu ========"
cd "${BUILD_DIR}/lvgl_menu"
# Clean previous builds if any
make clean &> /dev/null || true

# --- CRITICAL FIX: Initialize nested submodules ---
# This command will pull the 'lvgl' submodule which is inside 'lvgl_menu'.
echo "--> Initializing nested submodules for lvgl_menu (e.g., lvgl)..."
git submodule update --init --recursive
echo "--> Submodules initialized."

# Configure the build using the script's environment variables
./configure --prefix=/usr --cross-compile="${TOOLCHAIN_PREFIX}"

# Build the project
make -j$(nproc)

# --- CRITICAL FIX: Install to the main staging directory ---
# This places the final pico-menu binary into ${INSTALL_DIR}/usr/bin/
echo "--> Installing pico-menu to staging directory..."
make install DESTDIR="${INSTALL_DIR}"

echo "lvgl_menu executable is installed at: ${INSTALL_DIR}/usr/bin/pico-menu"
cd "${BUILD_DIR}"
echo "======== lvgl_menu compilation finished. ========"

# --- Compile nofrendo_nesemu_linux Submodule ---
echo ""
echo "======== 5.9 Compiling nofrendo_nesemu_linux (NES Emulator) ========"
cd "${BUILD_DIR}/nofrendo_nesemu_linux"

# 1. 确保子模块代码是最新的
echo "--> Initializing and updating submodule..."
# 这步对于刚添加的子模块是必要的，确保代码被拉取
git submodule update --init --recursive

# 2. 清理旧的编译目录
rm -rf build
mkdir build

# 3. 编译：关键步骤是使用 -DCMAKE_TOOLCHAIN_FILE 选项
# 强制让 CMake 使用主脚本在 Part 4 中生成的、路径正确的 $TOOLCHAIN_CMAKE_FILE
echo "--> Compiling using auto-generated toolchain file: ${TOOLCHAIN_CMAKE_FILE}"
cmake -B build \
    -DCMAKE_TOOLCHAIN_FILE="${TOOLCHAIN_CMAKE_FILE}" \
    -DCMAKE_BUILD_TYPE=Release \
    -DCMAKE_INSTALL_PREFIX=/usr # 统一安装路径

# 4. 使用 cmake --build 命令来编译（推荐方式，无需切换目录）
echo "--> Running build..."
cmake --build build -j$(nproc)

# 5. 使用 cmake --install 命令来安装
echo "--> Installing nofrendo executable to staging directory: ${INSTALL_DIR}"
cmake --install build --prefix="${INSTALL_DIR}"
echo "--> Entering directory ${BUILD_DIR}/nofrendo_nesemu_linux ..."
cd "${BUILD_DIR}/nofrendo_nesemu_linux"
cp  ./build/bin/nesemu ${INSTALL_DIR}/usr/bin

cd "${BUILD_DIR}"
echo "======== nofrendo_nesemu_linux compilation finished. ========"

# -------------- Compile finish -------------------- #

echo ""
echo "================================================================="
echo "All projects compiled successfully!"
echo "All dependency libraries are installed in: ${INSTALL_DIR}"
echo "PocketPy executable is: ${BUILD_DIR}/pocketpy/build/main"
echo "fbterm executable is: ${BUILD_DIR}/fbterm-truecolor/src/fbterm"

# -----------------------------------------------------------------------
# pack

echo ""
echo "====== 6.1 Creating export directory structure... ======"
EXPORT_DIR="${BUILD_DIR}/output"
# Clean and create output directory
rm -rf "${EXPORT_DIR}"
mkdir -p "${EXPORT_DIR}/usr/bin"
echo "Export directory '${EXPORT_DIR}' is ready."

echo ""
echo "====== 6.2 Exporting executables... ======"

# Export fbterm
echo "  -> Copying fbterm..."
cp -f "${BUILD_DIR}/fbterm-truecolor/src/fbterm" "${EXPORT_DIR}/usr/bin/"

# Export pocketpy (copy and rename build/main to pocketpy)
echo "  -> Copying and renaming pocketpy..."
cp -f "${BUILD_DIR}/pocketpy/build/main" "${EXPORT_DIR}/usr/bin/pocketpy"

# Export fontconfig tools (fc-cache, fc-list, etc.)
# --- UPDATED PATH: Tools are now in staging/usr/bin ---
echo "  -> Copying fontconfig tools..."
cp -f "${BUILD_DIR}/staging/usr/bin/"* "${EXPORT_DIR}/usr/bin/"

# Export lvgl_menu
echo "  -> Copying pico-menu..."
cp -f "${INSTALL_DIR}/usr/bin/pico-menu" "${EXPORT_DIR}/usr/bin/"

# Export nesemu
echo "  -> Copying nesemu..."
cp -f "${INSTALL_DIR}/usr/bin/nesemu" "${EXPORT_DIR}/usr/bin/"

echo "====== Executables exported. ======"
echo ""
echo "================================================================="
echo "Script finished! The 'output' directory has been generated and is ready for packaging."
echo "================================================================="


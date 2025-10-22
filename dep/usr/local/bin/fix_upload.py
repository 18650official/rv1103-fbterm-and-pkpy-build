#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
fix_upload.py
Extracts the binary file from a multipart/form-data upload.
This uses no external libraries and reads the file into memory.

Usage: python fix_upload.py <input_file> <output_file>
"""

import sys
import os

def extract_file_from_multipart(input_path, output_path):
    try:
        # 1. 以二进制模式(rb)读取整个被污染的文件
        with open(input_path, 'rb') as f_in:
            data = f_in.read()
    except Exception as e:
        print(f"Python Error: Failed to read input file {input_path}")
        print(str(e))
        sys.exit(1)

    try:
        # 2. 找到边界 (boundary)
        # 它是文件的第一行，去掉末尾的 \r\n
        boundary = data.split(b'\r\n', 1)[0]
        if not boundary.startswith(b'--'):
            print("Python Error: Invalid multipart format. Could not find boundary.")
            sys.exit(1)

        # 3. 找到二进制数据的 *起始* 位置
        # 它位于第一个 \r\n\r\n (双换行) 之后
        header_end_marker = b'\r\n\r\n'
        start_index = data.find(header_end_marker)
        if start_index == -1:
            print("Python Error: Could not find end of headers (no \r\n\r\n found).")
            sys.exit(1)

        # 数据的实际开头在 \r\n\r\n 之后
        start_index += len(header_end_marker)

        # 4. 找到二进制数据的 *结束* 位置
        # 它位于下一个 boundary 字符串 *之前*
        end_index = data.find(boundary, start_index)

        if end_index == -1:
            print(f"Python Error: Could not find end boundary.")
            sys.exit(1)

        # 5. 数据的实际结尾在 boundary 之前的那个 \r\n 处
        pre_boundary_marker = b'\r\n'
        real_end_index = data.rfind(pre_boundary_marker, start_index, end_index)

        if real_end_index == -1:
            print("Python Error: Could not find pre-boundary newline.")
            sys.exit(1)

        # 6. 切片，提取干净的二进制内容
        binary_content = data[start_index:real_end_index]

        # 7. 将干净的数据以二进制模式(wb)写入新文件
        with open(output_path, 'wb') as f_out:
            f_out.write(binary_content)

        print(f"Python: Successfully extracted {len(binary_content)} bytes to {output_path}")

    except Exception as e:
        print(f"Python Error: An error occurred during processing.")
        print(str(e))
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        # 确保传入了2个参数: <input_file> 和 <output_file>
        print(f"Usage: {sys.argv[0]} <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)

    extract_file_from_multipart(input_file, output_file)

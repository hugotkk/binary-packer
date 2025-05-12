#!/usr/bin/env python3

import os
import subprocess
import argparse
import shutil
import sys

def main():
    parser = argparse.ArgumentParser(description="Extract binary and its libraries")
    parser.add_argument("--dest", required=True, help="Destination folder")
    parser.add_argument("--binary", required=True, help="Full path to binary")
    args = parser.parse_args()

    dest_dir = os.path.abspath(args.dest)
    lib_dir = os.path.join(dest_dir, "lib")
    bin_dir = os.path.join(dest_dir, "bin")

    os.makedirs(lib_dir, exist_ok=True)
    os.makedirs(bin_dir, exist_ok=True)

    binary_path = os.path.abspath(args.binary)
    if not os.path.isfile(binary_path) or not os.access(binary_path, os.X_OK):
        print(f"Error: '{binary_path}' is not a valid executable.")
        sys.exit(1)

    # Copy libraries
    result = subprocess.run(["ldd", binary_path], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        parts = line.strip().split()
        if len(parts) >= 3 and parts[2].startswith("/"):
            lib_path = parts[2]
            try:
                shutil.copy2(lib_path, lib_dir)
                print(f"Copied library: {lib_path}")
            except Exception as e:
                print(f"Failed to copy {lib_path}: {e}")

    # Copy binary
    dest_binary = os.path.join(bin_dir, os.path.basename(binary_path))
    shutil.copy2(binary_path, dest_binary)
    print(f"Copied binary: {binary_path}")

    # Print command to run
    print("\nRun with:")
    print(f"LD_LIBRARY_PATH={lib_dir} {dest_binary}")

if __name__ == "__main__":
    main()
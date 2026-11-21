
import sys

from pathlib import Path

from config import HDFS_SECURE_DIR
from hash_utils import (
    calculate_sha256,
    save_hash,
    hdfs_upload
)


def main():

    if len(sys.argv) < 2:
        print("Usage: python3 register.py <local_file>")
        return

    local_file = Path(sys.argv[1])

    if not local_file.is_file():
        print("ERROR: File does not exist")
        return

    hdfs_path = f"{HDFS_SECURE_DIR}/{local_file.name}"

    try:
        print("[1] Uploading file to HDFS...")
        hdfs_upload(local_file, hdfs_path)

        print("[2] Calculating SHA-256...")
        digest = calculate_sha256(local_file)

        print("[3] Saving reference hash...")
        hash_path = save_hash(hdfs_path, digest)

        print("\n=== REGISTRATION SUCCESS ===")
        print(f"File: {hdfs_path}")
        print(f"SHA-256: {digest}")
        print(f"Hash record: {hash_path}")

    except Exception as error:
        print(f"ERROR: {error}")


if __name__ == "__main__":
    main()


import sys

from pathlib import Path

from hash_utils import hdfs_upload


def main():

    if len(sys.argv) != 3:
        print(
            "Usage: python3 replace.py "
            "<local_file> <hdfs_path>"
        )
        return

    local_file = Path(sys.argv[1])
    hdfs_path = sys.argv[2]

    if not local_file.is_file():
        print("ERROR: File does not exist")
        return

    try:
        print("[1] Replacing file in HDFS...")

        hdfs_upload(local_file, hdfs_path)

        print("[2] Replacement completed.")
        print(f"Target: {hdfs_path}")
        print("Reference hash was NOT modified.")

    except Exception as error:
        print(f"ERROR: {error}")


if __name__ == "__main__":
    main()



import sys
import tempfile

from pathlib import Path

from hash_utils import (
    calculate_sha256,
    load_hash,
    hdfs_download
)


def main():

    if len(sys.argv) != 2:
        print("Usage: python3 verify.py <hdfs_path>")
        return

    hdfs_path = sys.argv[1]

    try:
        print("[1] Loading reference hash...")
        reference_hash = load_hash(hdfs_path)

        with tempfile.TemporaryDirectory() as temp_dir:

            local_file = Path(temp_dir) / "downloaded_file"

            print("[2] Downloading file from HDFS...")
            hdfs_download(hdfs_path, local_file)

            print("[3] Calculating SHA-256...")
            actual_hash = calculate_sha256(local_file)

        print("\n=== VERIFICATION RESULT ===")
        print(f"Reference SHA-256: {reference_hash}")
        print(f"Actual SHA-256:    {actual_hash}")

        if actual_hash == reference_hash:
            print("\nRESULT: VALID")
            print("File integrity confirmed.")
        else:
            print("\nRESULT: INVALID")
            print("File content has been modified!")

    except Exception as error:
        print(f"ERROR: {error}")


if __name__ == "__main__":
    main()

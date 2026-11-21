
import hashlib
import json
import subprocess

from pathlib import Path

from config import HDFS_CMD, HASH_DIR


def calculate_sha256(filepath):
    """Calculate SHA-256 of entire file."""

    sha256 = hashlib.sha256()

    with open(filepath, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


def hash_record_path(hdfs_path):
    """Get local path for hash record."""

    filename = hashlib.sha256(
        hdfs_path.encode("utf-8")
    ).hexdigest()

    return HASH_DIR / f"{filename}.json"


def save_hash(hdfs_path, digest):
    """Save reference hash."""

    HASH_DIR.mkdir(parents=True, exist_ok=True)

    record = {
        "hdfs_path": hdfs_path,
        "sha256": digest
    }

    path = hash_record_path(hdfs_path)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(record, file, indent=4)

    return path


def load_hash(hdfs_path):
    """Load reference hash."""

    path = hash_record_path(hdfs_path)

    if not path.exists():
        raise FileNotFoundError(
            f"No registered hash for {hdfs_path}"
        )

    with open(path, "r", encoding="utf-8") as file:
        record = json.load(file)

    if record["hdfs_path"] != hdfs_path:
        raise ValueError("HDFS path mismatch")

    return record["sha256"]


def hdfs_download(hdfs_path, local_path):
    """Download file from HDFS."""

    subprocess.run(
        [HDFS_CMD, "dfs", "-get", "-f",
         hdfs_path, str(local_path)],
        check=True
    )


def hdfs_upload(local_path, hdfs_path):
    """Upload or replace file in HDFS."""

    subprocess.run(
        [HDFS_CMD, "dfs", "-put", "-f",
         str(local_path), hdfs_path],
        check=True
    )

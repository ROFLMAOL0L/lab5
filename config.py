from pathlib import Path

# HDFS directory
HDFS_SECURE_DIR = "/secure"

# Local directory for reference hashes
BASE_DIR = Path(__file__).resolve().parent
HASH_DIR = BASE_DIR / "hashes"

# Hadoop executable
HDFS_CMD = "hdfs"


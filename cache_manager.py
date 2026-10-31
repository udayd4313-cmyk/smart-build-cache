
import hashlib
import json
import subprocess
import sys
from pathlib import Path

CACHE_DIR = Path(".build_cache")
CACHE_DIR.mkdir(exist_ok=True)


def generate_hash(files):
    hasher = hashlib.sha256()

    for file in files:
        file_path = Path(file)

        if file_path.exists():
            hasher.update(file_path.read_bytes())

    return hasher.hexdigest()


def check_cache(current_hash):
    cache_file = CACHE_DIR / "cache.json"

    if not cache_file.exists():
        return False

    saved_data = json.loads(cache_file.read_text())

    return saved_data["hash"] == current_hash


def save_cache(current_hash):
    cache_file = CACHE_DIR / "cache.json"
    data = {"hash": current_hash}

    cache_file.write_text(json.dumps(data, indent=4))


def build_project():
    files = ["app.py", "requirements.txt"]
    current_hash = generate_hash(files)

    if check_cache(current_hash):
        print("CACHE HIT: Reusing existing cache.")
    else:
        print("CACHE MISS: Cache invalidated.")
        print("Starting new build...")

        result = subprocess.run(
            [sys.executable, "app.py"],
            check=True
        )

        if result.returncode == 0:
            save_cache(current_hash)
            print("Build completed. New cache saved.")


if __name__ == "__main__":
    build_project()


import sys
from pathlib import Path

# Add the main project folder to Python's search path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cache_manager import generate_hash, check_cache, save_cache


def test_generate_hash():
    file = Path("test_file.txt")
    file.write_text("Hello World")

    first_hash = generate_hash(["test_file.txt"])

    file.write_text("Hello Python")

    second_hash = generate_hash(["test_file.txt"])

    assert first_hash != second_hash

    file.unlink()


def test_cache_save_and_check(tmp_path):
    import cache_manager

    cache_manager.CACHE_DIR = tmp_path

    save_cache("abc123")

    assert check_cache("abc123") is True
    assert check_cache("different123") is False

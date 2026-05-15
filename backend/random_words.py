import random
from pathlib import Path


def get_random_words(file: Path, count: int = 20) -> list[str]:
    words = [
        line.strip()
        for line in file.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    return random.sample(words, min(count, len(words)))

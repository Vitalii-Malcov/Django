import os
from pathlib import Path

from django.conf import settings

ALLOWED_EXTENSIONS = ['.pdf', '.csv', '.doc', '.xlsx']
MAX_FILE_SIZE_MB = 2


def check_extension(filename: str) -> bool:
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


def check_file_size(file, required_size: int = MAX_FILE_SIZE_MB) -> bool:
    return file.size <= required_size * 1024 * 1024


def create_file_path(file_name: str) -> str:
    return f"projects/{Path(file_name).name}"


def save_file(file_path: str, file_content) -> str:
    full_path = os.path.join(settings.MEDIA_ROOT, file_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'wb') as destination:
        for chunk in file_content.chunks():
            destination.write(chunk)
    return file_path

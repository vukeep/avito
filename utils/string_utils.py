import re

def normalize_string(s: str) -> str:
    """
    Normalize a string by removing special characters and extra spaces.
    """
    return re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', '', s)).strip()

def truncate_text(s: str, length: int = 100) -> str:
    """
    Truncate a string to the specified length, adding ellipsis if necessary.
    """
    return s if len(s) <= length else s[:length] + '...'

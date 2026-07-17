import re

def validate_url(url: str) -> bool:
    if not url:
        return False
    # Simple regex for URL validation
    pattern = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
        r'localhost|' # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return bool(pattern.match(url))

def clean_text(text: str) -> str:
    if not text:
        return ""
    # Strip excessive whitespaces and outer quotes
    text = text.strip()
    # Normalize unicode spaces/newlines
    text = re.sub(r'\s+', ' ', text)
    return text

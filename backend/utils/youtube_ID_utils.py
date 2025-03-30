import re

def extract_video_id(url: str) -> str | None:
    """Extracts YouTube video ID from various URL formats."""
    # Standard watch URL
    match = re.search(r"watch\\?\?v\\?=([a-zA-Z0-9_-]{11})", url)
    if match:
        return match.group(1)

    # *** ADD THIS BLOCK ***
    # Shortened youtu.be URL
    match = re.search(r"youtu.be/([a-zA-Z0-9_-]{11})", url)
    if match:
        return match.group(1)
    # *** END OF ADDED BLOCK ***

    # Embedded URL
    match = re.search(r"embed/([a-zA-Z0-9_-]{11})", url)
    if match:
        return match.group(1)

    # Shorts URL
    match = re.search(r"shorts/([a-zA-Z0-9_-]{11})", url)
    if match:
        return match.group(1)

    # If URL is just the ID itself
    if re.match(r"^[a-zA-Z0-9_-]{11}$", url):
        return url

    return None # Return None if no pattern matches
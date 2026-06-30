from datetime import datetime
from PIL import Image
from pathlib import Path
from os import path

def time_ago(dt):
    diff = datetime.utcnow() - dt
    sec = diff.seconds

    if diff.days > 7 or diff.days < 0:
        return dt.strftime("%d %b %y")
    elif diff.days == 1:
        return "1 day ago"
    elif diff.days > 1:
        return f"{diff.days} days ago"
    elif sec <= 1:
        return "just now"
    elif sec < 60:
        return f"{sec} seconds ago"
    elif sec < 120:
        return "1 minute ago"
    elif sec < 3600:
        return f"{sec // 60} minutes ago"
    elif sec < 7200:
        return "1 hour ago"
    else:
        return f"{sec // 3600} hours ago"

def validate_save_pfp(stream, filename, max_res=(512, 512)):
    # Do not allow path traversal
    if ".." in filename or "/" in filename or "\\" in filename:
        raise ValueError("Invalid filename")

    img = Image.open(stream)
    # Convert to png
    img = img.convert("RGBA")

    img.thumbnail(max_res)
    img.save(f"static/pfps/{filename}.png", "PNG")

def delete_pfp(filename):
    # Do not allow path traversal
    if ".." in filename or "/" in filename or "\\" in filename:
        raise ValueError("Invalid filename")

    file_path = Path(f"static/pfps/{filename}.png")
    if file_path.exists():
        file_path.unlink()
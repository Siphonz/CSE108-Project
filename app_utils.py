from datetime import datetime

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
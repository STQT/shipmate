from datetime import timedelta

def timedelta_to_text(td: timedelta) -> str:
    total_seconds = int(td.total_seconds())
    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    if days > 0:
        return f"{days}d. {hours}hr {minutes}mins {seconds}secs"
    elif hours > 0:
        return f"{hours}hr {minutes}mins {seconds}secs"
    elif minutes > 0:
        return f"{minutes}mins {seconds}secs"
    else:
        return f"{seconds}secs"

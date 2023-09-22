def dtos(d):
    c = d.components
    s = f"{c.days}d" if c.days != 0 else ""
    s += f"{c.hours}h" if c.hours != 0 else ""
    s += f"{c.minutes}m" if c.minutes != 0 else ""
    s += f"{c.seconds}s" if c.seconds != 0 else ""
    return s

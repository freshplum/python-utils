def fill(lst, filler, length):
    """Fills a list with the filler up to the given length"""
    if lst is None:
        return [filler] * length
    return lst + [filler] * (length - len(lst))

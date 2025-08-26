#Helper function to separate arrays into strings.
def ArrayToCommaSeparatedString( iterable ):
    if isinstance( iterable, basestring ):
        return iterable

    if iterable is None:
        return ""

    return ",".join( str(x) for x in iterable )
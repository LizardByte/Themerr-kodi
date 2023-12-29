"""
Main entry point for the Themerr service.
"""

# lib imports
from themerr import plugin


def main():
    """
    Main entry point for the Themerr service.

    Creates a Themerr instance and starts it.

    Examples
    --------
    >>> main()
    """
    themerr = plugin.Themerr()
    themerr.start()


if __name__ == '__main__':
    main()  # pragma: no cover

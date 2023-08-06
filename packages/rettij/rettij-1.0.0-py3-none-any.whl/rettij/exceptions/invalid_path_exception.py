import os


class InvalidPathException(Exception):
    """
    Create a new InvalidPathException.

    Please use kind='Directory' when validating a directory path and kind='File' when validating a file path.
    """

    def __init__(self, path_str: str, kind: str) -> None:
        """
        Throw a new InvalidPathException.

        :param path_str: Path.
        :param kind: Kind of path.
        """
        self.path_str: str = os.path.normpath(path_str)
        super().__init__(f"There is no {kind} at path '{path_str}'! (normalized: {os.path.normpath(path_str)})")

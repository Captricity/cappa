class MissingExecutable(Exception):
    """Exception raised when a package manager executable is missing"""
    pass


class UnknownManager(Exception):
    """Exception raised when a requested package manager is unknown"""
    pass

class ValidHandlerUnavailable(Exception):
    """Exception is raised when a next valid task handler is not available because of existing task queue"""

    pass


class HandlerNotAvailable(Exception):
    """Exception is raised when the task does not have assigned handlers"""

    pass

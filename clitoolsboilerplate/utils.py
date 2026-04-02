"""
Utilities for [[PACKAGE_NAME_USER_FACING]].
"""
# MARK: Imports
from .logger import LoggerManager

# MARK: Constants
LOG_MANAGER = LoggerManager("clitoolsboilerplate.log")
LOGGER = LOG_MANAGER.getLogger("cli")

# MARK: Functions
def throwError(msg: str, t: type[Exception]) -> None:
    """
    Log an error message and raise a RuntimeError.

    msg: The error message to log and include in the exception.
    t: The type of exception to raise.
    """
    LOGGER.error(msg)
    raise t(msg)

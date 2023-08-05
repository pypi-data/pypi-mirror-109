#!usr/bin/python

# Copyright 2021 Deep Intelligence
# See LICENSE for details.


class DeepintBaseError(Exception):
    """Generic exception for package.
    
    Attributes:
        code: error's id in text format. Can be obtained from deepint.net API when a request is errored, or generated by this package when a comprobation error occurs.
        message: error's description. As well as the code can be generated by this package in comprobations or can be obtained from deepint.net API.

    Args:
        code: error's id in text format. Can be obtained from deepint.net API when a request is errored, or generated by this package when a comprobation error occurs.
        message: error's description. As well as the code can be generated by this package in comprobations or can be obtained from deepint.net API.
    """

    def __init__(self, code: str, message: str) -> None:
        self.code = code
        self.message = message
        super().__init__(self._build_message())

    def _build_message(self) -> str:
        """
        Formats the message for the exception.

        Returns:
            formatted message.
        """

        return f'{self.code}: {self.message} '


class DeepintHTTPError(DeepintBaseError):
    """Exception used on HTTP error response by deepint.net API.

    Args:
        code: error code provided by deepint.net API.
        message: messaged code provided by deepint.net API.
        url: resource that was being operated on when the error occurred.
        method: HTTP method performed on the request that originated the error.
    """

    def __init__(self, code: str, message: str, method: str, url: str) -> None:
        full_message = f'Error on HTTP {method} {url}. {message}'
        super().__init__(code=code, message=full_message)


class DeepintCredentialsError(DeepintBaseError):
    """Exception thrown when in the building process of a :obj:`deepint_sdk.credentials.Credentials` a token is not found.

    """

    def __init__(self):
        super().__init__(code="CREDENTIALS_NOT_FOUND", message="Unable to load credentials from file, env or parameter")


class DeepintTaskError(DeepintBaseError):
    """Exception raised when in the :obj:`deepint_sdk.core.Task.resolve` method, the task fails.

    Args:
        task: id of the failed task.
        name: name of the failed task.
        code: error code provided by deepint.net API.
        message: messaged code provided by deepint.net API.
    """

    def __init__(self, task: str, name: str, code: str, message: str) -> None:
        super().__init__(code=f"TASK_{code}", message=f"Task ({task}) {name} failed with description: {message}")

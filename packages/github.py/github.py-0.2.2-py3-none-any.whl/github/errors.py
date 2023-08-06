"""
/github/errors.py

    Copyright (c) 2019 ShineyDev
    
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

import typing

import aiohttp


class GitHubError(Exception):
    """
    The base Exception class for the wrapper. This could be used to
    catch all exceptions thrown by the wrapper.

    This exception is raised when GitHub returns arbitrary errors in
    the JSON response. The given error is the first error in the list.

    Attributes
    ----------
    message: :class:`str`
        The error message.
    data: :class:`dict`
        The data returned by the API.
    response: :class:`aiohttp.ClientResponse`
        The response of the failed HTTP request.
    """

    def __init__(self, message: str, *, response: aiohttp.ClientResponse, data: typing.Optional[dict]=None):
        self.message = message
        self.data = data
        self.response = response
        super().__init__("{1.status}: {0}".format(message, response))

class HTTPException(GitHubError):
    """
    This exception is raised when a HTTP request operation fails.
    """

    pass

class Forbidden(HTTPException):
    """
    This exception is raised when a "FORBIDDEN" status-message is returned.
    """

    pass

class Internal(HTTPException):
    """
    This exception is raised when an "INTERNAL" status-message is returned.
    """

    pass

class NotFound(HTTPException):
    """
    This exception is raised when a "NOT_FOUND" status-message is returned.
    """

    pass

class Unauthorized(HTTPException):
    """
    This exception is raised when a 401 status-code is returned.

    This exception is typically raised when invalid credentials are passed.
    """

    pass

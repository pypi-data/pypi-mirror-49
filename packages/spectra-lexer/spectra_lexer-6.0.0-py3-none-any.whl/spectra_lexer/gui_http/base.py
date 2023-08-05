import os
from typing import Callable

from spectra_lexer.core import Command
from spectra_lexer.view import VIEW


class GUIHTTP(VIEW):

    ADDRESS = "localhost", 80
    HTTP_PUBLIC = os.path.join(os.path.split(__file__)[0], "public")

    @Command
    def GUIHTTPServe(self) -> int:
        raise NotImplementedError

    @Command
    def GUIHTTPRequest(self, data:bytes, response_callback:Callable) -> None:
        """ Process JSON data obtained from a client request. """
        raise NotImplementedError

    @Command
    def GUIHTTPShutdown(self) -> None:
        """ Shut down the HTTP server. Threads with outstanding requests will finish them. """
        raise NotImplementedError

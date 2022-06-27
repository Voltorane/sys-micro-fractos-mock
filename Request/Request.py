import os
from stat import S_IREAD, S_IRGRP, S_IROTH


class Request:
    def __init__(self, RPC, next, arguments, capabilities):
        self.RPC = RPC
        self.next = next
        self.arguments = arguments
        self.capabilities = capabilities

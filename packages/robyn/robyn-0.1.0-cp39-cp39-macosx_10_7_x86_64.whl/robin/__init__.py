from .robin import *
from .robin import Server

class Robin:
    """This is the python wrapper for the Robin binaries.
    """
    def __init__(self) -> None:
        self.server = Server()

    def add_route(self, route_type, endpoint, handler):
        self.server.add_route(route_type, endpoint, handler)

    def start(self):
        self.server.start()

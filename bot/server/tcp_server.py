from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory as ServFactory
from typing import Dict, Callable
from . import Connection
import logging


class TcpServer(ServFactory):
    def __init__(self, host: str, port: int, callbacks: dict, *args, **kwargs):
        super(TcpServer, self).__init__(*args, **kwargs)
        self.port = port
        self.logger = logging.getLogger("tcp_server")
        self.callbacks: Dict[str, Callable] = callbacks
        self.listener = None
        self.host = host

    def buildProtocol(self, addr):
        return Connection(self.callbacks)

    def start(self):
        self.listener = reactor.listenTCP(self.port, self)
        self.logger.info(f"Listening to {self.host}:{self.port}")

    def stop(self):
        self.listener.stopListening()

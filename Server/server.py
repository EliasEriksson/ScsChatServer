from typing import *
import websockets
import asyncio


class Server:
    class AbortConnection(Exception):
        pass

    def __init__(self, lop: asyncio.AbstractEventLoop):
        self.messages = []
        self.clients: Set[websockets.WebSocketServerProtocol] = set()
        lop.create_task(self._process_messages())

    async def _process_messages(self):
        while True:
            while self.messages:
                message = self.messages.pop(0)
                for client in self.clients:
                    asyncio.create_task(self.send(client, message))

            await asyncio.sleep(0.01)

    async def receive(self, socket: websockets.WebSocketServerProtocol):
        try:
            message = await socket.recv()
            return message
        except websockets.ConnectionClosed:
            self.clients.remove(socket)
            raise self.AbortConnection()

    async def send(self, socket: websockets.WebSocketServerProtocol, message: str):
        try:
            await socket.send(message)
        except websockets.ConnectionClosed:
            self.clients.remove(socket)

    async def handle_connection(self, socket: websockets.WebSocketServerProtocol, _):
        self.clients.add(socket)
        try:
            while True:
                message = await self.receive(socket)
                self.messages.append(message)
        except self.AbortConnection:
            pass


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    server = websockets.serve(Server(loop).handle_connection, "", 2020)
    loop.run_until_complete(server)
    loop.run_forever()

from typing import *
import websockets
import asyncio
import json
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from asgiref.sync import sync_to_async


class Message:
    def __init__(self, message_data: Dict[str, Any], user):
        self.headers = message_data["headers"]
        self.message = message_data["message"]
        self.user = user


class Server:
    class AbortConnection(Exception):
        pass

    def __init__(self, lop: asyncio.AbstractEventLoop):
        self.messages: List[Message] = []
        self.clients: Dict[websockets.WebSocketServerProtocol, User] = {}
        lop.create_task(self._process_messages())

    async def _process_messages(self):
        """
        sends the collected messages to all connected clients.

        :return:
        """
        while True:
            while self.messages:
                message = self.messages.pop(0)
                for client in self.clients:
                    asyncio.create_task(self.send(client, message))

            await asyncio.sleep(0.01)

    async def receive(self, socket: websockets.WebSocketServerProtocol) -> Dict[str, Any]:
        try:
            message = await socket.recv()
            return json.loads(message)
        except websockets.ConnectionClosed:
            raise self.AbortConnection()

    async def send(self, socket: websockets.WebSocketServerProtocol, message: Message):
        try:
            response = {
                "headers": {
                    "user": message.user.username
                },
                "message": message.message
            }
            await socket.send(json.dumps(response))
        except websockets.ConnectionClosed:
            self.clients.pop(socket)

    @sync_to_async
    def get_user(self, session_key: str):
        try:
            session_data = Session.objects.get(session_key=session_key).get_decoded()
            user: User = User.objects.get(id=session_data["_auth_user_id"])
        except (Session.DoesNotExist, User.DoesNotExist):
            raise self.AbortConnection()
        return user

    async def handle_connection(self, socket: websockets.WebSocketServerProtocol, _):
        try:
            request = await self.receive(socket)

            if "headers" in request and "session_key" in request["headers"]:
                user = await self.get_user(request["headers"]["session_key"])
                self.clients.update({socket: user})
                while True:
                    message_data: Dict[str, Any] = await self.receive(socket)
                    self.messages.append(Message(message_data, user))
        except self.AbortConnection:
            pass

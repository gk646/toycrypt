#  SPDX-License-Identifier: GPL-3.0-only

from typing import List


class Message:
    _payload: str
    _sender: "Device"
    _target: "Device"

    def __init__(self, sender: "Device", target: "Device", content: str):
        self._payload = content
        self._sender = sender
        self._target = target

    def __str__(self):
        return f"Message from [{self._sender.get_name()}] to [{self._target.get_name()}]: {self._payload}"

    def get_content(self) -> str:
        return self._payload

    def get_sender(self) -> "Device":
        return self._sender

    def get_target(self) -> "Device":
        return self._target


class Connection:
    """
    Models an arbitrary network connection
    """
    _clients: List["Device"]
    _listeners: List["Device"]

    def __init__(self):
        self._clients = []
        self._listeners = []

    def add_listener(self, listener: "Device"):
        if listener in self._listeners:
            raise ValueError("Device is already listening")
        self._listeners.append(listener)

    def add_client(self, client: "Device"):
        if client in self._clients:
            raise ValueError("client is already connected")
        self._clients.append(client)

    def send_message(self, message: Message):
        if message.get_sender() not in self._clients:
            print("Message could not be sent - Target not connected")

        # Deliver the message to the target
        message.get_target().get_received_messages().append(message)

        # all listeners get the message as well
        for listener in self._listeners:
            listener.get_received_messages().append(message)

    def broadcast(self, message: Message):
        for listener in self._listeners:
            listener.get_received_messages().append(message)


class Device:
    """
    Models a network endpoint that can send and receive messages
    """
    _connection: Connection
    _name: str
    _in_messages: List[Message]
    _out_messages: List[Message]

    def __init__(self, name: str):
        self._name = name
        self._encryption_func = None
        self._in_messages = []
        self._out_messages = []

    def connect(self, connection: Connection):
        self._connection = connection
        self._connection.add_client(self)
        self._connection.broadcast(Message(self, self, f"{self._name} connected"))

    def send(self, target: "Device", content: str):
        if self._connection is None:
            raise ValueError("Device is not connected - Use connect() to connect this device")
        if self._encryption_func:
            content = self._encryption_func(content)
        message = Message(self, target, content)
        self._connection.send_message(message)

    def get_received_messages(self) -> List[Message]:
        return self._in_messages

    def get_sent_messages(self) -> List[Message]:
        return self._out_messages

    def get_name(self) -> str:
        return self._name

    def set_encryption(self, encryption_func):
        self._encryption_func = encryption_func

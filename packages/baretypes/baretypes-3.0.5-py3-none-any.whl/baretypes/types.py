from abc import ABCMeta, abstractmethod
from typing import Mapping, MutableMapping, AsyncIterable, Union, AbstractSet, Iterable, List
from typing import Any, Callable, Optional, Tuple
from typing import Awaitable


class ParseError(Exception):
    pass


class HttpInternalError(Exception):
    pass


class HttpDisconnectError(Exception):
    pass


class WebSocketInternalError(Exception):
    pass


Scope = Mapping[str, Any]
Message = Mapping[str, Any]
Context = Optional[Mapping[str, Any]]
Info = Optional[MutableMapping[str, Any]]

Receive = Callable[[], Awaitable[Message]]
Send = Callable[[Message], Awaitable[None]]

ASGIInstance = Callable[[Receive, Send], Awaitable[None]]
ASGIApp = Callable[[Scope], ASGIInstance]

LifespanHandler = Callable[[Scope, Info, Message], Awaitable[None]]

Header = Tuple[bytes, bytes]
Headers = List[Header]

RouteMatches = Mapping[str, Any]
Content = AsyncIterable[bytes]
PushResponse = Tuple[str, Headers]
PushResponses = Iterable[PushResponse]


class WebSocket(metaclass=ABCMeta):
    """A server side WebSocket.
    """

    @abstractmethod
    async def accept(self, subprotocol: Optional[str] = None) -> None:
        """Accept the socket.

        This must be done before any other action is taken.

        :param subprotocol: An optional subprotocol sent by the client.
        """
        ...

    @abstractmethod
    async def receive(self) -> Optional[Union[bytes, str]]:
        """Receive data from the WebSocket.

        :return: Either bytes of a string depending on the client.
        """
        ...

    @abstractmethod
    async def send(self, content: Union[bytes, str]) -> None:
        """Send data to the client.

        :param content: Either bytes or a strng.
        """
        ...

    @abstractmethod
    async def close(self, code: int = 1000) -> None:
        """Closes the WebSocket.

        :param code: The reason code (defaults to 1000).
        """
        ...


HttpResponse = Union[
    int,
    Tuple[int, Optional[Headers]],
    Tuple[int, Optional[Headers], Optional[Content]],
    Tuple[int, Optional[Headers], Optional[Content], Optional[PushResponses]]
]
HttpRequestCallback = Callable[[Scope, Info, RouteMatches, Content], Awaitable[HttpResponse]]
WebSocketRequestCallback = Callable[[Scope, Info, RouteMatches, WebSocket], Awaitable[None]]
HttpMiddlewareCallback = Callable[[Scope, Info, RouteMatches, Content, HttpRequestCallback], Awaitable[HttpResponse]]


class HttpRouter(metaclass=ABCMeta):

    @property
    @abstractmethod
    def not_found_response(self) -> HttpResponse:
        ...

    @not_found_response.setter
    @abstractmethod
    def not_found_response(self, value: HttpResponse) -> None:
        ...

    @abstractmethod
    def add(self, methods: AbstractSet[str], path: str, callback: HttpRequestCallback) -> None:
        ...

    @abstractmethod
    def resolve(self, method: str, path: str) -> Tuple[Optional[HttpRequestCallback], Optional[RouteMatches]]:
        ...


class WebSocketRouter(metaclass=ABCMeta):

    @abstractmethod
    def add(self, path: str, callback: WebSocketRequestCallback) -> None:
        ...

    @abstractmethod
    def resolve(self, path: str) -> Tuple[Optional[HttpRequestCallback], Optional[RouteMatches]]:
        ...

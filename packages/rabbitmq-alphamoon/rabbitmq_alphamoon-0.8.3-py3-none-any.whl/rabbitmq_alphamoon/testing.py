from contextlib import contextmanager
from typing import Any, Callable, Dict, List, Optional, Tuple

from rabbitmq_alphamoon import IQueueConnector


class ConnectorMock(IQueueConnector):
    def __init__(self, *args, **kwargs):
        self.__opened_connection = False
        self.init_args = args
        self.init_kwargs = kwargs

    @contextmanager
    def open_connection(self):
        if self.__opened_connection:
            raise RuntimeError("Connection already opened")
        try:
            self.__opened_connection = True
            yield self
        finally:
            self.__opened_connection = False

    def _verify_connection_opened(self):
        if not self.__opened_connection:
            raise RuntimeError("Connection not opened")

    def consume_forever(
        self,
        process_message_callback: Callable[[Any, Dict[str, Any]], None],
        max_allowed_memory: Optional[int] = None,
    ):
        raise NotImplementedError("consume_forever not implemented in " + type(self).__name__)

    def publish(self, message: Any) -> None:
        raise NotImplementedError("publish not implemented in " + type(self).__name__)

    @property
    def message_count(self) -> int:
        raise NotImplementedError("message_count not implemented in " + type(self).__name__)


def create_consumer_connector_mock(incoming_messages: List[Tuple[Any, Dict[str, Any]]]) -> object:
    class ConsumerConnectorMock(ConnectorMock):
        def consume_forever(
            self,
            process_message_callback: Callable[[Any, Dict[str, Any]], None],
            max_allowed_memory: Optional[int] = None,
        ):
            self._verify_connection_opened()
            for message, info in incoming_messages:
                process_message_callback(message, info)

    return ConsumerConnectorMock

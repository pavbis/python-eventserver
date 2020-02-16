class EventStoreError(Exception):
    """Base event store exception."""


class StreamReservedForProducer(EventStoreError):
    """Raised when stream already reserved for another producer."""

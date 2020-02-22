from eventsserver.value.objects import StreamName


class FindConsumersQuery:
    def __init__(self, stream_name: StreamName):
        self.__stream_name = stream_name

    def get_stream_name(self) -> StreamName:
        return self.__stream_name

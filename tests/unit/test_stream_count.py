from unittest import TestCase
from eventsserver.metrics.metrics_types import StreamCount, InvalidArgument


class StreamCountTest(TestCase):
    def test_it_raises_error_if_primitive_value_lower_than_zero(self):
        with self.assertRaises(InvalidArgument) as context:
            StreamCount(-12)
        self.assertTrue('Stream count cannot be lower than zero.' in str(context.exception))

    def test_it_returns_the_primitive_value(self):
        primitive_value = 1
        stream_count = StreamCount(primitive_value)

        self.assertEqual(primitive_value, int(stream_count))

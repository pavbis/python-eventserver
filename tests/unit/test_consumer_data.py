from unittest import TestCase
from eventsserver.dto.consumer_data import ConsumerData


class ConsumerDataTest(TestCase):
    def test_consumer_data_can_be_created_from_list(self) -> None:
        primitive_list = [
            'c3f390b8-302f-49af-b987-66ab0a931a62', 1,
            '2019-11-08 08:38:35.806000+00:00', 'unit-test', 55.5, 12
        ]

        consumer_data = ConsumerData.from_list(primitive_list)

        self.assertEqual('c3f390b8-302f-49af-b987-66ab0a931a62', str(consumer_data.get_consumer_id()))
        self.assertEqual('unit-test', str(consumer_data.get_event_name()))
        self.assertEqual(1, int(consumer_data.get_offset()))
        self.assertEqual('2019-11-08 08:38:35.806000+00:00', str(consumer_data.get_moved_at()))
        self.assertEqual(55.5, float(consumer_data.get_consumed_percentage()))
        self.assertEqual(12, int(consumer_data.get_behind()))

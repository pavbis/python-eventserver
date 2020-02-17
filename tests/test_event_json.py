from unittest import TestCase
from eventsserver.value.objects import EventId, EventJson, InvalidArgument


class EventJsonTest(TestCase):
    def test_it_raises_exception_if_provided_primitive_type_is_invalid_json(self):
        primitive_value = '(7hhf'

        with self.assertRaises(InvalidArgument) as context:
            EventJson(primitive_value)
        self.assertTrue('Value is not a JSON string.' in str(context.exception))

    def test_it_returns_provided_primitive_value(self):
        primitive_value = '{"event": {"id": "c3f390b8-302f-49af-b987-66ab0a931a62", "name": "Snickers", "version": ' \
                          '1}, "system": {"id": "alv1", "name": "codello alvine", "time": "2019-09-06 13:58:12", ' \
                          '"timezone": "Europe/Berlin"}, "payload": {}, "trigger": {"name": "/path/to/script.php", ' \
                          '"type": "system"}}'

        event_json = EventJson(primitive_value)

        self.assertEqual(primitive_value, str(event_json))

    def test_to_event_with_id_raises_invalid_argument_if_event_section_not_provided(self):
        primitive_value = '{"system": {"id": "alv1", "name": "codello alvine", "time": "2019-09-06 13:58:12",' \
                          '"timezone": "Europe/Berlin"}, "payload": {}, "trigger": {"name": "/path/to/script.php", ' \
                          '"type": "system"}} '

        event_id = EventId('c3f390b8-302f-49af-b987-66ab0a931a62')

        with self.assertRaises(InvalidArgument) as context:
            EventJson(primitive_value).to_event_with_id(event_id)
        self.assertTrue(
            'Event JSON is missing an event section. This event should be considered broken.' in str(context.exception)
        )

    def test_to_event_with_id_raises_invalid_argument_if_event_id_is_provided(self):
        primitive_value = '{"event": {"id": "c3f390b8-302f-49af-b987-66ab0a931a62", "name": "Snickers", "version": ' \
                          '1}, "system": {"id": "alv1", "name": "codello alvine", "time": "2019-09-06 13:58:12", ' \
                          '"timezone": "Europe/Berlin"}, "payload": {}, "trigger": {"name": "/path/to/script.php", ' \
                          '"type": "system"}}'

        event_id = EventId('c3f390b8-302f-49af-b987-66ab0a931a62')

        with self.assertRaises(InvalidArgument) as context:
            EventJson(primitive_value).to_event_with_id(event_id)
        self.assertTrue('Event already has an event ID.' in str(context.exception))

    def test_it_returns_event_with_id(self):
        primitive_value = '{"event": {"name": "Snickers", "version": ' \
                          '1}, "system": {"id": "alv1", "name": "codello alvine", "time": "2019-09-06 13:58:12", ' \
                          '"timezone": "Europe/Berlin"}, "payload": {}, "trigger": {"name": "/path/to/script.php", ' \
                          '"type": "system"}}'

        event_id = EventId('c3f390b8-302f-49af-b987-66ab0a931a62')
        event = EventJson(primitive_value).to_event_with_id(event_id)

        self.assertEqual(str(event_id), str(event.event_id))

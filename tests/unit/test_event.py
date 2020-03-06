from unittest import TestCase
from eventsserver.value.objects import Event


class EventTest(TestCase):
    def setUp(self) -> None:
        self.event_data_with_event_id = {'event': {'name': 'Snickers', 'version': 1, 'id': 'c3f390b8-302f-49af-b987'
                                                                                           '-66ab0a931a62'},
                                         'system': {'id': 'alv1', 'name': 'codello alvine',
                                                    'time': '2019-09-06 13:58:12',
                                                    'timezone': 'Europe/Berlin'},
                                         'payload': {'foo': 'bar'},
                                         'trigger': {'name': '/path/to/script.php', 'type': 'system'}}

    def test_it_can_be_created_from_event_data(self):
        event = Event.from_event_data(self.event_data_with_event_id)

        self.assertEqual('Snickers', str(event.event_name))
        self.assertEqual(1, int(event.event_version))
        self.assertEqual('c3f390b8-302f-49af-b987-66ab0a931a62', str(event.event_id))
        self.assertEqual('alv1', str(event.system_id))
        self.assertEqual('codello alvine', str(event.system_name))
        self.assertEqual('2019-09-06 13:58:12', str(event.system_time))
        self.assertEqual('Europe/Berlin', str(event.time_zone))
        self.assertEqual('/path/to/script.php', str(event.trigger_name))
        self.assertEqual('system', str(event.trigger_type))
        self.assertEqual("{'foo': 'bar'}", str(event.payload))
        self.assertEqual('{"foo": "bar"}', event.payload.to_json())

    def test_it_can_be_converted_to_event_data(self):

        expected = {'event': {'name': 'Snickers', 'version': 1, 'id': 'c3f390b8-302f-49af-b987-66ab0a931a62'},
                    'system': {'id': 'alv1', 'name': 'codello alvine', 'time': '2019-09-06 13:58:12',
                               'timezone': 'Europe/Berlin'},
                    'payload': {"{'foo': 'bar'}"}, 'trigger': {'name': '/path/to/script.php', 'type': 'system'}}

        event = Event.from_event_data(self.event_data_with_event_id)

        self.assertEqual(expected, event.to_event_data())

    def test_event_can_be_encoded_to_json(self):
        event_data = {'event': {'name': 'Snickers', 'version': 1, 'id': 'c3f390b8-302f-49af-b987-66ab0a931a62'},
                      'system': {'id': 'alv1', 'name': 'codello alvine', 'time': '2019-09-06 13:58:12',
                                 'timezone': 'Europe/Berlin'},
                      'payload': {}, 'trigger': {'name': '/path/to/script.php', 'type': 'system'}}

        expected = '{"event": {"id": "c3f390b8-302f-49af-b987-66ab0a931a62", "name": "Snickers", "version": 1}, ' \
                   '"system": {"id": "alv1", "name": "codello alvine", "time": "2019-09-06 13:58:12", "timezone": ' \
                   '"Europe/Berlin"}, "trigger": {"name": "/path/to/script.php", "type": "system"}, "payload": ["{}"]}'

        event = Event.from_event_data(event_data)

        self.assertEqual(expected, event.to_json())

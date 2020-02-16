CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Add example events, 1 stream 3 different events
INSERT INTO "events"
    ("streamName", "eventName", "sequence", "eventId", "event")
VALUES ('streamOne'::VARCHAR, 'ExampleEventOne'::VARCHAR,
        (SELECT COALESCE(MAX("sequence"), 0)
         FROM "events"
         WHERE "streamName" = 'streamOne'::VARCHAR
           AND "eventName" = 'ExampleEventOne'::VARCHAR
         LIMIT 1) + 1,
        '78e1bf5e-82d4-4ba8-9b0f-ae4ef0857033',
        json_strip_nulls('{
          "event": {
            "name": "ExampleEventOne",
            "version": 1
          },
          "system": {
            "id": "alv123",
            "name": "codello alvine",
            "time": "2019-09-06 13:58:12",
            "timezone": "Europe/Berlin"
          },
          "trigger": {
            "type": "system",
            "name": "/path/to/script.php"
          },
          "payload": {
            "los" : "angeles",
            "miami" : "heat"
          }
        }')::json),

       ('streamOne'::VARCHAR, 'ExampleEventTwo'::VARCHAR,
        (SELECT COALESCE(MAX("sequence"), 0)
         FROM "events"
         WHERE "streamName" = 'streamOne'::VARCHAR
           AND "eventName" = 'ExampleEventTwo'::VARCHAR
         LIMIT 1) + 1,
        uuid_generate_v4(),
        json_strip_nulls('{
          "event": {
            "name": "ExampleEventTwo",
            "version": 1
          },
          "system": {
            "id": "alv123",
            "name": "codello alvine",
            "time": "2019-09-06 14:58:12",
            "timezone": "Europe/Berlin"
          },
          "trigger": {
            "type": "system",
            "name": "/path/to/script.php"
          },
          "payload": {}
        }')::json),

       ('streamOne'::VARCHAR, 'ExampleEventTwo'::VARCHAR,
        (SELECT COALESCE(MAX("sequence"), 0)
         FROM "events"
         WHERE "streamName" = 'streamOne'::VARCHAR
           AND "eventName" = 'ExampleEventTwo'::VARCHAR
         LIMIT 1) + 1,
        uuid_generate_v4(),
        json_strip_nulls('{
          "event": {
            "name": "ExampleEventTwo",
            "version": 1
          },
          "system": {
            "id": "alv123",
            "name": "codello alvine",
            "time": "2019-09-06 14:59:12",
            "timezone": "Europe/Berlin"
          },
          "trigger": {
            "type": "system",
            "name": "/path/to/script.php"
          },
          "payload": {}
        }')::json),

       ('streamOne'::VARCHAR, 'ExampleEventTwo'::VARCHAR,
        (SELECT COALESCE(MAX("sequence"), 0)
         FROM "events"
         WHERE "streamName" = 'streamOne'::VARCHAR
           AND "eventName" = 'ExampleEventTwo'::VARCHAR
         LIMIT 1) + 1,
        uuid_generate_v4(),
        json_strip_nulls('{
          "event": {
            "name": "ExampleEventTwo",
            "version": 1
          },
          "system": {
            "id": "alv123",
            "name": "codello alvine",
            "time": "2019-09-06 14:59:30",
            "timezone": "Europe/Berlin"
          },
          "trigger": {
            "type": "system",
            "name": "/path/to/script.php"
          },
          "payload": {}
        }')::json),

       ('streamOne'::VARCHAR, 'ExampleEventThree'::VARCHAR,
        (SELECT COALESCE(MAX("sequence"), 0)
         FROM "events"
         WHERE "streamName" = 'streamOne'::VARCHAR
           AND "eventName" = 'ExampleEventThree'::VARCHAR
         LIMIT 1) + 1,
        uuid_generate_v4(),
        json_strip_nulls('{
          "event": {
            "name": "ExampleEventThree",
            "version": 1
          },
          "system": {
            "id": "alv123",
            "name": "codello alvine",
            "time": "2019-09-06 15:59:12",
            "timezone": "Europe/Berlin"
          },
          "trigger": {
            "type": "system",
            "name": "/path/to/script.php"
          },
          "payload": {}
        }')::json);

-- Add producer stream relation
INSERT INTO "producerStreamRelations" ("producerId", "streamName")
VALUES (uuid_generate_v4(), 'streamOne'::VARCHAR);

-- Add consumer offsets

DO
$$
    DECLARE
        consumerId VARCHAR := uuid_generate_v4();
    BEGIN
        INSERT INTO "consumerOffsets" ("consumerId", "streamName", "eventName", "offset")
        VALUES (consumerId, 'streamOne'::VARCHAR, 'ExampleEventOne'::VARCHAR, 1),
               (consumerId, 'streamOne'::VARCHAR, 'ExampleEventTwo'::VARCHAR, 2),
               (consumerId, 'streamOne'::VARCHAR, 'ExampleEventThree'::VARCHAR, 1);
    END
$$;

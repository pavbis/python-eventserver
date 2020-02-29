import json
from eventsserver.value.objects import ProvidesAggregatedJson, AggregatedJson, EmptyJson
from eventsserver.rdbms.connection import Connection


class ProvidesStatistics:
    def events_stats(self) -> ProvidesAggregatedJson:
        raise NotImplementedError

    def stream_stats(self) -> ProvidesAggregatedJson:
        raise NotImplementedError

    def streams_chart_stats(self) -> ProvidesAggregatedJson:
        raise NotImplementedError


class PostgreSqlStatisticsStorage(ProvidesStatistics):
    def __init__(self, connection: Connection):
        self.__connection = connection

    def events_stats(self) -> ProvidesAggregatedJson:
        with self.__connection.cursor() as cursor:
            cursor.execute('''WITH events_per_day AS (
                SELECT
                    CAST(calendar.entry as date) as date,
                    COALESCE(COUNT("eventId"), 0) as eventCount
                FROM
                    generate_series(
                        date_trunc('month', current_date),
                        date_trunc('month', current_date) + interval '1 month' - interval '1 day',
                        interval '1 day'
                    ) as calendar(entry)
                LEFT JOIN events ON CAST(events."createdAt" as date) = calendar.entry
                GROUP BY calendar.entry
                ORDER BY calendar.entry
            )

            SELECT json_agg(json_strip_nulls(row_to_json(t)))
            FROM (
                SELECT date, eventCount,
                    CASE
                        WHEN LAG(eventCount, 1)
                            OVER (order by date) IS NULL
                            THEN ''
                            
                        WHEN eventCount - LAG(eventCount, 1)
                            OVER (ORDER BY date) = 0
                            THEN ''
                
                        WHEN eventCount - lag(eventCount, 1)
                            OVER (ORDER BY date) < 0
                            THEN FORMAT('-%3s',
                                LAG(eventCount, 1)
                                OVER (ORDER BY date)
                                - eventCount)
                
                        ELSE FORMAT('+%3s',
                            eventCount - LAG(eventCount, 1) OVER (ORDER BY date))
                        END AS progress
                 FROM events_per_day
             ) t''')

            row = cursor.fetchone()

            return AggregatedJson(json.dumps(row[0]))

    def stream_stats(self) -> ProvidesAggregatedJson:
        with self.__connection.cursor() as cursor:
            cursor.execute('''SELECT json_agg(json_strip_nulls(row_to_json(q)))
            FROM (
                SELECT
                    pSR."streamName" as label,
                    COUNT(e) as value
                FROM "producerStreamRelations" pSR
                LEFT JOIN events e USING("streamName")
                GROUP BY pSR."streamName"
                ORDER BY value DESC
                LIMIT 10
             ) q''')

            row = cursor.fetchone()

            if row is None:
                return EmptyJson()

            return AggregatedJson(json.dumps(row[0]))

    def streams_chart_stats(self) -> ProvidesAggregatedJson:
        with self.__connection.cursor() as cursor:
            cursor.execute('''WITH number_of_events as
            (
                SELECT pSR."streamName",
                    COALESCE(e.eventscount, 0) AS "eventsCount",
                    COALESCE(cOF."countConsumedEvents", 0) AS "consumedEvents"
                FROM "producerStreamRelations" pSR
                LEFT JOIN (
                    SELECT
                        COUNT(1) AS eventscount,
                        "streamName" AS "streamName"
                    FROM events e
                    GROUP BY e."streamName"
                ) AS e USING ("streamName")
                LEFT JOIN (
                    SELECT
                        SUM("offset") AS "countConsumedEvents",
                        "streamName"
                    FROM "consumerOffsets"
                    GROUP BY "consumerOffsets"."streamName"
                ) AS cOF USING ("streamName")
                ORDER BY pSR."streamName" DESC
            )            
    
            SELECT json_agg(json_strip_nulls(row_to_json(q)))
            FROM (
                SELECT
                    "streamName",
                    "eventsCount",
                    "consumedEvents",
                    repeat(
                        text '✭',
                        ranking("eventsCount", (SELECT array_agg("eventsCount") FROM number_of_events), 5)
                    ) as ranking
                FROM number_of_events
             ) q''')

            row = cursor.fetchone()

            if row is None:
                return EmptyJson()

            return AggregatedJson(json.dumps(row[0]))

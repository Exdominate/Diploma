import psycopg2
from psycopg2 import sql
import json

stops = None
with open('stopsNew.json', 'r') as file:
    stops = json.load(file)

conn = psycopg2.connect(dbname='server_main', user='postgres',
                        password='14011999ok', host='localhost')

with conn.cursor() as cursor:
    for i in range(len(stops)):
        stops_name = stops[i]['stopName']
        stops_latitude = stops[i]['latLng']['latititude']
        stops_longitude = stops[i]['latLng']['longitude']
        stmt = sql.SQL('''INSERT INTO route_stop  VALUES ({id},'{stopName}',{latitude},{longitude})'''.format(id=i + 1,
                                                                                                              stopName=stops_name,
                                                                                                              latitude=stops_latitude,
                                                                                                              longitude=stops_longitude))
        cursor.execute(stmt)
        conn.commit()

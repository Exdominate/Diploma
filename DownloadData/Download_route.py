import psycopg2
from psycopg2 import sql
import json


routes = None
with open('routesNew.json', 'r') as file:
    routes = json.load(file)

# conn = psycopg2.connect(dbname='server_main', user='admin',
#                         password='anna030499', host='localhost')
#
# data = None
# with conn.cursor() as cursor:
#     cursor.execute('Select * from route_stop')
#     data = cursor.fetchall()
# routesNew = routes
# for i in range(len(routes['routes'])):
#     for j in range(len(routes['routes'][i]['stops'])):
#         routes['routes'][i]['stops'][j].pop('latLng')
#
# for i in range(len(routes['routes'])):
#     for j in range(len(routes['routes'][i]['stops'])):
#         for q in data:
#             if routes['routes'][i]['stops'][j]['idStop'] == q[0]:
#                 routes['routes'][i]['stops'][j].update({"latititude": q[2]})
#                 routes['routes'][i]['stops'][j].update({"longitude": q[3]})
# with open('routesNew.json', 'w') as file:
#     json.dump(routes, file)
# Добавления поля id в routes.json из базы данных, таблицы route_stops
#
# data = None
# with conn.cursor() as cursor:
#     cursor.execute('Select * from route_stop')
#     data = cursor.fetchall()
# for q in range(len(routes['routes'])):
#     for i in range(len(routes['routes'][q]['stops'])):
#         for j in data:
#             if (routes['routes'][q]['stops'][i]['latLng']['latititude'] == j[2]) and (routes['routes'][q]['stops'][i]['latLng']['longitude'] == j[3]):
#                 routes['routes'][q]['stops'][i].update({'idStop':j[0]})
#                 break

# s = str(routes['routes'][0]['stops'])
# s = s.replace('{','\'{')
# s.replace('}','}\'')


conn = psycopg2.connect(dbname='server_main', user='postgres',
                        password='14011999ok', host='localhost')
with conn.cursor() as cursor:
    for i in range(len(routes['routes'])):
        routName = routes['routes'][i]['routeName']
        buNumber = routes['routes'][i]['busNumber']
        stop = str(routes['routes'][i]['stops'])
        stop = stop.replace('\'','\"')
        stop = stop.replace('[','\'[')
        stop = stop.replace(']',']\'')
        s = sql.SQL(
            '''INSERT INTO route_route VALUES ({id},'{routeName}',{busNumber},{Stops})'''.format(id=i + 1,
                                                                                                     routeName=routName,
                                                                                                     busNumber=buNumber,
                                                                                                     Stops=stop
                                                                                                     ))

        cursor.execute(s)
        conn.commit()

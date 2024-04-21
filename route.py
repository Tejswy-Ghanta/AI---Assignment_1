#!/usr/local/bin/python3
# route.py : Find routes through maps
#
# Code by: Sri_Harsha_Vardhan_Prattipati IU ID- 2000932548
#
# Based on skeleton code by V. Mathur and D. Crandall, January 2021
#


# !/usr/bin/env python3
import math 
import sys
import csv
import heapq
#calculating time for delivery
def cal_del_time(speed,time,dist):
    delivery_time=0
    if int(speed)>50: delivery_time = delivery_time = delivery_time + float(time) + math.tanh(int(dist)/1000)*2*(float(time)+ delivery_time)
    else: delivery_time = delivery_time + float(time) 
    return delivery_time    
#calculating time 
def cal_time(distance,speed):
    return float(distance)/float(speed)
lst3=[]
def path(i):
    lst3.append(i)
    return lst3
# Funtion to find successors with least astar values
def findSucc(node, road):
    lst2=[]
    for i in road:
        if i[0]== node[1]:
            h = euclidian(node[1],i[1]) if euclidian(node[1],path(i[1])) else 0
            route_taken=node[6]
            route_taken = route_taken +[(i[1],"{} for {} miles".format(i[5],int(i[2])))]
            lst2.append((h,i[1],node[2]+1,node[3]+i[2],node[4]+cal_time(i[2],i[4]),node[5]+cal_del_time(i[4],node[4],i[2]),route_taken))

        if i[1] == node[1]:
            h = euclidian(node[1],i[0]) if euclidian(node[1],i[0]) else 0
            route_taken=node[6]
            route_taken = route_taken +[(i[0],"{} for {} miles".format(i[5],int(i[2])))]
            lst2.append((h,i[0],node[2]+1,node[3]+i[2],node[4]+cal_time(i[2],i[4]),node[5]+cal_del_time(i[4],node[4],i[2]),route_taken))
    return lst2

# Function to find euclidian distance between cities
def euclidian(start,end):  
    with open('city-gps.txt', newline='') as csvfile:
        datareader = csv.reader(csvfile, delimiter=' ')
        distance = []
        for i in datareader:
            #print(i)
            if(len(distance)==4):
                return math.sqrt((float(distance[0])-float(distance[2]))**2 +(float(distance[1])-float(distance[3]))**2)
            if((i[0])==start or (i[0]==end)):
                distance.append(float(i[1]))
                distance.append(float(i[2]))

def get_route(start,end,cost):
    cost_index = 1
    if(cost == 'segments'):
        cost_index = 2
    if(cost == 'distance'):
        cost_index = 3
    if(cost == 'time'):
        cost_index = 4
    if(cost == 'delivery'):
        cost_index = 4
 # since delivery has to chosen with respect to fast route we considers time itself as cost function
    lst = []
    queue=[]
    with open('road-segments.txt', newline='') as csvfile:
        datareader = csv.reader(csvfile, delimiter=' ')
        for row in datareader:
            add = (row[0],row[1],float(row[2]),1,float(row[3]),row[4])
            lst.append(add)
    explored=[]
    time = delivery_time = astar = heuristic = segments = distance = way=0
    route_taken = []
# design payload for successors
    x = (astar,(heuristic,start,segments,distance, time, delivery_time, route_taken, way))
    heapq.heappush(queue, x)
    while queue:

        s1 = heapq.heappop(queue)[1]
        succ = findSucc(s1,lst)
        for succss in succ:
            #print(succss)
            if (succss[1] == end):
                return {
                    "total-segments":succss[2],
                    "total-miles":succss[3],
                    "total-hours": succss[4],
                    "total-delivery-hours": succss[5],
                    "route-taken": succss[6]
                    }
            else:
               if succss[1]  not in explored:
                    if(succss[0]):
                        astar = succss[0] + succss[cost_index]
                        #astar = succss[cost_index]
                    else:
                        #print(succss)
                        astar = succss[cost_index]
                    explored.append(succss[1])
                    heapq.heappush(queue,[astar,succss])      
if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise(Exception("Error: expected 3 arguments"))

    (_, start_city, end_city, cost_function) = sys.argv
    if cost_function not in ("segments", "distance", "time", "delivery"):
        raise(Exception("Error: invalid cost function"))

    result = get_route(start_city, end_city, cost_function)
    
    print("Start in %s" % start_city)
    for step in result["route-taken"]:
        print("   Then go to %s via %s" % step)

    print("\n          Total segments: %4d" % result["total-segments"])
    print("             Total miles: %8.3f" % result["total-miles"])
    print("             Total hours: %8.5f" % result["total-hours"]) 
    print("Total hours for delivery: %8.3f" % result["total-delivery-hours"])

#!/usr/local/bin/python3
# assign.py : Assign people to teams
#
# Code by: lghanta
#
# Based on skeleton code by D. Crandall and B551 Staff, September 2021
#

import sys
import random
import itertools

def size_violation(person,data,team):
    #check person's team size preference from data & check with team's size - then return 2 else 0
    person_index = data[0].index(person)
    g_size = data[3][person_index]

    if len(team) != g_size:
        return 2
    return 0 

def st_req_not_assigned(person,data,team):
    #check person's requested list - if not in team - then return 3 else 0
    person_index = data[0].index(person)
    cost = 0

    for i in data[1][person_index]:
        if i not in team and i != 'xxx' and i!='zzz':
            cost = cost + 3

    return cost

def st_assigned_not_to_work(person,data,team):
    #check person's not-to-work with list - if in team - then return 10 else 0
    person_index = data[0].index(person)
    cost = 0

    for i in data[2][person_index]:
        if i in team:
            cost = cost + 10

    return cost

def compute_team_cost(team,data):
    total_cost = 0
    #find the total cost for the team and return the value
    for i in team:
        for k in range(len(i)):
            person = i[k]
            total_cost = total_cost + st_req_not_assigned(person,data,i) + st_assigned_not_to_work(person,data,i) + size_violation(person,data,i)

    return total_cost+(5*len(team))

def solver(input_file):
    """
    1. This function should take the name of a .txt input file in the format indicated in the assignment.
    2. It should return a dictionary with the following keys:
        - "assigned-groups" : a list of groups assigned by the program, each consisting of usernames separated by hyphens
        - "total-cost" : total cost (time spent by instructors in minutes) in the group assignment
    3. Do not add any extra parameters to the solver() function, or it will break our grading and testing code.
    4. Please do not use any global variables, as it may cause the testing code to fail.
    5. To handle the fact that some problems may take longer than others, and you don't know ahead of time how
       much time it will take to find the best solution, you can compute a series of solutions and then
       call "yield" to return that preliminary solution. Your program can continue yielding multiple times;
       our test program will take the last answer you 'yielded' once time expired.
    """
    persons = []
    preferred_teammates =[]
    not_preferred_teammates = []
    preferred_teamsizes = []
    data = []
    
    with open(input_file, 'r') as file:
        input_data = file.readlines()
    
    input_data = [i.strip().split() for i in input_data]
    
    for j in range(0,len(input_data)):
        persons.append(input_data[j][0])
        preferred_teammates.append(input_data[j][1].split('-'))
        not_preferred_teammates.append(input_data[j][2].split(','))
        preferred_teamsizes.append(len(input_data[j][1].split('-')))

    data.append(persons)
    data.append(preferred_teammates)
    data.append(not_preferred_teammates)
    data.append(preferred_teamsizes)

    final_teams = []
    size = len(data[0])
    
    all_permutations = []
    atleast_cost = 100000

    k = size
   
    while k > 0:
        for c in itertools.combinations_with_replacement([1,2,3],k):
            if max(c)<=3 and sum(c) == size:
                all_permutations.append(c)
        k = k-1

    size_1_teams = data[0].copy()
    size_2_teams = []
    size_3_teams = []

    #get teams with size 2
    for i in range(0,len(size_1_teams)):
        for j in range(i+1,len(size_1_teams)):
            size_2_teams.append([size_1_teams[i],size_1_teams[j]])
   
    #get teams with size 3
    for i in range(0,len(size_1_teams)):
        for j in range(i+1,len(size_1_teams)):
            for k in range(j+1,len(size_1_teams)):
                size_3_teams.append([size_1_teams[i],size_1_teams[j],size_1_teams[k]])

    # print(size_1_teams)
    # print(size_2_teams)
    # print(size_3_teams)

    dummy_team1 = size_1_teams.copy()
    dummy_team2 = size_2_teams.copy()
    dummy_team3 = size_3_teams.copy()
    
    while True:
        random.shuffle(dummy_team1)
        random.shuffle(dummy_team2)
        random.shuffle(dummy_team3)
        
        #get the possible combinations and compute costs
      
        for each_c in all_permutations:
            # print(each_c)
            visited_list = [0 for _ in range(size)]
            tobe_team = [[] for _ in range(len(each_c))]
            team_1 = dummy_team1.copy()
            team_2 = dummy_team2.copy()
            team_3 = dummy_team3.copy()
            final_teams.clear()

            for i in range(len(each_c)):
                if each_c[i] == 1 :
                    can_be_added =[]
                    # size 1 team

                    for t1 in team_1:
                        if visited_list[data[0].index(t1)] == 0:
                            can_be_added.append(t1)
                    
                    add_t1 = can_be_added.pop()
                    visited_list[data[0].index(add_t1)] = 1

                    tobe_team[i].append(add_t1)

                elif each_c[i] == 2 or each_c[i] == 3:
                    # size 2 and 3 team
                    can_be_added.clear()
                    to_iterate = []
                    if each_c[i] == 2:
                        to_iterate = team_2
                    else:
                        to_iterate = team_3
                    
                    for t2 in to_iterate:
                        t_can_be_added = True
                        for e in t2:
                            
                            if visited_list[data[0].index(e)] != 0:
                                t_can_be_added = False
                                break
                            
                        if t_can_be_added :
                            
                            for y in t2: 
                                visited_list[data[0].index(y)] = 1
                                tobe_team[i].append(y)
                            
                            break

            l_cost = compute_team_cost(tobe_team,data)
           
            g_size = 0
            
            for groups in tobe_team:
                g_size = g_size+len(groups)
            if g_size == size:
                for groups in tobe_team:
                    final_teams.append('-'.join(groups))
               
            if l_cost < atleast_cost:
                yield({"assigned-groups": final_teams, "total-cost" : l_cost})
                atleast_cost = l_cost

if __name__ == "__main__":
    #python3 assign.py test1.txt 
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected an input filename"))

    for result in solver(sys.argv[1]):
        print("----- Latest solution:\n" + "\n".join(result["assigned-groups"]))
        print("\nAssignment cost: %d \n" % result["total-cost"])
    

#!/usr/local/bin/python3
# solver2021.py : 2021 Sliding tile puzzle solver
#
# Code by: Shruthi Gutta IU ID
#
# Based on skeleton code by D. Crandall & B551 Staff, September 2021
#

from os import pathsep
import sys
import heapq
from copy import deepcopy

ROWS=5
COLS=5

def printable_board(board):
    return [ ('%3d ')*COLS  % board[j:(j+COLS)] for j in range(0, ROWS*COLS, COLS) ]

#This function is used to calculate successor states by performing row left on each row by taking two inputs; state and number of the row
def row_left(r,n):
    r=list(r[0])
    if n==0:
        t=r[0]
        for i in range(0,ROWS-1):
            r[i]=r[i+1]
        r[ROWS-1]=t
        return (tuple(r),'L1 ')
    if n==1:
        t=r[ROWS]
        for i in range(5,9):
            r[i]=r[i+1]
        r[ROWS+4]=t
        return (tuple(r), 'L2 ')
    if n==2:
        t=r[10]
        for i in range(10,14):
            r[i]=r[i+1]
        r[14]=t
        return (tuple(r),'L3 ')  
    if n==3:
        t=r[15]
        for i in range(15,19):
            r[i]=r[i+1]
        r[19]=t
        return (tuple(r),'L4' )  
    if n==4:
        t=r[20]
        for i in range(20,24):
            r[i]=r[i+1]
        r[24]=t
        return (tuple(r),'L5 ')
        
#This function is used to calculate successor states by performing row right on each row by taking two inputs; state and number of the row
def row_right(r,n):
    r=list(r[0])
    if n==0:
        t=r[4]
        for i in range(3,-1,-1):
            r[i+1]=r[i]
        r[0]=t
        return (tuple(r),'R1 ')
    if n==1:
        t=r[9]
        for i in range (8,4,-1):
            r[i+1]=r[i]
        r[5]=t
        return(tuple(r),'R2 ')
    if n==2:
        t=r[14]
        for i in range(13,9,-1):
            r[i+1]=r[i]
        r[10]=t
        return (tuple(r),'R3 ')
    if n==3:
        t=r[19]
        for i in range (18,14,-1):
            r[i+1]=r[i]
        r[15]=t
        return(tuple(r),'R4 ')
    if n==4:
        t=r[24]
        for i in range (23,19,-1):
            r[i+1]=r[i]
        r[20]=t
        return(tuple(r),'R5 ')

#This function is used to calculate successor states by performing row up on each column by taking two inputs; state and number of the column
def col_up(r,n):
    r=list(r[0])
    if n==0:
        t=r[0]
        for i in range(0,20,5):
            r[i]=r[i+5]
        r[20]=t
        return(tuple(r),'U1 ')
    if n==1:
        t=r[1]
        for i in range(1,21,5):
            r[i]=r[i+5]
        r[21]=t
        return(tuple(r),'U2 ')
    if n==2:
        t=r[2]
        for i in range(2,22,5):
            r[i]=r[i+5]
        r[22]=t
        return(tuple(r),'U3 ')
    if n==3:
        t=r[3]
        for i in range(3,23,5):
            r[i]=r[i+5]
        r[23]=t
        return(tuple(r),'U4 ')
    if n==4:
        t=r[4]
        for i in range(4,24,5):
            r[i]=r[i+5]
        r[24]=t
        return(tuple(r),'U5 ') 

#This function is used to calculate successor states by performing column down on each row by taking two inputs; state and number of the column
def col_down(r,n):
    r=list(r[0])
    if n==0:
        t=r[20]
        for i in range(20,0,-5):
            r[i]=r[i-5]
        r[0]=t
        return(tuple(r),'D1 ')
    if n==1:
        t=r[21]
        for i in range(21,1,-5):
            r[i]=r[i-5]
        r[1]=t
        return(tuple(r),'D2 ')
    if n==2:
        t=r[22]
        for i in range(22,2,-5):
            r[i]=r[i-5]
        r[2]=t
        return(tuple(r),'D3 ')
    if n==3:
        t=r[23]
        for i in range(23,3,-5):
            r[i]=r[i-5]
        r[3]=t
        return(tuple(r),'D4 ')
    if n==4:
        t=r[24]
        for i in range(24,4,-5):
            r[i]=r[i-5]
        r[4]=t
        return(tuple(r),'D5 ')

#This function is used to calculate successor state by rotating outer ring in clockwise direction
def out_c(state_old):
    r=0
    rows=4
    c=0
    cols=4
    final=[]
    state_old=list(state_old[0])
    state=[state_old[i:i + 5] for i in range(0, 25, 5)]
    past = state[c+1][r]

    # Move elements of c row one step rows
    for i in range(r, rows+1):
        present = state[c][i]
        state[c][i] = past
        past = present
    c += 1

    # Move elements of rowsmost column one step downwards
    for i in range(c, cols+1):
        present = state[i][rows]
        state[i][rows] = past
        past = present
    rows -= 1

    # Move elements of cols row one step r
    for i in range(rows, r-1, -1):
        present = state[cols][i]
        state[cols][i] = past
        past = present
    cols -= 1

    # Move elements of rmost column one step upwards
    for i in range(cols, c-1, -1):
        present = state[i][r]
        state[i][r] = past
        past = present
    r += 1
    for i in state:
        for j in i:
            final.append(j)

    return (tuple(final),'Oc ')

#This function is used to calculate successor state by rotating outer ring in counterclockwise direction
def out_cc(state_old):
    r=0
    rows=4
    c=0
    cols=4
    final=[]
    state_old=list(state_old[0])
    state=[state_old[i:i + 5] for i in range(0, 25, 5)]
    past = state[r][c+1]

    for i in range(r, rows+1):
        present=state[i][c]
        state[i][c] = past
        past= present
    c += 1

    for i in range(c, cols+1):
        present=state[rows][i]
        state[rows][i] = past
        past= present
    rows -= 1

    for i in range(rows, r-1, -1):
        present=state[i][cols]
        state[i][cols] = past
        past = present
    cols -= 1

    for i in range (cols,c-1, -1 ):
        present=state[r][i]
        state[r][i] = past
        past = present
    r += 1

    for i in state:
        for j in i:
            final.append(j)

    return (tuple(final),'Occ ')

#This function is used to calculate successor state by rotating inner ring in clockwise direction
def in_c(state_old):
    r=1
    rows=3
    c=1
    cols=3
    final=[]
    state_old=list(state_old[0])
    state=[state_old[i:i + 5] for i in range(0, 25, 5)]
    past = state[c+1][r]

    for i in range(r, rows+1):
        present = state[c][i]
        state[c][i] = past
        past = present
    c += 1

    for i in range(c, cols+1):
        present = state[i][rows]
        state[i][rows] = past
        past = present
    rows -= 1

    for i in range(rows, r-1, -1):
        present = state[cols][i]
        state[cols][i] = past
        past = present
    cols -= 1

    for i in range(cols, c-1, -1):
        present = state[i][r]
        state[i][r] = past
        past = present
    r += 1
    for i in state:
        for j in i:
            final.append(j)

    return (tuple(final),'Ic ')

#This function is used to calculate successor state by rotating inner ring in counterclockwise direction
def in_cc(state_old):
    r=1
    rows=3
    c=1
    cols=3
    final=[]
    state_old=list(state_old[0])
    state=[state_old[i:i + 5] for i in range(0, 25, 5)]
    past = state[r][c+1]

    for i in range(r, rows+1):
        present=state[i][c]
        state[i][c] = past
        past= present
    c += 1

    for i in range(c, cols+1):
        present=state[rows][i]
        state[rows][i] = past
        past= present
    rows -= 1

    for i in range(rows, r-1, -1):
        present=state[i][cols]
        state[i][cols] = past
        past = present
    cols -= 1

    for i in range (cols,c-1, -1 ):
        present=state[r][i]
        state[r][i] = past
        past = present
    r += 1

    for i in state:
        for j in i:
            final.append(j)

    return (tuple(final),'Icc ')
 

#This function is used to calculate manhatten distance between goal state and given state
def manhatten(next_state):
    next_state=list(next_state)
    state=[[] for _ in range(5)]
    k=0
    for i in range(0,5):
        for j in range(0,5):
            state[i].append(next_state[k])
            k=k+1
    goal={1:(0,0),2:(0,1),3:(0,2),4:(0,3),5:(0,4),6:(1,0),7:(1,1),8:(1,2),9:(1,3),10:(1,4),11:(2,0),12:(2,1),13:(2,2),14:(2,3),15:(2,4),16:(3,0),17:(3,1),18:(3,2),19:(3,3),20:(3,4),21:(4,0),22:(4,1),23:(4,2),24:(4,3),25:(4,4)}
    next={}
    sum=0

    for i in range(0,ROWS):
        for j in range (0,COLS):
            next[state[i][j]]=(i,j)
    for i in goal.keys():
       for j in next.keys():
            if i==j:
                sum=sum + abs(goal[i][0] - next[j][0]) + abs(goal[i][1] - next[j][1])
    return(sum)
    

# return a list of possible successor states
def successors(state):
    state=deepcopy(state)
    states=[]
    states=state[1]
    next_state=states[0]
    path_name=states[1]
    gs=states[2]
    hs=states[3]
    y1=[]
    
#Returns successors of five rows to left
    for i in range (0,5): 
        succ=row_left(state[1],i)
        staten=succ[0]
        pathn=succ[1]
        pathn=deepcopy(path_name)+ pathn
        hsn=manhatten(staten)
        y1.append((staten,pathn,gs+1,hsn))

#Returns successors of five rows to right
    for i in range (0,5): 
        succ=row_right(state[1],i)
        staten=succ[0]
        pathn=succ[1]
        pathn=deepcopy(path_name)+ pathn
        hsn=manhatten(staten)
        y1.append((staten,pathn,gs+1,hsn))

#Returns successors of five columns to down
    for i in range (0,5): 
        succ=col_down(state[1],i)
        staten=succ[0]
        pathn=succ[1]
        pathn=deepcopy(path_name)+ pathn
        hsn=manhatten(staten)
        y1.append((staten,pathn,gs+1,hsn))

#Returns successors of five columns to up
    for i in range (0,5): 
        succ=col_up(state[1],i)
        staten=succ[0]
        pathn=succ[1]
        pathn=deepcopy(path_name)+ pathn
        hsn=manhatten(staten)
        y1.append((staten,pathn,gs+1,hsn))

#Returns successor of rotating Outer loop clockwise 
    succ=out_c(state[1])
    staten=succ[0]
    pathn=succ[1]
    pathn=deepcopy(path_name)+ pathn
    hsn=manhatten(staten)
    y1.append((staten,pathn,gs+1,hsn))

#Returns successor of rotating Outer loop counterclockwise 
    succ=out_cc(state[1])
    staten=succ[0]
    pathn=succ[1]
    pathn=deepcopy(path_name)+ pathn
    hsn=manhatten(staten)
    y1.append((staten,pathn,gs+1,hsn))

#Returns successor of rotating Inner loop clockwise 
    succ=in_c(state[1])
    staten=succ[0]
    pathn=succ[1]
    pathn=deepcopy(path_name)+ pathn
    hsn=manhatten(staten)
    y1.append((staten,pathn,gs+1,hsn))

#Returns successor of rotating Inner loop counterclockwise 
    succ=in_cc(state[1])
    staten=succ[0]
    pathn=succ[1]
    pathn=deepcopy(path_name)+ pathn
    hsn=manhatten(staten)
    y1.append((staten,pathn,gs+1,hsn))
   
    return y1


# check if we've reached the goal
def is_goal(state):
    goal=(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25)
    if state==goal:
        return True
    else:
        return False


def solve(initial_board):
    #if is_goal(initial_board): return []
    fringe=[]
    path=''
    ds=0
    hs=0
    heapq.heappush(fringe,(ds+hs,(initial_board,path,ds,hs)))
    while fringe:
        state = heapq.heappop(fringe)
        s=state[1]  
        for succ in successors(state):
            if is_goal(s[0]):
                result = succ[1].split(' ')
                return result[:-2]
                #return succ[1]
            else:
                heapq.heappush(fringe,((succ[2]+succ[3]),succ))


# Please don't modify anything below this line
#
if __name__ == "__main__":
    if(len(sys.argv) != 2):
        raise(Exception("Error: expected a board filename"))

    start_state = []
    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [ int(i) for i in line.split() ]

    if len(start_state) != ROWS*COLS:
        raise(Exception("Error: couldn't parse start state file"))

    print("Start state: \n" +"\n".join(printable_board(tuple(start_state))))

    print("Solving...")
    route = solve(tuple(start_state))
    
    print("Solution found in " + str(len(route)) + " moves:" + "\n" + " ".join(route))

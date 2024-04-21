**Part 1: The 2021 Puzzle**

Description: The main objective of the code is to solve a scattered 25(5*5) tile puzzle in least possible moves. The possible moves can be the following
. Sliding any row of the puzzle one step right
. Sliding any row of the puzzle one step left
. Sliding any column of the puzzle one step right
. Sliding any column of the puzzle one step left
. Rotating the outer ring of the puzzle clockwise direction
. Rotating the outer ring of the puzzle counterclockwise direction
. Rotating the inner ring of the puzzle clockwise direction
. Rotating the inner ring of the puzzle counterclockwise direction

Start Space: The start space is the 25 tile puzzle scattered with numbers without any empty tile in it.

Goal Space: The goal space is to form a 5*5 tiles with consecutive numbers from 1 to 25

Successor: Successor Function returns all the spaces after performing all the possible moves on the input space give to that function. There are 24possible spaces which includes
1.  Moving first row left
2. Moving second row left
3. Moving third row left
4. Moving fourth row left
5. Moving fifth row left
6.  Moving first row right
7. Moving second row right
8. Moving third row right
9. Moving fourth row right
10. Moving fifth row right
11.  Moving first column up
12. Moving second column up
13. Moving third column up
14. Moving fourth column up
15. Moving fifth column up
16.  Moving first column down
17. Moving second column down
18. Moving third column down
19. Moving fourth column down
20. Moving fifth column down
21. Rotating the outer ring of the puzzle clockwise direction
22. Rotating the outer ring of the puzzle counterclockwise direction
23. Rotating the inner ring of the puzzle clockwise direction
24. Rotating the inner ring of the puzzle counterclockwise direction



Cost: Cost of the algorithm is f=g+h
g = the movement cost to move from the starting point to a given square on the grid, following the path generated to get there. 
h = the estimated movement cost to move from that given square on the grid to the final destination. 

Heuristic: Heuristic function returns the sum of Manhattan distances between each tile to its destination tile of the given space.

Search Algorithm: This code flows through A* algorithm where it checks at each state and chooses the following successor function on based of value of f=g+h. At each state, it picks the successor which has lowest value of f. Here g is the distance of the move from starting to the successive state and h is the calculated Manhattan distance between given state and final state. So, here I have considered g =1 for every move it moves and h=manhatten distance.


1. In this problem, what is the branching factor of the search tree? 
	
The branching factor of this each tree is 24 because we need to choose one among the 24 successive states for each move. Those 24 possible branching states are listed above.

2. If  the  solution  can  be  reached  in  7  moves,  about  how  many  states  would  we  need  to  explore  before  we
found it if we used BFS instead of A* search?  
	
If BFS is used, the total number of states needed to reach goal are b to the power d; that is the 24 to the power 7, which is equal to 4.58 billion


**Part 2: Road trip!**

State Space - routes between cities in united states of America

Successor Function - cities which are connected to start city and next.

Cost Function - Segments, distance, time, delivery hours.

Initial State - Start city.

Goal State - End city

Implementation -
Started the code by implementing adjacent lists but found out that all citities and connected cities are given already with speed highway and distance between citites parsed the road segments into a list. Using this list we took successors cities(connected cities) from start cities and found the successors of successors by implementing a priority queue. This queue pops out city into a fringe with least Astar + given cost function. Astar value is the Euclidian distance between city and parent city.Now the code repeats in loop to get all successors of successors till we find the end city. Once the end city is found it gives the path based on cost function entered and its values of segments, time, delivery, time according to cost function. 


**Part 3: Choosing teams**

(1)Description - 
Each student gives their preferences that include preferred team size, preferred team members and students they do not want to work with.

(2)State space - 
Consider combinations possible with the number of people to put into teams. For example, if 6 members need to be put into teams, the possible states to be considered include - (1,1,1,1,1,1),(1,1,1,1,2),(1,1,2,2),(1,2,3) (maximum team size is 3)
Possible teams are formed such that all students are placed in some or other team to form combinations. All these states are put into state space for search. 

Initial state - Randomly generated combination of people

(3)Successor function -
Team that has least cost based on time computed on different parameters like - requested team mates not assigned, group size assigned is not same as group size requested is chosen to be explored next.

Edge weights -
Every team combination has equal chance to be formed but cost - time to be spent because of the team decides whether the team can be finalised or not based on other available teams.

(4)Cost - 
Cost is computed based on the following parameters:
- If student's requested group size is not same as assigned group size, it adds up 2 minutes
- If student is assigned team members who are not same as requested team members, then for each violation, 3 minutes (5% of 60 minutes) gets added to the cost
- If student who is assigned to someone they requested not to work with, it costs 10 minutes extra for each violation
- Final cost is sum of all the above violations + number of teams * 5 minutes to correct the assignment 

(5)Goal state -
Find the least cost team combination in reasonable amount of time 
Heuristic -
Sum of all cost violations defined in cost function acts as the heuristic to decide the best combination among the available states.

(6) Search algorithm -
Depending on the number of persons to be teamed up, generate all the combinations using 'iter' module method. Randomly shuffle the teams (teams with size 1,2,3) to be picked to make it more time efficient. Then based on the generated combination, arrange persons in the teams accordingly. Use visited list to make sure same person is not added into multiple teams. Compute the cost function and yield the team combination. Keep yielding the teams along with the cost if a better cost effective team is found. 

(7) Assumptions, simplifications, design decisions -
Started off with thinking how to prune the state space based on the cost function and team preferences to avoid checking of all the possible team combinations which turned out not to be working. Completely rearranging the teams without taking into account the team preferences worked in finding the least cost combination. This seems to work like 'Local search' as there is no path to trace back or remember how the goal state is reached instead it is an arrrangement that is both cost and time effective. Hence, exploring all the nearest neighbbors and picking the one with minimal cost will drive to the solution eventually. It is not possible to guess the combination ahead based on the cost without exploring all the states.

The cost function is based on all the parameters given in the question. There are no alternative cost functions available to compare or choose from to comment whether the cost function is admissible or not. As there is only one cost function, the given function is admissible heuristic for computing the least cost combination on teams.

"""
@author: Supreeth Dhareshwar
"""

import os
import numpy as np

num_process = 0
wait_msg = []
msg_count = []

#Deadlock count; call to check for knot if only 2 or more deadlock cycles are present
num_deadlock = 0
#Knot count;
num_knot = 0

#Deadlock flag
deadlock_flag = False

#Path to input source file
resources_path = os.path.join(os.getcwd(), 'input.txt')

#Read the input file as a 2D WFG
def readInput():
    fp = open(file = resources_path, mode= "r", encoding="utf8")
    array2D = [[int(num) for num in line.split(',')] for line in fp if line.strip() != "" ]
    return array2D

#Display the read input in a specific format and also count message and wait status for each process
def displayGraph(array2D):
    global num_process, wait_msg,msg_count

    print("", end = '\t')
    for i in range(num_process):
        print("P"+str((i+1)), end = '\t')

    print("")	
    for i in range(num_process):
        print("P"+str((i+1)), end = '\t')
        for j in range(num_process):
            print(str(array2D[i][j]), end = '\t')
            if (array2D[i][j] == 1):
                msg_count[i] += 1
                wait_msg[i] = True
        print("")	    
	
    return

#General function for displaying formatted input in proper format
def displayLine(initProcess,destProcess,probeI,probeJ,probeK,msgCount,waitStatus,statusMsg):
    print("P" + initProcess + " --> P" + destProcess+ "\t(" +  probeI +  "," + probeJ + "," + probeK + ") \t" + msgCount  + " \t"+ waitStatus + " \t" + statusMsg)

#Contains logic for engaging query initiated by a process
def engaging_query(array2D, init, dest):
    global num_process, deadlock_flag,num_deadlock	
    for col in range(num_process):
        if array2D[dest][col] == 1 :
            if (init == col):
                displayLine(str(dest + 1),str(col + 1),str(init + 1),str(dest + 1),str(col + 1), str(msg_count[dest]),str(wait_msg[dest]),"DEADLOCK DETECTED" )
                deadlock_flag = True
                num_deadlock = num_deadlock + 1
                break
                            
            displayLine(str(dest + 1),str(col + 1),str(init + 1),str(dest + 1),str(col + 1), str(msg_count[dest]),str(wait_msg[dest]),"")
            engaging_query(array2D, init, col)
		
#Contains logic for replying back to intiating process	
def reply_query(array2D,  init,  dest):
    global num_process, msg_count,wait_msg,num_knot	

    col = num_process - 1
    while col >= 0:
        if array2D[col][dest] == 1 :
            if msg_count[dest] != 0:
                msg_count[dest] -= 1
            if msg_count[dest] == 0:
                wait_msg[dest] = False
            if init == col:
                displayLine(str(dest + 1),str(col + 1),str(init + 1),str(dest + 1),str(col + 1), str(msg_count[dest]),str(wait_msg[dest]),"KNOT DETECTED")
                num_knot += 1

                if wait_msg[dest] == False and msg_count[dest] == 0:
                    break

            if msg_count[dest] == 0 and wait_msg[dest] == False :
                array2D[col][dest] = 0
                            
            displayLine(str(dest + 1),str(col + 1),str(init + 1),str(dest + 1),str(col + 1), str(msg_count[dest]),str(wait_msg[dest]),"")
            reply_query(array2D, init, col)

        col -= 1

#General logic that initates deadlock detection from initial process probe
def detectDeadlock(array2D):
    global num_process,pid_probe,num_deadlock,msg_count,wait_msg
    print(".....................................INITIATING PROBE.....................................")
    print("DIRECTION \t PROBE \t MESSAGES \t WAIT FLAG\t STATUS")

    #Detecting deadlock
    for col in range(num_process):
        if array2D[pid_probe][col] == 1:
            displayLine(str(pid_probe + 1),str(col + 1),str(pid_probe + 1),str(pid_probe + 1),str(col + 1), str(msg_count[pid_probe]),str(wait_msg[pid_probe]),"")
            engaging_query(array2D, pid_probe, col)

    print("Number of deadlocks detected : "+ str(num_deadlock))
    print("Wait message array : ",msg_count)

#Logic for detecting Knot in system
def detectKnot(array2D):
    global num_process,pid_probe,msg_count,wait_msg
    print(".....................................DETECTING KNOT.....................................")
    print("DIRECTION \t PROBE \t MESSAGES \t WAIT FLAG\t STATUS")
    col = num_process
    while col > 0 :
        if array2D[col - 1][pid_probe] == 1 :
            displayLine(str(pid_probe + 1),str(col),str(pid_probe + 1),str(pid_probe + 1),str(col), str(msg_count[pid_probe]),str(wait_msg[pid_probe]),"")
            reply_query(array2D, pid_probe, col - 1)
        col -= 1

print("Reading WFG Input from input.txt")
#Parse the input text file as a 2D Array
wait_for_graph = readInput()

wait_for_graph = np.array(wait_for_graph)
num_rows, num_cols = wait_for_graph.shape
if num_rows != num_cols :
    print("Input is not a square matrix ! Ensure number of rows and columns match !")
elif num_rows <= 1 :
    print("Deadlock detection cannot be done! Ensure minimum No of Process > 1 !")
else:
    wait_msg = np.full(num_rows,False,dtype=bool)
    msg_count = np.full(num_rows,0,dtype=int)
    num_process = num_rows
    print(".....................................Displaying WFG.....................................")
    displayGraph(wait_for_graph)
    
    pid_probe = int(input("Enter the process initiating the probe (Between 1 and "+str(num_process)+"): "))
    if pid_probe < 1 or pid_probe > num_process:
        print("Invalid Process Id! Exiting !")
        exit()

    pid_probe = pid_probe - 1

	#Initializing the probe to detect deadlock
    detectDeadlock(wait_for_graph)
    if num_deadlock >= 2 :
        #Detect Knot
        detectKnot(wait_for_graph)
        
    print("Number of knots detected : "+ str(num_knot))
    if num_deadlock == num_knot :
        print("Equal number of Deadlock and Knot detected \nAll sent messages were received \nChandy-Misra-Haas OR algorithm is verified")
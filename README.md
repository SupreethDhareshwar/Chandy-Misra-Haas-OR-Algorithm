# Installation and Usage Guidelines

## Pre-requisites

* This project uses python 3.8.3 running on Ubuntu 18  
* Ensure pip3 is also to install packages
* Run `python3 -m pip install <package_name>` for installing packages like numpy
Example : `python3 -m pip install numpy` 
* Ensure input.txt has proper square matrix of 1s and 0s. Change the matrix for varying inputs. This file has to be in same directory as main.py 
* Here each row represents a process dependency on other process with 1 indicating dependency and 0 otherwise

## Running the project 

* cd to the project directory
* Run `python3 main.py`
* If provided input.txt is valid. It will ask for a process to initate probe from. 
* Provide valid process id and observe the results
* For the sample input.txt included in zip produces the below result :

Reading WFG Input from input.txt
.....................................Displaying WFG.....................................
        P1      P2      P3      P4      P5      P6      P7      P8
P1      0       1       0       0       0       0       0       0
P2      0       0       1       0       0       0       0       0
P3      0       0       0       1       1       0       0       0
P4      0       0       0       0       0       1       0       0
P5      0       0       0       0       0       0       1       0
P6      0       0       0       0       0       0       0       1
P7      0       0       0       0       0       0       0       1
P8      1       1       0       0       0       0       0       0
Enter the process initiating the probe (Between 1 and 8): 1
.....................................INITIATING PROBE.....................................
DIRECTION        PROBE   MESSAGES        WAIT FLAG       STATUS
P1 --> P2       (1,1,2)         1       True 
P2 --> P3       (1,2,3)         1       True 
P3 --> P4       (1,3,4)         2       True 
P4 --> P6       (1,4,6)         1       True 
P6 --> P8       (1,6,8)         1       True 
P8 --> P1       (1,8,1)         2       True    DEADLOCK DETECTED
P3 --> P5       (1,3,5)         2       True 
P5 --> P7       (1,5,7)         1       True 
P7 --> P8       (1,7,8)         1       True 
P8 --> P1       (1,8,1)         2       True    DEADLOCK DETECTED
Number of deadlocks detected : 2
Wait message array :  [1 1 2 1 1 1 1 2]
.....................................DETECTING KNOT.....................................
DIRECTION        PROBE   MESSAGES        WAIT FLAG       STATUS
P1 --> P8       (1,1,8)         1       True 
P8 --> P7       (1,8,7)         1       True 
P7 --> P5       (1,7,5)         0       False 
P5 --> P3       (1,5,3)         0       False 
P3 --> P2       (1,3,2)         1       True 
P2 --> P8       (1,2,8)         0       False 
P8 --> P7       (1,8,7)         0       False 
P8 --> P6       (1,8,6)         0       False 
P6 --> P4       (1,6,4)         0       False 
P4 --> P3       (1,4,3)         0       False 
P3 --> P2       (1,3,2)         0       False 
P2 --> P1       (1,2,1)         0       False   KNOT DETECTED
P2 --> P1       (1,2,1)         0       False   KNOT DETECTED
Number of knots detected : 2
Equal number of Deadlock and Knot detected 
All sent messages were received 
Chandy-Misra-Haas OR algorithm is verified


Author : Supreeth Dhareshwar






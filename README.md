This is my first attempt in simulating the The Vector Field Histogram (VFH) algorithm

the original referance is from the paper IEEE TRANSACTIONS ON ROBOTICS AND AUTOMATION, VOL. 7, NO.3, JUNE 1991

the original paper suggest the following :
The VFH method employs a two-stage data-reduction technique the first stage have info about the robot's environment
as a the two-dimensional Cartesian histogram grid that gets updated in real time then a one-dimensional polar histogram constructed around the robot's momentary resulting in creating some sectors and each sector have a
polar obstacle density .

in the original paper they used a sonar as the device to scan the environment using a formula in the paper they give points in the active window of the sonar values on how likly for a collision to happen and the polar obstacle density is the sum of all thos points then we decide what is the least likly road for a collasion to happen then some steering control using a narrow and wide road logic so the movment is more accurate in narrow obstacles and a threshold used to determine the candidate valleys and some speed controll(wich i also do but not as accurate as in the paper) which to be honest i didn't fully understand .

my approch works with the sonar as if it was a lazer plus the robot it self is simulated as a circle since it is easier to work with, now the (sonar) will cast from the edges of the robot in all directions 36 lines each line will see if it will have any collision with a list of obsicales that is already known (i know this is not realstic but i could not figure out a way to make it work for now ) and check if a collision happens then it will see how far it is then it will find the best path to take according to the longest sonar ray that leads the fastest way to the target.
speed controll happens if the robot will need to change the angel it is facing since without it the errors happens more often so i reduce the speed down and if the sonar ray is at full range it goes to a max speed value.

The simulation usses pygame and this is also the first time i used it.

during the coding procces i used LLM's to help me find bugs and quickly test some casses or teach me stuff i did not know if i heavely used an llm in any part of the code i will add (thanks gpt) at the end of the comment.

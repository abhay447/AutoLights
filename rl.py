from random import randint,random
import traffic
import runner

Q = {}
alfa = 0.9
gamma = 0.3
numSteps = 1

lastState = traffic.State(0,0)
lastAction = randint(0,1)
lastScore = 0
Q[lastState] = [0,0] #since Q for all s,a are initialized by zero

def upDateQ(lState,lAction,cState,reward):
    if lState not in Q:
        Q[lState] = [0,0]
    if cState not in Q:
        Q[cState] = [0,0]
    Q[lState][lAction] = ((1-alfa) * Q[lState][lAction] 
                          + alfa * (reward + gamma * max(Q[cState])))    
runner.startSim()
while True:
    currState = traffic.actOnState(lastAction)
    currScore = traffic.getCurrentScore()
    reward = currScore - lastScore
    upDateQ(lastState, lastAction, currState, reward)
    lastState = currState    
    lastAction = randint(0,1)        
    if numSteps >10000 and max(Q[lastState]) != min(Q[lastState]):
        lastAction = Q[lastState].index(max(Q[lastState]))        
        print lastState.disp(),max(Q[lastState])
    alfa = alfa * (2**(-1*numSteps))
    numSteps += 1
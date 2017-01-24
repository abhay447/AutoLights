from random import randint,random
import traffic
import runner
import pickle
import argparse

parser = argparse.ArgumentParser(description='A Q-learning approach for traffic lights')
parser.add_argument("-m","--mode",type=str,help="'train' or 'test'")
args = parser.parse_args()

try:
    with open('brainDict.pickle', 'rb') as handle:
        Q = pickle.load(handle)
except:
    Q = {}
    Q['numSteps'] = 0
    

def upDateQ(lState,lAction,cState,reward):
    if args.mode == 'test' or lAction==-1:
        return
    if lState not in Q:
        Q[lState] = [0,0]
    if cState not in Q:
        Q[cState] = [0,0]
    ALFA = 0.3
    GAMMA = 0.9
    Q[lState][lAction] = ((1-ALFA) * Q[lState][lAction] 
                          + ALFA * (reward + GAMMA * max(Q[cState])))
def getAction(state):
    if traffic.traci.trafficlights.getPhase("0") not in [1,3]:
        return -1

    if args.mode == 'train' or state not in Q:
        return randint(0,1)
    
    return Q[state].index(max(Q[state]))

def main():
    lastState = traffic.State(0,0)
    lastAction = randint(0,1)
    lastScore = 0
    Q[lastState] = [0,0] #since Q for all s,a are initialized by zero
    if args.mode == 'test':
        runner.startSim('sumo-gui')
    else:
        runner.startSim('sumo')

    for i in range(10000):
        currState = traffic.actOnState(lastAction)
        currScore = traffic.getCurrentScore()
        reward = currScore - lastScore
        upDateQ(lastState, lastAction, currState, reward)
        lastState = currState
        lastAction = getAction(lastState)
        lastScore = currScore
    
    runner.stopSim()
    if args.mode == 'train':
        with open('brainDict.pickle', 'wb') as handle:
            pickle.dump(Q, handle, protocol=pickle.HIGHEST_PROTOCOL)

if __name__=='__main__':
    main()
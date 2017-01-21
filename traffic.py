from runner import *
#State = recordclass('State','NSVeh NSTime EWVeh EWTime')
#StreamCount = recordclass('StreamCount','VehIn VehOut StagVeh StopTime')

class State():
    def __init__(self, nsv, ewv):
        self.NSVeh = nsv
        self.EWVeh = ewv
    
    def __hash__(self):
        return hash((self.NSVeh, self.EWVeh))
    
    def __eq__(self, other):
        """Override the default Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        """Define a non-equality test"""
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented
    
    def disp(self):
        print self.NSVeh, self.EWVeh

class StreamCount():
    def __init__(self,vin,vout,stagv,stime):
        self.VehIn = vin
        self.VehOut = vout
        self.StagVeh = stagv
        self.StopTime = stime
    def __hash__(self):
        return hash((self.VehIn, self.VehOut, self.StagVeh, self.StopTime))

VSFactor = 5 # vehicle scale factor smoothens vehicle count
TSFactor = 5 # time scale factor smoothens time count

EW = StreamCount([],[],0,0)
WE = StreamCount([],[],0,0)
NS = StreamCount([],[],0,0)
SN = StreamCount([],[],0,0)
Streams = [WE,SN,EW,NS]

def countVeh():
    for sIndex in range(len(Streams)):
        Streams[sIndex].VehIn += traci.inductionloop.getLastStepVehicleIDs(str(2*sIndex))
        Streams[sIndex].VehIn = list(set(Streams[sIndex].VehIn))
        Streams[sIndex].VehOut += traci.inductionloop.getLastStepVehicleIDs(str(2*sIndex+1))
        Streams[sIndex].VehOut = list(set(Streams[sIndex].VehOut))
        Streams[sIndex].StagVeh = len(Streams[sIndex].VehIn) - len(Streams[sIndex].VehOut)

# The program looks like this
#    <tlLogic id="0" type="static" programID="0" offset="0">
# the locations of the tls are      NESW
#        <phase duration="31" state="GrGr"/>
#        <phase duration="6"  state="yryr"/>
#        <phase duration="31" state="rGrG"/>
#        <phase duration="6"  state="ryry"/>
#    </tlLogic>


def switchPhase(phase):
    if traci.trafficlights.getPhase("0") in [1,3]:
        return
    
    if phase == 0:
        if traci.trafficlights.getPhase("0") == 2:
            traci.trafficlights.setPhase("0",3)
        else:
            traci.trafficlights.setPhase("0",0)
            EW.StopTime += 1
            WE.StopTime += 1
            SN.StopTime = 0
            NS.StopTime = 0
    
    else:
        if traci.trafficlights.getPhase("0") == 0:
            traci.trafficlights.setPhase("0",1)
        else:
            traci.trafficlights.setPhase("0",2)
            EW.StopTime = 0
            WE.StopTime = 0
            SN.StopTime += 1
            NS.StopTime += 1
        

def getCurrentScore():
    myScore = 0
    for s in Streams:
        myScore += s.StagVeh * s.StopTime
    return -1*myScore/1000

def actOnState(action):
    switchPhase(action)
    traci.simulationStep()
    countVeh()
    NSVeh = (Streams[1].StagVeh + Streams[3].StagVeh)/VSFactor
    EWVeh = (Streams[0].StagVeh + Streams[2].StagVeh)/VSFactor
    return State(NSVeh,EWVeh)

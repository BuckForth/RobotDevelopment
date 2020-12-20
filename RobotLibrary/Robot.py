import threading
import time

class Robot:
    """Robot class for robot control"""
    
    def __init__(self, servoKits = [], frequency = 50, name = "newRobot"):
        self.name = name
        self.servoKits = servoKits
        self.root = None
        self.frequency = frequency
        
    def servoDriver_thread(self):
        self.active = True
        while self.active:
            nodes = self.root.getList()
            for node in nodes:
                node.robot = self
                node.updateStep(deltaTime = 1.0/self.frequency)
            time.sleep(1.0/self.frequency)
    
    def initializeServos(self):
        kitCheck = True
        if len(self.servoKits) > 0:
            kitCheck += 0x01
        for kit in self.servoKits:
                if kit == None:
                    kitCheck = False
        if kitCheck:
            #Initialize Positions
            nodes = self.getNodeList()
            for node in nodes:
                node.currentPos = node.restPos
                if (node.currentPos < 0):
                    node.currentPos = 0
                if (node.currentPos > node.actuation_range):
                    node.currentPos = node.actuation_range
                node.destinationPos = node.currentPos
                    
            #Start servo update thread
            self.thread = threading.Thread(target=self.servoDriver_thread, daemon=True)
            self.thread.start()
        else:
            print("An error occurred initializing servo kits") 
        
    def disengage(self):
        self.active = False
        
    def getNode(self, nodeName):
        return self.root.getNode(nodeName)
    
    def getNodeList(self):
        return self.root.getList()
    
    def printStructure(self, full = False):
        self.root.printStructure(0,full)
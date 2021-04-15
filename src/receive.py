import can
import cantools
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'cav-ui-mock-input'))
from messages import *

from threading import Thread
import time

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
DBC_PATH = os.path.join(SCRIPT_DIR,'..','cav-ui-mock-input','CAVs_HMI.dbc') # path to .dbc file
VEHICLE_INFO = 'Vehicle_Info'
LEFT_LANE_A = 'Left_Lane_A'
RIGHT_LANE_A = 'Right_Lane_A'


class Receiver():
    def __init__(self, can_bus, vcan=False):
        if vcan:
            os.system('sudo modprobe vcan')
            os.system('sudo ip link add dev ' + can_bus + ' type vcan')
            os.system('sudo ip link set ' + can_bus + ' up type vcan')
        
        self._can_bus = can.interface.Bus(can_bus, bustype='socketcan')
        self._db = cantools.database.load_file(DBC_PATH)
        self._vehicleInfoDef = self._db.get_message_by_name('Vehicle_Info')
        self._leftLaneADef = self._db.get_message_by_name('Left_Lane_A')
        self._rightLaneADef = self._db.get_message_by_name('Right_Lane_A')
        self._vehicleInfo = None
        self._leftLaneA = None
        self._rightLaneA = None

    # gets latest message
    def getLeftLaneInfo(self):
        return self._leftLaneA

    def getRightLaneInfo(self):
        return self._rightLaneA
        
    def getVehicleInfo(self):
        return self._vehicleInfo

    # keep reading CAN messages
    def receive(self):
        while True:
            recvmsg = self._can_bus.recv() #received message
            arbitrationID = recvmsg.arbitration_id
            if arbitrationID == 0x000 or arbitrationID == 0x001 or arbitrationID == 0x002:
                try:
                    decoded = self._db.decode_message(recvmsg.arbitration_id, recvmsg.data) # decoded dictionary object
                except Exception as e:
                    print("An exception occured when decoding CAN message: " + str(e))

                # store into appropriate message object type
                if arbitrationID == self._vehicleInfoDef.frame_id:
                    self._vehicleInfo = Vehicle_Info(self._vehicleInfoDef, decoded)
                elif arbitrationID == self._leftLaneADef.frame_id:
                    self._leftLaneA = Left_Lane_A(self._leftLaneADef, decoded)
                elif arbitrationID == self._rightLaneADef.frame_id:
                    self._rightLaneA = Right_Lane_A(self._rightLaneADef, decoded)
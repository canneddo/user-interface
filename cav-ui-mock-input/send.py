import can
import os

os.system('sudo ip link set can1 type can bitrate 1000000')
os.system('sudo ifconfig can1 up')

can1 = can.interface.Bus('can1')

msg = can.Message(arbitration_id=0x123, data=[0, 1, 2, 3, 4, 5, 6, 7], extended_id=False)
can1.send(msg)

os.system('sudo ifconfig can1 down')
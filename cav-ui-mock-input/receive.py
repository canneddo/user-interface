import can
import os

os.system('sudo ip link set can0 type can bitrate 1000000')
os.system('sudo ifconfig can0 up')

can0 = can.interface.Bus('can0')

msg = can0.recv(10.0)
print(msg)

os.system('sudo ifconfig can0 down')
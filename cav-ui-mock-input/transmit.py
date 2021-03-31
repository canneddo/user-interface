import can
import cantools
import os

from threading import Thread

class Transmitter:
    def __init__(self, can_bus, can_db_fp='CAVs_HMI.dbc', vcan=False):
        if vcan:
            os.system('sudo modprobe vcan')
            os.system('sudo ip link add dev ' + can_bus + ' type vcan')
            os.system('sudo ip link set ' + can_bus + ' up type vcan')
        self._can_bus = can.interface.Bus(can_bus, bustype='socketcan')
        self._db = cantools.database.load_file(can_db_fp)
        self._periodic_sender = None

    def get_message_definition(self, message_name):
        return self._db.get_message_by_name(message_name)

    def send_message(self, message):
        msg = can.Message(arbitration_id=message.arbitration_id, data=message.get_data())
        self._can_bus.send(msg)

    def start(self, message):
        msg = can.Message(arbitration_id=message.arbitration_id, data=message.get_data())
        self._periodic_sender = self._can_bus.send_periodic(msg, 0.1)

    def update_message(self, message):
        msg = can.Message(arbitration_id=self._periodic_sender.can_id, data=message.get_data())
        if self._periodic_sender:
            self._periodic_sender.modify_data(msg)
    
    def stop(self):
        self._periodic_sender.stop()
        self._periodic_sender = None

import sys

from transmit import Transmitter
from messages import Left_Lane_A, Right_Lane_A, Vehicle_Info


class MsgTransmitter:
    def __init__(self, transmitter, message_name):
        self.transmitter = transmitter
        self.message_name = message_name
        self.message_def = self.transmitter.get_message_definition(message_name)

    def start(self, signals):
        self.transmitter.start(self._generate_message(signals))

    def update_message(self, signals):
        self.transmitter.update_message(self._generate_message(signals))

    def stop(self):
        self.transmitter.stop()

    def _generate_message(self, signal_dict):
        message = None
        if self.message_name == 'Vehicle_Info':
            message = Vehicle_Info(message_def=self.message_def, signals=signal_dict)
        if self.message_name == 'Left_Lane_A':
            message = Left_Lane_A(message_def=self.message_def, signals=signal_dict)
        if self.message_name == 'Right_Lane_A':
            message = Right_Lane_A(message_def=self.message_def, signals=signal_dict)
        return message

class InputHandler():
    def __init__(self):
        #set initial values
        self.inputs = {
            'lane_left_detected': 0,
            'lane_right_detected': 0,
            'vehicle_on': 0,
            'shifter_position': 0,
            'lane_centering_status': 0,
            'yaw_rate': 0,
            'desired_vehicle_pos': 0,
            'Left_Lane_A': {'lane_curvature_derivative': 0, 'lane_curvature': 0, 'lane_heading': 0, 'distance_to_lane': 0},
            'Right_Lane_A': {'lane_curvature_derivative': 0, 'lane_curvature': 0, 'lane_heading': 0, 'distance_to_lane': 0}
        }
        can_bus = 'vcan0'
        can_db_fp = 'CAVs_HMI.dbc'
        virtual_can = True
        if len(sys.argv[1:]) > 0:
            can_bus = sys.argv[1:][0]
            can_db_fp = sys.argv[1:][1]
            virtual_can = False
        self.vehicle_info = MsgTransmitter(Transmitter(can_bus, can_db_fp, virtual_can), 'Vehicle_Info')
        self.left_lane_a = MsgTransmitter(Transmitter(can_bus, can_db_fp, virtual_can), 'Left_Lane_A')
        self.right_lane_a = MsgTransmitter(Transmitter(can_bus, can_db_fp, virtual_can), 'Right_Lane_A')
        self.vehicle_info.start(self.get_inputs())
        self.left_lane_a.start(self.get_lane_parameters('Left_Lane_A'))
        self.right_lane_a.start(self.get_lane_parameters('Right_Lane_A'))

    def update_input(self, input_name, value):
        self.inputs[input_name] = value
        self.vehicle_info.update_message(self.get_inputs())

    def set_lane_parameters(self, lane_name, parameters):
        self.inputs[lane_name] = parameters
        if lane_name == 'Left_Lane_A':
            self.left_lane_a.update_message(self._map_lane_parameters(self.get_lane_parameters(lane_name)))
        elif lane_name == 'Right_Lane_A':
            self.right_lane_a.update_message(self._map_lane_parameters(self.get_lane_parameters(lane_name)))

    def get_lane_parameters(self, lane_name):
        return self.inputs[lane_name]

    def get_inputs(self):
        return self.inputs

    def _map_lane_parameters(self, lane_params):
        return {
            'lane_curvature_derivative': lane_params[0], 
            'lane_curvature': lane_params[1], 
            'lane_heading': lane_params[2], 
            'distance_to_lane': lane_params[3]
        }
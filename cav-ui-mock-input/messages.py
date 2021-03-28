class Message:
    def __init__(self, message_def=None, signals = []):
        signal_set = {}
        if signals:
            for signal in signals:
                signal_set[signal] = signals[signal]
        self._signals = signal_set
        self._message_def = message_def

    @property
    def name(self):
        return

    @property
    def arbitration_id(self):
        if self._message_def:
            return self._message_def.frame_id
        return

    @property
    def message_def(self):
        return self._arbitration_id

    @message_def.setter
    def message_def(self, message_def):
        self._message_def = message_def

    def get_signal(self, signal_name):
        return self._signals[signal_name]

    def set_signal(self, signal_name, signal_value):
        self._signals[signal_name] = signal_value

    def get_data(self):
        return self._message_def.encode(self._signals)
        

class Vehicle_Info(Message):
    @property
    def name(self):
        return 'Vehicle_Info'

    @property
    def lane_left_detected(self):
        return self.get_signal('lane_left_detected')

    @lane_left_detected.setter
    def left_lane_detected(self, left_lane_detected):
        self.set_signal('lane_left_detected', lane_left_detected)

    @property
    def lane_right_detected(self):
        return self.get_signal('lane_right_detected')

    @lane_right_detected.setter
    def lane_right_detected(self, lane_right_detected):
        self.set_signal('lane_right_detected', lane_right_detected)

    @property
    def vehicle_on(self):
        return self.get_signal('vehicle_on')

    @vehicle_on.setter
    def vehicle_on(self, vehicle_on):
        self.set_signal('vehicle_on', vehicle_on)

    @property
    def shifter_position(self):
        return self.get_signal('shifter_position')

    @shifter_position.setter
    def shifter_position(self, shifter_position):
        self.set_signal('shifter_position', shifter_position)

    @property
    def lane_centering_status(self):
        return self.get_signal('lane_centering_status')

    @lane_centering_status.setter
    def lane_centering_status(self, lane_centering_status):
        self.set_signal('lane_centering_status', lane_centering_status)

    @property
    def desired_vehicle_pos(self):
        return self.get_signal('desired_vehicle_pos')

    @desired_vehicle_pos.setter
    def desired_vehicle_pos(self, desired_vehicle_pos):
        self.set_signal('desired_vehicle_pos', desired_vehicle_pos)

    @property
    def yaw_rate(self):
        return self.get_signal('yaw_rate')

    @yaw_rate.setter
    def yaw_rate(self, yaw_rate):
        self.set_signal('yaw_rate', yaw_rate)


class Left_Lane_A(Message):   
    @property
    def name(self):
        return 'Left_Lane_A'

    @property
    def distance_to_lane(self):
        return self.get_signal('distance_to_lane')

    @distance_to_lane.setter
    def distance_to_lane(self, distance_to_lane):
        self.set_signal('distance_to_lane', distance_to_lane)

    @property
    def lane_curvature(self):
        return self.get_signal('lane_curvature')

    @lane_curvature.setter
    def lane_curvature(self, lane_curvature):
        self.set_signal('lane_curvature', lane_curvature)

    @property
    def lane_curvature_derivative(self):
        return self.get_signal('lane_curvature_derivative')

    @lane_curvature_derivative.setter
    def lane_curvature_derivative(self, lane_curvature_derivative):
        self.set_signal('lane_curvature_derivative', lane_curvature_derivative)


class Right_Lane_A(Message):   
    @property
    def name(self):
        return 'Right_Lane_A'

    @property
    def distance_to_lane(self):
        return self.get_signal('distance_to_lane')

    @distance_to_lane.setter
    def distance_to_lane(self, distance_to_lane):
        self.set_signal('distance_to_lane', distance_to_lane)

    @property
    def lane_curvature(self):
        return self.get_signal('lane_curvature')

    @lane_curvature.setter
    def lane_curvature(self, lane_curvature):
        self.set_signal('lane_curvature', lane_curvature)

    @property
    def lane_curvature_derivative(self):
        return self.get_signal('lane_curvature_derivative')

    @lane_curvature_derivative.setter
    def lane_curvature_derivative(self, lane_curvature_derivative):
        self.set_signal('lane_curvature_derivative', lane_curvature_derivative)
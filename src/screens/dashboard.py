from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_string("""
<Dashboard>:
    GridLayout:
        cols: 1
        size: root.width, root.height
        GridLayout:
            cols: 3
            Button:
                id: left_led
                size: root.width * 0.34, root.height * 0.05
                size_hint: None, None
                text: '***Left Side LEDs***'
                on_press:
                    left_led.background_color = [1,0,1,1]
                    center_led.background_color = [1,1,1,1]
                    right_led.background_color = [1,1,1,1]
            Button:
                id: center_led
                size: root.width * 0.34, root.height * 0.05
                background_color: [1,0,1,1]
                size_hint: None, None
                text: '***Center LEDs***'
                on_press:
                    center_led.background_color = [1,0,1,1]
                    left_led.background_color = [1,1,1,1]
                    right_led.background_color = [1,1,1,1]
            Button:
                id: right_led
                size: root.width * 0.34, root.height * 0.05
                size_hint: None, None
                text: '***Right Side LEDs***'
                on_press:
                    right_led.background_color = [1,0,1,1]
                    left_led.background_color = [1,1,1,1]
                    center_led.background_color = [1,1,1,1]
            Button:
                size: root.width * 0.34, root.height * 0.05
                size_hint: None, None
                text: 'Park'
                on_press:
                    root.manager.current = 'car_main_menu'
            Button:
                id: lane_centering
                size: root.width * 0.34, root.height * 0.05
                size_hint: None, None
                text: 'Lane Centering'
                background_color: 'white'
                on_press:
                    self.background_color = [0,1,0,1] if self.background_color == [1,1,1,1] and d_error.background_color == [1,1,1,1] else [1,1,1,1]
                    left_lane.opacity = 1 if left_lane.opacity == 0 and d_error.background_color == [1,1,1,1] else 0
                    left_lane.disabled = False if left_lane.disabled and d_error.background_color == [1,1,1,1] else True                    
                    right_lane.opacity = 1 if right_lane.opacity == 0 and d_error.background_color == [1,1,1,1] else 0
                    right_lane.disabled = False if right_lane.disabled and d_error.background_color == [1,1,1,1] else True
                    vehicle.opacity = 1 if vehicle.opacity == 0 and d_error.background_color == [1,1,1,1] else 0
            Button:
                id: d_error
                size: root.width * 0.34, root.height * 0.05
                size_hint: None, None
                text: 'Simulate Error'
                on_press:
                    self.background_color = [1,1,1,1] if self.background_color == [1,0,0,1] else [1,0,0,1]
                    # On Error, disable lane centering, restore defaults and turn off displays
                    lane_centering.background_color = [1,1,1,1]
                    left_lane.background_color = [1,1,1,1]
                    left_lane.opacity = 0
                    left_lane.disabled = True
                    right_lane.background_color = [1,1,1,1]
                    right_lane.opacity = 0
                    right_lane.disabled = True
                    vehicle.opacity = 0

            Button:
                size: root.width * 0.34, root.height * 0.05
                id: d_decelerate
                text: "Decrease Speed"
                on_press: d_speed.text = str(int(d_speed.text) - 5) if int(d_speed.text) > 0 else str(int(d_speed.text))
            Label:
                width: root.width * 0.34
                id: d_speed
                font_size: 40
                text: "0"
            Button:
                size: root.width * 0.34, root.height * 0.05
                id: d_accelerate
                text: 'Increase Speed'
                on_press: d_speed.text = str(int(d_speed.text) + 5) if int(d_speed.text) < 100 else str(int(d_speed.text))
            


        GridLayout:
            cols: 1
            Label:
                id: labelActive
                text: "Lane Centering Active"
                font_size: 30
                color: "green"
                opacity: 1 if ((lane_centering.background_color == [0,1,0,1]) and (d_error.background_color == [1,1,1,1]) and (int(d_speed.text) >= 60) and (left_lane.background_color == [0,1,0,1]) and (right_lane.background_color == [0,1,0,1])) else 0
            Label:
                id: labelInactive
                text: "Lane Centering Inactive"
                font_size: 30
                color: "yellow"
                opacity: 1 if ((lane_centering.background_color == [0,1,0,1]) and (d_error.background_color == [1,1,1,1]) and not ((int(d_speed.text) >= 60) and (left_lane.background_color == [0,1,0,1]) and (right_lane.background_color == [0,1,0,1]))) else 0
            Label:
                id: labelConnectionLost
                text: "Connection to Lane Centering Lost"
                font_size: 30
                color: "red"
                opacity: 1 if d_error.background_color == [1,0,0,1] else 0
        
        GridLayout:
            cols: 5
            Button:
                size: 100, 100
                background_color: [0,0,0,0]
                disabled: True
                opacity: 0

            Button:
                id: left_lane
                opacity: 0
                disabled: True
                size: 10, 150
                size_hint: None, None
                background_color: [1,1,1,1]
                on_press: 
                    self.background_color = app.changeLaneColor(self.background_color)

            Image:
                id: vehicle
                opacity: 0
                source: 'images/blazer.png'

            Button:
                id: right_lane
                opacity: 0
                disabled: True
                size: 10, 150
                pos: (0,0)
                size_hint: None, None
                background_color: [1,1,1,1]
                on_press: self.background_color = app.changeLaneColor(self.background_color)

            Button:
                size: 100, 100
                background_color: [0,0,0,0]
                disabled: True
                opacity: 0

            

        GridLayout:
            cols: 3
            height: root.height * 0.8
            Label:
                text: "Volume"
            Slider:
                id: volume_slider
                min: 0
                max: 100
                value: app.getVolume()
                value_track: True
                value_track_color: [0,100,200,1]
                step: 5
                orientation: 'horizontal'
                on_touch_up: app.setVolume(int(volume_slider.value))
            Label:
                text: str(int(volume_slider.value))

            Label:
                text: "LED Brightness"
            Slider:
                id: led_brightness_slider
                min: 0
                max: 100
                value: app.getLedBrightness()
                value_track: True
                value_track_color: [0,100,200,1]
                step: 5
                orientation: 'horizontal'
                on_touch_up: 
                    app.setLedBrightness(int(led_brightness_slider.value))
            Label:
                text: str(int(led_brightness_slider.value))
""")

class Dashboard(Screen):
    pass


from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_string("""
<Dashboard>:
    GridLayout:
        cols: 1
        size: root.width, root.height
        GridLayout:
            cols: 5
            Button:
                size: root.width * 0.2, root.height * 0.05
                size_hint: None, None
                text: 'Park'
                on_press:
                    app.playButtonTone()
                    root.manager.transition.direction = 'left'
                    root.manager.current = 'car_main_menu'
            Button:
                id: lane_centering
                size: root.width * 0.2, root.height * 0.05
                size_hint: None, None
                text: 'Lane Centering'
                background_color: 'white'
                on_press:
                    app.playButtonTone()
                    self.background_color = [0,1,0,1] if self.background_color == [1,1,1,1] and d_error.background_color == [1,1,1,1] else [1,1,1,1]
                    left_lane.opacity = 1 if left_lane.opacity == 0 and d_error.background_color == [1,1,1,1] else 0
                    left_lane.disabled = False if left_lane.disabled and d_error.background_color == [1,1,1,1] else True                    
                    right_lane.opacity = 1 if right_lane.opacity == 0 and d_error.background_color == [1,1,1,1] else 0
                    right_lane.disabled = False if right_lane.disabled and d_error.background_color == [1,1,1,1] else True
                    vehicle.opacity = 1 if vehicle.opacity == 0 and d_error.background_color == [1,1,1,1] else 0
            Button:
                id: d_error
                size: root.width * 0.2, root.height * 0.05
                size_hint: None, None
                text: 'Simulate Error'
                on_press:
                    app.playButtonTone()
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
                size: root.width * 0.2, root.height * 0.05
                id: d_decelerate
                size_hint: None, None
                text: "Decrease Speed"
                on_press:
                    app.playButtonTone() 
                    d_speed.text = str(int(d_speed.text) - 5) if int(d_speed.text) > 0 else str(int(d_speed.text))
            Button:
                size: root.width * 0.2, root.height * 0.05
                id: d_accelerate
                size_hint: None, None
                text: 'Increase Speed'
                on_press:
                    app.playButtonTone()  
                    d_speed.text = str(int(d_speed.text) + 5) if int(d_speed.text) < 100 else str(int(d_speed.text))
            Button:
                size: root.width * 0.2, root.height * 0.1
                size_hint: None, None
                background_color: [0,0,0,0]
                disabled: True
                opacity: 0
            Button:
                size: root.width * 0.2, root.height * 0.1
                size_hint: None, None
                background_color: [0,0,0,0]
                disabled: True
                opacity: 0
            Label:
                size: root.width * 0.2, root.height * 0.1
                size_hint: None, None
                id: d_speed
                font_size: 40
                text: "0" 
            Button:
                size: root.width * 0.2, root.height * 0.1
                size_hint: None, None
                background_color: [0,0,0,0]
                disabled: True
                opacity: 0
            Button:
                size: root.width * 0.2, root.height * 0.1
                size_hint: None, None
                background_color: [0,0,0,0]
                disabled: True
                opacity: 0


        GridLayout:
            cols: 1
            row_force_default: True
            row_default_height: 0
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
                text: "Error: \\nLane Centering has been compromised,\\ncontinue driving normally."
                font_size: 30
                color: "red"
                opacity: 1 if d_error.background_color == [1,0,0,1] else 0
        
        GridLayout:
            cols: 5
            row_force_default: True
            row_default_height: 140
            Button:
                size: 100, 140
                background_color: [0,0,0,0]
                disabled: True
                opacity: 0

            Button:
                id: left_lane
                opacity: 0
                disabled: True
                size: 10, 140
                size_hint: None, None
                background_color: [1,1,1,1]
                on_press:
                    app.playButtonTone()
                    self.background_color = app.changeLaneColor(self.background_color)

            Image:
                id: vehicle
                opacity: 0
                source: 'images/car.png'

            Button:
                id: right_lane
                opacity: 0
                disabled: True
                size: 10, 140
                pos: (0,0)
                size_hint: None, None
                background_color: [1,1,1,1]
                on_press:
                    app.playButtonTone()
                    self.background_color = app.changeLaneColor(self.background_color)

            Button:
                size: 100, 140
                background_color: [0,0,0,0]
                disabled: True
                opacity: 0

            

        GridLayout:
            cols: 5
            height: root.height * 0.6            
            Label:
                text: "Volume"
                font_size: 20
            CheckBox:
                active: True
                disabled: True
            Button:
                id: volume_down
                text: "-"
                font_size: 60
                on_release:
                    app.setVolume(int(volumeVal.text) - 5 if int(volumeVal.text) > 0 else int(volumeVal.text))
                    app.playButtonTone()   
            Label:
                id: volumeVal
                text: app.volume
                font_size: 30
            Button:
                id: volume_up
                text: "+"
                font_size: 60
                on_release:
                    app.setVolume(int(volumeVal.text) + 5 if int(volumeVal.text) < 100 else int(volumeVal.text))
                    app.playButtonTone() 

            Label:
                text: "LED Brightness"
                font_size: 20
            CheckBox:
                id: led_brightness_active
                active: app.ledBrightnessEnabled
                on_release:
                    app.playButtonTone()
                    app.enableLedBrightness(led_brightness_active.active)
            Button:
                id: led_brightness_down
                disabled: not led_brightness_active.active
                text: "-"
                font_size: 60
                on_release:
                    app.playButtonTone()
                    app.setLedBrightness(int(ledBrightnessVal.text) - 5 if int(ledBrightnessVal.text) > 0 else 0)  
            Label:
                id: ledBrightnessVal
                text: app.ledBrightness
                font_size: 30
            Button:
                id: led_brightness_up
                disabled: not led_brightness_active.active
                text: "+"
                font_size: 60
                on_release:
                    app.playButtonTone()
                    app.setLedBrightness(int(ledBrightnessVal.text) + 5 if int(ledBrightnessVal.text) < 100 else 100)
            
""")

class Dashboard(Screen):
    pass


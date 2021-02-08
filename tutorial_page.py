from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.videoplayer import VideoPlayer

from home_screen import CarHomeScreen

import json

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string("""
<Dashboard>:
    GridLayout:
        cols: 1
        size: root.width, root.height

        GridLayout:
            cols: 3
            Button:
                size: root.width * 0.33, root.height * 0.05
                size_hint: None, None
                text: 'Park'
                on_press:
                    root.manager.current = 'car_main_menu'
            Button:
                id: lane_centering
                size: root.width * 0.33, root.height * 0.05
                size_hint: None, None
                text: 'Lane Centering'
                background_color: 'white'
                on_press:
                    self.background_color = [0,1,0,1] if self.background_color == [1,1,1,1] else [1,1,1,1]
                    left_lane.opacity = 0 if left_lane.opacity == 1 else 1
                    left_lane.disabled = False if left_lane.disabled else True                    
                    right_lane.opacity = 0 if right_lane.opacity == 1 else 1
                    right_lane.disabled = False if right_lane.disabled else True
                    vehicle.opacity = 0 if vehicle.opacity == 1 else 1
            Button:
                id: d_error
                size: root.width * 0.33, root.height * 0.05
                size_hint: None, None
                text: 'Simulate Error'
                on_press:
                    self.background_color = [1,1,1,1] if self.background_color == [1,0,0,1] else [1,0,0,1]
            Button:
                size: root.width * 0.33, root.height * 0.05
                id: d_decelerate
                text: "Decrease Speed"
                on_press: d_speed.text = str(int(d_speed.text) - 5)
            Label:
                width: root.width * 0.33
                id: d_speed
                text: "0"
            Button:
                size: root.width * 0.33, root.height * 0.05
                id: d_accelerate
                text: 'Increase Speed'
                on_press: d_speed.text = str(int(d_speed.text) + 5)
            


        GridLayout:
            cols: 1
            Label:
                id: labelActive
                text: "Lane Centering Active"
                color: "green"
                opacity: 1 if ((lane_centering.background_color == [0,1,0,1]) and (d_error.background_color == [1,1,1,1]) and (int(d_speed.text) >= 60) and (left_lane.background_color == [0,1,0,1]) and (right_lane.background_color == [0,1,0,1])) else 0
            Label:
                id: labelInactive
                text: "Lane Centering Inactive"
                color: "yellow"
                opacity: 1 if ((lane_centering.background_color == [0,1,0,1]) and (d_error.background_color == [1,1,1,1]) and not ((int(d_speed.text) >= 60) and (left_lane.background_color == [0,1,0,1]) and (right_lane.background_color == [0,1,0,1]))) else 0
            Label:
                id: labelConnectionLost
                text: "Connection to Lane Centering Lost"
                color: "red"
                opacity: 1 if d_error.background_color == [1,0,0,1] else 0
        
        GridLayout:
            cols: 3
            Button:
                id: left_lane
                opacity: 0
                disabled: True
                size: 10, 150
                size_hint: None, None
                background_color: [1,1,1,1]
                on_press: self.background_color = app.changeLaneColor(self.background_color)

            Image:
                id: vehicle
                opacity: 0
                source: 'blazer.png'

            Button:
                id: right_lane
                opacity: 0
                disabled: True
                size: 10, 150
                padding_right: 200
                size_hint: None, None
                background_color: [1,1,1,1]
                on_press: self.background_color = app.changeLaneColor(self.background_color) 

            

        GridLayout:
            cols: 3
            height: root.height * 0.8
            Label:
                text: "Volume"
            Slider:
                id: d_volume_slider
                min: 0
                max: 100
                value: app.getValue('volume')
                value_track: True
                value_track_color: [0,100,200,1]
                step: 5
                orientation: 'horizontal'
                on_touch_up: app.setValue('volume', int(d_volume_slider.value))
            Label:
                text: str(int(d_volume_slider.value))

            Label:
                text: "LED Brightness"
            Slider:
                id: d_led_brightness_slider
                min: 0
                max: 100
                value: app.getValue('led_brightness')
                value_track: True
                value_track_color: [0,100,200,1]
                step: 5
                orientation: 'horizontal'
                on_touch_up: app.setValue('led_brightness', int(d_led_brightness_slider.value))
            Label:
                text: str(int(d_led_brightness_slider.value))


<SettingsScreen>:
    GridLayout:
        cols: 1
        size: root.width, root.height

        GridLayout:
            cols: 2
            height: root.height * 0.2
            Button:
                text: "Back"
                font_size: 30
                size: root.width * 0.2, root.height * 0.2
                size_hint: None, None
                on_press: root.manager.current = 'menu'
                
            Label:
                text: "Lane Centering Settings"
                font_size: 40
                size: root.width * 0.8, root.height * 0.2
                size_hint: None, None
        GridLayout:
            cols: 3
            height: root.height * 0.8
            Label:
                text: "Volume"
                font_size: 30
            Slider:
                id: volume_slider
                min: 0
                max: 100
                value: app.getValue('volume')
                value_track: True
                value_track_color: [0,100,200,1]
                step: 5
                orientation: 'horizontal'
                on_touch_up: app.setValue('volume', int(volume_slider.value))
            Label:
                text: str(int(volume_slider.value))
                font_size: 30

            Label:
                text: "LED Brightness"
                font_size: 30
            Slider:
                id: led_brightness_slider
                min: 0
                max: 100
                value: app.getValue('led_brightness')
                value_track: True
                value_track_color: [0,100,200,1]
                step: 5
                orientation: 'horizontal'
                on_touch_up: app.setValue('led_brightness', int(led_brightness_slider.value))
            Label:
                text: str(int(led_brightness_slider.value))
                font_size: 30


<MenuScreen>:
    CStackLayout:
        orientation: 'tb-lr'
        Button:
            size_hint_y: None
            size_hint_x: None
            height: '64dp'
            width: '192dp'
            text: 'Go to settings'
            on_press: root.manager.current = 'settings'
        Button:
            size_hint_y: None
            size_hint_x: None
            height: '64dp'
            width: '192dp'
            text: 'Tutorial Page'
            on_press: root.manager.current = 'tutorial'
        Button:
            size_hint_y: None
            size_hint_x: None
            height: '64dp'
            width: '192dp'
            text: 'Back'
            on_press: root.manager.current = 'car_main_menu'

# <SettingsScreen>:
#     CStackLayout:
#         orientation: 'tb-lr'
#         Button:
#             size_hint_y: None
#             size_hint_x: None
#             height: '64dp'
#             width: '192dp'
#             text: 'My settings button'
#         Button:
#             size_hint_y: None
#             size_hint_x: None
#             height: '64dp'
#             width: '192dp'
#             text: 'Back to menu'
#             on_press: 
#                 root.manager.current = 'menu'
#                 root.manager.transition.direction = 'left'

<TutorialScreen>:
    CStackLayout:
        orientation: 'tb-lr'
        Button:
            size_hint_y: None
            size_hint_x: None
            height: '64dp'
            width: '192dp'
            text: 'Start Tutorial'
            on_press: root.manager.current = 'video'
        Button:
            size_hint_y: None
            size_hint_x: None
            height: '64dp'
            width: '192dp'
            text: 'Start Alternate Tutorial'
            on_press: root.manager.current = 'video'
        Button:
            size_hint_y: None
            size_hint_x: None
            height: '64dp'
            width: '192dp'
            text: 'Back'
            on_press: 
                root.manager.current = 'menu'
                root.manager.transition.direction = 'left'

<VideoScreen>:
    CGridLayout:
        rows: 4
        columns: 1

        Button:
            size_hint_y: None
            size_hint_x: None
            height: '64dp'
            width: '192dp'
            text: 'Back'
            on_press: 
                root.manager.current = 'menu'
                root.manager.transition.direction = 'left'
                video_display.state = "pause"

        VideoPlayer:
            id: video_display
            source: "./hunter.mp4"
            width: 100.0

<CStackLayout@StackLayout+BackgroundColor>
<CGridLayout@GridLayout+BackgroundColor>

<BackgroundColor@Widget>
    pos_hint: {'center_x': .5, 'center_y': .5}
    size_hint: 1.0, 1.0
    canvas.before:
        Color:
            rgba: .2, .3, .4, 1
        Rectangle:
            size: self.size
            pos: self.pos

""")

# Declare both screens
class MenuScreen(Screen):
    pass

class SettingsScreen(Screen):
    pass

class TutorialScreen(Screen):
    pass

class VideoScreen(Screen):
    pass

class Dashboard(Screen):
    pass

class HMIApp(App):

    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(CarHomeScreen(name='car_main_menu'))
        sm.add_widget(Dashboard(name='dashboard'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(TutorialScreen(name='tutorial'))
        sm.add_widget(VideoScreen(name='video'))

        return sm
    
    def changeLaneColor(self, color):
        if (color[0] == 0 and color[2] == 0):
            return [1,1,1,1]
        elif (color[0] == 1 and color[2] == 1):
            return [0,1,0,1]
        return [1,1,1,1]

    def getValue(self, key):
        with open('storage.json') as f:
            data = json.load(f)
            f.close()

        return data['cav']['hmi']['settings'][key]

    def setValue(self, key, value):
        with open('storage.json') as f:
            data = json.load(f)
            f.close()

        data['cav']['hmi']['settings'][key] = value

        with open('storage.json', 'w') as f:
            json.dump(data, f)
            f.close()

if __name__ == '__main__':
    HMIApp.title = "Lane Centering"
    HMIApp().run()
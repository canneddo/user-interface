from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string("""

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
                on_press:
                    root.manager.transition.direction = 'left' 
                    root.manager.current = 'menu'
                
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
                # value: app.getValue('control','c_volume')
                value: app.getVolume()
                value_track: True
                value_track_color: [0,100,200,1]
                step: 5
                orientation: 'horizontal'
                on_touch_up: 
                    app.setVolume(int(volume_slider.value))
                # on_touch_up: app.setValue('control','c_volume', int(volume_slider.value))
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
                # value: app.getValue('control','c_ledBrightness')
                value: app.getLedBrightness()
                value_track: True
                value_track_color: [0,100,200,1]
                step: 5
                orientation: 'horizontal'
                on_touch_up: 
                    app.setLedBrightness(int(led_brightness_slider.value))
                # on_touch_up: app.setValue('control','c_ledBrightness', int(led_brightness_slider.value))
            Label:
                text: str(int(led_brightness_slider.value))
                font_size: 30

""")

class SettingsScreen(Screen):
    pass
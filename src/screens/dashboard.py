from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_string("""
<Dashboard>:
    GridLayout:
        cols: 1
        size: root.width, root.height

        GridLayout:
            cols: 1
            Label:
                id: labelActive
                text: "Lane Centering Active"                
                font_size: 30
                color: "green"
                opacity: 0
            Label:
                id: labelInactive
                text: "Lane Centering Inactive"
                font_size: 30
                color: "yellow"
                opacity: 1
            Label:
                id: labelConnectionLost
                text: "Error: \\nLane Centering has been compromised,\\ncontinue driving normally."
                font_size: 30
                color: "red"
                opacity: 0
        
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


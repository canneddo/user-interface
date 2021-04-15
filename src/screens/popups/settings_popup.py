from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout

Builder.load_string("""

<SettingsPopUp>:

    GridLayout:
        cols: 1
        size: root.width, root.height
        pos_hint: {"x":0, "y": 0}
        GridLayout:
            cols: 5
            row_force_default: True
            row_default_height: 80
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
                    app.playTone(app.Sound.CLICK)  
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
                    app.playTone(app.Sound.CLICK)

            Label:
                text: "LED \\nBrightness"
                font_size: 20
            CheckBox:
                id: led_brightness_active
                active: app.ledBrightnessEnabled
                on_release:
                    app.enableLedBrightness(led_brightness_active.active)
            Button:
                id: led_brightness_down
                disabled: not led_brightness_active.active
                text: "-"
                font_size: 60
                on_release:
                    app.setLedBrightness(int(ledBrightnessVal.text) - 5 if int(ledBrightnessVal.text) > 0 else 0)                    
                    app.playTone(app.Sound.CLICK)  
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
                    app.setLedBrightness(int(ledBrightnessVal.text) + 5 if int(ledBrightnessVal.text) < 100 else 100)
                    app.playTone(app.Sound.CLICK)
    
        
        Button:
            text: "Close"
            font_size: 20
            size_hint_y: 0.4
            pos_hint: {"x": 0.5, "y": 0.1}
            on_release:
                app.playTone(app.Sound.CLICK)
                app.closeSettingsPopUpWindow('intro_video', 'play')   

""")

class SettingsPopUp(FloatLayout):
    pass

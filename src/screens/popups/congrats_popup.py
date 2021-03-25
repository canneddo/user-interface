from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout

Builder.load_string("""

<CongratsPopUp>:
    Label:
        text: "You've completed the lane centering tutorial!"
        pos_hint: {"x":0.1, "y": 0.7}
        size_hint_y: None
        text_size: self.width, None
        height: self.texture_size[1]

    Button:
        text: "Close"
        font_size: 20
        size_hint: 0.4, 0.3
        pos_hint: {"x":0.3, "y": 0.1}
        on_release:
            app.playButtonTone()
            app.closeCongratsPopUpWindow()

""")

class CongratsPopUp(FloatLayout):
    pass



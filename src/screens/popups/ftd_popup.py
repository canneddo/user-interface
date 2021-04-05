from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout

Builder.load_string("""

<FTDPopUp>:
    Label:
        id: "ftd_popup_label"
        text: "Have you driven this vehicle model in the past 6 months?"
        # text_size: self.size
        # size_hint: 0.5, 0.2
        pos_hint: {"x":0.1, "y": 0.7}
        size_hint_y: None
        text_size: self.width, None
        height: self.texture_size[1]

    Button:
        id: "ftd_popup_yes_button"
        text: "Yes"
        font_size: 20
        size_hint: 0.4, 0.3
        pos_hint: {"x":0.1, "y": 0.1}
        on_release:
            app.playButtonTone()
            app.closeFTDPopUpWindow(False)
            

    Button:
        id: "ftd_popup_no_button"
        text: "No"
        font_size: 20
        size_hint: 0.4, 0.3
        pos_hint: {"x":0.5, "y": 0.1}
        on_release:
            app.playButtonTone() 
            app.playTutorial(True)

""")

class FTDPopUp(FloatLayout):
    pass



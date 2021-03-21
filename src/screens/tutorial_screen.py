from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_string("""

<TutorialScreen>:
    CStackLayout:
        orientation: 'tb-lr'
        Button:
            size_hint_y: None
            size_hint_x: None
            height: '64dp'
            width: '192dp'
            text: 'Lane Centering Tutorial'
            on_press:
                app.playButtonTone()
                root.manager.current = 'video'
                app.playBack(False)
        Button:
            size_hint_y: None
            size_hint_x: None
            height: '64dp'
            width: '192dp'
            text: 'Back'
            on_press:
                app.playButtonTone()
                root.manager.transition.direction = 'right' 
                root.manager.current = 'menu'

<CStackLayout@StackLayout+BackgroundColor>

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

class TutorialScreen(Screen):
    pass
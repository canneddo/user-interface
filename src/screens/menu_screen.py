from kivy.lang import Builder
from kivy.uix.screenmanager import Screen

Builder.load_string("""

<MenuScreen>:
    CStackLayout:
        orientation: 'tb-lr'
        Button:
            size_hint_y: None
            size_hint_x: None
            height: '64dp'
            width: '192dp'
            text: 'Settings'
            on_press:
                app.playTone(app.Sound.CLICK)
                root.manager.transition.direction = 'left' 
                root.manager.current = 'settings'
        Button:
            size_hint_y: None
            size_hint_x: None
            height: '64dp'
            width: '192dp'
            text: 'Tutorials'
            on_press: 
                app.playTone(app.Sound.CLICK)
                root.manager.transition.direction = 'left'
                root.manager.current = 'tutorial'
        Button:
            size_hint_y: None
            size_hint_x: None
            height: '64dp'
            width: '192dp'
            text: 'Back'
            on_press:
                app.playTone(app.Sound.CLICK)
                root.manager.transition.direction = 'right'
                root.manager.current = 'car_main_menu'

""")

class MenuScreen(Screen):
    pass

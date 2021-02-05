from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.config import Config
from kivy.core.window import Window
from kivy.core.image import Image as CoreImage
import io
from os.path import dirname, join

stacklayout_args = {
    'orientation': 'lr-tb',
    'padding': 10,
    'spacing': 10
}

curdir = dirname(__file__)
file_names = [join(curdir, 'images', image) for image in ['third_wheel_icon.png',
'pngfind.com-phone-icon-png-1835900.png',
'pngfind.com-location-symbol-png-1655717.png',
'pngfind.com-bluetooth-png-1528441.png',
'pngfind.com-musical-note-png-254061.png',
'pngfind.com-radio-png-524979.png',
'pngfind.com-settings-icon-png-859089.png']]

n = len(file_names)

i_path = 'F:/Programming/user-interface/src/images/pngfind.com-musical-note-png-254061.png'
button_args = {
    'width': 40 + 22 * 5,
    'height': 40 + 22 * 5,
    # 'background_color': (128,128,128, 1),
    # 'background_normal': i_path
}

root = StackLayout(**stacklayout_args)
for i in range(n):
    pass
    btn = Button(size_hint=(None, None), background_normal=file_names[i], **button_args)
    root.add_widget(btn)

class LoginScreen(GridLayout):

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text='User Name'))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text='password'))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)


class MyApp(App):

    def build(self):
        return root
        return LoginScreen()


if __name__ == '__main__':
    Window.size = ((40 + 22 * 5 + 10) * 5 + 10, 500)
    MyApp().run()
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.videoplayer import VideoPlayer

Builder.load_string("""
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
                video_player.state = 'stop'
                root.manager.transition.direction = 'right' 
                root.manager.current = 'tutorial'
                

        VideoPlayer:
            id: video_player
            source: "tutorial/tutorial_rev0.mp4"
            width: 100.0

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

class VideoScreen(Screen):
    pass
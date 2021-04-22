from kivy.uix.gridlayout import GridLayout
from kivy.graphics.texture import Texture

class LanePlot(GridLayout):
    def __init__(self, **kwargs):
        super(LanePlot, self).__init__(**kwargs)

    # re plots the lanes with the given parameters
    def update_plot(self, lane, a, b, c, d):
        image = None
        if (lane is 'left'):
            image = self.children[1]
        else:
            image = self.children[0]

        w, h = image.size
        w, h = int(w), int(h)
        buffer = [0] * w * h * 3
        size_per_pixel = 15 / h
        w_offset = w // 2
        for hi in range(h):
            x = hi * size_per_pixel
            print((a*x**3 + b*x**2 + c*x + d) / size_per_pixel)
            v = int((a*x**3 + b*x**2 + c*x + d) / size_per_pixel) + w_offset
            if (v >= w or v < 0):
                continue
            i = (w * (h - hi - 1) + v) * 3
            buffer[i], buffer[i+1], buffer[i+2] = 255, 255, 255
        texture = Texture.create(size=(w, h))
        texture.blit_buffer(bytes(buffer), colorfmt='rgb', bufferfmt='ubyte')
        image.texture = texture
        image.reload()
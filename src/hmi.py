from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from kivy.clock import Clock

# import screens
from screens.home_screen import CarHomeScreen
from screens.dashboard import Dashboard
from screens.video_screen import VideoScreen
from screens.tutorial_screen import TutorialScreen
from screens.settings_screen import SettingsScreen
from screens.menu_screen import MenuScreen
from screens.ftd_popup import FTDPopUp
from screens.intro_tutorial import IntroVideoScreen

from kivy.uix.popup import Popup


import json



class HMIApp(App):

    # settings
    volume = 0
    ledBrightness = 0

    # first time driver popup window
    ftdPopupWindow = Popup(title="First Time Driver", content=FTDPopUp(), size_hint=(None,None), size=(400,200), auto_dismiss=False)

    # screen manager
    sm = ScreenManager()

    '''
    Begins playback of video
    @param intro: True if intro video, False if accessed from menu
    '''
    def playBack(self, intro):
        video = 'intro_video' if intro else 'video'
        self.sm.get_screen(video).ids[video + '_player'].state = 'play'

    # get volume
    def getVolume(self):
        return self.volume

    # get brightness
    def getLedBrightness(self):
        return self.ledBrightness

    # Sets volume for both dashboard and settings slider values
    def setVolume(self, volume):
        self.volume = volume
        for screen in ['dashboard', 'settings']:
            self.sm.get_screen(screen).ids.volume_slider.value = volume

    # Sets brightness for both dashboard and settings slider values
    def setLedBrightness(self, brightness):
        self.ledBrightness = brightness
        for screen in ['dashboard', 'settings']:
            self.sm.get_screen(screen).ids.led_brightness_slider.value = brightness

    '''
    Gets settings from json
    Creates screen manager and adds all screens as widgets
    '''
    def build(self):

        self.getSettings()
        
        # Create the screen manager
        
        self.sm.add_widget(CarHomeScreen(name='car_main_menu'))
        self.sm.add_widget(Dashboard(name='dashboard'))
        self.sm.add_widget(SettingsScreen(name='settings'))
        self.sm.add_widget(MenuScreen(name='menu'))
        self.sm.add_widget(TutorialScreen(name='tutorial'))
        self.sm.add_widget(VideoScreen(name='video'))
        self.sm.add_widget(IntroVideoScreen(name='intro_video'))

        # open pop-up window
        Clock.schedule_once(lambda dt: self.openPopUpWindow(), 2)

        return self.sm

    # opens first time driver pop-up window
    def openPopUpWindow(self):
        self.ftdPopupWindow.open()

    # closes first time driver pop-up window
    def closePopUpWindow(self):
        self.ftdPopupWindow.dismiss()

    '''
    closes first time driver pop-up window
    switches to introductory video screen
    ''' 
    def playIntroTutorial(self):
        self.closePopUpWindow()
        self.sm.current = 'intro_video'
        self.playBack(True)

    '''
    Runs when application closes
    Saves system state
    '''
    def on_stop(self):
        data = ''
        with open('storage.json') as f:
            data = json.load(f)
            f.close()
            data['control']['c_volume'] = self.volume
            data['control']['c_ledBrightness'] = self.ledBrightness

        with open('storage.json', 'w') as f:
            json.dump(data, f)
            f.close()

    
    
    # Retrieves and stores settings in main memory
    def getSettings(self):

        # get settings
        self.volume = self.getValue('control', 'c_volume')
        self.ledBrightness = self.getValue('control', 'c_ledBrightness')


    
    # Toggles colour of lane in dashboard
    def changeLaneColor(self, color):
        if (color[0] == 0 and color[2] == 0):
            return [1,1,1,1]
        elif (color[0] == 1 and color[2] == 1):
            return [0,1,0,1]
        return [1,1,1,1]


    # Reads variable from settings json
    def getValue(self, vtype, key):
        with open('storage.json') as f:
            data = json.load(f)
            f.close()
            return data[vtype][key]

    
    # Writes variable to settings json    
    def setValue(self, vtype, key, value):
        data = ''
        with open('storage.json') as f:
            data = json.load(f)
            f.close()
            data[vtype][key] = value

        with open('storage.json', 'w') as f:
            json.dump(data, f)
            f.close()

if __name__ == '__main__':
    HMIApp.title = "Lane Centering"
    HMIApp().run()
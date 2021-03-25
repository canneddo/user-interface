from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.popup import Popup

# import screens
from screens.home_screen import CarHomeScreen
from screens.dashboard import Dashboard
from screens.video_screen import VideoScreen
from screens.tutorial_screen import TutorialScreen
from screens.settings_screen import SettingsScreen
from screens.menu_screen import MenuScreen
from screens.intro_tutorial import IntroVideoScreen

# pop up windows
from screens.popups.settings_popup import SettingsPopUp
from screens.popups.ftd_popup import FTDPopUp
from screens.popups.congrats_popup import CongratsPopUp

import sys
sys.path.insert(0, '../../Led-Module')
from LEDModuleLibraryV2 import LEDStrip

from time import sleep
import json


class HMIApp(App):

    # settings
    volume = StringProperty()
    ledBrightness = StringProperty()
    ledBrightnessEnabled = True

    # when intro video should be paused and settings pop-up displayed
    SETTINGS_POPUP_TIME = 67

    # popup windows
    ftdPopupWindow = None
    settingsPopUpWindow = None
    congratsPopUpWindow = None

    # screen manager
    sm = ScreenManager()

    # LED Strip
    strip = LEDStrip()

    '''
    Begins playback of video
    @param intro: True if intro video, False if accessed from menu
    '''
    def playTutorial(self, intro):

        video = None
        if (intro):
            self.closeFTDPopUpWindow()
            video = 'intro_video'
        else:
            video = 'video' 
        
        # specify transition screen and direction
        self.sm.transition.direction = 'left' 
        self.sm.current = video

        # get player and play
        player = self.getPlayer(video)
        player.state = 'play'

        # if intro, schedule pop-ups
        if (intro):
            Clock.schedule_once(lambda dt: self.openSettingsPopUpWindow(player))
            Clock.schedule_once(lambda dt: self.openCongratsPopUpWindow(player))

    # returns player
    def getPlayer(self, video):
        return self.sm.get_screen(video).ids[video + '_player']

    # schedules when to open settings pop up after pausing intro video
    def openSettingsPopUpWindow(self, player):
        Clock.schedule_interval(lambda dt: self.pauseVideoAtTime(player, self.SETTINGS_POPUP_TIME, self.settingsPopUpWindow), 1)

    # opens popup window
    def openPopUp(self, window):
        window.open()

    # schedules when to open settings pop up after intro video ends
    def openCongratsPopUpWindow(self, player):
        Clock.schedule_interval(lambda dt: self.pauseVideoAtTime(player, int(player.duration), self.congratsPopUpWindow), 1)

    # pauses videoplayer at timestamp and opens pop-up window
    def pauseVideoAtTime(self, player, timestamp, window):
        if (int(player.position) >= timestamp):
            player.state = 'pause'
            self.openPopUp(window)
            return False
        elif (player.state == 'stop'):
            return False

    # closes settings pop up and plays intro video
    def closeSettingsPopUpWindow(self, video):
        self.getPlayer(video).state = 'play'
        self.settingsPopUpWindow.dismiss()

    # closes congrats pop up and returns to main menu
    def closeCongratsPopUpWindow(self):
        self.congratsPopUpWindow.dismiss()
        self.sm.transition.direction = 'right'
        self.sm.current = 'car_main_menu'

    # get volume
    def getVolume(self):
        return self.volume

    # get brightness
    def getLedBrightness(self):
        return self.ledBrightness

    # Sets volume for settings slider value
    def setVolume(self, volume):
        self.volume = str(volume)      

    # Sets brightness for settings slider value
    def setLedBrightness(self, brightness):
        self.ledBrightness = str(brightness)
        self.strip.change_brightness(int(2.55*brightness))

    # Sets boolean status of led brightness 
    def enableLedBrightness(self, status):
        self.ledBrightnessEnabled = status
        for screen in ['settings', 'dashboard']:
            self.sm.get_screen(screen).ids.led_brightness_active.active = status

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
        Clock.schedule_once(lambda dt: self.openPopUp(self.ftdPopupWindow), 2)

        return self.sm

    # closes first time driver pop-up window
    def closeFTDPopUpWindow(self):
        self.ftdPopupWindow.dismiss()

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
            data['control']['c_ledBrightnessEnabled'] = self.ledBrightnessEnabled

        with open('storage.json', 'w') as f:
            json.dump(data, f)
            f.close()

    
    
    # Retrieves and stores settings in main memory
    def getSettings(self):
        with open('storage.json') as f:
            data = json.load(f)
            f.close()
            
            # get settings
            self.volume = data['control']['c_volume']
            self.ledBrightness = data['control']['c_ledBrightness']
            self.ledBrightnessEnabled = data['control']['c_ledBrightnessEnabled']
        
        # first time driver popup window
        self.ftdPopupWindow = Popup(title="First Time Driver", content=FTDPopUp(), size_hint=(None,None), size=(400,200), auto_dismiss=False)
    
        # settings pop up window
        self.settingsPopUpWindow = Popup(title="Change Lane Centering settings below", content=SettingsPopUp(), size_hint=(None,None), size=(600,300), auto_dismiss=False)

        # congrats pop up window
        self.congratsPopUpWindow = Popup(title="Congratulations!", content=CongratsPopUp(), size_hint=(None,None), size=(400,200), auto_dismiss=False)

    # Toggles colour of lane in dashboard
    def changeLaneColor(self, color):
        if (color[0] == 0 and color[2] == 0):
            return [1,1,1,1]
        elif (color[0] == 1 and color[2] == 1):
            return [0,1,0,1]
        return [1,1,1,1]

    def playButtonTone(self):
        tone = SoundLoader.load('sounds/tone.mp3')
        tone.volume = int(self.getVolume())/100
        tone.play()

if __name__ == '__main__':
    HMIApp.title = "Lane Centering"
    Window.fullscreen = True
    Window.size = (800,480)
    HMIApp().run()

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.core.audio import SoundLoader
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
# from kivy.event import EventDispatcher
from kivy.uix.popup import Popup
from kivy.uix.label import Label

# import screens
from screens.home_screen import CarHomeScreen
from screens.dashboard import Dashboard
from screens.video_screen import VideoScreen
from screens.tutorial_screen import TutorialScreen
from screens.settings_screen import SettingsScreen
from screens.menu_screen import MenuScreen
from screens.intro_tutorial import IntroVideoScreen

from receive import Receiver

# pop up windows
from screens.popups.settings_popup import SettingsPopUp
from screens.popups.ftd_popup import FTDPopUp
from screens.popups.congrats_popup import CongratsPopUp

import sys, os
# sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'LED-Module'))
# from LEDModuleLibraryV2 import LEDStrip

from time import sleep
from threading import Thread
import json

class HMIApp(App):

    # user settings
    volume = StringProperty()
    ledBrightness = StringProperty()
    ledBrightnessEnabled = True

    # vehicle info settings
    leftLaneDetected = NumericProperty(0)
    rightLaneDetected = NumericProperty(0)
    laneCenteringStatus = NumericProperty(0)
    shifterPosition = NumericProperty(0)
    vehiclePosition = NumericProperty(0)
    yawRate = NumericProperty(0)
    desiredVehiclePosition = NumericProperty(0)
    

    # left lane settings
    # distanceToLeftLane = NumericProperty()
    # leftLaneCurvature = NumericProperty()
    # leftLaneCurvatureDerivative = NumericProperty()
    # leftLaneHeading = NumericProperty()

    # # right lane settings
    # distanceToRightLane = NumericProperty()
    # rightLaneCurvature = NumericProperty()
    # rightLaneCurvatureDerivative = NumericProperty()
    # rightLaneHeading = NumericProperty()

    # when intro video should be paused and settings pop-up displayed
    SETTINGS_POPUP_TIME = 67

    # shutdown event
    shutdownEvent = None
    shutdownTimeOut = 30

    # popup windows
    ftdPopupWindow = Popup(title="First Time Driver", content=FTDPopUp(), size_hint=(None,None), size=(400,200), auto_dismiss=False)
    settingsPopUpWindow = None
    congratsPopUpWindow = Popup(title="Congratulations!", content=CongratsPopUp(), size_hint=(None,None), size=(400,200), auto_dismiss=False)

    newDriverPopUpWindow = Popup(title="New Driver", content=Label(text='You are a NEW driver.', font_size=20), size_hint=(None,None), size=(400,200), auto_dismiss=False)
    returningDriverPopUpWindow = Popup(title="Returning Driver", content=Label(text='You are a RETURNING driver.', font_size=20), size_hint=(None,None), size=(400,200), auto_dismiss=False)

    STORAGE_PATH = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    # screen manager
    sm = ScreenManager()

    # LED Strip
    # strip = LEDStrip()
    # strip.change_brightness(i**2)

    def on_shifterPosition(self, instance, value):
        self.switch()

    def on_leftLaneDetected(self, instance, value):
        self.laneDetected('left', int(self.leftLaneDetected))
        self.displayedMessage(int(self.laneCenteringStatus))

    def on_rightLaneDetected(self, instance, value):
        self.laneDetected('right', int(self.rightLaneDetected))
        self.displayedMessage(int(self.laneCenteringStatus))

    def on_laneCenteringStatus(self, instance, value):
        status = int(self.laneCenteringStatus)
        self.toggleLaneCentering(status)
        self.displayedMessage(status)
        self.shutDownAppOnError(status)
        
    def on_vehiclePosition(self, instance, value):
        pos, laneWidth = strip.vehicle_position_conversion(distFromLeft, distFromRight)
        strip.direction_to_travel(pos, laneWidth)

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

    # gets object from dashboard using id
    def getFromDashboard(self, id):
        return self.sm.get_screen('dashboard').ids[id]

    '''
    lane centering display (car and 2 lanes)
    param: status: 0 or 2(inactive), 1(active), 3(error)
    displays only when status is 1
    '''
    def toggleLaneCentering(self, status):
        objects = ['left_lane', 'right_lane', 'vehicle']
        opacity = 1 if status == 1 else 0
        for obj in objects:
            self.getFromDashboard(obj).opacity = opacity

    '''
    lanes detected
    param: side (left or right)
    param: detected (0 or 1)
    selected lane becomes green if detected is 1
    '''
    def laneDetected(self, side, detected):
        self.getFromDashboard(side + '_lane').background_color = [0,1,0,1] if detected == 1 else [1,1,1,1]

    def shutDownAppOnError(self, status):
        # initiate shutdown in 30s if status is 3 and current screen is dashboard
        if (status == 3 and self.sm.current == 'dashboard'):
            self.shutdownEvent = Clock.schedule_once(lambda dt: self.stop(), self.shutdownTimeOut)
        else:
            if self.shutdownEvent != None:
                # if status changes within 30 sec, unschedule and nullify event.
                Clock.unschedule(self.shutdownEvent)
                self.shutdownEvent = None
    
    '''
    which message to display
    param: status: 0 or 2(inactive), 1(active), 3(error)
    '''
    def displayedMessage(self, status):
        # list of labels
        labels = ['labelInactive', 'labelActive', 'labelConnectionLost']

        # get label objects
        objects = list(map(lambda label: self.getFromDashboard(label), labels))

        # conceal all labels
        for obj in objects:
            obj.opacity = 0
        
        # get correct index (2 is same as 0 since it is unused)
        index = None
        if status == 1:
            if int(self.leftLaneDetected) == 1 and int(self.rightLaneDetected) == 1:
                index = 1
            else:
                index = 0
        elif status == 3:
            index = 2

        # use appropriate index to target which label to display
        if index != None:
            objects[index].opacity = 1

    # returns player
    def getPlayer(self, video):
        return self.sm.get_screen(video).ids[video + '_player']

    # schedules when to open settings pop up after pausing intro video
    def openSettingsPopUpWindow(self, player):
        Clock.schedule_interval(lambda dt: self.pauseVideoAtTime(player, self.SETTINGS_POPUP_TIME, self.settingsPopUpWindow), 1)

    # opens popup window
    def openPopUp(self, window):
        window.open()

        
    # switches screens based on shifter position
    def switch(self):
        # switch to dashboard if not in park
        if int(self.shifterPosition) != 0:
            if self.sm.current == 'car_main_menu':
                self.homeToDashboard()
            elif self.sm.current == 'video':
                self.videoToDashboard(False)
            elif self.sm.current == 'intro_video':
                self.videoToDashboard(True)
            elif self.sm.current != 'dashboard':
                self.toDashboard()
        else:
            self.dashboardToHome()

    # receives input from mocked CAV
    def receive(self):
        receiver = Receiver('vcan0', True)
        t = Thread(target=receiver.receive, daemon=True, name='can-receiver')
        t.start()
        while True: 
            sleep(0.5)
            vehicleInfo = receiver.getVehicleInfo()
            leftLaneA = receiver.getLeftLaneInfo()
            rightLaneA = receiver.getRightLaneInfo()

            if (vehicleInfo is not None):
                self.shifterPosition = vehicleInfo.shifter_position
                self.leftLaneDetected = vehicleInfo.lane_left_detected
                self.rightLaneDetected = vehicleInfo.lane_right_detected
                self.laneCenteringStatus = vehicleInfo.lane_centering_status
            
            if((leftLaneA is not None) and (rightLaneA is not None)):
                self.vehiclePosition = leftLaneA.distance_to_lane - rightLaneA.distance_to_lane

    # thread starts receiver
    def startReceiver(self):
        receiverThread = Thread(target=self.receive, daemon=True, name='can-receiver-starter')
        receiverThread.start()

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
    def closeSettingsPopUpWindow(self, video, action):
        self.getPlayer(video).state = action
        self.settingsPopUpWindow.dismiss()

    # closes congrats pop up and returns to main menu
    def closeCongratsPopUpWindow(self):
        self.congratsPopUpWindow.dismiss()
        self.sm.transition.direction = 'right'
        self.sm.current = 'car_main_menu'

    # switches from home to dashboard
    def homeToDashboard(self):
        self.closeFTDPopUpWindow(None) # close if open
        self.toDashboard()

    # switches from dashboard to home
    def dashboardToHome(self):
        self.sm.transition.direction = 'left'
        self.sm.current = 'car_main_menu'

    '''
    switches from a video screen to dashboard
    param intro: (boolean) if current screen is intro_video
    '''
    def videoToDashboard(self, intro):
        video = 'intro_video' if intro else 'video' # get screen
        self.getPlayer(video).state == 'stop' # stop video (also unschedules pop-up scheduler)

        # close in case open
        if intro:
            self.closeSettingsPopUpWindow(video, 'stop')
            self.closeCongratsPopUpWindow()

        self.toDashboard()

    # switches to dashboard
    def toDashboard(self):
        self.sm.transition.direction = 'right'
        self.sm.current = 'dashboard'


    # get volume
    def getVolume(self):
        return self.volume

    # get brightness
    def getLedBrightness(self):
        return self.ledBrightness

    '''
    Sets volume level
    @param volume: (int) volume level
    ''' 
    def setVolume(self, volume):
        self.volume = str(volume)      

    '''
    Sets brightness level
    @param brightness: (int) brightness level
    ''' 
    def setLedBrightness(self, brightness):
        self.ledBrightness = str(brightness)
        self.strip.change_brightness(int(2.55*brightness))

    '''
    Sets brightness for settings slider value
    @param status: (boolean) brightness enabled
    '''  
    def enableLedBrightness(self, status):
        self.ledBrightnessEnabled = status
        if status:
            brightness = int(str(self.ledBrightness))
            self.strip.change_brightness(int(2.55*brightness))
        else:
            self.strip.change_brightness(0)

        # change checkbox status in settings page
        for screen in ['settings', 'dashboard']:
            self.sm.get_screen(screen).ids.led_brightness_active.active = status

    '''
    Gets settings from json
    Creates screen manager and adds all screens as widgets
    '''
    def build(self):

        # get settings from json
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
        Clock.schedule_once(lambda dt: self.openPopUp(self.ftdPopupWindow), 0)

        # start receiver
        self.startReceiver()

        return self.sm

    '''
    closes first time driver popup window
    opens another pop-up for 2 seconds notifying driver if they are new or returning.
    @param new: (boolean) new driver; defaults to true
    '''
    def closeFTDPopUpWindow(self, new=True):
        self.ftdPopupWindow.dismiss()
        if new != None:
            self.displayDriverStatus(new)

    ''' 
    Notifies driver if they are a new or returning driver
    @param new: (boolean) new driver
    '''
    def displayDriverStatus(self, new):
        popup = None
        if new:
            popup = self.newDriverPopUpWindow
        else:
            popup = self.returningDriverPopUpWindow

        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)
        return

    '''
    Runs when application closes
    Saves system state
    '''
    def on_stop(self):
        data = ''
        with open(os.path.join(self.STORAGE_PATH,'storage.json')) as f:
            data = json.load(f)
            f.close()
            data['control']['c_volume'] = self.volume
            data['control']['c_ledBrightness'] = self.ledBrightness
            data['control']['c_ledBrightnessEnabled'] = self.ledBrightnessEnabled

        with open(os.path.join(self.STORAGE_PATH,'storage.json'), 'w') as f:
            json.dump(data, f)
            f.close()    
    
    # Retrieves and stores settings in main memory
    def getSettings(self):
        with open(os.path.join(self.STORAGE_PATH,'storage.json')) as f:
            data = json.load(f)
            f.close()
            
            # get settings
            self.volume = data['control']['c_volume']
            self.ledBrightness = data['control']['c_ledBrightness']
            self.ledBrightnessEnabled = data['control']['c_ledBrightnessEnabled']
    
        # settings pop up window
        self.settingsPopUpWindow = Popup(title="Change Lane Centering settings below", content=SettingsPopUp(), size_hint=(None,None), size=(600,300), auto_dismiss=False)

        

    # Toggles colour of lane in dashboard
    def changeLaneColor(self, color):
        if (color[0] == 0 and color[2] == 0):
            return [1,1,1,1]
        elif (color[0] == 1 and color[2] == 1):
            return [0,1,0,1]
        return [1,1,1,1]

    def playButtonTone(self):
        tone = SoundLoader.load('sounds/tone.mp3')
        if tone:
            tone.volume = int(self.getVolume())/100
            tone.play()


if __name__ == '__main__':
    HMIApp.title = "Lane Centering"
    # Window.fullscreen = True
    Window.size = (800,480)
    HMIApp().run()

from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import MDList
from kivy.core.window import Window

import parselmouth
from parselmouth.praat import call
import pandas as pd
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv

import psycopg2

Window.size = (300, 500)

screen_helper = """
ScreenManager:
    Welcome:
    MenuScreen:
    ProfileScreen:
    ShowResult:
    LogIn:
    SignIn:
    Result:
    
<Welcome>:
    name: 'welcome'
    Screen:
        MDNavigationLayout:
            ScreenManager:
                Screen:
                    MDLabel:
                        text: "Tremors"
                        halign:"center"
                        theme_text_color: "Custom"
                        font_style:'H2'
                        text_color: 0, 1, 0, 1
                        pos_hint: {'center_x':0.5,'center_y':0.7}
                
                    MDRoundFlatButton:
                        text: "Let's Start"
                        font_style:'Button'
                        padding: "8dp"
                        spacing: "8dp"
                        md_bg_color: 0, 0.5, 0, 1
                        pos_hint: {'center_x':0.5,'center_y':0.4}
                        on_press: root.manager.current = 'menu'
                        elevation_normal:12
        
<ProfileScreen>:
    name: 'profile'
    Screen:
        MDNavigationLayout:
            ScreenManager:
                Screen:
                    MDRoundFlatButton:
                        text: "Log In"
                        font_style:'Button'
                        padding: "8dp"
                        spacing: "8dp"
                        md_bg_color: 0, 1, 0, 1
                        pos_hint: {'center_x':0.5,'center_y':0.7}
                        on_press: root.manager.current = 'LogIn'
                        elevation_normal:12
                    MDRoundFlatButton:
                        text: "Sign In"
                        font_style:'Button'
                        padding: "8dp"
                        spacing: "8dp"
                        md_bg_color: 0, 1, 0, 1
                        pos_hint: {'center_x':0.5,'center_y':0.3}
                        on_press: root.manager.current = 'SignIn'
                        elevation_normal:12


<LogIn>:
    name: 'LogIn'
    Screen:
        MDNavigationLayout:
            ScreenManager:
                Screen:
                    MDTextField:
                        id: username
                        hint_text: "Enter username"
                        helper_text: "or click on forgot username"
                        helper_text_mode: "on_focus"
                        icon_right: "text-account"
                        icon_right_color: app.theme_cls.primary_color
                        pos_hint:{'center_x': 0.5, 'center_y': 0.7}
                        size_hint_x:None
                        width:300
                    MDTextField:
                        id: email
                        hint_text: "Enter E-mail"
                        helper_text: "or click on forgot username"
                        helper_text_mode: "on_focus"
                        icon_right: "email-outline"
                        icon_right_color: app.theme_cls.primary_color
                        pos_hint:{'center_x': 0.5, 'center_y': 0.5}
                        size_hint_x:None
                        width:300
                    MDTextField:
                        id: paswd
                        hint_text: "Enter Password"
                        helper_text: "or click on forgot username"
                        helper_text_mode: "on_focus"
                        icon_right: "form-textbox-password"
                        icon_right_color: app.theme_cls.primary_color
                        pos_hint:{'center_x': 0.5, 'center_y': 0.3}
                        size_hint_x:None
                        width:300
                    
                    
                    MDRoundFlatButton:
                        text: "Log In"
                        font_style:'Button'
                        padding: "8dp"
                        spacing: "8dp"
                        md_bg_color: 0, 1, 0, 1
                        pos_hint: {'center_x':0.5,'center_y':0.2}
                        on_press: 
                            app.submit()
                            root.manager.current = 'menu'
                        elevation_normal:12
    
<SignIn>:
    name: 'SignIn'
    Screen:
        MDNavigationLayout:
            ScreenManager:
                Screen:
                    MDTextField:
                        id: usernamesignin
                        hint_text: "Enter username"
                        helper_text: "or click on forgot username"
                        helper_text_mode: "on_focus"
                        icon_right: "text-account"
                        icon_right_color: app.theme_cls.primary_color
                        pos_hint:{'center_x': 0.5, 'center_y': 0.7}
                        size_hint_x:None
                        width:300
                    MDTextField:
                        id: emailsignin
                        hint_text: "Enter E-mail"
                        helper_text: "or click on forgot username"
                        helper_text_mode: "on_focus"
                        icon_right: "email-outline"
                        icon_right_color: app.theme_cls.primary_color
                        pos_hint:{'center_x': 0.5, 'center_y': 0.5}
                        size_hint_x:None
                        width:300
                    MDTextField:
                        id: paswdsignin
                        hint_text: "Enter Password"
                        helper_text: "or click on forgot username"
                        helper_text_mode: "on_focus"
                        icon_right: "form-textbox-password"
                        icon_right_color: app.theme_cls.primary_color
                        pos_hint:{'center_x': 0.5, 'center_y': 0.3}
                        size_hint_x:None
                        width:300
                    MDRoundFlatButton:
                        text: "Create Account"
                        font_style:'Button'
                        padding: "8dp"
                        spacing: "8dp"
                        md_bg_color: 0, 1, 0, 1
                        pos_hint: {'center_x':0.5,'center_y':0.2}
                        on_press: app.submit()
                        elevation_normal:12
                        
                    MDRoundFlatButton:
                        text: "Log In"
                        font_style:'Button'
                        padding: "8dp"
                        spacing: "8dp"
                        md_bg_color: 0, 1, 0, 1
                        pos_hint: {'center_x':0.5,'center_y':0.1}
                        on_press: root.manager.current = 'LogIn'
                        elevation_normal:12
        
        
<MenuScreen>:
    name: 'menu'
    Screen:
        MDNavigationLayout:
            ScreenManager:
                Screen:
                    BoxLayout:
                        orientation: 'vertical'
                        MDToolbar:
                            title: 'Tremors'
                            
                            left_action_items: [['menu', lambda x: nav_drawer.set_state('toggle')]]
                            elevation:5
                        Widget:
                    
                    
                    MDLabel:
                        text: "Eusuf Abdullah"
                        halign:"center"
                        theme_text_color: "Custom"
                        font_style:'Subtitle2'
                        font_size: 32
                        text_color: 0, 1, 0, 1
                        pos_hint: {'center_x':0.5,'center_y':0.8}
                      
                    MDLabel:
                        text: "Please Record your voice"
                        halign:"center"
                        theme_text_color: "Secondary"
                        font_style:'Subtitle2'
                        text_color: 0, 1, 0, 1
                        pos_hint: {'center_x':0.5,'center_y':0.6}
                        
                    MDIconButton:
                        icon:'record-rec'
                        pos_hint: {'center_x':0.5,'center_y':0.5}
                        user_font_size: (dp(100))
                        theme_icon_color: "Red"
                        on_press:
                            app.recording()
                        
                    MDRoundFlatButton:
                        text: "Upload Report"
                        font_style:'Button'
                        padding: "8dp"
                        spacing: "8dp"
                        md_bg_color: 0, 1, 0, 1
                        pos_hint: {'center_x':0.5,'center_y':0.3}
                        on_press: app.voice_submit()
                        elevation_normal:12
                    MDRoundFlatButton:
                        text: "Show Report"
                        font_style:'Button'
                        padding: "8dp"
                        spacing: "8dp"
                        md_bg_color: 0, 1, 0, 1
                        pos_hint: {'center_x':0.5,'center_y':0.2}
                        on_press: root.manager.current = 'showresult'
                        elevation_normal:12
                    
                        
                    
                        
            MDNavigationDrawer:
                id: nav_drawer
                ContentNavigationDrawer:
                    orientation: 'vertical'
                    padding: "8dp"
                    spacing: "8dp"
                    Image:
                        id: avatar
                        size_hint: (1,1)
                        source: "eusuf.jpg"
                    MDLabel:
                        text: "Eusuf Abdullah"
                        font_style: "Subtitle1"
                        size_hint_y: None
                        height: self.texture_size[1]
                    MDLabel:
                        text: "eusufabdullah13@gmail.com"
                        size_hint_y: None
                        font_style: "Caption"
                        height: self.texture_size[1]
                    ScrollView:
                        DrawerList:
                            id: md_list
    
                            MDList:
                                OneLineIconListItem:
                                    text: "Profile"
    
                                    IconLeftWidget:
                                        icon: "face-profile"
    
    
    
                                OneLineIconListItem:
                                    text: "Upload"
    
                                    IconLeftWidget:
                                        icon: "upload"
    
    
                                OneLineIconListItem:
                                    text: "Logout"
    
                                    IconLeftWidget:
                                        icon: "logout"
    
<ShowResult>:
    name:'showresult'
    Screen:
        MDNavigationLayout:
            ScreenManager:
                Screen:
                    MDLabel:
                        id: word_label
                        text_size: self.size
                        halign: "center"
                        valign: "middle"
                        text: 'Voice Manipulation Report '
                        font_size: 32
                        pos_hint: {'center_x':0.5,'center_y':0.9}
                    MDRectangleFlatButton:
                        text: 'Result'
                        pos_hint: {'center_x':0.5,'center_y':0.2}
                        on_press: root.manager.current = 'result'
    
    
<Result>:
    name: 'result'
    Screen:
        MDNavigationLayout:
            ScreenManager:
                Screen:
                    MDLabel:
                        id: result_label
                        text: 'You are risk free'
                        halign: 'center'
                        pos_hint: {'center_x':0.5,'center_y':0.6}
                    MDRectangleFlatButton:
                        text: 'Back'
                        pos_hint: {'center_x':0.5,'center_y':0.3}
                        on_press: root.manager.current = 'menu'
                        
                    MDBottomAppBar:
                        MDToolbar:
                            title: ' '
                            icon: 'email-send-outline'
                            type: 'bottom'
                            left_action_items: [["whatsapp", lambda x: app.navigation_draw()]]
                            right_action_items: [["linkedin", lambda x: app.navigation_draw()]]
                            mode: 'free-end'
                            on_action_button: app.navigation_draw()
                        

"""

class Welcome(Screen):
    pass

class MenuScreen(Screen):
    pass

class ContentNavigationDrawer(BoxLayout):
    pass

class DrawerList( ThemableBehavior, MDList):
    pass

class ProfileScreen(Screen):
    pass


class Result(Screen):
    pass

class ShowResult(Screen):
    pass

class LogIn(Screen):
    pass

class SignIn(Screen):
    pass

# Create the screen manager
sm = ScreenManager()
sm.add_widget(Welcome(name='welcome'))
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(ProfileScreen(name='profile'))
sm.add_widget(Result(name='result'))
sm.add_widget(ShowResult(name='showresult'))
sm.add_widget(LogIn(name='LogIn'))
sm.add_widget(SignIn(name='SignIn'))



class DemoApp(MDApp):

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.primary_hue="A700"
        self.theme_cls.theme_style="Dark"
        conn = psycopg2.connect(
            host="ec2-3-230-122-20.compute-1.amazonaws.com",
            database="d7ef5fi0af4k0h",
            user="tisslgfjmjozpq",
            password="20412334f7a9c13154b954d53a1b92bea9072c02df8ff2354672b699999bace5",
            port="5432",
        )
        c = conn.cursor()
        c.execute("""CREATE TABLE if not exists user_info(name TEXT , email TEXT , password TEXT);""")
        c.execute("""CREATE TABLE if not exists voice_report(voice TEXT);""")
        conn.commit()
        conn.close()


        screen = Builder.load_string(screen_helper)
        return screen


    def recording(self):
        freq = 44100
        duration = 5
        recording = sd.rec(int(duration * freq),samplerate=freq, channels=2)
        sd.wait()
        write("recording0.wav", freq, recording)
        wv.write("recording1.wav", recording, freq, sampwidth=2)

    def submit(self):
        #username_signin =self.strng.get_screen('SignIn').ids.usernamesignin.text
        #email_signin =self.strng.get_screen('SignIn').ids.emailsignin.text
        #paswd_signin =self.strng.get_screen('SignIn').ids.paswdsignin.text

        conn = psycopg2.connect(
            host="ec2-3-230-122-20.compute-1.amazonaws.com",
            database="d7ef5fi0af4k0h",
            user="tisslgfjmjozpq",
            password="20412334f7a9c13154b954d53a1b92bea9072c02df8ff2354672b699999bace5",
            port="5432",
        )
        c = conn.cursor()
        sql_command = "INSERT INTO user_info (name,email,password) VALUES (%s)"
        values = (self.root.ids.usernamesignin.text, self.root.ids.emailsignin.text, self.root.ids.paswdsignin.text,)
        print(values)
        #values = (username_signin,email_signin,paswd_signin)
        c.execute(sql_command, values)
        '''self.root.ids.word_label.text = f'{self.root.ids.usernamesignin.text} Added'
        self.root.ids.word_label.text = f'{self.root.ids.emailsignin.text} Added'
        self.root.ids.word_label.text = f'{self.root.ids.paswdsignin.text} Added' '''

        conn.commit()
        conn.close()

    def voice_submit(self):
        conn = psycopg2.connect(
            host="ec2-3-230-122-20.compute-1.amazonaws.com",
            database="d7ef5fi0af4k0h",
            user="tisslgfjmjozpq",
            password="20412334f7a9c13154b954d53a1b92bea9072c02df8ff2354672b699999bace5",
            port="5432",
        )
        c = conn.cursor()

        sound = parselmouth.Sound("recording1.wav")
        manipulation = call(sound, "To Manipulation", 0.01, 75, 600)
        pitch = sound.to_pitch()
        pulses = parselmouth.praat.call([sound, pitch], "To PointProcess (cc)")
        voice_report_str = parselmouth.praat.call([sound, pitch, pulses], "Voice report", 0.0, 0.0, 75, 600, 1.3, 1.6,
                                                  0.03, 0.45)
        with open("voice_report.csv", "w") as file:
            file.write(voice_report_str + "\n")
        df = pd.read_csv('voice_report.csv', sep='\t')
        df.rename(columns={'   From 0 to 0 seconds (duration: 4.800000 seconds)': 'report'}, inplace=True)
        #text = ' '.join([i for i in df['report']])
        k = []
        for i in df['report']:
            print(i)
            k.append(i)
        #text = text.replace(",", " ")

        sql_command = "INSERT INTO voice_report (voice) VALUES (%s)"
        values = k
        c.execute(sql_command, values)
        '''self.root.ids.word_label.text = f'{self.root.ids.word_input.text} Added'
        self.root.ids.word_input.text = '' '''
        print(values)
        conn.commit()
        conn.close()

    def show_records(self):
        # Create Database Or Connect To One
        # conn = sqlite3.connect('first_db.db')
        conn = psycopg2.connect(
            host="ec2-3-230-122-20.compute-1.amazonaws.com",
            database="d7ef5fi0af4k0h",
            user="tisslgfjmjozpq",
            password="20412334f7a9c13154b954d53a1b92bea9072c02df8ff2354672b699999bace5",
            port="5432",
        )
        c = conn.cursor()
        c.execute("SELECT * FROM voice_report")
        records = c.fetchall()
        word = ''
        for record in records:
            word = f'{word}\n{record[0]}'
            self.root.ids.word_label.text = f'{word}'
        conn.commit()
        conn.close()



DemoApp().run()
#--[Start platform specific code]
"""This code to detect it's Android"""
from kivy.uix.screenmanager import Screen
from kivy.utils import platform
import os
os.environ['KIVY_GL_BACKEND'] = 'sdl2'
if platform != 'android':
    from kivy.config import Config
    Config.set("graphics","width",305)
    Config.set("graphics","height",580)
    Config.set('graphics', 'multisamples', '0')  # sdl error
    Config.set('kivy', 'window_icon', 'assets/img/subsidy-icon.png')  # the icon in top-left of window
#--[End platform specific code]

#--[Start Soft_Keyboard code ]
"""Code for android keyboard. when in android keyboard show textbox automatic go to top of keyboard"""
from kivy.core.window import Window
# Window.keyboard_anim_args = {"d":.2,"t":"linear"}
Window.keyboard_anim_args = {'d': 0.5, 't': 'in_out_quart'}
Window.softinput_mode="below_target"
#--[End Soft_Keyboard code ]

"""Main imports -> Requirements for this App"""
from main_imports import MDApp, MDIconButton, ILeftBodyTouch, TwoLineAvatarListItem, ImageLeftWidget, MDFlatButton, toast, Factory, MDCustomBottomSheet, MDThemePicker, Clock, MDDialog, ScreenManager
import kivymd.font_definitions
from kivymd.uix.button import MDRaisedButton
from baseclass.help import HelpScreen
import json
import requests
# import kivymd_extensions.akivymd
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import IRightBodyTouch
import plyer
import datetime

APP = MDApp.get_running_app()

class Home_Screen(Screen):
    pass

sm = ScreenManager()
sm.add_widget(Home_Screen(name = 'home'))

class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
    pass

class Container(IRightBodyTouch, MDBoxLayout):
    adaptive_width = True


class MainApp(MDApp):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.app = MDApp.get_running_app()
        
        self.APP_NAME = "SubsidyApp"
        self.COMPANY_NAME = "Optichem"

        self.title = "SubsidyApp"
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.primary_hue = "700"
        self.theme_cls.accent_palette = "Red"
        self.theme_cls.accent_hue = "100"
        self.theme_cls.theme_style = "Light"
        
        self.close_about_dialog = None
        self.content = None
        self.url  = "https://agriculturalsubsidy-default-rtdb.firebaseio.com/feedback/.json"

    user_idToken = ""
    local_id = ""
    email_id = ""
    dialog = None

    def show_about_dialog(self):
        if not self.close_about_dialog:
            self.close_about_dialog = MDDialog(
                size_hint=(.8, .7),
                title="HELP",
                type="custom",
                content_cls=HelpScreen(),
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release = self.close_dialog_about
                    )
                ]
            )
        self.close_about_dialog.open()

    def close_dialog_about(self, button):
        self.close_about_dialog.dismiss()
        self.close_about_dialog = None
     
    def send_feedback(self, the_label, feedback_content):
        self.url  = "https://agriculturalsubsidy-default-rtdb.firebaseio.com/feedback/.json"
        date = datetime.datetime.now()
        if feedback_content.split() == []:
            plyer.notification.notify( title="Error!", message = "Sorry, Invalid Credentials!")
            cancel_dialogue = MDFlatButton(text = 'Retry',on_release = self.close_dialog)
            self.dialog = MDDialog(title = 'Error',text = 'Please Send Again!',size_hint = (0.7,0.2),buttons = [cancel_dialogue])
            self.dialog.open()
        else:
            feedback = str({f'\"{the_label}\":{{"Message":\"{feedback_content}\","SentFrom":\"{the_label}\","DateSent":\"{date.strftime("%Y-%m-%d %H:%M:%S")}\"}}'})
            # feedback = str({f'\"{feedback_content}\":{{"SentFrom":\"{the_label}\"}}'})
            feedback = feedback.replace(".","-")
            feedback  = feedback.replace("\'","")
            send_to_database = json.loads(feedback)
            print((send_to_database))
            requests.patch(url = self.url,json = send_to_database)
            toast("Your Feedback has been Sent!")
            cancel_dialogue = MDFlatButton(text = 'OK',on_release = self.close_dialog)
            self.dialog = MDDialog(title = 'Success',text = 'Your Feedback has been Sent!!',size_hint = (0.7,0.2),buttons = [cancel_dialogue])
            self.dialog.open()

    def register_farmer(self, the_label, qrcode_details):
        self.url  = "https://agriculturalsubsidy-default-rtdb.firebaseio.com/registeredFarmer/.json"
        date = datetime.datetime.now()
        if qrcode_details.split() == []:
            cancel_dialogue = MDFlatButton(text = 'Retry',on_release = self.close_dialog)
            self.dialog = MDDialog(title = 'Error',text = 'Please Scan QRCode!',size_hint = (0.7,0.2),buttons = [cancel_dialogue])
            self.dialog.open()
        else:
            # qrcode_info = str({f'\"{qrcode_details}\":{{"RegisteredBy":\"{the_label}\"}}'})
            qrcode_info = str({f'\"{qrcode_details}\":{{"Details":\"{qrcode_details}\","RegisteredBy":\"{the_label}\","RegisteredDate":\"{date.strftime("%Y-%m-%d %H:%M:%S")}\"}}'})
            qrcode_info  = qrcode_info.replace(".","-")
            qrcode_info  = qrcode_info.replace("\'","")
            send_to_database = json.loads(qrcode_info)
            print((send_to_database))
            requests.patch(url = self.url,json = send_to_database)
            toast("Farmer Registered Successfully!")
            cancel_dialogue = MDFlatButton(text = 'OK',on_release = self.close_dialog)
            self.dialog = MDDialog(title = 'Success',text = 'Farmer Registered Successfully!',size_hint = (0.7,0.2),buttons = [cancel_dialogue])
            self.dialog.open()

    def close_dialog(self,obj):
        self.dialog.dismiss()

    def display_user_tokens(self):
        self.root.ids.the_label.text = self.email_id
    
    def show_custom_bottom_sheet(self):
        self.custom_sheet = MDCustomBottomSheet(screen=Factory.ContentCustomSheet())
        self.custom_sheet.open()

    def login_user(self):
        self.root.ids.firebase.go_home()
        self.root.current = 'firebase'

    def sign_out(self):
        self.root.ids.firebase.log_out()
        self.root.current = 'firebase'
    
    def view_notifications(self):
        self.root.ids.firebase.view_notifications_screen()
        self.root.current = 'firebase'

    def go_to_settings(self):
        self.root.ids.firebase.change_screen()
        self.root.current = 'firebase'

    def go_to_send_message(self):
        self.root.ids.firebase.senf_feedback()
        self.root.current = 'firebase'

    def view_registered_list(self):
        self.root.ids.firebase.show_all_farmers()
        self.root.current = 'firebase'

    def go_back_home(self):
        self.root.current = "home"


if __name__ == "__main__":
    # Start application from here.
    MainApp().run()


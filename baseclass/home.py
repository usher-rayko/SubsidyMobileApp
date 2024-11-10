# from firebase import Firebase
from kivymd.uix.button import MDRaisedButton
from main_imports import ImageLeftWidget, Clock, TwoLineAvatarListItem, Screen, MDDialog, MDFlatButton, MDApp, toast
from database import Database
from send_feedback import SendFeedback
import json
import requests


DATABASE = Database()
APP = MDApp.get_running_app()


class Home_Screen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)        
        self.send_feedback_dialog = None
        self.content = None
        self.hint_email = "Admin Email Address"
        self.feedback_title = None
        self.feedback_content = None
        self.url  = "https://agriculturalsubsidy-default-rtdb.firebaseio.com/feedback/.json"
        
    user_idToken = ""
    local_id = ""
    email_id = ""
    url  = "https://agriculturalsubsidy-default-rtdb.firebaseio.com/feedback/.json"
    dialog = None

    def display_user_tokens(self):
        self.root.ids.the_label.text = "Welcome: " + self.email_id

    # def on_pre_enter(self, *args):
        # self.send_feedback_button.bind(on_release=self.show_send_feedback_dialog)
        # self.load_data()

    def load_data(self):
        return

    def refresh_callback(self, *args):
        def refresh_callback(interval):
            self.ids.refresh_layout.refresh_done()

        self.load_data()
        Clock.schedule_once(refresh_callback, 1.5)

    def show_alert_dialog(self):
        if not self.send_feedback_dialog:
            self.send_feedback_dialog = MDDialog(
                size_hint=(.8, .7),
                title="SEND FEEDBACK",
                type="custom",
                # textbox="",
                content_cls=SendFeedback(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        text_color=APP.theme_cls.primary_color,
                        on_release=self.close_dialog
                    ),
                    MDFlatButton(
                        text="SEND",
                        text_color=APP.theme_cls.primary_color,
                        on_release= self.send_feedback
                    )
                ]
            )
        self.send_feedback_dialog.open()
    
    def send_feedback(self, button):
        try:
            feedbackTitle = self.ids.feedback_title.text
            feedbackContent = self.ids.feedback_content.text
            if feedbackTitle.split() == [] or feedbackContent.split() == []:
                cancel_btn_dialogue = MDFlatButton(text = 'Retry',on_release = self.close_dialog)
                self.dialog = MDDialog(title = 'Invalid Input',text = 'Please Enter a Valid Input',size_hint = (0.7,0.2),buttons = [cancel_btn_dialogue])
                self.dialog.open()
            else:
                print(feedbackTitle, feedbackContent)
                feedbackInfo = str({f'\"{feedbackTitle}\":{{"feedbackContent":\"{feedbackContent}\"}}'})
                # registration_info = str({f'\"{RegisteredFarmer}\"}}'})
                to_database = json.loads(feedbackInfo)
                print((to_database))
                requests.patch(url = self.url, json = to_database)
                toast("Feedback Sent Successfully!")
        except Exception as e:
            toast(str(e))

    def send_feedback2(self, button):
        try:
            self.url.push(self.root.ids.t.text)
            toast("Send Successfully ")
        except Exception as e:
            toast(str(e))

    # def send_feedback(self, button):
        # self.feedback_title = self.content.ids.feedback_title.text
        # self.feedback_content= self.content.ids.feedback_content.text

        # if (self.feedback_title and self.feedback_content):
            # If All fields are completed the add the Trip
            # DATABASE.send_new_feedback(self.feedback_title, self.feedback_content)
            # self.close_dialog("")
            # self.load_data()
        # else:
            # print("Please enter values")
            
    def close_dialog(self, button):
        self.send_feedback_dialog.dismiss()
        self.send_feedback_dialog = None 


'''   def send_feedback(self, button):
        # emailID = self.root.ids.email_id.text
        feedbackTitle = self.ids.feedback_title.text
        feedbackContent = self.ids.feedback_content.text

        if feedbackTitle.split() != "" or feedbackContent.split() != "":
            cancel_btn_feedback_dialogue = MDFlatButton(text = 'Retry',on_release = self.close_feedback_dialog)
            self.dialog = MDDialog(title = 'Invalid Input',text = 'Please Enter a valid Input',size_hint = (0.7,0.2),buttons = [cancel_btn_feedback_dialogue])
            self.dialog.open()

            print(feedbackTitle,feedbackContent)
            # feedback_info = str({f'{{"feedbackTitle":\"{feedbackTitle}\","feedbackContent":\"{feedbackContent}\"}}'})
            feedback_info = str({f'\"{feedbackTitle}\":{{"feedbackContent":\"{feedbackContent}\"}}'})
            feedback_info = feedback_info.replace(".","-")
            feedback_info = feedback_info.replace("\'","")
            to_database = json.loads(feedback_info)
            print((to_database))
            requests.patch(url = self.url,json = to_database)
            # self.strng.get_screen('home').manager.current = 'home'

    def close_feedback_dialog(self,obj):
        self.dialog.dismiss()'''

    

    
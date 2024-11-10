from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty, StringProperty
from kivy.event import EventDispatcher
from kivy.network.urlrequest import UrlRequest
from kivy.app import App
from kivy.lang import Builder
from kivy.factory import Factory
import certifi
import json
import requests

# KivyMD imports
from kivymd.toast import toast

# Python imports
import sys
sys.path.append("/".join(x for x in __file__.split("/")[:-1]))
from json import dumps
import os.path

# Load the kv files
folder = os.path.dirname(os.path.realpath(__file__))
Builder.load_file(folder + "/kv/signinscreen.kv")
Builder.load_file(folder + "/kv/signupscreen.kv")
Builder.load_file(folder + "/kv/welcomescreen.kv")
Builder.load_file(folder + "/kv/helpscreen.kv")
Builder.load_file(folder + "/kv/resetpasswordscreen.kv")
Builder.load_file(folder + "/kv/loadingpopup.kv")
Builder.load_file(folder + "/kv/settingsscreen.kv")
Builder.load_file(folder + "/kv/notificationsscreen.kv")
Builder.load_file(folder + "/kv/viewregisteredfarmers.kv")
Builder.load_file(folder + "/firebase.kv")

# Import the screens used to log the user in
from baseclass.welcomescreen import WelcomeScreen
from baseclass.helpscreen import HelpScreen
from baseclass.signinscreen import SignInScreen
from baseclass.signupscreen import SignUpScreen
from baseclass.resetpasswordscreen import ResetPasswordScreen
from baseclass.settingsscreen import SettingsScreen
from baseclass.notificationsscreen import Notification_Screen
from baseclass.viewregisteredfarmers import ViewRegisteredFarmers

class Firebase(Screen, EventDispatcher):
    # Firebase Project meta info - MUST BE CONFIGURED BY DEVELOPER
    web_api_key = StringProperty()  # From Settings tab in Firebase project

    # Firebase Authentication Credentials - what developers want to retrieve
    refresh_token = ""
    localId = ""
    idToken = ""
    emailID = ""

    # Properties used to send events to update some parts of the UI
    login_success = BooleanProperty(False)  # Called upon successful sign in
    login_state = StringProperty("")
    sign_up_msg = StringProperty()
    email_exists = BooleanProperty(False)
    email_not_found = BooleanProperty(False)
    remember_user = BooleanProperty(True)
    require_email_verification = BooleanProperty(True)

    debug = False
    popup = Factory.LoadingPopup()
    popup.background = folder + "/transparent_image.png"
    
    def login_offline(self):
        self.login_state = 'in'
        self.login_success = True

    def show_all_farmers(self):
        self.ids.screen_manager.current = 'view-farmers'

    def scan_qrcode(self):
        self.ids.screen_manager.current = 'qrcode_screen'

    def change_screen(self):
        self.ids.screen_manager.current = 'settings_screen'
    
    def view_notifications_screen(self):
        self.ids.screen_manager.current = 'alert'


    def log_out(self):
        '''Clear the user's refresh token, marked them as not signed in, and go back to the welcome screen.'''
        self.login_state = 'out'
        self.login_success = False
        self.refresh_token = ''
        self.ids.screen_manager.current = 'sign_in_screen'
        # Clear text fields
        self.ids.sign_in_screen.ids.email.text = ''
        self.ids.sign_in_screen.ids.password.text = ''
        self.ids.sign_up_screen.ids.email.text = ''
        self.ids.sign_up_screen.ids.password.text = ''

    def on_login_success(self, screen_name, login_success_boolean):
        """Overwrite this method to switch to your app's home screen."""
        print("Testing", self.login_success, self.login_state)
        print("self.login_success=", login_success_boolean)

    def sign_in_success(self, urlrequest, log_in_data):
        """Collects info from Firebase upon successfully registering a new user."""
        if self.debug:
            print("Successfully signed in a user: ", log_in_data)
        # User's email/password exist, but are they verified?
        self.hide_loading_screen()
        self.refresh_token = log_in_data['refreshToken']
        self.localId = log_in_data['localId']
        self.idToken = log_in_data['idToken']
        self.emailID = log_in_data['email']
        # self.save_refresh_token(self.refresh_token)

        if self.require_email_verification:
            self.check_if_user_verified_email()
        else:
            self.login_state = 'in'
            self.login_success = True

    def sign_in(self, email, password):
        """Called when the "Log in" button is pressed. Sends the user's email and password in an HTTP request to the Firebase Authentication service."""
        if self.debug:
            print("Attempting to sign user in: ", email, password)
        sign_in_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key=" + self.web_api_key
        sign_in_payload = dumps(
            {"email": email, "password": password, "returnSecureToken": True})

        UrlRequest(sign_in_url, req_body=sign_in_payload,
                   on_success=self.sign_in_success,
                   on_failure=self.sign_in_failure,
                   on_error=self.sign_in_error, ca_file=certifi.where())

    def sign_in_failure(self, urlrequest, failure_data):
        """Displays an error message to the user if their attempt to create an account was invalid."""
        self.hide_loading_screen()
        self.email_not_found = False  # Triggers hiding the sign in button
        msg = failure_data['error']['message'].replace("_", " ").capitalize()
        toast(msg)
        if msg == "Email not found":
            self.email_not_found = True
        if self.debug:
            print("Couldn't sign the user in: ", failure_data)

    def sign_in_error(self, *args):
        self.hide_loading_screen()
        if self.debug:
            print("Sign in error", args)

    def reset_password(self, email):
        """Called when the "Reset password" button is pressed."""
        if self.debug:
            print("Attempting to send a password reset email to: ", email)
        reset_pw_url = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getOobConfirmationCode?key=" + self.web_api_key
        reset_pw_data = dumps({"email": email, "requestType": "PASSWORD_RESET"})

        UrlRequest(reset_pw_url, req_body=reset_pw_data,
                   on_success=self.successful_reset,
                   on_failure=self.sign_in_failure,
                   on_error=self.sign_in_error, ca_file=certifi.where())

    def successful_reset(self, urlrequest, reset_data):
        """Notifies the user that a password reset email has been sent to them."""
        self.hide_loading_screen()
        if self.debug:
            print("Successfully sent a password reset email", reset_data)
        toast("Reset password instructions sent to your email.")

    def sign_out(self):
        self.localId = ''
        self.idToken = ''
        self.emailID = ''
        self.clear_refresh_token_file()
        self.ids.screen_manager.current = 'welcome_screen'
        toast("Signed out")

    # def clear_refresh_token_file(self):
        # with open(self.refresh_token_file, 'w') as f:
            # f.write('')

    def display_loading_screen(self, *args):
        self.popup.open()

    def hide_loading_screen(self, *args):
        self.popup.dismiss()

    def check_if_user_verified_email(self):
        if self.debug:
            print("Attempting to check if the user signed in has verified their email")
        check_email_verification_url = "https://identitytoolkit.googleapis.com/v1/accounts:lookup?key=" + self.web_api_key
        check_email_verification_data = dumps(
            {"idToken": self.idToken})

        UrlRequest(check_email_verification_url, req_body=check_email_verification_data,
                   on_success=self.got_verification_info,
                   on_failure=self.could_not_get_verification_info,
                   on_error=self.could_not_get_verification_info,
                   ca_file=certifi.where())

    def could_not_get_verification_info(self, request, result):
        if self.debug:
            print("could_not_get_verification_info", request, result)
        self.hide_loading_screen()
        toast("Failed to check email verification status.")

    def got_verification_info(self, request, result):
        if self.debug:
            print("got_verification_info", request, result)
        if result['users'][0]['emailVerified']:
            self.login_state = 'in'
            self.login_success = True
        else:
            toast("Your email is not verified yet.\n Please check your email.")

    def send_verification_email(self, email):
        """Sends a verification email."""
        if self.debug:
            print("Attempting to send a email verification email to: ", email)
        verify_email_url = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode?key=" + self.web_api_key
        verify_email_data = dumps(
            {"idToken": self.idToken, "requestType": "VERIFY_EMAIL"})

        UrlRequest(verify_email_url, req_body=verify_email_data,
                   on_success=self.successful_verify_email_sent,
                   on_failure=self.unsuccessful_verify_email_sent,
                   on_error=self.unsuccessful_verify_email_sent,
                   ca_file=certifi.where())

    def unsuccessful_verify_email_sent(self, *args):
        toast("Couldn't send email verification email")

    def successful_verify_email_sent(self, *args):
        toast("A verification email has been sent. \nPlease check your email.")

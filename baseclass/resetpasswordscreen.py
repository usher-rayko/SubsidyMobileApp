from kivy.uix.screenmanager import Screen, SlideTransition

class ResetPasswordScreen(Screen):
    def go_back(self):
        self.parent.transition = SlideTransition(direction="right")
        self.parent.current = self.parent.current = "sign_in_screen"
        self.parent.transition = SlideTransition(direction="left")


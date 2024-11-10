from main_imports import Screen, MDGridBottomSheet, MDFlatButton, MDDialog, SlideTransition, MDThemePicker


class SettingsScreen(Screen):
    def go_back(self):
        self.parent.transition = SlideTransition(direction="right")
        self.parent.current = self.parent.current = "home"
        self.parent.transition = SlideTransition(direction="left")
    
    def change_mode(self, checkbox, value):
        if value:
            self.app.theme_cls.theme_style = "Dark"
        else:
            self.app.theme_cls.theme_style = "Light"

    @staticmethod
    def show_theme_picker():
        theme_dialog = MDThemePicker()
        theme_dialog.open()
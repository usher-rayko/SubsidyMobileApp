from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder
from kivymd.app import MDApp


Builder.load_string('''
<HelpScreen>
    orientation: "vertical"
    size_hint_y: None
    height: "420dp"
    MDLabel:
        text: "HOW TO USE THIS SYSTEM!"
        halign: "center"
        bold: True
    MDLabel:
        text: "1. Click on 'Get Started!' to continue to the signin page."
    MDLabel:
        text: "2. Provide valid details to login into the system."
    MDLabel:
        text: "3. If you forgot your login details, click on 'Forgot Password' to change it."
    MDLabel:
        text: "4. After a success login, click on Scan ID to register a farmer."
    MDLabel:
        text: "5. To send feedback, click on feedback button on the dashboard."
''')

APP = MDApp.get_running_app()

class HelpScreen(MDBoxLayout):
    def __init__(self, **kw):
        super().__init__()

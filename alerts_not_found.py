from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout


def no_alert_message():
    nt_message = MDBoxLayout(orientation="vertical")
    nt_message.add_widget(MDLabel(font_size="100sp", font_style="H1"))
    nt_message.add_widget(MDLabel(text="NO ALERTS AVAILABLE!", halign="center", font_size="100sp",
                                font_style="H3"))
    for i in range(2):
        nt_message.add_widget(MDLabel(font_size="100sp", font_style="H1"))
    return nt_message
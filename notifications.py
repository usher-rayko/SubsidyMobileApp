from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout

Builder.load_string("""
<PushNotifications>:
    canvas:
        Color:
            rgba: 0, .5, .8, 0.2
        RoundedRectangle:
            # radius: (40, 40)
            pos: self.pos
            size: self.size   
    MDLabel:
        id: title
        font_size: 16
        bold: True
        theme_text_color: "Primary"
        # halign:"center"
        size_hint: (.90, 0.70)
        pos_hint: {"center_x": .7, "center_y": .9}
    
    OneLineIconListItem:
        id: description
        pos_hint: {"center_x": .5, "center_y": .65}
        size_hint: (.90, 0.70)
        font_size: 12
        IconLeftWidget:
            icon: "assets/img/Reminders_48px.png"
    MDLabel:
        id: date
        font_size: 12
        theme_text_color: "Primary"
        # halign:"center"
        size_hint: (.90, 0.70)
        pos_hint: {"center_x": .7, "center_y": .35}
""")

class PushNotifications(RelativeLayout):
    def __init__(self, **kw):
        super().__init__()
        self.ids.title.text = kw['title']
        self.ids.description.text = kw['description']
        self.ids.date.text = kw['date']


from kivy.uix.relativelayout import RelativeLayout
from kivy.lang import Builder
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout

Builder.load_string("""
<ViewFarmers>:
    canvas:
        Color:
            rgba: 0, .5, .8, 0.2
        RoundedRectangle:
            # radius: (40, 40)
            pos: self.pos
            size: self.size   
    MDLabel:
        id: details
        font_size: 16
        # bold: True
        theme_text_color: "Primary"
        size_hint: (.90, 0.70)
        pos_hint: {"center_x": .57, "center_y": .70}
    MDLabel:
        id: regBy
        font_size: 16
        theme_text_color: "Primary"
        size_hint: (.90, 0.70)
        pos_hint: {"center_x": .57, "center_y": .30}
    MDLabel:
        id: regdate
        font_size: 13
        theme_text_color: "Primary"
        size_hint: (.90, 0.70)
        pos_hint: {"center_x": .57, "center_y": .12}
    OneLineIconListItem:
        # id: regdate
        # pos_hint: {"center_x": .48, "center_y": .6}
        # size_hint: (.90, 0.70)
        # font_size: 8
        # IconLeftWidget:
            # icon: "assets/img/opt_icon.png"

""")

class ViewFarmers(RelativeLayout):
    def __init__(self, **kw):
        super().__init__()
        self.by = kw['regBy']
        self.det = kw['details']
        # self.date_ = kw['regdate']
        self.date_ = kw['regdate']
        self.ids.regBy.text = f"Registered By: {self.by}"
        self.ids.details.text = f"Scanned Details: {self.det}"
        self.ids.regdate.text = f"Registered On: {self.date_}"


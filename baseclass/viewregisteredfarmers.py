from main_imports import Screen, TwoLineAvatarListItem, ImageLeftWidget, Clock
import requests
import json
from viewfarmers import ViewFarmers
from list_not_found import *
import plyer


class ViewRegisteredFarmers(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.url  = "https://agriculturalsubsidy-default-rtdb.firebaseio.com/registeredFarmer/.json"
    
    def list_available(type_request):
        get_request = requests.get(f'https://agriculturalsubsidy-default-rtdb.firebaseio.com/registeredFarmer/.json')
        data = json.loads(get_request.content.decode())
        return data

    def on_pre_enter(self, *args):
        self.load_data()

    def load_data(self):
        farmers_data = self.list_available()
        self.ids.show_farmers.clear_widgets()
        self.refresh_available_registered_farmers(farmers_data)
   
    def refresh_available_registered_farmers(self, farmers_data ):
        try :
            for Details, data in farmers_data .items():
                self.ids.show_farmers.add_widget(ViewFarmers(
                    # regBy=data[f"Registered By: 'RegisteredBy'"],
                    regBy=data['RegisteredBy'],
                    details=data['Details'],
                    regdate=data['RegisteredDate'],
                    reload_data=self.load_data

                ))
                plyer.notification.notify(title="Success!", message = "Please wait for the list!")
        except :
            temp = no_alert_message()
            self.ids.show_farmers.add_widget(temp)

    def refresh_callback(self, *args):
        def refresh_callback(interval):
            self.ids.refresh_layout.refresh_done()

        self.load_data()
        Clock.schedule_once(refresh_callback, 1.5)

from main_imports import Screen,Clock,toast
import requests
import json
from notifications import PushNotifications
from alerts_not_found import *
import plyer


class Notification_Screen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.url  = "https://agriculturalsubsidy-default-rtdb.firebaseio.com/pushnotifications/.json"
    
    def notifications_available(type_request):
        get_request = requests.get(f'https://agriculturalsubsidy-default-rtdb.firebaseio.com/pushnotifications/.json')
        data = json.loads(get_request.content.decode())
        return data

    def on_pre_enter(self, *args):
        self.load_data()

    def load_data(self):
        notification_data = self.notifications_available()
        self.ids.notification_grid.clear_widgets()
        self.refresh_available_notifications(notification_data)
   
    def refresh_available_notifications(self, notification_data):
        try :
            for Description, data in notification_data.items():
                self.ids.notification_grid.add_widget(PushNotifications(
                    title=data['Title'],
                    description=data['Description'],
                    date=data['DateSent'],
                    reload_data=self.load_data

                ))
                plyer.notification.notify(title="Success!", message = "You have notifications!")
        except :
            temp = no_alert_message()
            self.ids.notification_grid.add_widget(temp)

    def refresh_callback(self, *args):
        def refresh_callback(interval):
            self.ids.refresh_layout.refresh_done()

        self.load_data()
        Clock.schedule_once(refresh_callback, 1.5)

    
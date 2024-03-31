from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from kivy.uix.boxlayout import BoxLayout
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivymd.uix.boxlayout import MDBoxLayout
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from utils.datetime_utils import get_current_datetime_tz
from utils.firebase_controller import FirebaseController
from utils.get_rasp_uuid import getserial
from utils.remote_requests import RemoteRequests

Builder.load_file("components/homepage/graph_view.kv")


class GraphView(MDBoxLayout):
    def __init__(self, **kwargs):
        super(GraphView, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint = (1, 1)

        self.menu = None
        self.dropdown = None
        self.dropdown_items = ["Last 24h", "Last 7 days", "Last 30 days"]

        # local_tz = datetime.now(timezone.utc).astimezone().tzinfo

        self.end_datetime = get_current_datetime_tz()
        self.start_datetime = self.end_datetime - timedelta(days=1)

        Clock.schedule_once(self.add_graph, 0.1)
        Clock.schedule_once(self.init_dropdown, 0.1)

    def add_graph(self, *args):
        self.update_plot()

    def update_plot(self):
        graph_box = self.ids.graph_box
        graph_box.clear_widgets()

        fig, ax = plt.subplots()

        moisture_info_list = RemoteRequests().get_moisture_info(self.start_datetime,
                                                                self.end_datetime)

        if moisture_info_list is None or len(moisture_info_list) == 0:
            ax.plot(["No data"], [0])
            ax.grid()
            ax.set_xlabel('Time')
            ax.set_ylabel('Moisture (%)')
            plt.tight_layout(pad=3.0)
            graph_box.add_widget(FigureCanvasKivyAgg(plt.gcf()))
            return

        timestamps = [moisture_info["measurementTime"] for moisture_info in moisture_info_list]
        # local_tz = datetime.now(timezone.utc).astimezone().tzinfo
        local_tz = ZoneInfo("Europe/Bucharest")
        timestamps = [timestamp.astimezone(local_tz) for timestamp in timestamps]

        values = [moisture_info["measurementValuePercent"] for moisture_info in moisture_info_list]

        ax.plot(timestamps, values, color='red', marker='o')

        ax.grid()
        ax.set_xlabel('Time')
        ax.set_ylabel('Moisture (%)')

        ax.set_ylim(0, 100)

        xfmt = mdates.DateFormatter('%d %b\n%H:%M')
        ax.xaxis.set_major_formatter(xfmt)
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
        plt.xticks(rotation=45, ha="right")

        plt.tight_layout(pad=3.0)

        graph_box.add_widget(FigureCanvasKivyAgg(plt.gcf()))

        # TODO: check timezone and add some kind of loading spinner

    def init_dropdown(self, *args):
        self.dropdown = DropDown()

        for item in self.dropdown_items:
            btn = Button(text=item, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.select_item(self.dropdown_items.index(btn.text)))
            btn.padding = (10, 0)
            self.dropdown.add_widget(btn)

        mainbutton = self.ids.mainbutton
        mainbutton.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=lambda instance, x: setattr(mainbutton, 'text', self.dropdown_items[x]))

    def select_item(self, index):
        print(f"Selected item: {index}")
        self.dropdown.select(index)

        # local_tz = datetime.now(timezone.utc).astimezone().tzinfo
        # self.end_datetime = datetime.now(local_tz)

        self.end_datetime = get_current_datetime_tz()

        if index == 0:
            self.start_datetime = self.end_datetime - timedelta(days=1)
        elif index == 1:
            self.start_datetime = self.end_datetime - timedelta(days=7)
        elif index == 2:
            self.start_datetime = self.end_datetime - timedelta(days=30)

        self.update_plot()

    def refresh_data(self, *args):
        self.update_plot()

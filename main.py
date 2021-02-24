from kivy.support import install_twisted_reactor
install_twisted_reactor()
from twisted.internet import reactor, protocol
import pickle
import sentry_sdk
import time
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from datetime import datetime
from kivy.clock import Clock
import plyer


HOST = 'IP ADDRESS HERE'

def POPUP(title, message):
    pop = Popup(title=title, content=Label(text=message),
                size_hint=(None, None), size=(550, 550))
    pop.open()



class EchoClient(protocol.Protocol):
    def connectionMade(self):
        self.factory.app.on_connection(self.transport)

    def dataReceived(self, data):
        try:
            self.factory.app.print_message(data.decode('utf-8'))
        except UnicodeDecodeError as e:
            self.factory.app.print_message(pickle.loads(data))

#   Simple echo client the app runs by sending different length messages to get
#   different responses to build another screen you must have the corresponding
#   messages added on the server.

class EchoClientFactory(protocol.ClientFactory):
    protocol = EchoClient

    def __init__(self, app):
        self.app = app

    def startedConnecting(self, connector):
        self.app.print_message('Started to connect.')

    def clientConnectionLost(self, connector, reason):
        self.app.print_message('Lost connection.')

    def clientConnectionFailed(self, connector, reason):
        self.app.print_message('Connection failed.')

def Confirmation_Email(LabelText, Button1Text, PopupTitle, button1function, button2function):
    box = BoxLayout(orientation = 'vertical', padding = (10))
    box.add_widget(Label(text=''))
    box.add_widget(Label(text = LabelText))
    box.add_widget(Label(text = ''))
    btn1 = Button(text = Button1Text,  background_normal='', background_color=(0, 0.52156863, 0.25098039, 1))
    btn2 = Button(text = "NO GO BACK", background_normal='', background_color=(0.89803922, 0.25882353, 0.25882353, 1))
    box.add_widget(btn1)
    box.add_widget(Label(text=''))
    box.add_widget(btn2)

    # Add Label Inbetween Buttons to give a bit more room for the fat thumbs

    popup = Popup(title=PopupTitle, title_size= (30),
                  title_align = 'center', content = box,
                  size_hint=(None, None), size=(550, 550),
                  auto_dismiss = True)

    btn1.bind(on_press = button1function)
    btn1.bind(on_release=popup.dismiss)
    btn2.bind(on_press = button2function)
    btn2.bind(on_release = popup.dismiss)
    popup.open()

ORANGE = (1, 0.45098039, 0, 1)
GREENo = (0.37647059, .88627451, 0.21960784, 1)
GREEN = (0, 0.52156863, 0.25098039, 1)
REDi = (0.88627451, 0.32156863, 0.21960784, 1)
RED = (0.89803922, 0.25882353, 0.25882353, 1)
DARK_BLUE = (0, .4666, 0.70196, 1)
LIGHT_BLUE = (0.6627451, 0.77254902, 0.83921569, 1)
ORANGE_RED = (1, 0.27058824, 0, 1)
YELLOW_ORANGE = (1, 0.68235294, 0.25882353, 1)
TOMATO = (1, 0.38823529, 0.27843137, 1)
TOMATO = (0.93333333, 0.74901961, 0.00392157, 1)
PURPLE = (0.68235294, 0, 0.72156863, 1)
BLACK = (0, 0, 0, 1)
GREY = (0.69019608, 0.69019608, 0.69019608, 1)
WHITE = (1, 1, 1, 1)
YELLOW_GOLD = (0.96862745, 0.70196078, 0.02745098, 1)
RECONNECT_GREEN = (0.5647058823529, 0.9176470588235, 0.2588235294117, 1)

class Login_Screen(Screen):

    def __init__(self, **kwargs):
        super(Login_Screen, self).__init__(**kwargs)
        Clock.schedule_interval(self.ticket, 5)




    def connect_to_server(self):
        reactor.connectTCP(HOST, 8000, EchoClientFactory(self))

    def on_connection(self, connection):
        self.print_message("Connected successfully!")
        self.connection = connection

    def connecter_to_server(self, instance):
        reactor.connectTCP(HOST, 8000, EchoClientFactory(self))

    def ticker(self, *args):
        msg = ['The College Dropout']
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)

    def ticket(self, *args):
        msg = ['Update']
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            self.connect_to_server()


    def packitman(self, instance):
        pass

    def print_message(self, msg):
        if len(msg) == 1:
            print("Tickback Received")
        if len(msg) == 11:
            global Just_refs
            global date_used
            global Auth_List
            global statuslist
            global Checked_Refs
            global Checked_Statuslist
            global PutAway_Reference_List
            global PutAway_Status_List
            global Shipment_Reference_List
            global Shipment_Status_List
            global Shipment_Arrival_List
            date_used = msg[0]
            Just_refs = msg[1]
            statuslist = msg[2]
            Auth_List = msg[3]
            Checked_Statuslist = msg[4]
            Checked_Refs = msg[5]
            Shipment_Status_List = msg[6]
            Shipment_Reference_List = msg[7]
            Shipment_Arrival_List = msg[8]
            PutAway_Reference_List = msg[9]
            PutAway_Status_List = msg[10]
            print("Updated")
            kwargs = {'title': 'hello', 'message': 'new ting',}
            plyer.notification.notify(**kwargs)







    # Functions to set which user is using the app
    # Just add another to add a user.
    def setuserm(self):
        global User
        User = 'Martin Coles'
        App.get_running_app().root.current = 'Selection_Screen'
    def setuserk(self):
        global User
        User = 'Kieran Johnson'
        App.get_running_app().root.current = 'Selection_Screen'
    def setuserj(self):
        global User
        User = 'Joe Dewhurst'
        App.get_running_app().root.current = 'Selection_Screen'
    def setuserp(self):
        global User
        User = 'Peter Smith'
        App.get_running_app().root.current = 'Selection_Screen'

class Selection_Screen(Screen):
    # On Enter the app sends a simple 1 length message as a ticker
    # to the server to keep the app connection alive

    def on_enter(self, *args):
        self.connect_to_server()
        self.ticker()

    def connect_to_server(self):
        reactor.connectTCP(HOST, 8000, EchoClientFactory(self))

    def connecter_to_server(self, instance):
        reactor.connectTCP(HOST, 8000, EchoClientFactory(self))

    def ticker(self, *args):
        msg = ['The College Dropout']
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)

    def packitman(self, instance):
        pass

    def on_connection(self, connection):
        self.print_message("Connected successfully!")
        self.connection = connection


    # 4 Different messages to load up the different screens of the app


    def Get_Picking_Lists(self, *args):
        msg = [[1],[2]]
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT',  self.connecter_to_server, self.packitman)

    def Get_Check_Lists(self, *args):
        msg = [[1],[2],[3]]
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT',  self.connecter_to_server, self.packitman)

    def Get_Shipment_Lists(self, *args):
        msg = [[1],[2],[3],[4]]
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT',  self.connecter_to_server, self.packitman)

    def Get_Put_Away_Lists(self, *args):
        global Talib
        global Mos_Def
        msg = [[1],[2],[3],[4],[5]]
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)

    def logout(self):
        global User
        User = ''

    def print_message(self, msg):

        # Tick back receive code,

        if len(msg) == 1:
            print("Tickback Received")

        # If a length of 2 is received we know that the ref lists are empty

        if len(msg) == 2:
            POPUP('ALERT', 'No Refs Yet')

        # Picking Mode bootup receive code.

        if len(msg) == 6:
            global Just_refs
            global date_used
            global Auth_List
            date_used = msg[0]
            Just_refs = msg[1]
            Auth_List = msg[3]
            global statuslist
            statuslist = msg[2]
            App.get_running_app().root.current = 'Picking_Mode'

        # Checking Mode bootup receive code.

        if len(msg) == 4:
            global Checked_Refs
            global Checked_Statuslist
            Checked_Refs = msg[2]
            Checked_Statuslist = msg[3]
            App.get_running_app().root.current = "Checking_Mode"

        # Put-Away Mode bootup receive code.

        if len(msg) == 5:
            global PutAway_Reference_List
            global PutAway_Status_List
            PutAway_Reference_List = msg[3]
            PutAway_Status_List = msg[4]
            App.get_running_app().root.current = "Put_Away_Mode"

        # Shipment Receipting mode receive code.

        if len(msg) == 8:
            global Shipment_Reference_List
            global Shipment_Status_List
            global Shipment_Arrival_List
            Shipments = msg[7]
            Shipment_Reference_List = Shipments[0]
            Shipment_Status_List = Shipments[1]
            Shipment_Arrival_List = Shipments[2]
            Shipment_Reference_List = Shipment_Reference_List[0]
            Shipment_Status_List = Shipment_Status_List[0]
            Shipment_Arrival_List = Shipment_Arrival_List[0]
            App.get_running_app().root.current = "Receipting_Mode"

class Picking_Mode(Screen):

    def on_enter(self, *args):
        global Just_refs
        global statuslist
        global scrollview1
        layout1 = GridLayout(cols=1, spacing=10, padding=[50, 15, 50, 15],row_default_height=150, size_hint_y=None)
        layout1.bind(minimum_height=layout1.setter('height'))
        for count,ref in enumerate(Just_refs):
            boxi = BoxLayout(orientation='horizontal', spacing=5, padding=[5, 5, 5, 5])
            if statuslist[count] == 'Not Picked':
                btn = Button(text=str(ref), size_hint_x=0.63, background_normal = '', background_color = [0, .4666, 0.70196, 1], font_size=60, id=str(count))
                btn.bind(on_press=self.send)
                btn2 = Button(text=str(statuslist[count]), size_hint_x=0.303, background_normal = '', background_color = [0.89803922, 0.25882353, 0.25882353, 1], font_size=60, id=str(count))
                btn2.bind(on_press=self.send)
                boxi.add_widget(btn)
                boxi.add_widget(btn2)
                layout1.add_widget(boxi)
            if statuslist[count] == 'Incomplete':
                btn = Button(text=str(ref), size_hint_x=0.63, background_normal = '', background_color = [0.96862745, 0.70196078, 0.02745098, 1], font_size=60, id=str(count))
                btn.bind(on_press=self.send)
                btn2 = Button(text=str(statuslist[count]), size_hint_x=0.303, background_normal = '', background_color = [0.96862745, 0.70196078, 0.02745098, 1], font_size=60, id=str(count))
                btn2.bind(on_press=self.send)
                boxi.add_widget(btn)
                boxi.add_widget(btn2)
                layout1.add_widget(boxi)
            if statuslist[count] == 'Not Sent!':
                btn = Button(text=str(ref), size_hint_x=0.63, background_normal = '', background_color = [0.68235294, 0, 0.72156863, 1], font_size=60, id=str(count))
                btn.bind(on_press=self.send)
                btn2 = Button(text=str(statuslist[count]), size_hint_x=0.303, background_normal = '', background_color = [0.68235294, 0, 0.72156863, 1], font_size=60, id=str(count))
                btn2.bind(on_press=self.send)
                boxi.add_widget(btn)
                boxi.add_widget(btn2)
                layout1.add_widget(boxi)
            if statuslist[count] == 'Complete':
                btn = Button(text=str(ref), size_hint_x=0.63, background_normal = '', background_color = [0, 0.52156863, 0.25098039, 1], font_size=60, id=str(count))
                btn.bind(on_press=self.send)
                btn2 = Button(text=str(statuslist[count]), size_hint_x=0.303, background_normal = '', background_color = [0, 0.52156863, 0.25098039, 1], font_size=60, id=str(count))
                btn2.bind(on_press=self.send)
                boxi.add_widget(btn)
                boxi.add_widget(btn2)
                layout1.add_widget(boxi)
            if statuslist[count] == 'Complete Error':
                btn = Button(text=str(ref), size_hint_x=0.63, background_normal = '', background_color = ORANGE, font_size=60, id=str(count))
                btn.bind(on_press=self.send)
                btn2 = Button(text=str(statuslist[count]), size_hint_x=0.303, background_normal = '', background_color = ORANGE, font_size=60, id=str(count))
                btn2.bind(on_press=self.send)
                boxi.add_widget(btn)
                boxi.add_widget(btn2)
                layout1.add_widget(boxi)
        scrollview1 = ScrollView(scroll_type=['bars'],bar_width='10dp')
        scrollview1.add_widget(layout1)
        self.ids.boxer.add_widget(scrollview1)
        self.ids.date_displayer.text = str(datetime.now().strftime('%Y-%m-%d'))

    def on_leave(self, *args):
        global scrollview1
        self.ids.boxer.remove_widget(scrollview1)

    def Refresh_Function(self, *args):
        self.ids.boxer.remove_widget(scrollview1)
        msg = [[1],[2],[3],[4],[5],[6]]
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connect_to_server, self.packitman)

    def send(self, instance):
        global chops
        chops = instance.id
        chops = int(chops)
        self.send_chops()

    def connect_to_server(self, instance):
        reactor.connectTCP(HOST, 8000, EchoClientFactory(self))

    def connect_to_server1(self):
        reactor.connectTCP(HOST, 8000, EchoClientFactory(self))

    def ticker(self, *args):
        msg = ['The College Dropout']
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connect_to_server, self.packitman)

    def packitman(self, instance):
        pass

    def on_connection(self, connection):
        self.print_message("Connected successfully!")
        self.connection = connection

    def print_message(self, msg):
        global statuslist
        global Just_refs
        global Auth_List
        global scrollview1

        # Tick back message.

        if len(msg) == 1:
            print("Tickback Received")

        # This is the response if the button clicked doesnt have a ref associated with it.

        if len(msg) == 2:
            POPUP('ALERT','No Ref Clicked')

        # Refresh receive code fills out labels after receiving the latest list.

        if len(msg) == 4:
            statuslist = msg[3]
            Just_refs = msg[2]
            Auth_List = msg[1]
            layout1 = GridLayout(cols=1, spacing=10, padding=[50, 15, 50, 15], row_default_height=150, size_hint_y=None)
            layout1.bind(minimum_height=layout1.setter('height'))
            for count, ref in enumerate(Just_refs):
                boxi = BoxLayout(orientation='horizontal', spacing=5, padding=[5, 5, 5, 5])
                if statuslist[count] == 'Not Picked':
                    btn = Button(text=str(ref), size_hint_x=0.63, background_normal='',
                                 background_color=[0, .4666, 0.70196, 1], font_size=60, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2 = Button(text=str(statuslist[count]), size_hint_x=0.303, background_normal='',
                                  background_color=[0.89803922, 0.25882353, 0.25882353, 1], font_size=60, id=str(count))
                    btn2.bind(on_press=self.send)
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    layout1.add_widget(boxi)
                if statuslist[count] == 'Incomplete':
                    btn = Button(text=str(ref), size_hint_x=0.63, background_normal='',
                                 background_color=[0.96862745, 0.70196078, 0.02745098, 1], font_size=60, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2 = Button(text=str(statuslist[count]), size_hint_x=0.303, background_normal='',
                                  background_color=[0.96862745, 0.70196078, 0.02745098, 1], font_size=60, id=str(count))
                    btn2.bind(on_press=self.send)
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    layout1.add_widget(boxi)
                if statuslist[count] == 'Not Sent!':
                    btn = Button(text=str(ref), size_hint_x=0.63, background_normal='',
                                 background_color=[0.68235294, 0, 0.72156863, 1], font_size=60, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2 = Button(text=str(statuslist[count]), size_hint_x=0.303, background_normal='',
                                  background_color=[0.68235294, 0, 0.72156863, 1], font_size=60, id=str(count))
                    btn2.bind(on_press=self.send)
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    layout1.add_widget(boxi)
                if statuslist[count] == 'Complete':
                    btn = Button(text=str(ref), size_hint_x=0.63, background_normal='',
                                 background_color=[0, 0.52156863, 0.25098039, 1], font_size=60, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2 = Button(text=str(statuslist[count]), size_hint_x=0.303, background_normal='',
                                  background_color=[0, 0.52156863, 0.25098039, 1], font_size=60, id=str(count))
                    btn2.bind(on_press=self.send)
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    layout1.add_widget(boxi)
                if statuslist[count] == 'Complete Error':
                    btn = Button(text=str(ref), size_hint_x=0.63, background_normal='', background_color=ORANGE,
                                 font_size=60, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2 = Button(text=str(statuslist[count]), size_hint_x=0.303, background_normal='',
                                  background_color=ORANGE, font_size=60, id=str(count))
                    btn2.bind(on_press=self.send)
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    layout1.add_widget(boxi)
            scrollview1 = ScrollView(scroll_type=['bars'], bar_width='10dp')
            scrollview1.add_widget(layout1)
            self.ids.boxer.add_widget(scrollview1)
        # On enter fillout code, receives latest list and uploads it to the screen.

        if len(msg) == 6:
            Just_refs = msg[1]
            statuslist = msg[2]
            Auth_List = msg[3]
            self.CheckStatus()

        # The response length means that the app knows it can progress into the next
        # screen, this is the response after "sending chops".

        if len(msg) == 7:
            global locs
            global codes
            global picked
            locs = msg[4]
            codes = msg[5]
            picked = msg[6]
            App.get_running_app().root.current = 'Individual_Picklist'

    def send_chops(self, *args):
        global chops
        global Just_refs
        msg = [[1],[2],[3],[4],[5],[6]]
        msg.append([chops])
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connect_to_server, self.packitman)

class Individual_Picklist(Screen):
    def connect_to_server(self):
        reactor.connectTCP(HOST, 8000, EchoClientFactory(self))

    def connecter_to_server(self, instance):
        reactor.connectTCP(HOST, 8000, EchoClientFactory(self))

    def on_connection(self, connection):
        self.print_message("Connected successfully!")
        self.connection = connection

    def ticker(self, *args):
        msg = ['The College Dropout']
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            print(e)
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)

    def packitman(self, instance):
        pass

    def on_enter(self, *args):
        global locs
        global codes
        global picked
        global scrollview2

        layout1 = GridLayout(cols=1, spacing=10, padding=[50, 15, 50, 15],row_default_height=150, size_hint_y=None)
        layout1.bind(minimum_height=layout1.setter('height'))
        try:
            for count,ref in enumerate(locs):
                boxi = BoxLayout(orientation='horizontal', spacing=5, padding=[5, 5, 5, 5])
                if picked[count] == 'No':
                    btn = Button(text=str(ref), size_hint_x=0.3, background_normal = '', background_color = [0, .4666, 0.70196, 1], font_size=30, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2 = Button(text=str(codes[count]), size_hint_x=0.6, background_normal = '', background_color = [0, .4666, 0.70196, 1], font_size=40, id=str(count))
                    btn2.bind(on_press=self.send)
                    btn3 = Button(text=str(picked[count]), size_hint_x=0.1, background_normal = '', background_color = [0.89803922, 0.25882353, 0.25882353, 1], id=str(count))
                    btn3.bind(on_press=self.quickmark)
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    boxi.add_widget(btn3)
                    layout1.add_widget(boxi)
                if picked[count] == 'Yes':
                    btn = Button(text=str(ref), size_hint_x=0.3, background_normal = '', background_color = [0, 0.52156863, 0.25098039, 1], font_size=30, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2 = Button(text=str(codes[count]), size_hint_x=0.6, background_normal = '', background_color = [0, 0.52156863, 0.25098039, 1], font_size=40, id=str(count))
                    btn2.bind(on_press=self.send)
                    btn3 = Button(text=str(picked[count]), size_hint_x=0.1, background_normal = '', background_color = [0, 0.52156863, 0.25098039, 1], id=str(count))
                    btn3.bind(on_press=self.quickmark)
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    boxi.add_widget(btn3)
                    layout1.add_widget(boxi)
                if picked[count] == 'Yes E':
                    btn = Button(text=str(ref), size_hint_x=0.3, background_normal = '', background_color = [1, 0.45098039, 0, 1], font_size=30, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2 = Button(text=str(codes[count]), size_hint_x=0.6, background_normal = '', background_color = [1, 0.45098039, 0, 1], font_size=40, id=str(count))
                    btn2.bind(on_press=self.send)
                    btn3 = Button(text=str(picked[count]), size_hint_x=0.1, background_normal = '', background_color = [1, 0.45098039, 0, 1], id=str(count))
                    btn3.bind(on_press=self.quickmark)
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    boxi.add_widget(btn3)
                    layout1.add_widget(boxi)
        except IndexError:
            pass
        scrollview2 = ScrollView(scroll_type=['bars'],bar_width='10dp')
        scrollview2.add_widget(layout1)
        self.ids.paxson.add_widget(scrollview2)
        self.ids.picklistnum.text = Just_refs[int(chops)]

    def print_message(self, msg):
        global locs
        global desc
        global codes
        global qop
        global qoc
        global pick_status
        global error_log
        global picked
        global scrollview2
        global statuslist
        # Tickback message

        if len(msg) == 1:
            print("Tickback Received")

        # This is the response when a quick mark is used.

        if len(msg) == 2:
            statuslist = msg[0]
            picked = msg[1]
            print(picked)
            self.ids.paxson.remove_widget(scrollview2)
            layout1 = GridLayout(cols=1, spacing=10, padding=[50, 15, 50, 15], row_default_height=150, size_hint_y=None)
            layout1.bind(minimum_height=layout1.setter('height'))
            for count, ref in enumerate(locs):
                boxi = BoxLayout(orientation='horizontal', spacing=5, padding=[5, 5, 5, 5])
                if picked[count] == 'No':
                    btn = Button(text=str(ref), size_hint_x=0.3, background_normal='',
                                 background_color=[0, .4666, 0.70196, 1], font_size=30, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2 = Button(text=str(codes[count]), size_hint_x=0.6, background_normal='',
                                  background_color=[0, .4666, 0.70196, 1], font_size=40, id=str(count))
                    btn2.bind(on_press=self.send)
                    btn3 = Button(text=str(picked[count]), size_hint_x=0.1, background_normal='',
                                  background_color=[0.89803922, 0.25882353, 0.25882353, 1], id=str(count))
                    btn3.bind(on_press=self.quickmark)
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    boxi.add_widget(btn3)
                    layout1.add_widget(boxi)
                if picked[count] == 'Yes':
                    btn = Button(text=str(ref), size_hint_x=0.3, background_normal='',
                                 background_color=[0, 0.52156863, 0.25098039, 1], font_size=30, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2 = Button(text=str(codes[count]), size_hint_x=0.6, background_normal='',
                                  background_color=[0, 0.52156863, 0.25098039, 1], font_size=40, id=str(count))
                    btn2.bind(on_press=self.send)
                    btn3 = Button(text=str(picked[count]), size_hint_x=0.1, background_normal='',
                                  background_color=[0, 0.52156863, 0.25098039, 1], id=str(count))
                    btn3.bind(on_press=self.quickmark)
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    boxi.add_widget(btn3)
                    layout1.add_widget(boxi)
                if picked[count] == 'Yes E':
                    btn = Button(text=str(ref), size_hint_x=0.3, background_normal='',
                                 background_color=[1, 0.45098039, 0, 1], font_size=30, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2 = Button(text=str(codes[count]), size_hint_x=0.6, background_normal='',
                                  background_color=[1, 0.45098039, 0, 1], font_size=40, id=str(count))
                    btn2.bind(on_press=self.send)
                    btn3 = Button(text=str(picked[count]), size_hint_x=0.1, background_normal='',
                                  background_color=[1, 0.45098039, 0, 1], id=str(count))
                    btn3.bind(on_press=self.quickmark)
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    boxi.add_widget(btn3)
                    layout1.add_widget(boxi)
            scrollview2 = ScrollView(scroll_type=['bars'], bar_width='10dp')
            scrollview2.add_widget(layout1)
            self.ids.paxson.add_widget(scrollview2)
            POPUP('Success', 'Logged into the server!')



        # Refresh function for the individual picklists.

        if len(msg) == 7:
            locs = msg[4]
            codes = msg[5]
            picked = msg[6]
            layout1 = GridLayout(cols=1, spacing=10, padding=[50, 15, 50, 15], row_default_height=150, size_hint_y=None)
            layout1.bind(minimum_height=layout1.setter('height'))
            for count, ref in enumerate(locs):
                boxi = BoxLayout(orientation='horizontal', spacing=5, padding=[5, 5, 5, 5])
                if picked[count] == 'No':
                    btn = Button(text=str(ref), size_hint_x=0.3, background_normal='',
                                 background_color=[0, .4666, 0.70196, 1], font_size=30, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2 = Button(text=str(codes[count]), size_hint_x=0.6, background_normal='',
                                  background_color=[0, .4666, 0.70196, 1], font_size=40, id=str(count))
                    btn2.bind(on_press=self.send)
                    btn3 = Button(text=str(picked[count]), size_hint_x=0.1, background_normal='',
                                  background_color=[0.89803922, 0.25882353, 0.25882353, 1], id=str(count))
                    btn3.bind(on_press=self.quickmark)
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    boxi.add_widget(btn3)
                    layout1.add_widget(boxi)
                if picked[count] == 'Yes':
                    btn = Button(text=str(ref), size_hint_x=0.3, background_normal='',
                                 background_color=[0, 0.52156863, 0.25098039, 1], font_size=30, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2 = Button(text=str(codes[count]), size_hint_x=0.6, background_normal='',
                                  background_color=[0, 0.52156863, 0.25098039, 1], font_size=40, id=str(count))
                    btn2.bind(on_press=self.send)
                    btn3 = Button(text=str(picked[count]), size_hint_x=0.1, background_normal='',
                                  background_color=[0, 0.52156863, 0.25098039, 1], id=str(count))
                    btn3.bind(on_press=self.quickmark)
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    boxi.add_widget(btn3)
                    layout1.add_widget(boxi)
                if picked[count] == 'Yes E':
                    btn = Button(text=str(ref), size_hint_x=0.3, background_normal='',
                                 background_color=[1, 0.45098039, 0, 1], font_size=30, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2 = Button(text=str(codes[count]), size_hint_x=0.6, background_normal='',
                                  background_color=[1, 0.45098039, 0, 1], font_size=40, id=str(count))
                    btn2.bind(on_press=self.send)
                    btn3 = Button(text=str(picked[count]), size_hint_x=0.1, background_normal='',
                                  background_color=[1, 0.45098039, 0, 1], id=str(count))
                    btn3.bind(on_press=self.quickmark)
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    boxi.add_widget(btn3)
                    layout1.add_widget(boxi)
            scrollview2 = ScrollView(scroll_type=['bars'], bar_width='10dp')
            scrollview2.add_widget(layout1)
            self.ids.paxson.add_widget(scrollview2)


        # Confirmation email receipt, to allow the user to know if they have
        # successfully logged something.

        if len(msg) == 10:
            POPUP('Success', 'Logged into the server!')

        if len(msg) == 6:
            locs = msg[0]
            desc = msg[1]
            codes = msg[2]
            qop = msg[3]
            qoc = msg[4]
            pick_status = msg[5]
            error_log = ['None'] * (len(pick_status))

    def on_leave(self, *args):
        global scrollview2
        self.ids.paxson.remove_widget(scrollview2)

    def send(self, instance):
        global chips
        chips = instance.id
        chips = int(chips)
        self.send_Chips_and_Chops()

    def quickmark(self, instance):
        global chips
        global payload
        chips = instance.id
        if instance.text == 'No':
            payload = 'Yes'
            return Confirmation_Email("You're going to mark\nthis as picked", "Yes",'Alert', self.quick_mark_as_picked, self.packitman)

        else:
            payload = 'No'
            return Confirmation_Email("You're going to mark\nthis as NOT picked", "Yes", 'Alert', self.quick_mark_as_picked,
                                      self.packitman)



    def quick_mark_as_picked(self, *args):
        global User
        global chops
        global payload
        msg = [[1], [2], [3], [4], [5]]
        msg.append([User])
        msg.append([chips])
        msg.append([chops])
        msg.append([payload])
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)

    def send_Chips_and_Chops(self, *args):
        global chops
        global chips
        global codes
        msg = [[1],[2],[3],[4],[5],[6]]
        msg.append([chops])
        msg.append([chips])
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError:
            return Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)
        App.get_running_app().root.current = 'Individual_Item'

    def send_chops(self, *args):
        global chops
        global Just_refs
        msg = [[1],[2],[3],[4],[5],[6]]
        msg.append([chops])
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)

    def refresh(self):
        global scrollview2
        self.ids.paxson.remove_widget(scrollview2)
        self.send_chops()

class Individual_Item(Screen):

    def connect_to_server(self):
        reactor.connectTCP(HOST, 8000, EchoClientFactory(self))

    def connecter_to_server(self, instance):
        reactor.connectTCP(HOST, 8000, EchoClientFactory(self))

    def ticker(self, *args):
        msg = ['The College Dropout']
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)

    def packitman(self, instance):
        pass

    def on_connection(self, connection):
        self.print_message("Connected successfully!")
        self.connection = connection

    def print_message(self, msg):
        global picked
        global statuslist
        if len(msg) == 5:
            locs = msg[0]
            desc = msg[1]
            codes = msg[2]
            qop = msg[3]
            qoc = msg[4]
        if len(msg) == 2:
            picked = msg[0]
            statuslist = msg[1]
            POPUP('Alert', 'Please mark list\nas complete')
        if len(msg) == 10:
            picked = msg[0]
            statuslist = msg[1]
            POPUP('Alert', 'Item Logged\nList is Picked')
        if len(msg) == 9:
            picked = msg[0]
            statuslist = msg[1]
            POPUP('Alert', 'Item Logged\nList is still incomplete')
        if len(msg) == 7:
            POPUP('Alert', 'Picklist already\ncomplete')

    def on_enter(self, *args):
        global constantvalue
        global dpgc213
        constantvalue = 0
        dpgc213 = 0
        self.connect_to_server()
        self.ticker()
        try:
            global codes
            global chops
            global locs
            global desc
            global qoc
            global qop
            global Just_refs
            global chips
            global pick_status
            global error_log
            if pick_status[int(chips)] == 'Yes':
                POPUP('ERROR', 'Item Already\nPicked!')
            if pick_status[int(chips)] == 'Yes E':
                POPUP('ERROR', 'Item Picked\nWith Error')
            self.ids.Marko_Picko.disabled = False
            self.ids.itemnumberdisplay.text = ('Item Number : '+ str(int(chips)+1)+ '/' + str(len(codes)))
            splititfam = 0
            try:
                dex = desc[int(chips)]
                try:
                    T = dex.index('mm')
                    a, b = dex[:T + 2], dex[T + 3:]
                    splititfam = 1
                except ValueError as e:
                    try:
                        T = dex.index('MM')
                        a, b = dex[:T + 2], dex[T + 3:]
                        splititfam = 1
                    except ValueError as e:
                        splititfam = 0
                if splititfam == 1:
                    self.ids.description.text = a + '\n' + b
                if splititfam == 0:
                    self.ids.description.text = desc[int(chips)]
                self.ids.refnum.text = str(Just_refs[int(chops)])
                self.ids.location.text = locs[int(chips)]
                self.ids.productcode.text = codes[int(chips)]
                self.ids.qop.text = str(qop[int(chips)])
                self.ids.qoc.text = str(qoc[int(chips)])
            except IndexError as e:
                POPUP('No More Items!', 'Picklist Complete')
        except AttributeError as e:
            pass
        except NameError as e:
            POPUP('Error', 'Please enter again')

    def are_ya_sure_buddy(self):
        Confirmation_Email('Is This Item Picked!','Item Picked', 'Please Confirm', self.Item_Picked, self.packitman)

    def Item_Picked(self, instance):
        global codes
        global chops
        global locs
        global desc
        global qoc
        global qop
        global Just_refs
        global chips
        global picked
        global error_log
        global chunks
        global User
        global logger
        global constantvalue
        global dpgc213
        constantvalue = 0
        dpgc213 = 0
        if self.ids.error.text == '':
            msg = [[chops], [chips], [User], [None], [1],[2],[3],[4],[5],[6]]

        else:
            error = self.ids.error.text
            msg = [[chops], [chips], [User], [error], [1], [2], [3], [4], [5], [6]]
            self.ids.error.text = ''
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            return Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)

        chips += 1
        chunks = chips
        if (chips+1) > len(codes):
            chips -= 1
        self.ids.itemnumberdisplay.text = ('Item Number : ' + str(chips +1) + '/' + str(len(codes)))
        splititfam = 0
        try:
            dex = desc[chunks]
            try:
                T = dex.index('mm')
                a, b = dex[:T + 2], dex[T + 3:]
                splititfam = 1
            except ValueError as e:
                try:
                    T = dex.index('MM')
                    a, b = dex[:T + 2], dex[T + 3:]
                    splititfam = 1
                except ValueError as e:
                    splititfam = 0
            if splititfam == 1:
                self.ids.description.text = a + '\n' + b
            if splititfam == 0:
                self.ids.description.text = desc[chunks]
            self.ids.location.text = locs[chunks]
            self.ids.productcode.text = codes[chunks]
            self.ids.qop.text = str(qop[chunks])
            self.ids.qoc.text = str(qoc[chunks])

        except IndexError as e:
            POPUP('No More Items!', 'Please click\ncomplete button')

    def Previous_Item(self):
        global codes
        global locs
        global desc
        global qoc
        global qop
        global Just_refs
        global chips
        global picked
        global error_log
        global chunks
        chips -= 1
        if (chips+1) <= 0:
            chips += 1
            return POPUP('Error', 'This is the\nfirst item')
        self.ids.itemnumberdisplay.text = ('Item Number : ' + str(chips +1) + '/' + str(len(codes)))
        chunks = chips
        print('this is chunks ' + str(chunks))
        splititfam = 0
        try:
            dex = desc[chunks]
            try:
                T = dex.index('mm')
                a, b = dex[:T + 2], dex[T + 3:]
                splititfam = 1
            except ValueError as e:
                try:
                    T = dex.index('MM')
                    a, b = dex[:T + 2], dex[T + 3:]
                    splititfam = 1
                except ValueError as e:
                    splititfam = 0
            if splititfam == 1:
                self.ids.description.text = a + '\n' + b
            if splititfam == 0:
                self.ids.description.text = desc[chunks]
            self.ids.location.text = locs[chunks]
            self.ids.productcode.text = codes[chunks]
            self.ids.qop.text = str(qop[chunks])
            self.ids.qoc.text = str(qoc[chunks])

        except IndexError as e:
            POPUP('No More Items!', 'Please click\ncomplete button')

    def are_yu_sure_abeet_that(self):
        Confirmation_Email('Is This Picklist\nReady To Check?', 'Complete', 'Please Confirm', self.Log_Picklist_as_picked, self.packitman)

    def Log_Picklist_as_picked(self, instance):
        global chops
        global codes
        global locs
        global desc
        global qoc
        global qop
        global Just_refs
        global chips
        global picked
        global error_log
        global condition
        global statuslist
        if statuslist[chops] == 'Complete':
            return POPUP('Error','Already Marked as Complete')
        if statuslist[chops] == 'Complete Error':
            return POPUP('Error','Already Marked as Complete')
        ref = Just_refs[int(chops)]
        ulog = [[chops], [chips]]
        msg = [[User], [qoc], [qop], [ref], [chops],[chips], [1],[2],[3],[4],[5]]
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)
        condition = 1
        self.ids.Marko_Picko.disabled = True

    def Placed_Carton_On_Pallet(self):
        global constantvalue
        global dpgc213
        global qoc
        global qop
        global chips
        valued = 1.0
        dpgc213 += valued
        value = qop[chips]/qoc[chips]
        print(value)
        constantvalue += value
        self.ids.qop.text = str(constantvalue) + ' / ' + str(qop[chips])
        self.ids.qoc.text = str(dpgc213) + ' / ' +str(qoc[chips])
        if constantvalue == qop[chips]:
            POPUP('Done!', 'Item Picked!')

        if constantvalue < 0:
            self.ids.qop.text = str(qop[chips])
            constantvalue = 0
            POPUP('Error!', 'You Removed\nToo Much!')
        if dpgc213 < 0:
            self.ids.qoc.text = str(qoc[chips])
            dpgc213 = 0

    def Removed_Carton_On_Pallet(self):
        global constantvalue
        global dpgc213
        global qoc
        global qop
        global chips
        valued = 1.0
        dpgc213 -= valued
        value = qop[chips] / qoc[chips]
        print(value)
        constantvalue -= value
        self.ids.qop.text = str(constantvalue) + ' / ' + str(qop[chips])
        self.ids.qoc.text = str(dpgc213) + ' / ' + str(qoc[chips])
        if constantvalue == qop[chips]:
            POPUP('Done!', 'Item Picked!')

        if constantvalue < 0:
            self.ids.qop.text = str(qop[chips])
            constantvalue = 0
            POPUP('Error!', 'You Removed\nToo Much!')
        if dpgc213 < 0:
            self.ids.qoc.text = str(qoc[chips])
            dpgc213 = 0

    def Placed_Piece_On_Pallet(self):
        global constantvalue
        global dpgc213
        global qoc
        global qop
        global chips
        valued = 1.0
        constantvalue += valued
        self.ids.qop.text = str(constantvalue) + ' / ' + str(qop[chips])
        self.ids.qoc.text = str(dpgc213) + ' / ' + str(qoc[chips])
        if constantvalue == qop[chips]:
            POPUP('Done!', 'Item Picked!')

        if constantvalue < 0:
            self.ids.qop.text = str(qop[chips])
            constantvalue = 0
            POPUP('Error!', 'You Removed\nToo Much!')
        if dpgc213 < 0:
            self.ids.qoc.text = str(qoc[chips])
            dpgc213 = 0

    def Removed_Piece_On_Pallet(self):
        global constantvalue
        global dpgc213
        global qoc
        global qop
        global chips
        valued = 1.0
        constantvalue -= valued
        self.ids.qop.text = str(constantvalue) + ' / ' + str(qop[chips])
        self.ids.qoc.text = str(dpgc213) + ' / ' + str(qoc[chips])
        if constantvalue == qop[chips]:
            POPUP('Done!', 'Item Picked!')

        if constantvalue < 0:
            self.ids.qop.text = str(qop[chips])
            constantvalue = 0
            POPUP('Error!', 'You Removed\nToo Much!')
        if dpgc213 < 0:
            self.ids.qoc.text = str(qoc[chips])
            dpgc213 = 0

class Checking_Mode(Screen):
    def connecter_to_server(self, instance):
        reactor.connectTCP(HOST, 8000, EchoClientFactory(self))

    def ticker(self, *args):
        msg = ['The College Dropout']
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)

    def packitman(self, instance):
        pass

    def connect_to_server(self):
        reactor.connectTCP(HOST, 8000, EchoClientFactory(self))

    def Get_Check_Lists(self, *args):
        global scroll
        self.ids.boxer.remove_widget(scroll)
        msg = [[1],[2],[3]]
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT',  self.connecter_to_server, self.packitman)

    def on_connection(self, connection):
        self.print_message("Connected successfully!")
        self.connection = connection

    def on_leave(self, *args):
        global scroll
        self.ids.boxer.remove_widget(scroll)

    def print_message(self, msg):

    # This is the tickback message response code.

        if len(msg) == 1:
            print("Tickback Received")

    # This is the refresh response code it gets the latest data and uploads it to the screen

        if len(msg) == 4:
            global Checked_Refs
            global Checked_Statuslist
            global scroll
            Checked_Refs = msg[2]
            Checked_Statuslist = msg[3]
            layout1 = GridLayout(cols=1, spacing=10, padding=[50, 15, 50, 15],row_default_height=150, size_hint_y=None)
            layout1.bind(minimum_height=layout1.setter('height'))
            for count,ref in enumerate(Checked_Refs):
                boxi = BoxLayout(orientation='horizontal', spacing=5, padding=[5, 5, 5, 5])
                if Checked_Statuslist[count] == 'Not Checked':
                    btn = Button(text=str(ref), size_hint_x=0.63, background_normal = '', background_color = DARK_BLUE, font_size=60, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2 = Button(text=str(Checked_Statuslist[count]), size_hint_x=0.303, background_normal = '', background_color = RED, font_size=60, id=str(count))
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    layout1.add_widget(boxi)
                if Checked_Statuslist[count] == 'Incomplete':
                    btn = Button(text=str(ref), size_hint_x=0.63, background_normal = '', background_color = TOMATO, font_size=60, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2 = Button(text=str(Checked_Statuslist[count]), size_hint_x=0.303, background_normal = '', background_color = TOMATO, font_size=60, id=str(count))
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    layout1.add_widget(boxi)
                if Checked_Statuslist[count] == 'Not Sent!':
                    btn = Button(text=str(ref), size_hint_x=0.63, background_normal = '', background_color = PURPLE, font_size=60, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2 = Button(text=str(Checked_Statuslist[count]), size_hint_x=0.303, background_normal = '', background_color = PURPLE, font_size=60, id=str(count))
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    layout1.add_widget(boxi)
                if Checked_Statuslist[count] == 'Checked':
                    btn = Button(text=str(ref), size_hint_x=0.63, background_normal = '', background_color = GREEN, font_size=60, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2 = Button(text=str(Checked_Statuslist[count]), size_hint_x=0.303, background_normal = '', background_color = GREEN, font_size=60, id=str(count))
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    layout1.add_widget(boxi)
                if Checked_Statuslist[count] == 'Checked Error':
                    btn = Button(text=str(ref), size_hint_x=0.63, background_normal = '', background_color = ORANGE, font_size=60, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2 = Button(text=str(Checked_Statuslist[count]), size_hint_x=0.303, background_normal = '', background_color = ORANGE, font_size=60, id=str(count))
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    layout1.add_widget(boxi)
            scroll = ScrollView(scroll_type=['bars'],bar_width='10dp')
            scroll.add_widget(layout1)
            self.ids.boxer.add_widget(scroll)

    # This is the response code received when no item is clicked.

        if len(msg) == 9:
            POPUP('Alert', 'No Item Clicked')

    # This is the response code for the send MBDTF function
    # it gets the data and after confirming it it changes screen.

        if len(msg) == 11:
            global coders
            global users
            global statusers
            global activator
            global Checklist_Cartons
            Checklist_Cartons = msg[6]
            activator = msg[7]
            coders = msg[8]
            users = msg[9]
            statusers = msg[10]
            App.get_running_app().root.current = 'Individual_Checklist'

    def on_enter(self, *args):
        global Checked_Refs
        global Checked_Statuslist
        global scroll
        layout1 = GridLayout(cols=1, spacing=10, padding=[50, 15, 50, 15], row_default_height=150, size_hint_y=None)
        layout1.bind(minimum_height=layout1.setter('height'))
        for count, ref in enumerate(Checked_Refs):
            boxi = BoxLayout(orientation='horizontal', spacing=5, padding=[5, 5, 5, 5])
            if Checked_Statuslist[count] == 'Not Checked':
                btn = Button(text=str(ref), size_hint_x=0.63, background_normal='', background_color=DARK_BLUE,
                             font_size=60, id=str(count))
                btn.bind(on_press=self.send)
                btn2 = Button(text=str(Checked_Statuslist[count]), size_hint_x=0.303, background_normal='',
                              background_color=RED, font_size=60, id=str(count))
                boxi.add_widget(btn)
                boxi.add_widget(btn2)
                layout1.add_widget(boxi)
            if Checked_Statuslist[count] == 'Incomplete':
                btn = Button(text=str(ref), size_hint_x=0.63, background_normal='', background_color=TOMATO,
                             font_size=60, id=str(count))
                btn.bind(on_press=self.send)
                btn2 = Button(text=str(Checked_Statuslist[count]), size_hint_x=0.303, background_normal='',
                              background_color=TOMATO, font_size=60, id=str(count))
                boxi.add_widget(btn)
                boxi.add_widget(btn2)
                layout1.add_widget(boxi)
            if Checked_Statuslist[count] == 'Not Sent!':
                btn = Button(text=str(ref), size_hint_x=0.63, background_normal='', background_color=PURPLE,
                             font_size=60, id=str(count))
                btn.bind(on_press=self.send)
                btn2 = Button(text=str(Checked_Statuslist[count]), size_hint_x=0.303, background_normal='',
                              background_color=PURPLE, font_size=60, id=str(count))
                boxi.add_widget(btn)
                boxi.add_widget(btn2)
                layout1.add_widget(boxi)
            if Checked_Statuslist[count] == 'Checked':
                btn = Button(text=str(ref), size_hint_x=0.63, background_normal='', background_color=GREEN,
                             font_size=60, id=str(count))
                btn.bind(on_press=self.send)
                btn2 = Button(text=str(Checked_Statuslist[count]), size_hint_x=0.303, background_normal='',
                              background_color=GREEN, font_size=60, id=str(count))
                boxi.add_widget(btn)
                boxi.add_widget(btn2)
                layout1.add_widget(boxi)
            if Checked_Statuslist[count] == 'Checked Error':
                btn = Button(text=str(ref), size_hint_x=0.63, background_normal='', background_color=ORANGE,
                             font_size=60, id=str(count))
                btn.bind(on_press=self.send)
                btn2 = Button(text=str(Checked_Statuslist[count]), size_hint_x=0.303, background_normal='',
                              background_color=ORANGE, font_size=60, id=str(count))
                boxi.add_widget(btn)
                boxi.add_widget(btn2)
                layout1.add_widget(boxi)
        scroll = ScrollView(scroll_type=['bars'], bar_width='10dp')
        scroll.add_widget(layout1)
        self.ids.boxer.add_widget(scroll)
        self.ids.date_displayer2.text = str(datetime.now().strftime('%Y-%m-%d'))

    def send(self,instance):
        global MBDTF
        global Checked_Refs
        MBDTF = instance.id
        MBDTF = int(MBDTF)
        self.Send_MBDTF()

    def Send_MBDTF(self, *args):
        global MBDTF
        msg = [[1],[2],[3],[4],[5],[6],[7],[8],[9], [10],[11]]
        msg.append([MBDTF])
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)

    def ho_ho_hold_up_now(self):
        Confirmation_Email('Send Email To Office', 'Yes', 'Please Confirm', self.send_email_to_office, self.packitman)

    def send_email_to_office(self, instance, *args):
        msg = [[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],
               [1],[2],[3]]
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)

class Individual_Checklist(Screen):
    def connecter_to_server(self, instance):
        reactor.connectTCP(HOST, 8000, EchoClientFactory(self))

    def ticker(self, *args):
        msg = ['The College Dropout']
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)

    def packitman(self, instance):
        pass

    def connect_to_server(self):
        reactor.connectTCP(HOST, 8000, EchoClientFactory(self))

    def on_connection(self, connection):
        self.print_message("Connected successfully!")
        self.connection = connection

    def print_message(self, msg):

    # This is the tickback response code.

        if len(msg) == 1:
            print("Tickback Received")

    # This is the response code after sending the MBDTF and Throne variables.

        if len(msg) == 12:
            global Checklist_Codes
            global Checklist_Descs
            global Checklist_Errors
            global Checklist_Users
            global Checklist_QOCs
            global Checklist_QOPs
            global Active_Ref
            global Checklist_Locs
            Active_Ref = msg[4]
            Checklist_Errors = msg[5]
            Checklist_Users = msg[6]
            Checklist_Codes = msg[7]
            Checklist_Descs = msg[8]
            Checklist_QOPs = msg[9]
            Checklist_QOCs = msg[10]
            Checklist_Locs = msg[11]
            App.get_running_app().root.current = 'Individual_Check'

    # This is the response for when the refresh function is called.

        if len(msg) == 11:
            global coders
            global users
            global statusers
            global activator
            global scrol
            activator = msg[7]
            coders = msg[8]
            users = msg[9]
            statusers = msg[10]

            layout1 = GridLayout(cols=1, spacing=10, padding=[50, 15, 50, 15], row_default_height=150, size_hint_y=None)
            layout1.bind(minimum_height=layout1.setter('height'))
            for count, ref in enumerate(coders):
                boxi = BoxLayout(orientation='horizontal', spacing=5, padding=[5, 5, 5, 5])
                if statusers[count] == 'No':
                    btn = Button(text=str(ref), size_hint_x=0.6, background_normal='',
                                 background_color=[0, .4666, 0.70196, 1], font_size=30, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2 = Button(text=str(Checklist_Cartons[count]), size_hint_x=0.27, background_normal='',
                                  background_color=[0, .4666, 0.70196, 1], font_size=40, id=str(count))
                    btn2.bind(on_press=self.send)
                    btn3 = Button(text=str(statusers[count]), size_hint_x=0.13, background_normal='',
                                  background_color=[0.89803922, 0.25882353, 0.25882353, 1], id=str(count))
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    boxi.add_widget(btn3)
                    layout1.add_widget(boxi)
                if statusers[count] == 'Yes':
                    btn = Button(text=str(ref), size_hint_x=0.6, background_normal='',
                                 background_color=[0, 0.52156863, 0.25098039, 1], font_size=30, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2 = Button(text=str(Checklist_Cartons[count]), size_hint_x=0.27, background_normal='',
                                  background_color=[0, 0.52156863, 0.25098039, 1], font_size=40, id=str(count))
                    btn2.bind(on_press=self.send)
                    btn3 = Button(text=str(statusers[count]), size_hint_x=0.13, background_normal='',
                                  background_color=[0, 0.52156863, 0.25098039, 1], id=str(count))
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    boxi.add_widget(btn3)
                    layout1.add_widget(boxi)
                if statusers[count] == 'Yes E':
                    btn = Button(text=str(ref), size_hint_x=0.6, background_normal='',
                                 background_color=[1, 0.45098039, 0, 1], font_size=30, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2 = Button(text=str(Checklist_Cartons[count]), size_hint_x=0.27, background_normal='',
                                  background_color=[1, 0.45098039, 0, 1], font_size=40, id=str(count))
                    btn2.bind(on_press=self.send)
                    btn3 = Button(text=str(statusers[count]), size_hint_x=0.13, background_normal='',
                                  background_color=[1, 0.45098039, 0, 1], id=str(count))
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    boxi.add_widget(btn3)
                    layout1.add_widget(boxi)
            scrol = ScrollView(scroll_type=['bars'], bar_width='10dp')
            scrol.add_widget(layout1)
            self.ids.boxer.add_widget(scrol)

    # This is the response code for when MBDTF and Throne
    # are sent but no item was clicked

        if len(msg) == 9:
            POPUP('Alert', 'No Item Clicked')

    # Response code when you quick mark as checked.

        if len(msg) == 2:
            global Checked_Statuslist
            Checked_Statuslist = msg[0]
            statusers = msg[1]
            self.ids.boxer.remove_widget(scrol)
            layout1 = GridLayout(cols=1, spacing=10, padding=[50, 15, 50, 15], row_default_height=150, size_hint_y=None)
            layout1.bind(minimum_height=layout1.setter('height'))
            for count, ref in enumerate(coders):
                boxi = BoxLayout(orientation='horizontal', spacing=5, padding=[5, 5, 5, 5])
                if statusers[count] == 'No':
                    btn = Button(text=str(ref), size_hint_x=0.6, background_normal='',
                                 background_color=[0, .4666, 0.70196, 1], font_size=30, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2 = Button(text=str(Checklist_Cartons[count]), size_hint_x=0.27, background_normal='',
                                  background_color=[0, .4666, 0.70196, 1], font_size=40, id=str(count))
                    btn2.bind(on_press=self.send)
                    btn3 = Button(text=str(statusers[count]), size_hint_x=0.13, background_normal='',
                                  background_color=[0.89803922, 0.25882353, 0.25882353, 1], id=str(count))
                    btn3.bind(on_press=self.quickmark)
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    boxi.add_widget(btn3)
                    layout1.add_widget(boxi)
                if statusers[count] == 'Yes':
                    btn = Button(text=str(ref), size_hint_x=0.6, background_normal='',
                                 background_color=[0, 0.52156863, 0.25098039, 1], font_size=30, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2 = Button(text=str(Checklist_Cartons[count]), size_hint_x=0.27, background_normal='',
                                  background_color=[0, 0.52156863, 0.25098039, 1], font_size=40, id=str(count))
                    btn2.bind(on_press=self.send)
                    btn3 = Button(text=str(statusers[count]), size_hint_x=0.13, background_normal='',
                                  background_color=[0, 0.52156863, 0.25098039, 1], id=str(count))
                    btn3.bind(on_press=self.quickmark)
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    boxi.add_widget(btn3)
                    layout1.add_widget(boxi)
                if statusers[count] == 'Yes E':
                    btn = Button(text=str(ref), size_hint_x=0.6, background_normal='',
                                 background_color=[1, 0.45098039, 0, 1], font_size=30, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2 = Button(text=str(Checklist_Cartons[count]), size_hint_x=0.27, background_normal='',
                                  background_color=[1, 0.45098039, 0, 1], font_size=40, id=str(count))
                    btn2.bind(on_press=self.send)
                    btn3 = Button(text=str(statusers[count]), size_hint_x=0.13, background_normal='',
                                  background_color=[1, 0.45098039, 0, 1], id=str(count))
                    btn3.bind(on_press=self.quickmark)
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    boxi.add_widget(btn3)
                    layout1.add_widget(boxi)
            scrol = ScrollView(scroll_type=['bars'], bar_width='10dp')
            scrol.add_widget(layout1)
            self.ids.boxer.add_widget(scrol)
            POPUP('Alert', 'Logged in server')

    def send(self, instance):
        global Checklist_Cartons
        global Throne
        global statusers
        Throne = instance.id
        Throne = int(Throne)
        self.Watch_The_Throne()

    def Watch_The_Throne(self, *args):
        global MBDTF
        global Throne
        # Has To Be The Length Of 63
        msg = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10],
               [11],[12]]
        msg.append([MBDTF])
        msg.append([Throne])
        msg = pickle.dumps(msg, protocol=2)

        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)

    def on_enter(self, *args):
        global scrol
        global coders
        global users
        global statusers
        global activator
        global Checklist_Cartons
        global Checked_Refs
        global MBDTF
        layout1 = GridLayout(cols=1, spacing=10, padding=[50, 15, 50, 15], row_default_height=150, size_hint_y=None)
        layout1.bind(minimum_height=layout1.setter('height'))
        for count, ref in enumerate(coders):
            boxi = BoxLayout(orientation='horizontal', spacing=5, padding=[5, 5, 5, 5])
            if statusers[count] == 'No':
                btn = Button(text=str(ref), size_hint_x=0.6, background_normal='',
                             background_color=[0, .4666, 0.70196, 1], font_size=30, id=str(count))
                btn.bind(on_press=self.send)
                btn2 = Button(text=str(Checklist_Cartons[count]), size_hint_x=0.27, background_normal='',
                              background_color=[0, .4666, 0.70196, 1], font_size=40, id=str(count))
                btn2.bind(on_press=self.send)
                btn3 = Button(text=str(statusers[count]), size_hint_x=0.13, background_normal='',
                              background_color=[0.89803922, 0.25882353, 0.25882353, 1], id=str(count))
                btn3.bind(on_press=self.quickmark)
                boxi.add_widget(btn)
                boxi.add_widget(btn2)
                boxi.add_widget(btn3)
                layout1.add_widget(boxi)
            if statusers[count] == 'Yes':
                btn = Button(text=str(ref), size_hint_x=0.6, background_normal='',
                             background_color=[0, 0.52156863, 0.25098039, 1], font_size=30, id=str(count))
                btn.bind(on_press=self.send)
                btn2 = Button(text=str(Checklist_Cartons[count]), size_hint_x=0.27, background_normal='',
                              background_color=[0, 0.52156863, 0.25098039, 1], font_size=40, id=str(count))
                btn2.bind(on_press=self.send)
                btn3 = Button(text=str(statusers[count]), size_hint_x=0.13, background_normal='',
                              background_color=[0, 0.52156863, 0.25098039, 1], id=str(count))
                btn3.bind(on_press=self.quickmark)
                boxi.add_widget(btn)
                boxi.add_widget(btn2)
                boxi.add_widget(btn3)
                layout1.add_widget(boxi)
            if statusers[count] == 'Yes E':
                btn = Button(text=str(ref), size_hint_x=0.6, background_normal='',
                             background_color=[1, 0.45098039, 0, 1], font_size=30, id=str(count))
                btn.bind(on_press=self.send)
                btn2 = Button(text=str(Checklist_Cartons[count]), size_hint_x=0.27, background_normal='',
                              background_color=[1, 0.45098039, 0, 1], font_size=40, id=str(count))
                btn2.bind(on_press=self.send)
                btn3 = Button(text=str(statusers[count]), size_hint_x=0.13, background_normal='',
                              background_color=[1, 0.45098039, 0, 1], id=str(count))
                btn3.bind(on_press=self.quickmark)
                boxi.add_widget(btn)
                boxi.add_widget(btn2)
                boxi.add_widget(btn3)
                layout1.add_widget(boxi)
        scrol = ScrollView(scroll_type=['bars'], bar_width='10dp')
        scrol.add_widget(layout1)
        self.ids.boxer.add_widget(scrol)
        self.ids.date_displayer2.text = str(datetime.now().strftime('%Y-%m-%d'))
        self.ids.ref_displayer.text = str(Checked_Refs[MBDTF])

    def on_leave(self, *args):
        global scrol
        self.ids.boxer.remove_widget(scrol)

    def Send_MBDTF(self, *args):
        global scrol
        self.ids.boxer.remove_widget(scrol)
        global MBDTF
        msg = [[1],[2],[3],[4],[5],[6],[7],[8],[9], [10],[11]]
        msg.append([MBDTF])
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)

    def quickmark(self, instance):
        global Throne
        global payloader
        Throne = instance.id
        Throne = int(Throne)
        if instance.text == 'No':
            payloader = 'Yes'
            return Confirmation_Email("You're going to mark\nthis as Checked", "Yes", 'Alert',
                                      self.quickmarker, self.packitman)

        else:
            payloader = 'No'
            return Confirmation_Email("You're going to mark\nthis as NOT Checked", "Yes", 'Alert',
                                      self.quickmarker,
                                      self.packitman)

    def quickmarker(self, instance):
        global payloader
        Maga = [['Be'], ['Be'], ['Be'], ['Be'], ['Be'], [1], [2], [3], [4], [5], [6]]
        Maga.append([payloader])
        Maga.append(MBDTF)
        Maga.append(Throne)
        Maga.append(User)
        self.Dragon_Energy(Maga=Maga)

    def Dragon_Energy(self, Maga):
        msg = Maga
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)

class Individual_Check(Screen):


    def connect_to_server(self):
        reactor.connectTCP(HOST, 8000, EchoClientFactory(self))

    def on_connection(self, connection):
        self.print_message("Connected successfully!")
        self.connection = connection
    def connecter_to_server(self, instance):
        reactor.connectTCP(HOST, 8000, EchoClientFactory(self))
    def ticker(self, *args):
        msg = ['The College Dropout']
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            print(e)
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)
    def packitman(self, instance):
        pass

    def print_message(self, msg):

    # This is the tickback response message.

        if len(msg) == 1:
            print("Tickback Received")

        if len(msg) == 9:
            global statusers
            global Checked_Statuslist
            Checked_Statuslist = msg[0]
            statusers = msg[1]
            POPUP('Alert', 'Items still need checking')

        if len(msg) == 10:
            Checked_Statuslist = msg[0]
            statusers = msg[1]
            POPUP('Alert', 'Checklist is complete')

        if len(msg) == 12:
            global Checklist_Codes
            global Checklist_Descs
            global Checklist_Errors
            global Checklist_Users
            global Checklist_QOCs
            global Checklist_QOPs
            global Active_Ref
            global Checklist_Locs
            Active_Ref = msg[4]
            Checklist_Errors = msg[5]
            Checklist_Users = msg[6]
            Checklist_Codes = msg[7]
            Checklist_Descs = msg[8]
            Checklist_QOPs = msg[9]
            Checklist_QOCs = msg[10]
            Checklist_Locs = msg[11]
            self.on_enter()

    def Mark_As_Picked_In_Server(self, *args):
        Readied = [['1'], ['2'], ['3'], ['4'], ['5'], ['6'], ['7'] ,['8'], ['9'], ['10'],
                   ['11'], ['12'], ['13']]
        global User
        global MBDTF
        global Throne

        readier = [User]
        red = [Throne]
        Yao_Ming = [MBDTF]

        Readied.append(Yao_Ming)
        Readied.append(red)
        Readied.append(readier)
        msg = pickle.dumps(Readied, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)

    def I_Was_Coming_From_West_Wid_A_Car_Full_O(self, instance):
        pass

    def on_enter(self, *args):
        global Checklist_Codes
        global Checklist_Descs
        global Checklist_Errors
        global Checklist_Users
        global Checklist_QOCs
        global Checklist_QOPs
        global Throne
        global Active_Ref
        global Checklist_Locs
        global constantvalue1
        global dpgc2131
        self.connect_to_server()
        self.ticker()
        constantvalue1 = 0
        dpgc2131 = 0
        splititfam = 0
        try:
            dex = Checklist_Descs[Throne]
            try:
                T = dex.index('mm')
                a, b = dex[:T + 2], dex[T + 3:]
                splititfam = 1
            except ValueError as e:
                try:
                    T = dex.index('MM')
                    a, b = dex[:T + 2], dex[T + 3:]
                    splititfam = 1
                except ValueError as e:
                    splititfam = 0
            if splititfam == 1:
                self.ids.description.text = str( a + '\n' + b)
            if splititfam == 0:
                self.ids.description.text = str(Checklist_Codes[Throne] + '\n' + Checklist_Descs[Throne])
            self.ids.itemnumberdisplay.text = ('Item Number : ' + str(Throne + 1) + '/' + str(len(Checklist_Codes)))
            self.ids.refnum.text = str(Active_Ref[0])
            self.ids.error.text = str(Checklist_Errors[Throne])
            self.ids.productcode.text = str(Checklist_Codes[Throne])
            self.ids.qop.text = str(Checklist_QOPs[Throne])
            self.ids.qoc.text = str(Checklist_QOCs[Throne])
            self.ids.pickedby.text = str(Checklist_Users[Throne])
        except NameError as e:
            self.Watch_The_Throne()
    def Next_Item(self):
        Confirmation_Email('Mark item as checked', 'Checked', 'Please Confirm', self.Next_Item1, self.I_Was_Coming_From_West_Wid_A_Car_Full_O)
    def Next_Item1(self , instance):
        self.Mark_As_Picked_In_Server()
        global Checklist_Codes
        global Checklist_Descs
        global Checklist_Errors
        global Checklist_Users
        global Checklist_QOCs
        global Checklist_QOPs
        global Throne
        global Active_Ref
        global constantvalue1
        global dpgc2131
        constantvalue1 = 0
        dpgc2131 = 0
        Throne += 1
        Watch_The = Throne
        if Throne >= len(Checklist_Codes):
            Throne -= 1
        splititfam = 0
        try:
            dex = Checklist_Descs[Throne]
            try:
                T = dex.index('mm')
                a, b = dex[:T + 2], dex[T + 3:]
                splititfam = 1
            except ValueError as e:
                try:
                    T = dex.index('MM')
                    a, b = dex[:T + 2], dex[T + 3:]
                    splititfam = 1
                except ValueError as e:
                    splititfam = 0
            if splititfam == 1:
                self.ids.description.text = str(a + '\n' + b)
            if splititfam == 0:
                self.ids.description.text = str(Checklist_Descs[Watch_The])
            self.ids.itemnumberdisplay.text = ('Item Number : ' + str(Throne+1) + '/' + str(len(Checklist_Codes)))
            self.ids.error.text = str(Checklist_Errors[Watch_The])
            self.ids.productcode.text = Checklist_Codes[Watch_The]
            self.ids.qop.text = str(Checklist_QOPs[Watch_The])
            self.ids.qoc.text = str(Checklist_QOCs[Watch_The])
            self.ids.pickedby.text = str(Checklist_Users[Watch_The])

        except IndexError as e:
            print(e)
            POPUP('No More Items!', 'Checklist Complete')

    def Previous_Item(self):
        global Checklist_Codes
        global Checklist_Descs
        global Checklist_Errors
        global Checklist_Users
        global Checklist_QOCs
        global Checklist_QOPs
        global Throne
        global Active_Ref
        Throne -= 1
        Watch_The = Throne
        if (Watch_The+1) <= 0:
            Throne += 1
            Watch_The += 1
        splititfam = 0
        try:
            dex = Checklist_Descs[Watch_The]
            try:
                T = dex.index('mm')
                a, b = dex[:T + 2], dex[T + 3:]
                splititfam = 1
            except ValueError as e:
                try:
                    T = dex.index('MM')
                    a, b = dex[:T + 2], dex[T + 3:]
                    splititfam = 1
                except ValueError as e:
                    splititfam = 0
            if splititfam == 1:
                self.ids.description.text = str(a + '\n' + b)
            if splititfam == 0:
                self.ids.description.text = Checklist_Descs[Watch_The]
            self.ids.itemnumberdisplay.text = ('Item Number : ' + str(Throne+1) + '/' + str(len(Checklist_Codes)))
            self.ids.error.text = str(Checklist_Errors[Watch_The])
            self.ids.productcode.text = Checklist_Codes[Watch_The]
            self.ids.qop.text = str(Checklist_QOPs[Watch_The])
            self.ids.qoc.text = str(Checklist_QOCs[Watch_The])
            self.ids.pickedby.text = str(Checklist_Users[Watch_The])

        except IndexError as e:
            POPUP('No More Items!', 'Please click\ncomplete button')

    def Placed_Carton_On_Pallet(self):
        global constantvalue1
        global dpgc2131
        global Checklist_QOCs
        global Checklist_QOPs
        global Throne
        valued = 1.0
        dpgc2131 += valued
        value = float(Checklist_QOPs[Throne]) / float(Checklist_QOCs[Throne])
        print(value)
        constantvalue1 += value
        self.ids.qop.text = str(constantvalue1) + ' / ' + str(Checklist_QOPs[Throne])
        self.ids.qoc.text = str(dpgc2131) + ' / ' +str(Checklist_QOCs[Throne])
        if constantvalue1 == float(Checklist_QOPs[Throne]):
            POPUP('Done!', 'Item Picked!')

        if constantvalue1 < 0:
            self.ids.qop.text = str(Checklist_QOPs[Throne])
            constantvalue1 = 0
            POPUP('Error!', 'You Removed\nToo Much!')
        if dpgc2131 < 0:
            self.ids.qoc.text = str(Checklist_QOCs[Throne])
            dpgc2131 = 0

    def Removed_Carton_On_Pallet(self):
        global constantvalue1
        global dpgc2131
        global Checklist_QOCs
        global Checklist_QOPs
        global Throne
        valued = 1.0
        dpgc2131 -= valued
        value = float(Checklist_QOPs[Throne]) / float(Checklist_QOCs[Throne])
        print(value)
        constantvalue1 -= value
        self.ids.qop.text = str(constantvalue1) + ' / ' + str(Checklist_QOPs[Throne])
        self.ids.qoc.text = str(dpgc2131) + ' / ' + str(Checklist_QOCs[Throne])
        if constantvalue1 == float(Checklist_QOPs[Throne]):
            POPUP('Done!', 'Item Picked!')

        if constantvalue1 < 0:
            self.ids.qop.text = str(Checklist_QOPs[Throne])
            constantvalue1 = 0
            POPUP('Error!', 'You Removed\nToo Much!')
        if dpgc2131 < 0:
            self.ids.qoc.text = str(Checklist_QOCs[Throne])
            dpgc2131 = 0

    def Placed_Piece_On_Pallet(self):
        global constantvalue1
        global dpgc2131
        global Checklist_QOCs
        global Checklist_QOPs
        global Throne
        valued = 1.0
        constantvalue1 += valued
        self.ids.qop.text = str(constantvalue1) + ' / ' + str(Checklist_QOPs[Throne])
        self.ids.qoc.text = str(dpgc2131) + ' / ' + str(Checklist_QOCs[Throne])
        if constantvalue1 == qop[chips]:
            POPUP('Done!', 'Item Picked!')

        if constantvalue1 < 0:
            self.ids.qop.text = str(qop[chips])
            constantvalue1 = 0
            POPUP('Error!', 'You Removed\nToo Much!')
        if dpgc2131 < 0:
            self.ids.qoc.text = str(qoc[chips])
            dpgc2131 = 0

    def Removed_Piece_On_Pallet(self):
        global constantvalue1
        global dpgc2131
        global Checklist_QOCs
        global Checklist_QOPs
        global Throne
        valued = 1.0
        constantvalue1 -= valued
        self.ids.qop.text = str(constantvalue1) + ' / ' + str(Checklist_QOPs[Throne])
        self.ids.qoc.text = str(dpgc2131) + ' / ' + str(Checklist_QOCs[Throne])
        if constantvalue1 == qop[chips]:
            POPUP('Done!', 'Item Picked!')

        if constantvalue1 < 0:
            self.ids.qop.text = str(qop[chips])
            constantvalue1 = 0
            POPUP('Error!', 'You Removed\nToo Much!')
        if dpgc2131 < 0:
            self.ids.qoc.text = str(qoc[chips])
            dpgc2131 = 0

class Individual_Check_Error(Screen):



    def connect_to_server(self):
        reactor.connectTCP(HOST, 8000, EchoClientFactory(self))

    def on_connection(self, connection):
        self.print_message("Connected successfully!")
        self.connection = connection
    def connecter_to_server(self, instance):
        reactor.connectTCP(HOST, 8000, EchoClientFactory(self))
    def ticker(self, *args):
        msg = ['The College Dropout']
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)
    def packitman(self, instance):
        pass
    def Confirmation_Emails(self, LabelText, Button1Text, PopupTitle, button1function):
        global taxi

        box = BoxLayout(orientation='vertical', padding=(10))
        box.add_widget(Label(text=''))
        box.add_widget(Label(text=LabelText))
        box.add_widget(Label(text=''))
        backstrap = BoxLayout(orientation='horizontal')
        taxi = TextInput(id='plastic', multiline=False, font_size=40, input_type='number', input_filter='int')
        backstrap.add_widget(Label(text=''))
        backstrap.add_widget(taxi)
        backstrap.add_widget(Label(text=''))
        btn1 = Button(text=Button1Text, background_normal='', background_color=(0, 0.52156863, 0.25098039, 1))
        box.add_widget(Label(text='', size_hint_y=0.3))
        box.add_widget(backstrap)
        box.add_widget(Label(text='', size_hint_y=0.3))
        box.add_widget(btn1)
        box.add_widget(Label(text=''))

        # Add Label Inbvetween Buttons to give a bit more room for the fat thumbs

        popup = Popup(title=PopupTitle, title_size=(30),
                      title_align='center', content=box,
                      size_hint=(None, None), size=(600, 600),
                      auto_dismiss=True)

        btn1.bind(on_press=button1function)
        btn1.bind(on_release=popup.dismiss)
        popup.open()
    def Confirmation_EmailsIP(self, LabelText, Button1Text, PopupTitle, button1function):
        global taxir

        box = BoxLayout(orientation='vertical', padding=(10))
        box.add_widget(Label(text=''))
        box.add_widget(Label(text=LabelText))
        box.add_widget(Label(text=''))
        backstrap = BoxLayout(orientation='horizontal')
        taxir = TextInput(id='plastic', multiline=False, font_size=40)
        backstrap.add_widget(taxir)
        btn1 = Button(text=Button1Text, background_normal='', background_color=(0, 0.52156863, 0.25098039, 1))
        box.add_widget(Label(text='', size_hint_y=0.3))
        box.add_widget(backstrap)
        box.add_widget(Label(text='', size_hint_y=0.3))
        box.add_widget(btn1)
        box.add_widget(Label(text=''))

        # Add Label Inbvetween Buttons to give a bit more room for the fat thumbs

        popup = Popup(title=PopupTitle, title_size=(30),
                      title_align='center', content=box,
                      size_hint=(None, None), size=(600, 600),
                      auto_dismiss=True)

        btn1.bind(on_press=button1function)
        btn1.bind(on_release=popup.dismiss)
        popup.open()

    def IP_makesure(self):
        self.Confirmation_EmailsIP('Enter Product Code', 'Log Error','Incorrect Product',self.incorrect_product)

    def QS_makesure(self):
        self.Confirmation_Emails('Enter The Quantity Missing', 'Log Error', 'Quantity Short',self.quantity_short)
    def QE_makesure(self):
        self.Confirmation_Emails('Enter The Quantity Extra', 'Log Error', 'Quantity Extra',self.quantity_extra)
    def QD_makesure(self):
        self.Confirmation_Emails('Enter The Quantity Damaged', 'Log Error', 'Quantity Extra',self.quantity_damaged)

    def send_message(self, *args):
        global ready_up
        msg = ready_up
        gsm = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(gsm)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)
    def print_message(self, msg):
        if len(msg) == 5:
            locs = msg[0]
            desc = msg[1]
            codes = msg[2]
            qop = msg[3]
            qoc = msg[4]
        if len(msg) == 1:
            POPUP('Error', 'Please mark list\nas complete')
        if len(msg) == 14:
            POPUP('Error', 'Please send again')
        if len(msg) == 10:
            global statusers
            global Checked_Statuslist
            Checked_Statuslist = msg[0]
            statusers = msg[1]
            POPUP('Done!', 'Logged Thank You!')

        pass

    def on_enter(self, *args):
        global Checklist_Codes
        global Checklist_Descs
        global Checklist_Errors
        global Checklist_Users
        global Checklist_QOCs
        global Checklist_QOPs
        global Throne
        global Active_Ref
        global Checklist_Locs
        global constantvalue1
        global dpgc2131
        self.connect_to_server()
        self.ticker()
        self.ids.date_displayer2.text = 'Item Number : ' + str(Throne+1) + '/' + str(len(Checklist_Locs))
        self.ids.ProductCode.text = ''
        self.ids.QOP.text = ''
        self.ids.QOC.text = ''
        self.ids.locat.text = ''
        splititfam = 0
        try:
            dex = Checklist_Descs[Throne]
            try:
                T = dex.index('mm')
                a, b = dex[:T + 2], dex[T + 3:]
                splititfam = 1
            except ValueError as e:
                try:
                    T = dex.index('MM')
                    a, b = dex[:T + 2], dex[T + 3:]
                    splititfam = 1
                except ValueError as e:
                    splititfam = 0
            if splititfam == 1:
                self.ids.ProductCode.text = str(Checklist_Codes[Throne] + '\n' + a + '\n' + b )
            if splititfam == 0:
                self.ids.ProductCode.text = str(Checklist_Codes[Throne] + '\n' + Checklist_Descs[Throne])
            self.ids.QOP.text = Checklist_QOPs[Throne]
            self.ids.QOC.text = Checklist_QOCs[Throne]
            self.ids.locat.text = Checklist_Locs[Throne]
        except IndexError as e:
            Throne -= 1
            POPUP('Checked!', 'Checklist\nComplete')
            self.ids.date_displayer2.text = 'Item Number : ' + str(Throne + 1) + '/' + str(len(Checklist_Locs))
            self.ids.ProductCode.text = str(Checklist_Codes[Throne] + '\n' + Checklist_Descs[Throne])
            self.ids.QOP.text = Checklist_QOPs[Throne]
            self.ids.QOC.text = Checklist_QOCs[Throne]
            self.ids.locat.text = Checklist_Locs[Throne]
    def incorrect_product(self, instance, *args):
        global User
        global MBDTF
        global Throne
        global taxir
        global Readied_Up
        Readied_Up = [['H'], ['H'], [1],[2],[3],[4],[5],[6], [7],[8],[9],[10], [11], [User], [MBDTF], [Throne]]
        error = taxir.text
        if error == '':
            return POPUP('Error','No Product Code Written')
        readied_error = str('Incorrect Product ' + error)

        Readied_Up.append(readied_error)
        msg = pickle.dumps(Readied_Up, protocol=2)
        Confirmation_Email(readied_error,'Log Error','Please Confirm',self.send_IP,self.packitman)
    def send_IP(self, instance, *args):
        global Readied_Up
        global User
        global MBDTF
        global Throne
        global taxir
        msg = pickle.dumps(Readied_Up, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            print(e)
            return Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)
        Throne += 1
        self.on_enter()
    def quantity_extra(self,instance,*args):
        global User
        global MBDTF
        global Throne
        global Readied_Up
        global taxi
        Readied_Up = [['H'], ['H'],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13], [User], [MBDTF], [Throne]]
        error = taxi.text
        if error == '':
            return POPUP('Error', 'No Quantity Specified')
        readied_error = str('Quantity Extra ' + error)
        Readied_Up.append(readied_error)
        msg = pickle.dumps(Readied_Up, protocol=2)
        Confirmation_Email(readied_error, 'Log Error', 'Please Confirm', self.send_IP, self.packitman)
        # if msg and self.connection:
        #     self.connection.write(msg)
        # Throne += 1
        # self.on_enter()

    def quantity_short(self, instance,*args):
        global User
        global MBDTF
        global Throne
        global Readied_Up
        global taxi
        Readied_Up = [['H'], ['H'],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[User], [MBDTF], [Throne]]
        error = taxi.text
        if error == '':
            return POPUP('Error', 'No Quantity Specified')
        readied_error = str('Quantity Short ' + error)
        Readied_Up.append(readied_error)
        msg = pickle.dumps(Readied_Up, protocol=2)
        Confirmation_Email(readied_error, 'Log Error', 'Please Confirm', self.send_IP, self.packitman)
        # if msg and self.connection:
        #     self.connection.write(msg)
        # Throne += 1
        # self.on_enter()

    def quantity_damaged(self, instance,*args):
        global User
        global MBDTF
        global Throne
        global Readied_Up
        global taxi
        Readied_Up = [['H'], ['H'],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13], [User], [MBDTF], [Throne]]
        error = taxi.text
        if error == '':
            return POPUP('Error', 'No Quantity Specified')
        readied_error = str('Quantity Damaged ' + error)
        Readied_Up.append(readied_error)
        msg = pickle.dumps(Readied_Up, protocol=2)
        Confirmation_Email(readied_error, 'Log Error', 'Please Confirm', self.send_IP, self.packitman)
        # if msg and self.connection:
        #     self.connection.write(msg)
        # Throne += 1
        # self.on_enter()
    def log_error(self, *args):
        global User
        global MBDTF
        global Throne

        Readied_Up = [['H'],['H'],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[User],[MBDTF],[Throne]]
        if self.ids.Incorrect_Product.text == '':

            if self.ids.Quantity_Extra.text == '':
                if self.ids.Quantity_Short.text == '':
                    error = self.ids.Quantity_Damaged.text
                    readied_error = str('Quantity Damaged ' + error)
                    Readied_Up.append(readied_error)

            if self.ids.Quantity_Damaged.text == '':
                if self.ids.Quantity_Short.text == '':
                    error = self.ids.Quantity_Extra.text
                    readied_error = str('Quantity Extra ' + error)
                    Readied_Up.append(readied_error)
                if self.ids.Quantity_Extra.text == '':
                    error = self.ids.Quantity_Short.text
                    readied_error = str('Quantity Short ' + error)
                    Readied_Up.append(readied_error)

        if self.ids.Quantity_Damaged.text == '':
            if self.ids.Quantity_Extra.text == '':
                if self.ids.Quantity_Short.text == '':
                    error = self.ids.Incorrect_Product.text
                    readied_error = str('Incorrect Product ' + error)
                    Readied_Up.append(readied_error)

        msg = pickle.dumps(Readied_Up, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            print(e)
            return Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)
        Throne += 1
        self.on_enter()

    def printout(self):
        global Checklist_Codes
        global Checklist_Descs
        global Checklist_Errors
        global Checklist_Users
        global Checklist_QOCs
        global Checklist_QOPs
        global Throne
        global Active_Ref
        global Checklist_Locs
        global constantvalue1
        global dpgc2131

class Receipting_Mode(Screen):


    def connecter_to_server(self, instance):
        reactor.connectTCP(HOST, 8000, EchoClientFactory(self))

    def ticker(self, *args):
        msg = ['The College Dropout']
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)

    def packitman(self, instance):
        pass

    def on_enter(self, *args):
        global Shipment_Reference_List
        global Shipment_Status_List
        global Shipment_Arrival_List
        global scro
        self.connect_to_server()
        self.ticker()
        self.ids.date_displayer.text = str(datetime.now().strftime('%Y-%m-%d'))
        layout1 = GridLayout(cols=1, spacing=10, padding=[50, 15, 50, 15], row_default_height=150, size_hint_y=None)
        layout1.bind(minimum_height=layout1.setter('height'))
        for count, ref in enumerate(Shipment_Reference_List):
            boxi = BoxLayout(orientation='horizontal', spacing=5, padding=[5, 5, 5, 5])
            if Shipment_Status_List[count] == 'Arrived':
                btn = Button(text=str(ref), background_normal='',
                             background_color=[0, .4666, 0.70196, 1], font_size=30, id=str(count))
                btn2 = Button(text=str(Shipment_Arrival_List[count]), size_hint_x=0.55, background_normal='',
                              background_color=[0, .4666, 0.70196, 1], font_size=40, id=str(count))
                btn.bind(on_press=self.send)
                btn2.bind(on_press=self.send)
                btn3 = Button(text=str(statusers[count]), size_hint_x=0.35, background_normal='',
                              background_color=[0, .4666, 0.70196, 1], id=str(count))
                boxi.add_widget(btn)
                boxi.add_widget(btn2)
                boxi.add_widget(btn3)
                layout1.add_widget(boxi)
            if Shipment_Status_List[count] == 'Not Arrived':
                btn = Button(text=str(ref), background_normal='',
                             background_color=[0.89803922, 0.25882353, 0.25882353, 1], font_size=30)
                btn2 = Button(text=str(Shipment_Arrival_List[count]), size_hint_x=0.55, background_normal='',
                              background_color=[0.89803922, 0.25882353, 0.25882353, 1], font_size=40)
                btn.bind(on_press=self.send)
                btn2.bind(on_press=self.send)
                btn3 = Button(text=str(Shipment_Status_List[count]), size_hint_x=0.35, background_normal='',
                              background_color=[0.89803922, 0.25882353, 0.25882353, 1])
                boxi.add_widget(btn)
                boxi.add_widget(btn2)
                boxi.add_widget(btn3)
                layout1.add_widget(boxi)
            if Shipment_Status_List[count] == 'In Progress':
                btn = Button(text=str(ref), background_normal='',
                             background_color=ORANGE, font_size=30)
                btn2 = Button(text=str(Shipment_Arrival_List[count]), size_hint_x=0.55, background_normal='',
                              background_color=ORANGE, font_size=40)
                btn.bind(on_press=self.send)
                btn2.bind(on_press=self.send)
                btn3 = Button(text=str(Shipment_Status_List[count]), size_hint_x=0.35, background_normal='',
                              background_color=ORANGE)
                boxi.add_widget(btn)
                boxi.add_widget(btn2)
                boxi.add_widget(btn3)
                layout1.add_widget(boxi)
            if Shipment_Status_List[count] == 'Receipted':
                btn = Button(text=str(ref), background_normal='',
                             background_color=GREEN, font_size=30)
                btn2 = Button(text=str(Shipment_Arrival_List[count]), size_hint_x=0.55, background_normal='',
                              background_color=GREEN, font_size=40)
                btn.bind(on_press=self.send)
                btn2.bind(on_press=self.send)
                btn3 = Button(text=str(Shipment_Status_List[count]), size_hint_x=0.35, background_normal='',
                              background_color=GREEN)
                boxi.add_widget(btn)
                boxi.add_widget(btn2)
                boxi.add_widget(btn3)
                layout1.add_widget(boxi)
            if Shipment_Status_List[count] == 'Not Sent!':
                btn = Button(text=str(ref), background_normal='',
                             background_color=PURPLE, font_size=30)
                btn2 = Button(text=str(Shipment_Arrival_List[count]), size_hint_x=0.55, background_normal='',
                              background_color=PURPLE, font_size=40)
                btn.bind(on_press=self.send)
                btn2.bind(on_press=self.send)
                btn3 = Button(text=str(Shipment_Status_List[count]), size_hint_x=0.35, background_normal='',
                              background_color=PURPLE)
                boxi.add_widget(btn)
                boxi.add_widget(btn2)
                boxi.add_widget(btn3)
                layout1.add_widget(boxi)
        scro = ScrollView(scroll_type=['bars'], bar_width='10dp')
        scro.add_widget(layout1)
        self.ids.bally.add_widget(scro)

    def connect_to_server(self):
        reactor.connectTCP(HOST, 8000, EchoClientFactory(self))

    def on_connection(self, connection):
        self.print_message("Connected successfully!")
        self.connection = connection

    def Get_Shipments(self, *args):
        global scro
        self.ids.bally.remove_widget(scro)
        msg = [[1],[2],[3],[4]]
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT',  self.connecter_to_server, self.packitman)

    def print_message(self, msg):

    # This is the response code that is called after we send Talib.

        if len(msg) == 4:
            global Shipment_Codes
            global Shipment_Quantity_Cartons
            global Individual_Shipment_Status
            global List_Of_Cartons_Placed
            Shipment_Codes = msg[0]
            Shipment_Quantity_Cartons = msg[1]
            Individual_Shipment_Status = msg[2]
            List_Of_Cartons_Placed = msg[3]
            App.get_running_app().root.current = 'Individual_Receipt_List'

    # This is the tickback response code

        if len(msg) == 1:
            print("Tickback Received")

        if len(msg) == 9:
            POPUP('Alert', 'Container Marked as\nNot Arrived')
        if len(msg) == 10:
            POPUP('Alert', 'Container Marked as\n Arrived')

        if len(msg) == 11:
            POPUP('Alert', 'No Item Was Clicked!')

    # This is the refresh function response code.

        if len(msg) == 8:
            global Shipment_Reference_List
            global Shipment_Status_List
            global Shipment_Arrival_List
            global scro
            Shipments = msg[7]
            Shipment_Reference_List = Shipments[0]
            Shipment_Status_List = Shipments[1]
            Shipment_Arrival_List = Shipments[2]
            Shipment_Reference_List = Shipment_Reference_List[0]
            Shipment_Status_List = Shipment_Status_List[0]
            Shipment_Arrival_List = Shipment_Arrival_List[0]
            layout1 = GridLayout(cols=1, spacing=10, padding=[50, 15, 50, 15], row_default_height=150, size_hint_y=None)
            layout1.bind(minimum_height=layout1.setter('height'))
            for count, ref in enumerate(Shipment_Reference_List):
                boxi = BoxLayout(orientation='horizontal', spacing=5, padding=[5, 5, 5, 5])
                if Shipment_Status_List[count] == 'Arrived':
                    btn = Button(text=str(ref), background_normal='',
                                 background_color=[0, .4666, 0.70196, 1], font_size=30, id=str(count))
                    btn2 = Button(text=str(Shipment_Arrival_List[count]), size_hint_x=0.55, background_normal='',
                                  background_color=[0, .4666, 0.70196, 1], font_size=40, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2.bind(on_press=self.send)
                    btn3 = Button(text=str(statusers[count]), size_hint_x=0.35, background_normal='',
                                  background_color=[0, .4666, 0.70196, 1], id=str(count))
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    boxi.add_widget(btn3)
                    layout1.add_widget(boxi)
                if Shipment_Status_List[count] == 'Not Arrived':
                    btn = Button(text=str(ref), background_normal='',
                                 background_color=[0.89803922, 0.25882353, 0.25882353, 1], font_size=30)
                    btn2 = Button(text=str(Shipment_Arrival_List[count]), size_hint_x=0.55, background_normal='',
                                  background_color=[0.89803922, 0.25882353, 0.25882353, 1], font_size=40)
                    btn.bind(on_press=self.send)
                    btn2.bind(on_press=self.send)
                    btn3 = Button(text=str(Shipment_Status_List[count]), size_hint_x=0.35, background_normal='',
                                  background_color=[0.89803922, 0.25882353, 0.25882353, 1])
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    boxi.add_widget(btn3)
                    layout1.add_widget(boxi)
                if Shipment_Status_List[count] == 'In Progress':
                    btn = Button(text=str(ref), background_normal='',
                                 background_color=ORANGE, font_size=30)
                    btn2 = Button(text=str(Shipment_Arrival_List[count]), size_hint_x=0.55, background_normal='',
                                  background_color=ORANGE, font_size=40)
                    btn.bind(on_press=self.send)
                    btn2.bind(on_press=self.send)
                    btn3 = Button(text=str(Shipment_Status_List[count]), size_hint_x=0.35, background_normal='',
                                  background_color=ORANGE)
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    boxi.add_widget(btn3)
                    layout1.add_widget(boxi)
                if Shipment_Status_List[count] == 'Receipted':
                    btn = Button(text=str(ref), background_normal='',
                                 background_color=GREEN, font_size=30)
                    btn2 = Button(text=str(Shipment_Arrival_List[count]), size_hint_x=0.55, background_normal='',
                                  background_color=GREEN, font_size=40)
                    btn.bind(on_press=self.send)
                    btn2.bind(on_press=self.send)
                    btn3 = Button(text=str(Shipment_Status_List[count]), size_hint_x=0.35, background_normal='',
                                  background_color=GREEN)
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    boxi.add_widget(btn3)
                    layout1.add_widget(boxi)
                if Shipment_Status_List[count] == 'Not Sent!':
                    btn = Button(text=str(ref), background_normal='',
                                 background_color=PURPLE, font_size=30)
                    btn2 = Button(text=str(Shipment_Arrival_List[count]), size_hint_x=0.55, background_normal='',
                                  background_color=PURPLE, font_size=40)
                    btn.bind(on_press=self.send)
                    btn2.bind(on_press=self.send)
                    btn3 = Button(text=str(Shipment_Status_List[count]), size_hint_x=0.35, background_normal='',
                                  background_color=PURPLE)
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    boxi.add_widget(btn3)
                    layout1.add_widget(boxi)
            scro = ScrollView(scroll_type=['bars'], bar_width='10dp')
            scro.add_widget(layout1)
            self.ids.bally.add_widget(scro)

        if len(msg) == 10:
            POPUP('Confirmed!', 'Logged Thank You!')
            self.Get_Shipments()
        if len(msg) == 18:
            self.Get_Shipments()

    def on_leave(self, *args):
        global scro
        self.ids.bally.remove_widget(scro)

    def send(self, instance):
        global Shipment_Reference_List
        global Talib
        ref_clicked = instance.text
        for count, ref in enumerate(Shipment_Reference_List):
            if ref == ref_clicked:
                Talib = count
                break
        self.Send_Talib()

    def Send_Talib(self, *args):
        global Talib
        msg = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10],
               [11], [12], [13], [14], [15], [16], [17], [18], [19]]
        msg.append([Talib])
        gsm = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(gsm)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)

    def potential_Talib(self, tt):
        global Talib
        Talib = tt
        global Shipment_Status_List
        if Shipment_Status_List[Talib] == 'Not Arrived':
            self.Mark_Container_As_Arrived()
        else:
            self.Mark_Container_As_Not_Arrived()

class Individual_Receipt_List(Screen):
    def connect_to_server(self):
        reactor.connectTCP(HOST, 8000, EchoClientFactory(self))

    def connecter_to_server(self, instance):
        reactor.connectTCP(HOST, 8000, EchoClientFactory(self))
    def ticker(self, *args):
        msg = ['The College Dropout']
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)
    def packitman(self, instance):
        pass

    def on_enter(self, *args):
        global Shipment_Codes
        global Shipment_Quantity_Cartons
        global Individual_Shipment_Status
        global List_Of_Cartons_Placed
        global cro
        layout1 = GridLayout(cols=1, spacing=10, padding=[50, 15, 50, 15], row_default_height=150, size_hint_y=None)
        layout1.bind(minimum_height=layout1.setter('height'))
        for count, ref in enumerate(Shipment_Codes):
            try:
                boxi = BoxLayout(orientation='horizontal', spacing=5, padding=[5, 5, 5, 5])
                if Individual_Shipment_Status[count] == 'In Progress':
                    btn = Button(text=str(ref), background_normal='',
                                 background_color=ORANGE, font_size=30, id=str(count))
                    btn2 = Button(text=str(float(List_Of_Cartons_Placed[count])) + ' / ' + str(
                    float(Shipment_Quantity_Cartons[count])), size_hint_x=0.55, background_normal='',
                                  background_color=ORANGE, font_size=40, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2.bind(on_press=self.send)
                    btn3 = Button(text=str(Individual_Shipment_Status[count]), size_hint_x=0.35, background_normal='',
                                  background_color=ORANGE, id=str(count))
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    boxi.add_widget(btn3)
                    layout1.add_widget(boxi)
                if Individual_Shipment_Status[count] == 'Receipted':
                    btn = Button(text=str(ref), background_normal='',
                                 background_color=GREEN, font_size=30, id=str(count))
                    btn2 = Button(text=str(float(List_Of_Cartons_Placed[count])) + ' / ' + str(
                    float(Shipment_Quantity_Cartons[count])), size_hint_x=0.55, background_normal='',
                                  background_color=GREEN, font_size=40, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2.bind(on_press=self.send)
                    btn3 = Button(text=str(Individual_Shipment_Status[count]), size_hint_x=0.35, background_normal='',
                                  background_color=GREEN, id=str(count))
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    boxi.add_widget(btn3)
                    layout1.add_widget(boxi)
                if Individual_Shipment_Status[count] == 'No':
                    btn = Button(text=str(ref), background_normal='',
                                 background_color=DARK_BLUE, font_size=30, id=str(count))
                    btn2 = Button(text=str(float(List_Of_Cartons_Placed[count])) + ' / ' + str(
                    float(Shipment_Quantity_Cartons[count])), size_hint_x=0.55, background_normal='',
                                  background_color=DARK_BLUE, font_size=40, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2.bind(on_press=self.send)
                    btn3 = Button(text=str(Individual_Shipment_Status[count]), size_hint_x=0.35, background_normal='',
                                  background_color=RED, id=str(count))
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    boxi.add_widget(btn3)
                    layout1.add_widget(boxi)
            except IndexError:
                POPUP('Alert', 'Something went wrong please try again')
        cro = ScrollView(scroll_type=['bars'], bar_width='10dp')
        cro.add_widget(layout1)
        self.ids.rajpac.add_widget(cro)
        self.ids.date_displayer.text = str(datetime.now().strftime('%Y-%m-%d'))

    def on_connection(self, connection):
        self.print_message("Connected successfully!")
        self.connection = connection

    def send(self, instance):
        global Mos_Def
        Mos_Def = instance.id
        Mos_Def = int(Mos_Def)
        self.Send_Mos_Def()

    def Send_Talib(self, *args):
        global cro
        self.ids.rajpac.remove_widget(cro)
        global Talib
        msg = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10],
               [11], [12], [13], [14], [15], [16], [17], [18], [19]]
        msg.append([Talib])
        gsm = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(gsm)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)

    def on_leave(self, *args):
        global cro
        self.ids.rajpac.remove_widget(cro)

    def print_message(self, msg):

        # This is the refresh function.

        if len(msg) == 4:
            global Shipment_Codes
            global Shipment_Quantity_Cartons
            global Individual_Shipment_Status
            global List_Of_Cartons_Placed
            global Shipment_Descriptions
            global Shipment_Quantity_Pieces
            Shipment_Codes = msg[0]
            Shipment_Quantity_Cartons = msg[1]
            Individual_Shipment_Status = msg[2]
            List_Of_Cartons_Placed = msg[3]
            global cro
            layout1 = GridLayout(cols=1, spacing=10, padding=[50, 15, 50, 15], row_default_height=150, size_hint_y=None)
            layout1.bind(minimum_height=layout1.setter('height'))
            for count, ref in enumerate(Shipment_Codes):
                boxi = BoxLayout(orientation='horizontal', spacing=5, padding=[5, 5, 5, 5])
                if Individual_Shipment_Status[count] == 'In Progress':
                    btn = Button(text=str(ref), background_normal='',
                                 background_color=ORANGE, font_size=30, id=str(count))
                    btn2 = Button(text=str(float(List_Of_Cartons_Placed[count])) + ' / ' + str(
                        float(Shipment_Quantity_Cartons[count])), size_hint_x=0.55, background_normal='',
                                  background_color=ORANGE, font_size=40, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2.bind(on_press=self.send)
                    btn3 = Button(text=str(Individual_Shipment_Status[count]), size_hint_x=0.35, background_normal='',
                                  background_color=ORANGE, id=str(count))
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    boxi.add_widget(btn3)
                    layout1.add_widget(boxi)
                if Individual_Shipment_Status[count] == 'Receipted':
                    btn = Button(text=str(ref), background_normal='',
                                 background_color=GREEN, font_size=30, id=str(count))
                    btn2 = Button(text=str(float(List_Of_Cartons_Placed[count])) + ' / ' + str(
                        float(Shipment_Quantity_Cartons[count])), size_hint_x=0.55, background_normal='',
                                  background_color=GREEN, font_size=40, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2.bind(on_press=self.send)
                    btn3 = Button(text=str(Individual_Shipment_Status[count]), size_hint_x=0.35, background_normal='',
                                  background_color=GREEN, id=str(count))
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    boxi.add_widget(btn3)
                    layout1.add_widget(boxi)
                if Individual_Shipment_Status[count] == 'No':
                    btn = Button(text=str(ref), background_normal='',
                                 background_color=DARK_BLUE, font_size=30, id=str(count))
                    btn2 = Button(text=str(float(List_Of_Cartons_Placed[count])) + ' / ' + str(
                        float(Shipment_Quantity_Cartons[count])), size_hint_x=0.55, background_normal='',
                                  background_color=DARK_BLUE, font_size=40, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2.bind(on_press=self.send)
                    btn3 = Button(text=str(Individual_Shipment_Status[count]), size_hint_x=0.35, background_normal='',
                                  background_color=RED, id=str(count))
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    boxi.add_widget(btn3)
                    layout1.add_widget(boxi)
            cro = ScrollView(scroll_type=['bars'], bar_width='10dp')
            cro.add_widget(layout1)
            self.ids.rajpac.add_widget(cro)

        # This is the response code that trails after you send mos def
        # and talib it confirms the filtered lists and changes screen

        if len(msg) == 6:
            global Shipment_Pallet_Amounts
            Shipment_Codes = msg[0]
            Shipment_Quantity_Cartons = msg[1]
            Individual_Shipment_Status = msg[2]
            Shipment_Descriptions = msg[3]
            Shipment_Quantity_Pieces = msg[4]
            Shipment_Pallet_Amounts = msg[5]
            App.get_running_app().root.current = "Individual_Receipt"

        # Tickback function as seen on every screen.

        if len(msg) == 1:
            print("Tickback Received")

        # a 9 length response code means that the item was quick marked

        if len(msg) == 9:
            self.Send_Talib()
            self.Clear_Labels()
            self.Fillout_Labels()
            POPUP('Alert', 'Item Marked As Receipted')

        # A length of 2 means no ref was clicked

        if len(msg) == 2:
            POPUP('Error', 'No Item Clicked')

        # A length of 10 means it was unmarked as receipted

        if len(msg) == 10:
            self.Send_Talib()
            self.Clear_Labels()
            self.Fillout_Labels()
            POPUP('Confirmed!', 'Item Marked as NOT Receipted')

    def Send_Mos_Def(self, *args):
        global Talib
        global User
        global Mos_Def
        msg = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10],
               [11], [12], [13], [14], [15], [16], [17], [18], [19], [20],
               [21]]
        msg.append([Talib])
        msg.append([Mos_Def])
        gsm = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(gsm)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)

class Individual_Receipt(Screen):


    def connecter_to_server(self, instance):
        reactor.connectTCP(HOST, 8000, EchoClientFactory(self))
    def ticker(self, *args):
        msg = ['The College Dropout']
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)
    def packitman(self, instance):
        pass

    def Amount_on_Pallet_Generator(self):
        global Shipment_Pallet_Amounts
        global Pallet_Number_Counter
        global Talib
        global Mos_Def
        global Is_This_The_First_Value
        # We want the shipment pallet number counter pallet number
        try:
            ALL_PALLETS = Shipment_Pallet_Amounts[Mos_Def]
            Is_This_The_First_Value = False
            Pallet_In_Question = ALL_PALLETS[Pallet_Number_Counter]
            Pallet_Number = Pallet_In_Question[0]
            Pallet_Amount = Pallet_In_Question[1]
            Pallet_B4 = ALL_PALLETS[Pallet_Number_Counter-1]
            PayPAL = Pallet_B4[1]
            if Pallet_Number_Counter == 0:
                PayPAL = 0
            Pallet_Amounto = Pallet_Amount - PayPAL
            return Pallet_Number, Pallet_Amounto
        except TypeError:
            Is_This_The_First_Value = True
            return 1, 0.00
        except IndexError:
            return None, None

    def Change_Pallet(self):
        global Shipment_Pallet_Amounts
        global Pallet_Number_Counter
        global Talib
        global Mos_Def
        Pallet_Number_Counter += 1
        self.i_am_groot()
    def Change_Pallet_To_Previous(self):
        global Shipment_Pallet_Amounts
        global Pallet_Number_Counter
        global Talib
        global Mos_Def
        Pallet_Number_Counter -= 1
        if Pallet_Number_Counter < 0:
            Pallet_Number_Counter += 1
            return POPUP('Error', 'This Is Already The First Pallet')

        self.i_am_groot()

    def on_enter(self, *args):
        global Shipment_Codes
        global Shipment_Quantity_Cartons
        global Individual_Shipment_Status
        global Shipment_Descriptions
        global Shipment_Quantity_Pieces
        global Shipment_Reference_List
        global List_Of_Cartons_Placed
        global Talib
        global Mos_Def
        global Shipment_Pallet_Amounts
        global Pallet_Number_Counter
        global Is_This_The_First_Value
        self.connect_to_server()
        self.ticker()
        Pallet_Number_Counter = 0
        self.ids.Marko_Picko.disabled = False
        Pallet_Number, Pallet_Amount = self.Amount_on_Pallet_Generator()
        if Is_This_The_First_Value is False:
            Groot = len(Shipment_Pallet_Amounts[Mos_Def])
        else:
            Groot = 1
        try:
            self.ids.itemnumberdisplay.text = str('Item Number :  ' + str(Mos_Def+1) + '/' + str(len(Shipment_Quantity_Cartons)))

            self.ids.palletnum.text = str('Pallet Number : ' + str(Pallet_Number) + '/' + str(Groot))

            self.ids.refnum.text = Shipment_Reference_List[Talib]

            dex = Shipment_Descriptions[Mos_Def]
            try:
                T = dex.index('mm')
                a, b = dex[:T + 2], dex[T + 3:]
                p2 = False
            except ValueError:
                try:
                    T = dex.index('MM')
                    a, b = dex[:T + 2], dex[T + 3:]
                    p2 = False
                except ValueError:
                    p2 = True
            if p2 == True:
                self.ids.description.text = str(dex)
            else:
                self.ids.description.text = str(a) + '\n' + str(b)
            self.ids.productcode.text = Shipment_Codes[Mos_Def]
            self.ids.qoc.text = str(Shipment_Quantity_Cartons[Mos_Def])
            self.ids.qop.text = str(Shipment_Quantity_Pieces[Mos_Def])
            self.ids.qoc_Placed.text = str(List_Of_Cartons_Placed[Mos_Def])
            quantity_of_pieces_placed = float(Shipment_Quantity_Pieces[Mos_Def])/float(Shipment_Quantity_Cartons[Mos_Def])
            self.ids.qop_Placed.text = str(quantity_of_pieces_placed * List_Of_Cartons_Placed[Mos_Def])
            self.ids.qoc_Placed_pallet.text = str(Pallet_Amount)
            self.ids.qop_Placed_pallet.text = str(quantity_of_pieces_placed * List_Of_Cartons_Placed[Mos_Def])
        except IndexError:
            POPUP('Error', 'No More Items!')
            Mos_Def -= 1
            self.on_enter()
    def i_am_groot(self):
        global Shipment_Codes
        global Shipment_Quantity_Cartons
        global Individual_Shipment_Status
        global Shipment_Descriptions
        global Shipment_Quantity_Pieces
        global Shipment_Reference_List
        global List_Of_Cartons_Placed
        global Talib
        global Mos_Def
        global Shipment_Pallet_Amounts
        global Pallet_Number_Counter
        self.ids.Marko_Picko.disabled = False
        Pallet_Number, Pallet_Amount = self.Amount_on_Pallet_Generator()
        if Pallet_Number == None:
            return POPUP('Error', 'You Havent Created The Pallet!')
        Groot = len(Shipment_Pallet_Amounts[Mos_Def])
        try:
            pieces_in_box = float(Shipment_Quantity_Pieces[Mos_Def])/float(Shipment_Quantity_Cartons[Mos_Def])
            self.ids.itemnumberdisplay.text = str('Item Number :  ' + str(Mos_Def+1) + '/' + str(len(Shipment_Quantity_Cartons)))

            self.ids.palletnum.text = str('Pallet Number : ' + str(Pallet_Number) + '/' + str(Groot))

            self.ids.refnum.text = Shipment_Reference_List[Talib]

            dex = Shipment_Descriptions[Mos_Def]
            try:
                T = dex.index('mm')
                a, b = dex[:T + 2], dex[T + 3:]
                p2 = False
            except ValueError:
                try:
                    T = dex.index('MM')
                    a, b = dex[:T + 2], dex[T + 3:]
                    p2 = False
                except ValueError:
                    p2 = True
            if p2 == True:
                self.ids.description.text = str(dex)
            else:
                self.ids.description.text = str(a) + '\n' + str(b)
            self.ids.productcode.text = Shipment_Codes[Mos_Def]
            self.ids.qoc.text = str(Shipment_Quantity_Cartons[Mos_Def])
            self.ids.qop.text = str(Shipment_Quantity_Pieces[Mos_Def])
            self.ids.qoc_Placed.text = str(List_Of_Cartons_Placed[Mos_Def])
            quantity_of_pieces_placed = float(Shipment_Quantity_Pieces[Mos_Def])/float(Shipment_Quantity_Cartons[Mos_Def])
            self.ids.qop_Placed.text = str(quantity_of_pieces_placed * List_Of_Cartons_Placed[Mos_Def])
            self.ids.qoc_Placed_pallet.text = str(Pallet_Amount)
            to_place_on_virtual_pallet = float(Pallet_Amount)*float(pieces_in_box)
            self.ids.qop_Placed_pallet.text = str(to_place_on_virtual_pallet)
        except IndexError:
            POPUP('Error', 'No More Items!')
            Mos_Def -= 1
            self.on_enter()
    def on_entered(self):
        global Shipment_Codes
        global Shipment_Quantity_Cartons
        global Individual_Shipment_Status
        global Shipment_Descriptions
        global Shipment_Quantity_Pieces
        global Shipment_Reference_List
        global Talib
        global Mos_Def
        if Mos_Def < 0:
            POPUP('Error', 'This is the first Item!')
            Mos_Def += 1
        try:

            self.ids.itemnumberdisplay.text = str('Item Number :  ' + str(Mos_Def+1) + '/' + str(len(Shipment_Quantity_Cartons)))

            self.ids.refnum.text = Shipment_Reference_List[Talib]

            dex = Shipment_Descriptions[Mos_Def]
            try:
                T = dex.index('mm')
                a, b = dex[:T + 2], dex[T + 3:]
                p2 = False
            except ValueError:
                try:
                    T = dex.index('MM')
                    a, b = dex[:T + 2], dex[T + 3:]
                    p2 = False
                except ValueError:
                    p2 = True
            if p2 == True:
                self.ids.description.text = str(dex)
            else:
                self.ids.description.text = str(a) + '\n' + str(b)
            self.ids.productcode.text = Shipment_Codes[Mos_Def]
            self.ids.qoc.text = str(Shipment_Quantity_Cartons[Mos_Def])
            self.ids.qop.text = str(Shipment_Quantity_Pieces[Mos_Def])
            self.ids.qoc_Placed.text = str(List_Of_Cartons_Placed[Mos_Def])
            quantity_of_pieces_placed = float(Shipment_Quantity_Pieces[Mos_Def])/float(Shipment_Quantity_Cartons[Mos_Def])
            self.ids.qop_Placed.text = str(quantity_of_pieces_placed * List_Of_Cartons_Placed[Mos_Def])
        except IndexError:
            POPUP('Error', 'No More Items!')
            self.on_enter()
    def on_ent(self):
        global Shipment_Codes
        global Shipment_Quantity_Cartons
        global Individual_Shipment_Status
        global Shipment_Descriptions
        global Shipment_Quantity_Pieces
        global Shipment_Reference_List
        global Talib
        global Mos_Def
        if Mos_Def < 0:
            POPUP('Error', 'This is the first Item!')
            Mos_Def += 1
        try:

            self.ids.itemnumberdisplay.text = str('Item Number :  ' + str(Mos_Def+1) + '/' + str(len(Shipment_Quantity_Cartons)))

            self.ids.refnum.text = Shipment_Reference_List[Talib]

            dex = Shipment_Descriptions[Mos_Def]
            try:
                T = dex.index('mm')
                a, b = dex[:T + 2], dex[T + 3:]
                p2 = False
            except ValueError:
                try:
                    T = dex.index('MM')
                    a, b = dex[:T + 2], dex[T + 3:]
                    p2 = False
                except ValueError:
                    p2 = True
            if p2 == True:
                self.ids.description.text = str(dex)
            else:
                self.ids.description.text = str(a) + '\n' + str(b)
            self.ids.productcode.text = Shipment_Codes[Mos_Def]
            self.ids.qoc.text = str(Shipment_Quantity_Cartons[Mos_Def])
            self.ids.qop.text = str(Shipment_Quantity_Pieces[Mos_Def])
            self.ids.qoc_Placed.text = str(List_Of_Cartons_Placed[Mos_Def])
            quantity_of_pieces_placed = float(Shipment_Quantity_Pieces[Mos_Def])/float(Shipment_Quantity_Cartons[Mos_Def])
            self.ids.qop_Placed.text = str(quantity_of_pieces_placed * List_Of_Cartons_Placed[Mos_Def])
        except IndexError:
            POPUP('Error', 'No More Items!')
            self.on_enter()



    def print_message(self, msg):

    # Tickback message

        if len(msg) == 1:
            print("Tickback Received")

    # This is the response that is received after you place a pallet

        if len(msg) == 2:
            POPUP('Alert','Success, Cartons placed\non pallet')

    # This is the response code that is received after you remove a pallet.

        if len(msg) == 3:
            POPUP('Alert', 'Success, Cartons Removed')

    # This is the response code for the get pallet tag message it gets the pallet tag number
    # whilst the user is palletizing an item.

        if len(msg) == 4:
            global pallet_tag_number
            pallet_tag_number = msg[3]

    # This is the response when you mark as put away but the item list is not ready to putaway.

        if len(msg) == 5:
            POPUP('Alert','List not ready\nto be put away.')

    # This is the response when an item is successfully receipted.

        if len(msg) == 10:
            POPUP('Success', 'Item Receipted')

    # This is the response when something is marked as put away and the put away is successful.

        if len(msg) == 12:
            POPUP('Success', 'Items Receipted\nand ready to Put-Away')

    # This is the response after a pallet is created, it sends the updated pallet amounts.

        if len(msg) == 13:
            global Shipment_Pallet_Amounts
            Shipment_Pallet_Amounts = msg[12]
            Shipment_Pallet_Amounts = Shipment_Pallet_Amounts[0]
            self.i_am_groot()
            POPUP('Success','Pallet Created')




    def connect_to_server(self):
        reactor.connectTCP(HOST, 8000, EchoClientFactory(self))

    def on_connection(self, connection):
        self.print_message("Connected successfully!")
        self.connection = connection

    def update_padding(self, text_input, *args):
        text_width = text_input._get_text_width(
            text_input.text,
            text_input.tab_width,
            text_input._label_cached
        )
        text_input.padding_x = (text_input.width - text_width) / 2


    def Confirmation_Emails(self, LabelText, Button1Text, PopupTitle, button1function):
        global taxi

        box = BoxLayout(orientation='vertical', padding=(10))
        box.add_widget(Label(text=''))
        box.add_widget(Label(text=LabelText))
        box.add_widget(Label(text=''))
        backstrap = BoxLayout(orientation='horizontal')
        taxi = TextInput(id='plastic', multiline=False, font_size=40, input_type='number', input_filter='int')
        backstrap.add_widget(Label(text=''))
        backstrap.add_widget(taxi)
        backstrap.add_widget(Label(text=''))
        btn1 = Button(text=Button1Text, background_normal='', background_color=(0, 0.52156863, 0.25098039, 1))
        box.add_widget(Label(text='', size_hint_y=0.3))
        box.add_widget(backstrap)
        box.add_widget(Label(text='', size_hint_y=0.3))
        box.add_widget(btn1)
        box.add_widget(Label(text=''))

        # Add Label Inbvetween Buttons to give a bit more room for the fat thumbs

        popup = Popup(title=PopupTitle, title_size=(30),
                      title_align='center', content=box,
                      size_hint=(None, None), size=(600, 600),
                      auto_dismiss=True)

        btn1.bind(on_press=button1function)
        btn1.bind(on_release=popup.dismiss)
        popup.open()

    def Placed_Carton(self):
        self.Confirmation_Emails('Mark the Amount Placed', 'Cartons Placed', 'Please Confirm', self.Amount_Of_Cartons)

    def Removed_Carton(self):
        self.Confirmation_Emails('Mark the Amount Removed', 'Cartons Removed', 'Please Confirm', self.Amount_Of_Cartons_To_Remove)

    def Amount_Of_Cartons(self, instance):
        global taxi
        global List_Of_Cartons_Placed
        global Shipment_Quantity_Cartons
        global Mos_Def
        global Cartons_Placed_Right_Now
        try:
            Cartons_Placed_Right_Now = float(taxi.text)
        except ValueError:
            return POPUP('Alert', 'No Cartons Entered')

        if float(float(List_Of_Cartons_Placed[Mos_Def]) + float(taxi.text)) > float(Shipment_Quantity_Cartons[Mos_Def]):
            # We need to tell user to lower amount of cartons
            POPUP('Error', 'Too Many Cartons\nPlaced, According to\nShipment List Please\nEnsure Its Correct!')
            List_Of_Cartons_Placed[Mos_Def] = float(List_Of_Cartons_Placed[Mos_Def]) + float(taxi.text)
            self.Add_Cartons_To_Virtual_Pallet(Cartons_Placed=Cartons_Placed_Right_Now)
        else:

            List_Of_Cartons_Placed[Mos_Def] = float(List_Of_Cartons_Placed[Mos_Def]) + float(taxi.text)
            self.Add_Cartons_To_Virtual_Pallet(Cartons_Placed=Cartons_Placed_Right_Now)


        self.on_enter()
    def Amount_Of_Cartons_To_Remove(self, instance):
        global taxi
        global List_Of_Cartons_Placed
        global Shipment_Quantity_Cartons
        global Mos_Def
        global Cartons_Placed_Right_Now

        Cartons_Placed_Right_Now = float(taxi.text)

        if float(List_Of_Cartons_Placed[Mos_Def]) - float(taxi.text) < 0:
            # We need to tell user to raise the amount of cartons
            POPUP('Error', 'Too Many Cartons\nRemoved!, Reverting Back!')
            List_Of_Cartons_Placed[Mos_Def] = float(List_Of_Cartons_Placed[Mos_Def])
        else:

            List_Of_Cartons_Placed[Mos_Def] = float(List_Of_Cartons_Placed[Mos_Def]) - float(taxi.text)
            self.Removed_Cartons_To_Virtual_Pallet(Cartons_Placed=Cartons_Placed_Right_Now)


        self.on_enter()

    def Add_Cartons_To_Virtual_Pallet(self, Cartons_Placed, *args):
        global Talib
        global Mos_Def
        global Cartons_Placed_Right_Now
        msg = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10],
               [11], [12], [13], [14], [15], [16], [17], [18], [19], [20],
               [21]]
        msg.append([Talib])
        msg.append([Mos_Def])
        msg.append([Cartons_Placed_Right_Now])
        gsm = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(gsm)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)
    def Removed_Cartons_To_Virtual_Pallet(self, Cartons_Placed, *args):
        global Talib
        global Mos_Def
        global Cartons_Placed_Right_Now
        msg = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10],
               [11], [12], [13], [14], [15], [16], [17], [18], [19], [20],
               [21], [22]]
        msg.append([Talib])
        msg.append([Mos_Def])
        msg.append([Cartons_Placed_Right_Now])
        gsm = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(gsm)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)

    def Mark_Individual_Item_Group_As_Receipted(self, *args):
        global Talib
        global Mos_Def
        global User
        global Shipment_Quantity_Cartons
        try:
            full_stack = Shipment_Quantity_Cartons[Mos_Def]
        except IndexError:
            return POPUP('Error', 'This Is Already Receipted!')
        msg = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10],
               [11], [12], [13], [14], [15], [16], [17], [18], [19], [20],
               [21], [22]]
        msg.append([full_stack])
        msg.append([Talib])
        msg.append([Mos_Def])
        msg.append([User])
        gsm = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(gsm)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)

    def Ye_The_Goat(self, instance):
        print('I Love It Tho, You Know?')

    def Marko_Receipto(self):
        Confirmation_Email('Are These Cartons Receipted', 'Yes', 'Please Confirm', self.Next_Item, self.Ye_The_Goat)

    def Next_Item(self, instance):
        global Mos_Def
        self.Mark_Individual_Item_Group_As_Receipted()
        Mos_Def += 1
        try:
            self.on_entered()
        except IndexError:
            POPUP('Alert', 'Last Item Complete!')

    def Previous_Item(self):
        global Mos_Def
        Mos_Def -= 1
        try:
            self.on_entered()
        except IndexError:
            POPUP('Alert', 'This is the first item!')
    def Are_Ya_Sure_Mate(self):
        Confirmation_Email('Is This Container Ready\nTo Be Put-Away?', 'Yes', 'Please Confirm', self.Mark_As_Ready_To_PutAway, self.Ye_The_Goat)

    def Palletize(self):
        self.getpallet_tag()
        Confirmation_Email('Is The Pallet Filled Up?\nThis Cannot Be Undone', 'Yes', 'Please Confirm', self.Enter_Pallet_Tag_Number, self.Ye_The_Goat)

    def Enter_Pallet_Tag_Number(self, instance):
        global pallet_tag_number
        self.Confirmation_Emailz('Is This The Pallet Number?',str(pallet_tag_number[0]), 'Yes', 'ALERT', self.Pallet_Finished, self.shower)


    def shower(self,instance):
        self.Confirmation('Please Enter Pallet Tag', 'Confirm', 'ALERT', self.Pallet_Finished2)

    def Confirmation_Emailz(self, LabelText, pallet_tag_number, Button1Text, PopupTitle, button1function, btn2function):
        global taxi

        box = BoxLayout(orientation='vertical', padding=(10))
        box.add_widget(Label(text=''))
        box.add_widget(Label(text=LabelText))
        box.add_widget(Label(text=''))
        backstrap = BoxLayout(orientation='horizontal')
        box.add_widget(Label(text=pallet_tag_number))
        backstrap.add_widget(Label(text=''))
        backstrap.add_widget(Label(text=''))
        btn1 = Button(text=Button1Text, background_normal='', background_color=(0, 0.52156863, 0.25098039, 1))
        btn2 = Button(text='No', background_normal='', background_color=(0.89803922, 0.25882353, 0.25882353, 1))
        box.add_widget(backstrap)
        box.add_widget(btn1)
        box.add_widget(Label(text='', size_hint_y=0.9))
        box.add_widget(btn2)
        box.add_widget(Label(text=''))

        # Add Label Inbvetween Buttons to give a bit more room for the fat thumbs

        popup = Popup(title=PopupTitle, title_size=(30),
                      title_align='center', content=box,
                      size_hint=(None, None), size=(600, 600),
                      auto_dismiss=True)

        btn1.bind(on_press=button1function)
        btn1.bind(on_release=popup.dismiss)
        btn2.bind(on_press=btn2function)
        btn2.bind(on_release=popup.dismiss)
        popup.open()
    def Confirmation(self, LabelText, Button1Text, PopupTitle, button1function):
        global taxip

        box = BoxLayout(orientation='vertical', padding=(10))
        box.add_widget(Label(text=''))
        box.add_widget(Label(text=LabelText))
        box.add_widget(Label(text=''))
        backstrap = BoxLayout(orientation='horizontal')
        taxip = TextInput(id='plastic', multiline=False, font_size=40, input_type='number', input_filter='int')
        box.add_widget(taxip)
        btn1 = Button(text=Button1Text, background_normal='', background_color=(0, 0.52156863, 0.25098039, 1))
        box.add_widget(Label(text='', size_hint_y=0.3))
        box.add_widget(backstrap)
        box.add_widget(Label(text='', size_hint_y=0.3))
        box.add_widget(btn1)
        box.add_widget(Label(text=''))

        # Add Label Inbvetween Buttons to give a bit more room for the fat thumbs

        popup = Popup(title=PopupTitle, title_size=(30),
                      title_align='center', content=box,
                      size_hint=(None, None), size=(600, 600),
                      auto_dismiss=True)

        btn1.bind(on_press=button1function)
        btn1.bind(on_release=popup.dismiss)
        popup.open()





    def getpallet_tag(self, *args):
        msg = [1,2,3,4,5,6,7,8,9,10,
               11,12,13,14,15,16,17,18,19,20,
               21,22,23,24,25,26,27,28]
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)

    def Mark_As_Ready_To_PutAway(self, instance,  *args):
        global Talib
        global Mos_Def
        msg = [[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],
               [11],[12],[13],[14],[15],[16],[17],[18],[19],
               [20],[21],[22],[23],[24],[25]]
        msg.append([Talib])
        msg.append([Mos_Def])
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)

    def Pallet_Finished(self, instance):
        # The Pallet is now filled up so i want to get a new one and log that pallet one is complete with x amount of cartons on it
        global Talib
        global User
        global Mos_Def
        global Pallet_Number_Counter
        global Shipment_Pallet_Amounts
        global pallet_tag_number
        global taxip
        Amount_For_Specific_Item = Shipment_Pallet_Amounts[Mos_Def]
        try:
            Amount_For_Specific_Item = Amount_For_Specific_Item[Pallet_Number_Counter]
        except TypeError:
            pass
        if Amount_For_Specific_Item == 0.00:
            return POPUP('Error', "You can't palletize an empty pallet!")
        Roddy_Richh = [[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],
                       [11],[12],[13],[14],[15],[16],[17],[18],[19],[20],
                       [21],[22],[23],[24],[25]]
        Roddy_Richh.append(pallet_tag_number)
        Roddy_Richh.append([User])
        Roddy_Richh.append([Talib])
        Roddy_Richh.append([Mos_Def])
        msg = pickle.dumps(Roddy_Richh, protocol=2)
        self.send_pallet(msg)
    def Pallet_Finished2(self, instance, *args):
        # The Pallet is now filled up so i want to get a new one and log that pallet one is complete with x amount of cartons on it
        global Talib
        global User
        global Mos_Def
        global Pallet_Number_Counter
        global Shipment_Pallet_Amounts
        global pallet_tag_number
        global taxip
        ptem = taxip.text
        ptem = int(ptem)
        Amount_For_Specific_Item = Shipment_Pallet_Amounts[Mos_Def]
        try:
            Amount_For_Specific_Item = Amount_For_Specific_Item[Pallet_Number_Counter]
        except TypeError:
            pass
        if Amount_For_Specific_Item == 0.00:
            return POPUP('Error', "You can't palletize an empty pallet!")
        Roddy_Richh = [[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],
                       [11],[12],[13],[14],[15],[16],[17],[18],[19],[20],
                       [21],[22],[23],[24],[25]]
        Roddy_Richh.append([ptem])
        Roddy_Richh.append([User])
        Roddy_Richh.append([Talib])
        Roddy_Richh.append([Mos_Def])
        msg = pickle.dumps(Roddy_Richh, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)

    def send_pallet(self, msg, *args):
        msg = msg
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)

class Receipting_Error(Screen):


    def connect_to_server(self):
        reactor.connectTCP(HOST, 8000, EchoClientFactory(self))

    def on_connection(self, connection):
        self.print_message("Connected successfully!")
        self.connection = connection

    def on_enter(self, *args):
        global Shipment_Codes
        global Shipment_Quantity_Cartons
        global Individual_Shipment_Status
        global Shipment_Descriptions
        global Shipment_Quantity_Pieces
        global Shipment_Reference_List
        global List_Of_Cartons_Placed
        global Talib
        global Mos_Def
        global Shipment_Pallet_Amounts
        global Pallet_Number_Counter
        global Is_This_The_First_Value
        global POWER
        global Extra
        try:

            self.ids.itemnumberdisplay.text = str(
                'Item Number :  ' + str(Mos_Def + 1) + '/' + str(len(Shipment_Quantity_Cartons)))

            self.ids.refnum.text = Shipment_Reference_List[Talib]

            self.ids.productcode.text = Shipment_Codes[Mos_Def]

            self.ids.qoc.text = str(Shipment_Quantity_Cartons[Mos_Def])
            self.ids.qop.text = str(Shipment_Quantity_Pieces[Mos_Def])
            self.ids.qoc_rec.text = str(List_Of_Cartons_Placed[Mos_Def])
            quantity_of_pieces_placed = float(Shipment_Quantity_Pieces[Mos_Def]) / float(Shipment_Quantity_Cartons[Mos_Def])
            self.ids.qop_rec.text = str(quantity_of_pieces_placed * List_Of_Cartons_Placed[Mos_Def])
            total_cartons_receipted = List_Of_Cartons_Placed[Mos_Def]
            cartons_invoice_number = Shipment_Quantity_Cartons[Mos_Def]
            if total_cartons_receipted > cartons_invoice_number:
                Extra = True
            else:
                Extra = False
            if Extra is True:
                POWER = ('Shipment Number ' + str(Shipment_Reference_List[Mos_Def]) + '\n with product code '
                                        + Shipment_Codes[Mos_Def] + ' and description\n ' + Shipment_Descriptions[Mos_Def] + ' has ' + str(total_cartons_receipted - cartons_invoice_number) + ' Cartons Extra ' )
                self.ids.AutoMessage_Displayer.text = POWER

            if Extra is False:
                POWER = ('Shipment Number ' + str(Shipment_Reference_List[Mos_Def]) + '\n with product code '
                                        + Shipment_Codes[Mos_Def] + ' and description\n ' + Shipment_Descriptions[Mos_Def] + ' has ' + str(
                                        total_cartons_receipted - cartons_invoice_number) + ' Cartons Short ')
                self.ids.AutoMessage_Displayer.text = POWER
        except IndexError as e:
            pass
        self.connect_to_server()
        self.ticker()

    def send_auto_msg(self, *args):
        global POWER
        global Talib
        global Mos_Def
        reday = [[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],
                 [11],[12],[13],[14],[15],[16],[17],[18],[19],[20],
                 [21],[22],[23],[24],[25],[26],[27]]
        reday.append([POWER])
        reday.append([Talib])
        reday.append([Mos_Def])
        msg = pickle.dumps(reday, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            print(e)
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)

    def connecter_to_server(self, instance):
        reactor.connectTCP(HOST, 8000, EchoClientFactory(self))
    def ticker(self, *args):
        msg = ['The College Dropout']
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            print(e)
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)
    def packitman(self, instance):
        print('Hello')
    def print_message(self, msg):
        print(msg)
        global statuslist
        global chops
        if len(msg) == 1:

            statuslist[int(chops)] = 'Not Sent!'
        if len(msg) == 14:
            POPUP('Error', 'Please Try Again')
        if len(msg) == 18:
            pass


class Put_Away_Mode(Screen):


    def connecter_to_server(self, instance):
        reactor.connectTCP(HOST, 8000, EchoClientFactory(self))
    def ticker(self, *args):
        msg = ['The College Dropout']
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)
    def packitman(self, instance):
        pass

    def connect_to_server(self):
        reactor.connectTCP(HOST, 8000, EchoClientFactory(self))

    def on_connection(self, connection):
        self.print_message("Connected successfully!")
        self.connection = connection
    def PutAway_Mode(self, *args):
        global locat
        self.ids.heads.remove_widget(locat)
        global Talib
        global Mos_Def
        msg = [[1],[2],[3],[4],[5]]
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connect_to_server, self.packitman)


    def Send_Tom(self, *args):
        global Tom
        msg = [[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],
               [11],[12],[13],[14],[15],[16],[17],[18],[19],[20],
               [21],[22],[23],[24],[25],[26],[27],[28],[29],[30]]
        msg.append([Tom])
        gsm = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(gsm)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)


    def print_message(self, msg):

        if len(msg) == 1:
            print("Tickback Received")

        if len(msg) == 4:
            global Put_Away_Product_Codes
            global Put_Away_Statuses
            global Put_Away_Pallet_Amounts
            global Put_Away_Pallets_Complete
            Put_Away_Product_Codes = msg[0]
            Put_Away_Statuses = msg[1]
            Put_Away_Pallet_Amounts = msg[2]
            Put_Away_Pallets_Complete = msg[3]
            App.get_running_app().root.current = 'Individual_Put_Away'
        if len(msg) == 2:
            POPUP('Error', 'No Item Selected')
        if len(msg) == 14:
            POPUP('Error', 'Please Try Again')
        if len(msg) == 5:
            global PutAway_Reference_List
            global PutAway_Status_List
            PutAway_Reference_List = msg[3]
            PutAway_Status_List = msg[4]
            global locat
            layout1 = GridLayout(cols=1, spacing=10, padding=[50, 15, 50, 15], row_default_height=150, size_hint_y=None)
            layout1.bind(minimum_height=layout1.setter('height'))
            for count, ref in enumerate(PutAway_Reference_List):
                boxi = BoxLayout(orientation='horizontal', spacing=5, padding=[5, 5, 5, 5])
                if PutAway_Status_List[count] == 'Not Put-Away':
                    btn = Button(text=str(ref), size_hint_x=0.63, background_normal='',
                                 background_color=[0, .4666, 0.70196, 1], font_size=60, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2 = Button(text=str(PutAway_Status_List[count]), size_hint_x=0.37, background_normal='',
                                  background_color=[0.89803922, 0.25882353, 0.25882353, 1], font_size=60, id=str(count))
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    layout1.add_widget(boxi)
                if PutAway_Status_List[count] == 'In Progress':
                    btn = Button(text=str(ref), size_hint_x=0.63, background_normal='',
                                 background_color=[0.96862745, 0.70196078, 0.02745098, 1], font_size=60, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2 = Button(text=str(PutAway_Status_List[count]), size_hint_x=0.37, background_normal='',
                                  background_color=[0.96862745, 0.70196078, 0.02745098, 1], font_size=60, id=str(count))
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    layout1.add_widget(boxi)
                if PutAway_Status_List[count] == 'Not Sent!':
                    btn = Button(text=str(ref), size_hint_x=0.63, background_normal='',
                                 background_color=[0.68235294, 0, 0.72156863, 1], font_size=60, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2 = Button(text=str(PutAway_Status_List[count]), size_hint_x=0.37, background_normal='',
                                  background_color=[0.68235294, 0, 0.72156863, 1], font_size=60, id=str(count))
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    layout1.add_widget(boxi)
                if PutAway_Status_List[count] == 'Put-Away':
                    btn = Button(text=str(ref), size_hint_x=0.63, background_normal='',
                                 background_color=[0, 0.52156863, 0.25098039, 1], font_size=60, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2 = Button(text=str(PutAway_Status_List[count]), size_hint_x=0.37, background_normal='',
                                  background_color=[0, 0.52156863, 0.25098039, 1], font_size=60, id=str(count))
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    layout1.add_widget(boxi)
            locat = ScrollView(scroll_type=['bars'], bar_width='10dp')
            locat.add_widget(layout1)
            self.ids.heads.add_widget(locat)
        if len(msg) == 18:
            self.PutAway_Mode()

    def send(self, instance):
        global Tom
        global PutAway_Reference_List
        Tom = instance.id
        Tom = int(Tom)
        self.Send_Tom()


    def on_enter(self, *args):
        global PutAway_Reference_List
        global PutAway_Status_List
        self.connect_to_server()
        self.ticker()
        global locat
        layout1 = GridLayout(cols=1, spacing=10, padding=[50, 15, 50, 15], row_default_height=150, size_hint_y=None)
        layout1.bind(minimum_height=layout1.setter('height'))
        for count, ref in enumerate(PutAway_Reference_List):
            boxi = BoxLayout(orientation='horizontal', spacing=5, padding=[5, 5, 5, 5])
            if PutAway_Status_List[count] == 'Not Put-Away':
                btn = Button(text=str(ref), size_hint_x=0.63, background_normal='',
                             background_color=[0, .4666, 0.70196, 1], font_size=60, id=str(count))
                btn.bind(on_press=self.send)
                btn2 = Button(text=str(PutAway_Status_List[count]), size_hint_x=0.37, background_normal='',
                              background_color=[0.89803922, 0.25882353, 0.25882353, 1], font_size=60, id=str(count))
                boxi.add_widget(btn)
                boxi.add_widget(btn2)
                layout1.add_widget(boxi)
            if PutAway_Status_List[count] == 'In Progress':
                btn = Button(text=str(ref), size_hint_x=0.63, background_normal='',
                             background_color=[0.96862745, 0.70196078, 0.02745098, 1], font_size=60, id=str(count))
                btn.bind(on_press=self.send)
                btn2 = Button(text=str(PutAway_Status_List[count]), size_hint_x=0.37, background_normal='',
                              background_color=[0.96862745, 0.70196078, 0.02745098, 1], font_size=60, id=str(count))
                boxi.add_widget(btn)
                boxi.add_widget(btn2)
                layout1.add_widget(boxi)
            if PutAway_Status_List[count] == 'Not Sent!':
                btn = Button(text=str(ref), size_hint_x=0.63, background_normal='',
                             background_color=[0.68235294, 0, 0.72156863, 1], font_size=60, id=str(count))
                btn.bind(on_press=self.send)
                btn2 = Button(text=str(PutAway_Status_List[count]), size_hint_x=0.37, background_normal='',
                              background_color=[0.68235294, 0, 0.72156863, 1], font_size=60, id=str(count))
                boxi.add_widget(btn)
                boxi.add_widget(btn2)
                layout1.add_widget(boxi)
            if PutAway_Status_List[count] == 'Put-Away':
                btn = Button(text=str(ref), size_hint_x=0.63, background_normal='',
                             background_color=[0, 0.52156863, 0.25098039, 1], font_size=60, id=str(count))
                btn.bind(on_press=self.send)
                btn2 = Button(text=str(PutAway_Status_List[count]), size_hint_x=0.37, background_normal='',
                              background_color=[0, 0.52156863, 0.25098039, 1], font_size=60, id=str(count))
                boxi.add_widget(btn)
                boxi.add_widget(btn2)
                layout1.add_widget(boxi)
        locat = ScrollView(scroll_type=['bars'], bar_width='10dp')
        locat.add_widget(layout1)
        self.ids.heads.add_widget(locat)
        self.ids.date_displayer.text = str(datetime.now().strftime('%Y-%m-%d'))

    def on_leave(self, *args):
        global locat
        self.ids.heads.remove_widget(locat)

class Individual_Put_Away(Screen):



    def connect_to_server(self):
        reactor.connectTCP(HOST, 8000, EchoClientFactory(self))
    def connecter_to_server(self, instance):
        reactor.connectTCP(HOST, 8000, EchoClientFactory(self))
    def ticker(self, *args):
        msg = ['The College Dropout']
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            print(e)
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)
    def packitman(self, instance):
        pass
    def on_connection(self, connection):
        self.print_message("Connected successfully!")
        self.connection = connection

    def print_message(self, msg):
        print(msg)
        global statuslist
        global chops
        if len(msg) == 1:
            print("Tickback Received")
        if len(msg) == 14:
            POPUP('Error', 'Please Try Again')
        if len(msg) == 10:
            global Product_Codes
            global Descriptions
            global QOP
            global QOC
            global Cartons_Placed
            global Pallet_Amounts
            Product_Codes = msg[4]
            Descriptions = msg[5]
            QOP = msg[6]
            QOC = msg[7]
            Cartons_Placed = msg[8]
            Pallet_Amounts = msg[9]
            App.get_running_app().root.current = 'Put_Away_Item'
        if len(msg) == 4:
            global Put_Away_Product_Codes
            global Put_Away_Statuses
            global Put_Away_Pallet_Amounts
            global Put_Away_Pallets_Complete
            Put_Away_Product_Codes = msg[0]
            Put_Away_Statuses = msg[1]
            Put_Away_Pallet_Amounts = msg[2]
            Put_Away_Pallets_Complete = msg[3]
            global Kanye
            lens_of_pallets = []
            for am in Put_Away_Pallet_Amounts:
                print(am)
                length_of_it = len(am)
                if am == [1,0.0,0]:
                    length_of_it = 1
                lens_of_pallets.append(length_of_it)

            layout1 = GridLayout(cols=1, spacing=10, padding=[50, 15, 50, 15], row_default_height=150, size_hint_y=None)
            layout1.bind(minimum_height=layout1.setter('height'))
            for count, ref in enumerate(Put_Away_Product_Codes):
                boxi = BoxLayout(orientation='horizontal', spacing=5, padding=[5, 5, 5, 5])
                if Put_Away_Statuses[count] == 'In Progress':
                    btn = Button(text=str(ref), background_normal='',
                                 background_color=ORANGE, font_size=30, size_hint_x=0.5, id=str(count))
                    btn2 = Button(text=str(str(Put_Away_Pallets_Complete[count]) + ' / ' + str(lens_of_pallets[count])), size_hint_x=0.35, background_normal='',
                                  background_color=ORANGE, font_size=40, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2.bind(on_press=self.send)
                    btn3 = Button(text=str(Put_Away_Statuses[count]), size_hint_x=0.3, background_normal='',
                                  background_color=ORANGE, id=str(count))
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    boxi.add_widget(btn3)
                    layout1.add_widget(boxi)
                if Put_Away_Statuses[count] == 'Put-Away':
                    btn = Button(text=str(ref), background_normal='',
                                 background_color=GREEN, font_size=30, size_hint_x=0.5, id=str(count))
                    btn2 = Button(text=str(str(Put_Away_Pallets_Complete[count]) + ' / ' + str(lens_of_pallets[count])), size_hint_x=0.35, background_normal='',
                                  background_color=GREEN, font_size=40, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2.bind(on_press=self.send)
                    btn3 = Button(text=str(Put_Away_Statuses[count]), size_hint_x=0.3, background_normal='',
                                  background_color=GREEN, id=str(count))
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    boxi.add_widget(btn3)
                    layout1.add_widget(boxi)
                if Put_Away_Statuses[count] == 'No':
                    btn = Button(text=str(ref), background_normal='',
                                 background_color=DARK_BLUE, font_size=30, size_hint_x=0.5, id=str(count))
                    btn2 = Button(text=str(str(Put_Away_Pallets_Complete[count]) + ' / ' + str(lens_of_pallets[count])), size_hint_x=0.35, background_normal='',
                                  background_color=DARK_BLUE, font_size=40, id=str(count))
                    btn.bind(on_press=self.send)
                    btn2.bind(on_press=self.send)
                    btn3 = Button(text=str(Put_Away_Statuses[count]), size_hint_x=0.3, background_normal='',
                                  background_color=RED, id=str(count))
                    boxi.add_widget(btn)
                    boxi.add_widget(btn2)
                    boxi.add_widget(btn3)
                    layout1.add_widget(boxi)
            Kanye = ScrollView(scroll_type=['bars'], bar_width='10dp')
            Kanye.add_widget(layout1)
            self.ids.JoshManik.add_widget(Kanye)

    def on_enter(self, *args):
        self.connect_to_server()
        self.ticker()
        global Kanye
        global Put_Away_Product_Codes
        global Put_Away_Statuses
        global Put_Away_Pallet_Amounts
        global Put_Away_Pallets_Complete

        lens_of_pallets = []
        for am in Put_Away_Pallet_Amounts:
            print(am)
            length_of_it = len(am)
            if am == [1,0.0,0]:
                length_of_it = 1
            lens_of_pallets.append(length_of_it)

        layout1 = GridLayout(cols=1, spacing=10, padding=[50, 15, 50, 15], row_default_height=150, size_hint_y=None)
        layout1.bind(minimum_height=layout1.setter('height'))
        for count, ref in enumerate(Put_Away_Product_Codes):
            boxi = BoxLayout(orientation='horizontal', spacing=5, padding=[5, 5, 5, 5])
            if Put_Away_Statuses[count] == 'In Progress':
                btn = Button(text=str(ref), background_normal='',
                             background_color=ORANGE, font_size=30, size_hint_x=0.5, id=str(count))
                btn2 = Button(text=str(str(Put_Away_Pallets_Complete[count]) + ' / ' + str(lens_of_pallets[count])),
                              size_hint_x=0.35, background_normal='',
                              background_color=ORANGE, font_size=40, id=str(count))
                btn.bind(on_press=self.send)
                btn2.bind(on_press=self.send)
                btn3 = Button(text=str(Put_Away_Statuses[count]), size_hint_x=0.3, background_normal='',
                              background_color=ORANGE, id=str(count))
                boxi.add_widget(btn)
                boxi.add_widget(btn2)
                boxi.add_widget(btn3)
                layout1.add_widget(boxi)
            if Put_Away_Statuses[count] == 'Put-Away':
                btn = Button(text=str(ref), background_normal='',
                             background_color=GREEN, font_size=30, size_hint_x=0.5, id=str(count))
                btn2 = Button(text=str(str(Put_Away_Pallets_Complete[count]) + ' / ' + str(lens_of_pallets[count])),
                              size_hint_x=0.35, background_normal='',
                              background_color=GREEN, font_size=40, id=str(count))
                btn.bind(on_press=self.send)
                btn2.bind(on_press=self.send)
                btn3 = Button(text=str(Put_Away_Statuses[count]), size_hint_x=0.3, background_normal='',
                              background_color=GREEN, id=str(count))
                boxi.add_widget(btn)
                boxi.add_widget(btn2)
                boxi.add_widget(btn3)
                layout1.add_widget(boxi)
            if Put_Away_Statuses[count] == 'No':
                btn = Button(text=str(ref), background_normal='',
                             background_color=DARK_BLUE, font_size=30, size_hint_x=0.5, id=str(count))
                btn2 = Button(text=str(str(Put_Away_Pallets_Complete[count]) + ' / ' + str(lens_of_pallets[count])),
                              size_hint_x=0.35, background_normal='',
                              background_color=DARK_BLUE, font_size=40, id=str(count))
                btn.bind(on_press=self.send)
                btn2.bind(on_press=self.send)
                btn3 = Button(text=str(Put_Away_Statuses[count]), size_hint_x=0.3, background_normal='',
                              background_color=RED, id=str(count))
                boxi.add_widget(btn)
                boxi.add_widget(btn2)
                boxi.add_widget(btn3)
                layout1.add_widget(boxi)
        Kanye = ScrollView(scroll_type=['bars'], bar_width='10dp')
        Kanye.add_widget(layout1)
        self.ids.JoshManik.add_widget(Kanye)
        self.ids.date_displayer.text = str(datetime.now().strftime('%Y-%m-%d'))

    def on_leave(self, *args):
        global Kanye
        self.ids.JoshManik.remove_widget(Kanye)

    def Send_Tom(self, *args):
        global Kanye
        self.ids.JoshManik.remove_widget(Kanye)
        global Tom
        msg = [[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],
               [11],[12],[13],[14],[15],[16],[17],[18],[19],[20],
               [21],[22],[23],[24],[25],[26],[27],[28],[29],[30]]
        msg.append([Tom])
        gsm = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(gsm)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)

    def send(self, instance):
        global Put_Away_Product_Codes
        global Jerry
        Jerry = instance.id
        Jerry = int(Jerry)
        self.Send_Tom_And_Jerry()

    def Send_Tom_And_Jerry(self):
        global Tom
        global Jerry
        msg = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10],
               [11], [12], [13], [14], [15], [16], [17], [18], [19], [20],
               [21], [22], [23], [24], [25], [26], [27], [28], [29], [30]]
        msg.append([Tom])
        msg.append([Jerry])
        gsm = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(gsm)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)

class Put_Away_Item(Screen):


    def connecter_to_server(self, instance):
        reactor.connectTCP(HOST, 8000, EchoClientFactory(self))
    def ticker(self, *args):
        msg = ['The College Dropout']
        msg = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(msg)
        except AttributeError as e:
            print(e)
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)
    def packitman(self, instance):
        pass

    def connect_to_server(self):
        reactor.connectTCP(HOST, 8000, EchoClientFactory(self))

    def on_connection(self, connection):
        self.print_message("Connected successfully!")
        self.connection = connection

    def on_enter(self, *args):
        global Product_Codes
        global Descriptions
        global QOP
        global QOC
        global Tom
        global Jerry
        global Cartons_Placed
        global Pallet_Amounts
        global Put_Away_Pallet_Amounts
        global Pallet_Number_ID
        global PutAway_Reference_List
        self.ids.refnum.text = str(PutAway_Reference_List[int(Tom)])
        self.connect_to_server()
        self.ticker()
        Pallet_Number_ID = 0
        try:
            Last_Pallet = False
            quantity_of_pieces_placed = float(QOP[Jerry]) / float(QOC[Jerry])
            Tdog = (Put_Away_Pallet_Amounts[Jerry])
            pallet = Tdog[Pallet_Number_ID]
            if Pallet_Number_ID == (len(Tdog)-1):
            #     Need to figure out actual amount backwards now so need a trigger
                Last_Pallet = True
            if Last_Pallet == False:
                p2d2 = Tdog[Pallet_Number_ID+1]
                amzi = p2d2[1]
            Amount = pallet[1]
            paltag = pallet[2]
            ammo = Amount * quantity_of_pieces_placed
            qop_total = Cartons_Placed[Jerry] * quantity_of_pieces_placed
            if Last_Pallet == False:
                Actual_Amount = amzi - Amount

            if Last_Pallet == True:
                p2d2 = Tdog[Pallet_Number_ID-1]
                amzi = p2d2[1]
                Actual_Amount = Amount - amzi

            amzo = Actual_Amount * quantity_of_pieces_placed
            dex = Descriptions[Jerry]
            try:
                T = dex.index('mm')
                a, b = dex[:T + 2], dex[T + 3:]
                p2 = False
            except ValueError:
                try:
                    T = dex.index('MM')
                    a, b = dex[:T + 2], dex[T + 3:]
                    p2 = False
                except ValueError:
                    p2 = True
            if p2 == True:
                self.ids.Description.text = str(dex)
            else:
                self.ids.Description.text = str(a) + '\n' + str(b)
            try:
                self.ids.itemnumberdisplay.text = 'Item Number :' + str(Jerry + 1) + '/' + str(len(Cartons_Placed))
                self.ids.palletnum.text = 'Pallet Number : ' + str(Pallet_Number_ID+1)+ '/' + str(len(Tdog))
                self.ids.ProductCode.text = Product_Codes[Jerry]
                self.ids.Pallet_Tag.text = str(paltag)
                self.ids.QOP_Total.text = str(qop_total)
                self.ids.QOC_Total.text = str(Cartons_Placed[Jerry])
                self.ids.QOP_ONPAL.text = str(amzo)
                self.ids.QOC_ONPAL.text = str(Actual_Amount)
                self.ids.Location.text = ''
            except IndexError:
                pass
        except IndexError:
            POPUP('ALERT', 'Last Pallet Complete')
            self.ids.Location.text = ''
    def fillout(self):
        global Product_Codes
        global Descriptions
        global QOP
        global QOC
        global Tom
        global Jerry
        global Cartons_Placed
        global Pallet_Amounts
        global Put_Away_Pallet_Amounts
        global Pallet_Number_ID
        try:
            Last_Pallet = False
            quantity_of_pieces_placed = float(QOP[Jerry]) / float(QOC[Jerry])
            Tdog = (Put_Away_Pallet_Amounts[Jerry])
            pallet = Tdog[Pallet_Number_ID]
            if Pallet_Number_ID == (len(Tdog)-1):
            #     Need to figure out actual amount backwards now so need a trigger
                Last_Pallet = True
            if Last_Pallet == False:
                p2d2 = Tdog[Pallet_Number_ID+1]
                amzi = p2d2[1]
            Amount = pallet[1]
            paltag = pallet[2]
            ammo = Amount * quantity_of_pieces_placed
            qop_total = Cartons_Placed[Jerry] * quantity_of_pieces_placed
            if Last_Pallet == False:
                Actual_Amount = amzi - Amount

            if Last_Pallet == True:
                p2d2 = Tdog[Pallet_Number_ID-1]
                amzi = p2d2[1]
                Actual_Amount = Amount - amzi

            amzo = Actual_Amount * quantity_of_pieces_placed
            dex = Descriptions[Jerry]
            try:
                T = dex.index('mm')
                a, b = dex[:T + 2], dex[T + 3:]
                p2 = False
            except ValueError:
                try:
                    T = dex.index('MM')
                    a, b = dex[:T + 2], dex[T + 3:]
                    p2 = False
                except ValueError:
                    p2 = True
            if p2 == True:
                self.ids.Description.text = str(dex)
            else:
                self.ids.Description.text = str(a) + '\n' + str(b)
            try:
                self.ids.itemnumberdisplay.text = 'Item Number :' + str(Jerry + 1) + '/' + str(len(Cartons_Placed))
                self.ids.palletnum.text = 'Pallet Number : ' + str(Pallet_Number_ID+1)+ '/' + str(len(Tdog))
                self.ids.ProductCode.text = Product_Codes[Jerry]
                self.ids.Pallet_Tag.text = str(paltag)
                self.ids.QOP_Total.text = str(qop_total)
                self.ids.QOC_Total.text = str(Cartons_Placed[Jerry])
                self.ids.QOP_ONPAL.text = str(amzo)
                self.ids.QOC_ONPAL.text = str(Actual_Amount)
                self.ids.Location.text = ''
            except IndexError:
                pass
        except IndexError:
            POPUP('ALERT', 'Last Pallet Complete')
            self.ids.Location.text = ''
    def fillouta(self):
        global Product_Codes
        global Descriptions
        global QOP
        global QOC
        global Tom
        global Jerry
        global Cartons_Placed
        global Pallet_Amounts
        global Put_Away_Pallet_Amounts
        global Pallet_Number_ID
        try:
            Last_Pallet = False
            quantity_of_pieces_placed = float(QOP[Jerry]) / float(QOC[Jerry])
            Tdog = (Put_Away_Pallet_Amounts[Jerry])
            pallet = Tdog[Pallet_Number_ID]
            if Pallet_Number_ID == (len(Tdog)-1):
            #     Need to figure out actual amount backwards now so need a trigger
                Last_Pallet = True
            if Last_Pallet == False:
                p2d2 = Tdog[Pallet_Number_ID+1]
                amzi = p2d2[1]
            Amount = pallet[1]
            paltag = pallet[2]
            ammo = Amount * quantity_of_pieces_placed
            qop_total = Cartons_Placed[Jerry] * quantity_of_pieces_placed
            if Last_Pallet == False:
                Actual_Amount = amzi - Amount

            if Last_Pallet == True:
                p2d2 = Tdog[Pallet_Number_ID-1]
                amzi = p2d2[1]
                Actual_Amount = Amount - amzi

            amzo = Actual_Amount * quantity_of_pieces_placed
            dex = Descriptions[Jerry]
            try:
                T = dex.index('mm')
                a, b = dex[:T + 2], dex[T + 3:]
                p2 = False
            except ValueError:
                try:
                    T = dex.index('MM')
                    a, b = dex[:T + 2], dex[T + 3:]
                    p2 = False
                except ValueError:
                    p2 = True
            if p2 == True:
                self.ids.Description.text = str(dex)
            else:
                self.ids.Description.text = str(a) + '\n' + str(b)
            try:
                self.ids.itemnumberdisplay.text = 'Item Number :' + str(Jerry + 1) + '/' + str(len(Cartons_Placed))
                self.ids.palletnum.text = 'Pallet Number : ' + str(Pallet_Number_ID+1)+ '/' + str(len(Tdog))
                self.ids.ProductCode.text = Product_Codes[Jerry]
                self.ids.Pallet_Tag.text = str(paltag)
                self.ids.QOP_Total.text = str(qop_total)
                self.ids.QOC_Total.text = str(Cartons_Placed[Jerry])
                self.ids.QOP_ONPAL.text = str(amzo)
                self.ids.QOC_ONPAL.text = str(Actual_Amount)
                self.ids.Location.text = ''
            except IndexError:
                pass
        except IndexError:
            POPUP('ALERT', 'Last Pallet Complete')
            self.ids.Location.text = ''
    def fill(self):
        global Product_Codes
        global Descriptions
        global QOP
        global QOC
        global Tom
        global Jerry
        global Cartons_Placed
        global Pallet_Amounts
        global Put_Away_Pallet_Amounts
        global Pallet_Number_ID
        try:
            Last_Pallet = False
            quantity_of_pieces_placed = float(QOP[Jerry]) / float(QOC[Jerry])
            Tdog = (Put_Away_Pallet_Amounts[Jerry])
            pallet = Tdog[Pallet_Number_ID]
            if Pallet_Number_ID == (len(Tdog)-1):
            #     Need to figure out actual amount backwards now so need a trigger
                Last_Pallet = True
            if Last_Pallet == False:
                p2d2 = Tdog[Pallet_Number_ID+1]
                amzi = p2d2[1]
            Amount = pallet[1]
            paltag = pallet[2]
            ammo = Amount * quantity_of_pieces_placed
            qop_total = Cartons_Placed[Jerry] * quantity_of_pieces_placed
            if Last_Pallet == False:
                Actual_Amount = amzi - Amount

            if Last_Pallet == True:
                p2d2 = Tdog[Pallet_Number_ID-1]
                amzi = p2d2[1]
                Actual_Amount = Amount - amzi

            amzo = Actual_Amount * quantity_of_pieces_placed
            dex = Descriptions[Jerry]
            try:
                T = dex.index('mm')
                a, b = dex[:T + 2], dex[T + 3:]
                p2 = False
            except ValueError:
                try:
                    T = dex.index('MM')
                    a, b = dex[:T + 2], dex[T + 3:]
                    p2 = False
                except ValueError:
                    p2 = True
            if p2 == True:
                self.ids.Description.text = str(dex)
            else:
                self.ids.Description.text = str(a) + '\n' + str(b)
            try:
                self.ids.itemnumberdisplay.text = 'Item Number :' + str(Jerry + 1) + '/' + str(len(Cartons_Placed))
                self.ids.palletnum.text = 'Pallet Number : ' + str(Pallet_Number_ID+1)+ '/' + str(len(Tdog))
                self.ids.ProductCode.text = Product_Codes[Jerry]
                self.ids.Pallet_Tag.text = str(paltag)
                self.ids.Description.text = a +'\n'+ b
                self.ids.QOP_Total.text = str(qop_total)
                self.ids.QOC_Total.text = str(Cartons_Placed[Jerry])
                self.ids.QOP_ONPAL.text = str(amzo)
                self.ids.QOC_ONPAL.text = str(Actual_Amount)
                self.ids.Location.text = ''
            except IndexError:
                pass
        except IndexError:
            pass
    def print_message(self, msg):

    # This is the response for the standard tickback message.

        if len(msg) == 1:
            print("Tickback Received")
        if len(msg) == 2:
            POPUP('Success','Logged Into System!')
        if len(msg) == 14:
            POPUP('Error', 'Please Try Again')
        if len(msg) == 10:
            global Product_Codes
            global Descriptions
            global QOP
            global QOC
            global Cartons_Placed
            global Pallet_Amounts
            Product_Codes = msg[4]
            Descriptions = msg[5]
            QOP = msg[6]
            QOC = msg[7]
            Cartons_Placed = msg[8]
            Pallet_Amounts = msg[9]
            App.get_running_app().root.current = 'Put_Away_Item'
        if len(msg) == 4:
            POPUP('Success','Logged Into System!')
        if len(msg) == 5:
            POPUP('Error','Pallets Not Put Away Yet')
            global Jerry
        if len(msg) == 12:
            POPUP('Success', 'Pallet Created!')
        if len(msg) == 17:
            POPUP('Error', 'Locations Not Entered!')

    def checkers(self):
        global Product_Codes
        global Descriptions
        global QOP
        global QOC
        global Tom
        global Jerry
        global Cartons_Placed
        global Pallet_Amounts
        global Put_Away_Pallet_Amounts
        global Pallet_Number_ID
        Last_Pallet = False
        quantity_of_pieces_placed = float(QOP[Jerry]) / float(QOC[Jerry])
        Tdog = (Put_Away_Pallet_Amounts[Jerry])
        pallet = Tdog[Pallet_Number_ID]
        if Pallet_Number_ID == (len(Tdog)-1):
        #     Need to figure out actual amount backwards now so need a trigger
            Last_Pallet = True
        if Last_Pallet == False:
            p2d2 = Tdog[Pallet_Number_ID+1]
            amzi = p2d2[1]
        Amount = pallet[1]
        paltag = pallet[2]
        ammo = Amount * quantity_of_pieces_placed
        qop_total = Cartons_Placed[Jerry] * quantity_of_pieces_placed
        if Last_Pallet == False:
            Actual_Amount = amzi - Amount

        if Last_Pallet == True:
            p2d2 = Tdog[Pallet_Number_ID-1]
            amzi = p2d2[1]
            Actual_Amount = Amount - amzi

        amzo = Actual_Amount * quantity_of_pieces_placed
        dex = Descriptions[Jerry]
        try:
            T = dex.index('mm')
            a, b = dex[:T + 2], dex[T + 3:]
            p2 = False
        except ValueError:
            try:
                T = dex.index('MM')
                a, b = dex[:T + 2], dex[T + 3:]
                p2 = False
            except ValueError:
                p2 = True
        Confirmation_Email('You are Putting Away\n' + Product_Codes[Jerry] + '\n' + str(Actual_Amount)+ 'Cartons\n'+str(paltag)+' Pallet Tag',
                            'YES', 'Please Confirm', self.nexta_pallet, self.No1youngHOV)

    def mark_container_as_putaway(self, *args):
        global Tom
        global Jerry
        msg = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10],
               [11], [12], [13], [14], [15], [16], [17], [18], [19], [20],
               [21], [22], [23], [24], [25], [26], [27], [28], [29], [30],
               [31], [32], [33]]
        msg.append([Tom])
        msg.append([Jerry])
        gsm = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(gsm)
        except AttributeError as e:
            print(e)
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)
    def Log_Location_Placed(self, *args):
        global Pallet_Number_ID
        global Tom
        global Jerry
        global User
        Location_Placed = self.ids.Location.text
        if Location_Placed == '':
            return POPUP('ALERT', 'Please Enter A Location!')
        msg = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10],
               [11], [12], [13], [14], [15], [16], [17], [18], [19], [20],
               [21], [22], [23], [24], [25], [26], [27], [28]]
        msg.append([User])
        msg.append([Location_Placed])
        msg.append([Pallet_Number_ID])
        msg.append([Tom])
        msg.append([Jerry])
        gsm = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(gsm)
        except AttributeError as e:
            print(e)
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)

    def No1youngHOV(self, instance):
        pass

    def next_pallet(self):
        global Pallet_Number_ID
        Pallet_Number_ID += 1
        self.fillouta()
    def nexta_pallet(self, instance):
        global Pallet_Number_ID
        Location_Placed = self.ids.Location.text
        if Location_Placed == '':
            return POPUP('ALERT', 'Please Enter A Location!')
        self.Log_Location_Placed()
        Pallet_Number_ID += 1
        self.fillouta()
    def prev_pallet(self):
        global Pallet_Number_ID
        Pallet_Number_ID -= 1
        if Pallet_Number_ID < 0:
            Pallet_Number_ID += 1
            self.fillouta()
        else:
            self.fillouta()

    def Item_Complete(self):
        global Jerry
        self.Log_Item_As_Receipted()
        Jerry += 1
        global Pallet_Number_ID
        Pallet_Number_ID = 0

        self.fill()
    def PrevItem_Complete(self):
        global Jerry
        Jerry -= 1
        if Jerry < 0:
            Jerry += 1
        self.fill()

    def Log_Item_As_Receipted(self, *args):
        global Tom
        global Jerry
        msg = [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10],
               [11], [12], [13], [14], [15], [16], [17], [18], [19], [20],
               [21], [22], [23], [24], [25], [26], [27], [28], [29], [30],
               [31], [32]]
        msg.append([Tom])
        msg.append([Jerry])
        gsm = pickle.dumps(msg, protocol=2)
        try:
            if msg and self.connection:
                self.connection.write(gsm)
        except AttributeError as e:
            Confirmation_Email('Please Reconnect', 'Connect', 'ALERT', self.connecter_to_server, self.packitman)

    def update_padding(self, text_input, *args):
        text_width = text_input._get_text_width(
            text_input.text,
            text_input.tab_width,
            text_input._label_cached
        )
        text_input.padding_x = (text_input.width - text_width) / 2

class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super(ScreenManagement, self).__init__(**kwargs)
        self.add_widget(Login_Screen(name='Login_Screen'))
        self.add_widget(Selection_Screen(name='Selection_Screen'))
        self.add_widget(Picking_Mode(name='Picking_Mode'))
        self.add_widget(Individual_Picklist(name='Individual_Picklist'))
        self.add_widget(Individual_Item(name='Individual_Item'))
        self.add_widget(Checking_Mode(name='Checking_Mode'))
        self.add_widget(Individual_Checklist(name='Individual_Checklist'))
        self.add_widget(Individual_Check(name='Individual_Check'))
        self.add_widget(Individual_Check_Error(name='Individual_Check_Error'))
        self.add_widget(Receipting_Mode(name='Receipting_Mode'))
        self.add_widget(Individual_Receipt_List(name='Individual_Receipt_List'))
        self.add_widget(Individual_Receipt(name='Individual_Receipt'))
        self.add_widget(Receipting_Error(name='Receipting_Error'))
        self.add_widget(Put_Away_Mode(name='Put_Away_Mode'))
        self.add_widget(Individual_Put_Away(name='Individual_Put_Away'))
        self.add_widget(Put_Away_Item(name='Put_Away_Item'))


pres = Builder.load_file("main.kv")



class CLIENTApp(App):

    def build(self):
        return pres


class ticker():

    def connect(self):
        reactor.connectTCP(HOST, 8000, EchoClientFactory(self))


    def on_connection(self, connection):
        self.print_message("Connected successfully!")
        self.connection = connection

    def print_message(self, msg):
        print(msg)

    def send(self):
        msg = 'Is there a new ref'
        try:
            if msg and self.connection:
                self.connection.write(msg)
                return True
        except AttributeError as e:
            return False

    def loopdiloop(self):
        while 1:
            print('skeep cuh')
            time.sleep(5)
            self.connect()
            if self.send() is True:
                time.sleep(200)
            else:
                print('fail')
if __name__ == '__main__':
    CLIENTApp().run()


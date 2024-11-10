"""IMPORT all modules here that use in this app."""

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivymd.app import MDApp
from kivymd.uix.bottomsheet import MDGridBottomSheet
from kivymd.uix.button import MDFlatButton
from kivymd.uix.card import MDCard, MDSeparator
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.list import ImageLeftWidget, TwoLineAvatarListItem
from kivymd.uix.screen import MDScreen
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.textfield import MDTextField
from kivy.factory import Factory
from kivymd.uix.button import MDIconButton
from kivymd.uix.list import ILeftBodyTouch
from kivy.uix.screenmanager import Screen
from kivy.properties import BooleanProperty, StringProperty
from kivy.event import EventDispatcher
from kivy.network.urlrequest import UrlRequest
from kivy.lang import Builder
from kivy.factory import Factory
import certifi
from kivymd.toast import toast
from kivymd.uix.button import MDFloatingActionButtonSpeedDial
from kivymd.uix.bottomsheet import MDCustomBottomSheet
from kivymd.uix.picker import MDThemePicker
from kivymd.uix.bottomsheet import MDGridBottomSheet
# from baseclass.ui_class import OneLineTextDialog

#--[End Non UI Imports]
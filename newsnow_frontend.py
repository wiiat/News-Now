import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty, StringProperty, ObjectProperty
from kivy.graphics import Line
from kivy.core.window import Window
from newsnow_backend import WebScraper
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.lang import Builder

kivy.require("1.11.0")
Window.clearcolor = (.54, .84, .89, 1)


class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 60)

    def window_check(self):
        if Window.width / Window.height != 4/3:
            Window.size = (800, 600)

    def update(self, dt):
        self.window_check()


class TopicSelectionPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 60)
        # base window aspect ratio is 4:3
        # base window is 800 x 600 pixels

    blm_button = ObjectProperty(None)
    covid_button = ObjectProperty(None)
    Button.count = 0
    Button.background_down = ""

    def button_collision(self):
        font_instance = Window.width / 14
        buttons = [self.covid_button, self.blm_button]
        for button in buttons:
            if button.collide_point(*Window.mouse_pos):
                animation = Animation(font_size=font_instance + 6, s=1/60, duration=.07)
                button.color = (.96, .60, .61)
                button.outline_width = 3
                button.outline_color = (1, 1, 1)
                if button.count == 0:
                    animation.start(button)
                    button.count += 1
            else:
                button.count = 0
                Animation.cancel_all(button)
                button.color = (1, 1, 1, 1)
                button.font_size = font_instance
                button.outline_width = 0

    def update(self, dt):
        self.button_collision()
        return True


class NewsSelectionPage(Screen):
    pass


class NewsNowApp(App):
    def build(self):
        kv_file = Builder.load_file("newsnow.kv")

        return kv_file


if __name__ == '__main__':
    fullapp = NewsNowApp()
    fullapp.run()

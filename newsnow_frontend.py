import kivy
from kivy.app import App, runTouchApp
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty, StringProperty
from kivy.graphics import Line
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.config import Config
from newsnow_backend import WebScraper
import csv
import webbrowser
from kivy.uix.scrollview import ScrollView
import kivy.modules

kivy.require("1.11.0")
Window.clearcolor = (.54, .84, .89, 1)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # base window aspect ratio is 4:3
        # base window is 800 x 600 pixels
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

    blm_button = ObjectProperty(None)
    covid_button = ObjectProperty(None)

    Button.count = 0
    Button.background_down = ""
    Button.background_normal = ""
    Button.markup = True

    def button_collision(self):
        font_instance = 57
        buttons = [self.covid_button, self.blm_button]
        for button in buttons:
            if button.collide_point(*Window.mouse_pos):
                animation = Animation(font_size=font_instance + 6, s=1/60, duration=.06)
                button.color = (.96, .60, .61)
                if button.count == 0:
                    animation.start(button)
                    button.count += 1
            else:
                button.count = 0
                Animation.cancel_all(button)
                button.color = (1, 1, 1, 1)
                button.font_size = font_instance

    def update(self, dt):
        self.button_collision()


class NewsSelectionPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.update, 1 / 60)

    GridLayout.col_force_default = True
    GridLayout.row_force_default = True

    back_button = ObjectProperty(None)
    fox_button = ObjectProperty(None)
    nypost_button = ObjectProperty(None)
    dailymail_button = ObjectProperty(None)
    newsmax_button = ObjectProperty(None)
    reason_button = ObjectProperty(None)
    wtimes_button = ObjectProperty(None)
    bbc_button = ObjectProperty(None)
    npr_button = ObjectProperty(None)
    usa_button = ObjectProperty(None)
    abc_button = ObjectProperty(None)
    nbc_button = ObjectProperty(None)
    nytimes_button = ObjectProperty(None)
    vox_button = ObjectProperty(None)
    msnbc_button = ObjectProperty(None)
    mjones_button = ObjectProperty(None)
    buttons = [back_button, fox_button, nypost_button, dailymail_button,
               vox_button, msnbc_button, mjones_button, newsmax_button,
               reason_button, wtimes_button, bbc_button, npr_button,
               usa_button, abc_button, nbc_button, nytimes_button]

    def button_collision(self):
        font_instance = 26.7
        alt_fontinstance = 19
        buttons = [self.back_button, self.fox_button, self.nypost_button, self.dailymail_button,
                   self.vox_button, self.msnbc_button, self.mjones_button, self.newsmax_button,
                   self.reason_button, self.wtimes_button, self.bbc_button, self.npr_button,
                   self.usa_button, self.abc_button, self.nbc_button, self.nytimes_button]
        for button in buttons:
            if button.collide_point(*Window.mouse_pos):
                if button == self.back_button:
                    animation = Animation(font_size=font_instance + 6, s=1 / 60, duration=.06)
                    button.background_color = (1, 1, 1, 1)
                    button.color = (.96, .60, .61, 1)
                else:
                    if button == self.wtimes_button:
                        animation = Animation(font_size=alt_fontinstance - 1, s=1 / 60, duration=.04)
                    elif button == self.mjones_button:
                        animation = Animation(font_size=alt_fontinstance + 5, s=1 / 60, duration=.06)
                    else:
                        animation = Animation(font_size=font_instance + 3, s=1 / 60, duration=.06)
                    button.background_color = (.96, .60, .61, 1)
                    button.color = (1, 1, 1, 1)
                if button.count == 0:
                    animation.start(button)
                    button.count += 1
            else:
                button.count = 0
                Animation.cancel_all(button)
                if button == self.back_button:
                    button.color = (1, 1, 1, 1)
                    button.background_color = (.96, .60, .61, 1)
                else:
                    button.color = (.96, .60, .61, 1)
                    button.background_color = (1, 1, 1, 1)
                if button == self.wtimes_button:
                    button.font_size = alt_fontinstance + 2
                elif button == self.mjones_button:
                    button.font_size = alt_fontinstance + 3
                else:
                    button.font_size = font_instance

    def update(self, dt):
        self.button_collision()


class FoxNews(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.articles, 0)
        Clock.schedule_interval(self.update, 1 / 60)

    back_button = ObjectProperty(None)
    menu_button = ObjectProperty(None)
    news_articles = ObjectProperty(None)

    buttons = (back_button, menu_button)
    Label.count = 0

    def button_collision(self):
        font_instance = 26.7
        buttons = [self.back_button, self.menu_button]
        for button in buttons:
            if button.collide_point(*Window.mouse_pos):
                animation = Animation(font_size=font_instance + 6, s=1 / 60, duration=.06)
                button.background_color = (1, 1, 1, 1)
                button.color = (.96, .60, .61, 1)
                if button.count == 0:
                    animation.start(button)
                    button.count += 1
            else:
                button.count = 0
                Animation.cancel_all(button)
                button.color = (1, 1, 1, 1)
                button.background_color = (.96, .60, .61, 1)
                button.font_size = font_instance

    def text_collision(self):
        labels = [i for i in self.news_articles.children]
        for label in labels:
            if len(label.text) > 190:
                font_instance = 25
            else:
                font_instance = 30
            label.size = label.texture_size
            if label.collide_point(*label.to_widget(*Window.mouse_pos)):
                animation = Animation(font_size=font_instance + 1, s=1 / 60, duration=.06)
                label.color = (.96, .60, .61, 1)
                if label.count == 0:
                    animation.start(label)
                    label.count += 1
            else:
                label.count = 0
                Animation.cancel_all(label)
                label.color = (1, 1, 1, 1)
                label.font_size = font_instance

    def openlink(self, instance):
        webbrowser.open(instance, new=2)

    def articles(self, dt):
        titles = self.csv_load()[0]
        links = self.csv_load()[1]
        for lnk, items in zip(links, titles):
            if len(items.strip()) == 0 or len(lnk.strip()) == 0:
                continue
            article_widget = Label(text="[ref={}][b]{}[/b][/ref]".format(lnk, items), markup=True,
                                   font_size=30, halign='left', text_size=(700, None), size_hint_y=None)
            self.news_articles.add_widget(article_widget)
            article_widget.on_ref_press = self.openlink

    def csv_load(self):
        webscrape = WebScraper()
        topic_dict = {'covid': webscrape.covid_words, 'blm': webscrape.blm_words}
        webscrape.keyword_lite(topic_dict[TopicSelectionPage.topic], webscrape.foxnews[0],
                               webscrape.foxnews[1], webscrape.foxnews[3])
        titles = []
        links = []
        with open('foxnews.csv', 'r') as f:
            csv_data = list(csv.reader(f))
            for num in range(len(csv_data)):
                titles.append(csv_data[num][0])
                links.append(csv_data[num][1])
        articles = (titles, links)

        return articles

    def update(self, dt):
        self.button_collision()
        self.text_collision()


class NyPost(Screen):
    pass


class DailyMail(Screen):
    pass


class Newsmax(Screen):
    pass


class Reason(Screen):
    pass


class WashingtonTimes(Screen):
    pass


class BBC(Screen):
    pass


class NPR(Screen):
    pass


class USAToday(Screen):
    pass


class ABC(Screen):
    pass


class NBC(Screen):
    pass


class NyTimes(Screen):
    pass


class MotherJones(Screen):
    pass


class MSNBC(Screen):
    pass


class Vox(Screen):
    pass


class NewsNowApp(App):
    def build(self):
        kv_file = Builder.load_file("newsnowkivy.kv")

        return kv_file


if __name__ == '__main__':
    fullapp = NewsNowApp()
    fullapp.run()

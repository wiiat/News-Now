import kivy
from kivy.app import App, runTouchApp
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
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
from kivy.graphics.vertex_instructions import Rectangle
from kivy.uix.textinput import TextInput
from kivy.graphics import Color
from kivy.uix.popup import Popup
import requests
from requests.exceptions import ConnectionError

kivy.require("1.11.0")
Window.clearcolor = (.68, .87, .94, 1)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


class ScreenManagement(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # base window aspect ratio is 4:3
        # base window is 800 x 600 pixels
        Clock.schedule_interval(self.update, 1 / 60)

    def window_check(self):
        if Window.width / Window.height != 4 / 3:
            Window.size = (800, 600)

    def update(self, dt):
        self.window_check()


class TopicSelectionPage(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.blm_button = Button(background_color=(0, 0, 0, 0), text="[b]Black Lives Matter[/b]", font_size=57)
        self.covid_button = Button(background_color=(0, 0, 0, 0), text="[b]Coronavirus[/b]", font_size=57)
        self.button_keys = {self.blm_button: 'blm', self.covid_button: 'covid'}

        self.search_grid = GridLayout(cols=2, cols_minimum={1: 400}, rows_minimum={0: 50}, spacing=[80, 0],
                                      pos=(200, 50))
        self.search_bar = TextInput(multiline=False, padding=[15, 10], font_size=25, background_normal="",
                                    background_active="", cursor_color=(.96, .60, .61, 1), cursor_width='3sp',
                                    foreground_color=(.96, .60, .61, 1))
        self.search_text = Label(text="[b]Search:[/b]", font_size=35, markup=True)

        Clock.schedule_once(self.update_once, 0)
        Clock.schedule_interval(self.update, 1 / 60)

    base_widget = ObjectProperty(None)
    Button.count = 0
    Button.background_down = ""
    Button.background_normal = ""
    Button.markup = True

    count = ""

    def on_pre_enter(self, *args):
        self.search_bar.text = ""

    def on_enter(self, *args):
        Clock.schedule_once(self.update_alert, 0)

    def update_alert(self, dt):
        scraper = WebScraper()
        if len(self.children) > 1:
            self.remove_widget(self.children[0])
        else:
            pass
        while True:
            try:
                if scraper.update_check() is True:
                    pass
                else:
                    self.add_widget(Label(text="[b]An update is available![/b]", font_size=30, markup=True,
                                          pos=(0, -250), outline_width=2, outline_color=(1, 1, 1, 1),
                                          color=(.96, .60, .61, 1)))
                break
            except requests.exceptions.ConnectionError:
                self.add_widget(Label(text="[b]No internet connection detected!", font_size=30, markup=True,
                                      pos=(0, -250), outline_width=2, outline_color=(1, 1, 1, 1), color=(.96, .60, .61,
                                                                                                         1)))
                break

    @classmethod
    def count_change(cls, a):
        button_keys = {'[b]Black Lives Matter[/b]': 'blm', "[b]Coronavirus[/b]": 'covid'}
        if a.text in button_keys.keys():
            cls.count = cls.button_keys = button_keys[a.text]
        else:
            cls.count = a.text

    def pressed(self, button):
        self.count_change(button)
        self.manager.current = "site"

    def button_collision(self):
        font_instance = 57
        buttons = [self.covid_button, self.blm_button]
        for button in buttons:
            if button.collide_point(*Window.mouse_pos):
                animation = Animation(font_size=font_instance + 6, s=1 / 60, duration=.06)
                button.color = (.96, .60, .61)
                if button.count == 0:
                    animation.start(button)
                    button.count += 1
            else:
                button.count = 0
                Animation.cancel_all(button)
                button.color = (1, 1, 1, 1)
                button.font_size = font_instance

    def update_once(self, dt):
        count = 0

        with self.search_text.canvas.before:
            Color(.96, .60, .61, 1)
            Rectangle(size=(197, 50), pos=(120, 100))

        self.base_widget.add_widget(self.search_grid)
        self.search_grid.add_widget(self.search_text)
        self.search_grid.add_widget(self.search_bar)
        self.search_bar.bind(on_text_validate=self.pressed)

        for bttn in self.button_keys.keys():
            bttn.size = bttn.texture_size
            bttn.pos = (self.base_widget.center_x - (bttn.width / 2), 280 - (85 * count))
            bttn.bind(on_press=self.pressed)
            while True:
                try:
                    self.base_widget.add_widget(bttn)
                    break
                except kivy.uix.widget.WidgetException:
                    self.base_widget.remove_widget(bttn)
                    self.base_widget.add_widget(bttn)
                    break
            count += 1

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


class Sites(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.webscrape_site = ()
        self.site_csv = ''
        self.next = True
        self.prev = True
        Clock.schedule_interval(self.update, 1 / 60)

    back_button = ObjectProperty(None)
    menu_button = ObjectProperty(None)
    refresh_button = ObjectProperty(None)
    news_articles = ObjectProperty(None)
    next_button = ObjectProperty(None)
    previous_button = ObjectProperty(None)

    buttons = (back_button, menu_button)
    Label.count = 0
    no_art = Label(text="[b]No Articles :/[/b]", markup=True, font_size=80)

    def on_pre_enter(self, *args):
        self.news_articles.clear_widgets()

    def on_enter(self):
        self.loading()

    def button_collision(self):
        font_instance = 26.7
        color1 = (1, 1, 1, 1)
        color2 = (.96, .60, .61, 1)
        button_count = 0
        sidebar = [self.menu_button, self.refresh_button]
        buttons = [self.back_button, self.menu_button, self.refresh_button]
        if self.next is False:
            sidebar.append(self.previous_button)
            buttons.append(self.previous_button)
        elif self.prev is False:
            button_count = 1
            sidebar.append(self.next_button)
            buttons.append(self.next_button)
        else:
            control_list = [self.next_button, self.previous_button]
            for i in control_list:
                sidebar.append(i)
                buttons.append(i)

        for button in buttons:
            if button in sidebar:
                color1 = (.96, .60, .61, 1)
                color2 = (1, 1, 1, 1)
                if button_count == 0:
                    if button == self.refresh_button:
                        font_instance = 20
                    elif button == self.previous_button:
                        font_instance = 18.5
                    else:
                        font_instance = 24
                else:
                    if button == self.refresh_button:
                        font_instance = 20
                    else:
                        font_instance = 24

            if button.collide_point(*Window.mouse_pos):
                animation = Animation(font_size=font_instance + 3, s=1 / 60, duration=.06)
                button.background_color = color1
                button.color = color2
                if button.count == 0:
                    animation.start(button)
                    button.count += 1
            else:
                button.count = 0
                Animation.cancel_all(button)
                button.background_color = color2
                button.color = color1
                button.font_size = font_instance

    def text_collision(self):
        labels = [i for i in self.news_articles.children]
        if self.no_art in labels:
            pass
        else:
            for label in labels:
                font_instance = 35
                if label.collide_point(*label.to_widget(*Window.mouse_pos)):
                    animation = Animation(font_size=font_instance + 2, s=1 / 60, duration=.06)
                    label.color = (.96, .60, .61, 1)
                    if label.count == 0:
                        animation.start(label)
                        label.count += 1
                else:
                    label.count = 0
                    Animation.cancel_all(label)
                    label.color = (1, 1, 1, 1)
                    label.font_size = font_instance

    def loading(self):
        self.add_widget(Label(text="[b]Loading...[/b]", markup=True, font_size=60))
        Clock.schedule_once(self.articles, 0)

    def articles(self, dt):
        self.remove_widget(self.children[0])
        titles = self.csv_load()[0]
        links = self.csv_load()[1]
        if len(titles) == 0:
            if self.no_art.parent is None:
                self.news_articles.add_widget(self.no_art)
            else:
                self.no_art.parent.remove_widget(self.no_art)
                self.news_articles.add_widget(self.no_art)
        else:
            for lnk, items in zip(links, titles):
                if len(items) > 90:
                    clipped = items[:90] + "..."
                else:
                    clipped = items
                article_widget = Label(text="[ref={}][b]{}[/b][/ref]".format(lnk, clipped), markup=True,
                                       font_size=35, text_size=(580, None), halign='left', size_hint_y=None,
                                       shorten_from='right')
                article_widget.on_ref_press = self.openlink
                self.news_articles.add_widget(article_widget)

    def openlink(self, instance):
        webbrowser.open(instance, new=2)

    def csv_load(self):
        webscrape = WebScraper()
        topic = TopicSelectionPage()
        topic_dict = {'covid': webscrape.covid_words, 'blm': webscrape.blm_words}
        if topic.count in topic_dict.keys():
            csv_data = webscrape.keyword_lite(topic_dict[topic.count], *self.webscrape_site)
        else:
            csv_data = webscrape.keyword_lite(topic.count.split(" "), *self.webscrape_site)
        titles = []
        links = []
        for num in range(len(csv_data)):
            titles.append(csv_data[num][0])
            links.append(csv_data[num][1])
        articles = (titles, links)

        return articles

    def update(self, dt):
        self.button_collision()
        self.text_collision()


class SiteLayout(Sites):
    site_layout = ObjectProperty(None)


class FoxNews(SiteLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'foxnews'
        self.webscrape_site = (WebScraper.foxnews[0], WebScraper.foxnews[1], WebScraper.foxnews[2])
        self.site_csv = WebScraper.foxnews[0]
        self.prev = False
        Clock.schedule_once(self.layout_override, 0)

    def layout_override(self, dt):
        self.site_layout.children[0].children[5].text = "[b]Fox News[/b]"
        self.site_layout.children[0].remove_widget(self.site_layout.children[0].children[1])
        self.site_layout.children[0].canvas.before.add(Rectangle(pos=(38, 265), size=(120, 190)))


class NyPost(SiteLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'nypost'
        self.webscrape_site = (WebScraper.nypost[0], WebScraper.nypost[1], WebScraper.nypost[2])
        self.site_csv = WebScraper.nypost[0]
        Clock.schedule_once(self.layout_override, 0)

    def layout_override(self, dt):
        self.site_layout.children[0].children[5].text = "[b]New York Post[/b]"
        self.site_layout.children[0].canvas.before.add(Rectangle(pos=(38, 205), size=(120, 250)))


class DailyMail(SiteLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'dailymail'
        self.webscrape_site = (WebScraper.dailymail[0], WebScraper.dailymail[1], WebScraper.dailymail[2])
        self.site_csv = WebScraper.dailymail[0]
        Clock.schedule_once(self.layout_override, 0)

    def layout_override(self, dt):
        self.site_layout.children[0].children[5].text = "[b]Daily Mail[/b]"
        self.site_layout.children[0].canvas.before.add(Rectangle(pos=(38, 205), size=(120, 250)))


class Newsmax(SiteLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'newsmax'
        self.webscrape_site = (WebScraper.newsmax[0], WebScraper.newsmax[1], WebScraper.newsmax[2])
        self.site_csv = WebScraper.newsmax[0]
        Clock.schedule_once(self.layout_override, 0)

    def layout_override(self, dt):
        self.site_layout.children[0].children[5].text = "[b]Newsmax[/b]"
        self.site_layout.children[0].canvas.before.add(Rectangle(pos=(38, 205), size=(120, 250)))


class Reason(SiteLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'reason'
        self.webscrape_site = (WebScraper.reason[0], WebScraper.reason[1], WebScraper.reason[2])
        self.site_csv = WebScraper.reason[0]
        Clock.schedule_once(self.layout_override, 0)

    def layout_override(self, dt):
        self.site_layout.children[0].children[5].text = "[b]Reason[/b]"
        self.site_layout.children[0].canvas.before.add(Rectangle(pos=(38, 205), size=(120, 250)))


class WashingtonTimes(SiteLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'wtimes'
        self.webscrape_site = (WebScraper.wtimes[0], WebScraper.wtimes[1], WebScraper.wtimes[2])
        self.site_csv = WebScraper.wtimes[0]
        Clock.schedule_once(self.layout_override, 0)

    def layout_override(self, dt):
        self.site_layout.children[0].children[5].text = "[b]Washington Times[/b]"
        self.site_layout.children[0].canvas.before.add(Rectangle(pos=(38, 205), size=(120, 250)))


class BBC(SiteLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'bbc'
        self.webscrape_site = (WebScraper.bbc[0], WebScraper.bbc[1], WebScraper.bbc[2])
        self.site_csv = WebScraper.bbc[0]
        Clock.schedule_once(self.layout_override, 0)

    def layout_override(self, dt):
        self.site_layout.children[0].children[5].text = "[b]BBC News[/b]"
        self.site_layout.children[0].canvas.before.add(Rectangle(pos=(38, 205), size=(120, 250)))


class NPR(SiteLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'npr'
        self.webscrape_site = (WebScraper.npr[0], WebScraper.npr[1], WebScraper.npr[2])
        self.site_csv = WebScraper.npr[0]
        Clock.schedule_once(self.layout_override, 0)

    def layout_override(self, dt):
        self.site_layout.children[0].children[5].text = "[b]NPR News[/b]"
        self.site_layout.children[0].canvas.before.add(Rectangle(pos=(38, 205), size=(120, 250)))


class USAToday(SiteLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'usatoday'
        self.webscrape_site = (WebScraper.usatoday[0], WebScraper.usatoday[1], WebScraper.usatoday[2])
        self.site_csv = WebScraper.usatoday[0]
        Clock.schedule_once(self.layout_override, 0)

    def layout_override(self, dt):
        self.site_layout.children[0].children[5].text = "[b]USA Today[/b]"
        self.site_layout.children[0].canvas.before.add(Rectangle(pos=(38, 205), size=(120, 250)))


class ABC(SiteLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'abc'
        self.webscrape_site = (WebScraper.abc[0], WebScraper.abc[1], WebScraper.abc[2])
        self.site_csv = WebScraper.abc[0]
        Clock.schedule_once(self.layout_override, 0)

    def layout_override(self, dt):
        self.site_layout.children[0].children[5].text = "[b]ABC News[/b]"
        self.site_layout.children[0].canvas.before.add(Rectangle(pos=(38, 205), size=(120, 250)))


class NBC(SiteLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'nbc'
        self.webscrape_site = (WebScraper.nbc[0], WebScraper.nbc[1], WebScraper.nbc[2])
        self.site_csv = WebScraper.nbc[0]
        Clock.schedule_once(self.layout_override, 0)

    def layout_override(self, dt):
        self.site_layout.children[0].children[5].text = "[b]NBC News[/b]"
        self.site_layout.children[0].canvas.before.add(Rectangle(pos=(38, 205), size=(120, 250)))


class NyTimes(SiteLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'nytimes'
        self.webscrape_site = (WebScraper.nytimes[0], WebScraper.nytimes[1], WebScraper.nytimes[2])
        self.site_csv = WebScraper.nytimes[0]
        Clock.schedule_once(self.layout_override, 0)

    def layout_override(self, dt):
        self.site_layout.children[0].children[5].text = "[b]New York Times[/b]"
        self.site_layout.children[0].canvas.before.add(Rectangle(pos=(38, 205), size=(120, 250)))


class MotherJones(SiteLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'mjones'
        self.webscrape_site = (WebScraper.mjones[0], WebScraper.mjones[1], WebScraper.mjones[2])
        self.site_csv = WebScraper.mjones[0]
        self.next = False
        Clock.schedule_once(self.layout_override, 0)

    def layout_override(self, dt):
        self.site_layout.children[0].children[5].text = "[b]Mother Jones[/b]"
        self.site_layout.children[0].remove_widget(self.site_layout.children[0].children[2])
        self.site_layout.children[0].canvas.before.add(Rectangle(pos=(38, 205), size=(120, 250)))


class MSNBC(SiteLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'msnbc'
        self.webscrape_site = (WebScraper.msnbc[0], WebScraper.msnbc[1], WebScraper.msnbc[2])
        self.site_csv = WebScraper.msnbc[0]
        Clock.schedule_once(self.layout_override, 0)

    def layout_override(self, dt):
        self.site_layout.children[0].children[5].text = "[b]MSNBC News[/b]"
        self.site_layout.children[0].canvas.before.add(Rectangle(pos=(38, 205), size=(120, 250)))


class Vox(SiteLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = 'vox'
        self.webscrape_site = (WebScraper.vox[0], WebScraper.vox[1], WebScraper.vox[2])
        self.site_csv = WebScraper.vox[0]
        Clock.schedule_once(self.layout_override, 0)

    def layout_override(self, dt):
        self.site_layout.children[0].children[5].text = "[b]Vox News[/b]"
        self.site_layout.children[0].canvas.before.add(Rectangle(pos=(38, 205), size=(120, 250)))


class NewsNowApp(App):
    def build(self):
        self.icon = 'NN-icon.ico'
        kv_file = Builder.load_file("newsnowkivy.kv")

        return kv_file


if __name__ == '__main__':
    fullapp = NewsNowApp()
    fullapp.run()

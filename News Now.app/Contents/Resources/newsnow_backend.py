from bs4 import BeautifulSoup
import requests
import csv


class WebScraper:
    blm_words = ('blm', 'black', 'african american', 'black lives matter', 'slavery', 'racism', 'protests',
                 'protesters', 'racist')
    covid_words = ('coronavirus', 'covid-19', 'pandemic', 'covid')
    stocks = ['stocks', 'stock market']
    trump_words = ('trump')

    foxnews = ('foxnews.csv', 'info', 'https://www.foxnews.com/')
    nypost = ('nypost.csv', 'headline-container', 'https://nypost.com/')
    dailymail = ('dailymail.csv', 'linkro-darkred', 'https://www.dailymail.co.uk/')
    reason = ('reason.csv', 'main', 'https://reason.com/')
    bbc = ('bbc.csv', 'media__content', 'https://www.bbc.com/')
    nytimes = ('nytimes.csv', 'css-15zaaaz eq74mwp0', 'https://www.nytimes.com/')
    newsmax = ('newsmax.csv', 'nmLeftColumn', 'https://www.newsmax.com/')
    wtimes = ('wtimes.csv', 'contained', 'https://www.washingtontimes.com/')
    npr = ('npr.csv', 'story-text', 'https://www.npr.org/')
    usatoday = ('usatoday.csv', 'gnt_cw', 'https://www.usatoday.com/')
    abc = ('abc.csv', 'main-container', 'https://abcnews.go.com/')
    nbc = ('nbc.csv', 'layout-container zone-a-margin lead-type--threeUp', 'https://www.nbcnews.com/')
    mjones = ('mjones.csv', 'grid', 'https://www.motherjones.com//')
    msnbc = ('msnbc.csv', 'layout-container zone-a-margin lead-type--threeUp', 'https://www.msnbc.com/')
    vox = ('vox.csv', 'c-entry-box--compact__body', 'https://www.vox.com/')

    def keyword_lite(self, word_list, file, class1, link):
        special = ('dailymail.csv', 'bbc.csv', 'nytimes.csv', 'newsmax.csv',
                   'wtimes.csv', 'abc.csv')
        special2 = ('newsmax.csv', 'wtimes.csv', 'abc.csv')
        local_link = requests.get(link).text
        soup = BeautifulSoup(local_link, 'lxml')
        if file in special2:
            bowl = soup.find_all(id=class1)
        else:
            bowl = soup.find_all(class_=class1)
        articles = [items.find_all('a') for items in bowl]
        articles2 = [a for i in articles for a in i]
        my_file = open(file, 'w')
        csv_file = csv.writer(my_file)
        article_links = set({})
        for articles in articles2:
            if 'href' not in str(articles):
                continue
            if len(articles['href']) < 5:
                continue
            if '/' not in articles['href']:
                continue
            elif file in special and '.co' not in articles['href']:
                new_articles = link + articles['href']
            elif '//' in articles['href'][:2]:
                new_articles = 'https://' + articles['href'][2:]
            elif 'http' in articles['href'][:6]:
                if 'https' in articles['href'][:5]:
                    new_articles = articles['href']
                else:
                    new_articles = 'https' + articles['href'][4:]
            else:
                continue
            if any(words in articles.text.lower() for words in word_list):
                if len(articles.text) < 3:
                    continue
                elif new_articles in article_links or articles.text in article_links:
                    continue
                elif 'getty images' in articles.text.lower():
                    continue
                else:
                    article_links.add(new_articles)
                    article_links.add(articles.text)
                    csv_file.writerow([articles.text.strip(), new_articles])
            else:
                continue
        my_file.close()

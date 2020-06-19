from bs4 import BeautifulSoup
import requests
import csv
from textblob import TextBlob


class WebScraper:
    blm_words = ('blm', 'black', 'african american', 'black lives matter', 'slavery', 'racism', 'protests',
                 'protesters', 'racist')
    covid_words = ('coronavirus', 'covid-19', 'pandemic', 'covid')
    stocks = ['stocks', 'stock market']
    trump_words = ('trump')

    foxnews = ('foxnews.csv', 'info', 'article-body', 'https://www.foxnews.com/')
    nypost = ('nypost.csv', 'headline-container', 'entry-content entry-content-read-more', 'https://nypost.com/')
    dailymail = ('dailymail.csv', 'linkro-darkred', 'articleBody', 'https://www.dailymail.co.uk/')
    reason = ('reason.csv', 'main', 'entry-content', 'https://reason.com/')
    bbc = ('bbc.csv', 'media__content', 'story-body__inner', 'https://www.bbc.com/')
    nytimes = ('nytimes.csv', 'css-15zaaaz eq74mwp0', 'css-1vxca1d e1qksbhf0', 'https://www.nytimes.com/')
    newsmax = ('newsmax.csv', 'nmLeftColumn', 'mainArticleDiv', 'https://www.newsmax.com/')
    wtimes = ('wtimes.csv', 'contained', 'font-resizer', 'https://www.washingtontimes.com/')
    npr = ('npr.csv', 'story-text', 'storytext storylocation linkLocation', 'https://www.npr.org/')
    usatoday = ('usatoday.csv', 'gnt_cw', 'gnt_ar_b', 'https://www.usatoday.com/')
    abc = ('abc.csv', 'main-container', 'abcnews', 'https://abcnews.go.com/')
    nbc = ('nbc.csv', 'layout-container zone-a-margin lead-type--threeUp',
           'article-body__content', 'https://www.nbcnews.com/')
    mjones = ('mjones.csv', 'grid', 'entry-content', 'https://www.motherjones.com//')
    msnbc = ('msnbc.csv', 'layout-container zone-a-margin lead-type--threeUp',
             'article-body__content', 'https://www.msnbc.com/')
    vox = ('vox.csv', 'c-entry-box--compact__body', 'l-col__main', 'https://www.vox.com/')

    def keyword_search(self, word_list, file, class1, class2, link):
        special = ('dailymail.csv', 'bbc.csv', 'nytimes.csv', 'newsmax.csv', 'wtimes.csv', 'abc.csv')
        special2 = ('newsmax.csv', 'wtimes.csv', 'abc.csv')
        local_link = requests.get(link).text
        soup = BeautifulSoup(local_link, 'lxml')
        if file in special2:
            bowl = soup.find_all(id=class1)
        else:
            bowl = soup.find_all(class_=class1)
        articles = [items.find_all('a') for items in bowl]
        articles2 = [a for i in articles for a in i]
        csv_file = csv.writer(open(file, 'w'))
        csv_file.writerow(['Article', 'Link'])
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
            elif 'https' in articles['href'][:6] or 'http' in articles['href'][:6]:
                new_articles = articles['href']
            else:
                continue
            article_site = requests.get(new_articles).text
            article_soup = BeautifulSoup(article_site, 'lxml')
            if file in special2:
                article_body = article_soup.find(id=class2)
            else:
                article_body = article_soup.find(class_=class2)
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
            elif article_body is None:
                continue
            else:
                article_paragraphs = [p.text for p in article_body.find_all('p')
                                      if any(words in p.text.lower() for words in word_list)]
                if len(article_paragraphs) == 0:
                    continue
                else:
                    if new_articles in article_links or articles.text in article_links:
                        continue
                    else:
                        for p in article_paragraphs:
                            for words in word_list:
                                count = 0
                                if words in p.lower():
                                    count += 1
                                else:
                                    continue
                                if p.lower().count(words) > 1 or count > 2:
                                    if len(articles.text) < 3:
                                        continue
                                    elif 'getty images' in articles.text.lower():
                                        continue
                                    else:
                                        article_links.add(new_articles)
                                        article_links.add(articles.text)
                                        csv_file.writerow([articles.text.strip(), new_articles])
                                else:
                                    continue

    def title_splitter(self, file, class1, class2, link):
        special = ('dailymail.csv', 'bbc.csv', 'nytimes.csv', 'newsmax.csv', 'wtimes.csv', 'abc.csv')
        special2 = ('newsmax.csv', 'wtimes.csv', 'abc.csv')
        local_link = requests.get(link).text
        soup = BeautifulSoup(local_link, 'lxml')
        title = {}
        duplicates = []
        if file in special2:
            bowl = soup.find_all(id=class1)
        else:
            bowl = soup.find_all(class_=class1)
        articles = [items.find_all('a') for items in bowl]
        articles2 = [a for i in articles for a in i]
        for articles in articles2:
            print(articles['href'])
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
            elif 'https' in articles['href'][:6] or 'http' in articles['href'][:6]:
                new_articles = articles['href']
            else:
                continue
            article_site = requests.get(new_articles).text
            article_soup = BeautifulSoup(article_site, 'lxml')
            if file in special2:
                article_body = article_soup.find(id=class2)
            else:
                article_body = article_soup.find(class_=class2)
            if article_body is None:
                continue
            else:
                if new_articles in duplicates:
                    continue
                else:
                    title[tuple(articles.text.lower().strip().split(" "))] = new_articles
                    duplicates.append(new_articles)
        return title

    def stitle_comparer(self, words1, words2):
        comparison = set({})
        count = 0
        if max(len(words2), len(words1)) == words1:
            longest = words1
            shortest = words2
        else:
            longest = words2
            shortest = words1
        blob1 = TextBlob(" ".join(longest)).noun_phrases
        blob2 = TextBlob(" ".join(shortest)).noun_phrases
        for values in blob1:
            comparison.add(values)
        for word in blob2:
            if word in comparison:
                count += 1
            else:
                continue
        if 0 < count < len(blob2):
            return True
        else:
            return False

    def ltitle_comparer(self, x, y):
        csv_file = csv.writer(open('similar_articles.csv', 'w'))
        csv_file.writerow(['Article 1', 'Article 2', 'Link 1', 'Link 2'])
        keys1 = [i for i in x.keys() if i is not None]
        keys2 = [i for i in y.keys() if i is not None]
        for k1 in keys1:
            for k2 in keys2:
                if self.stitle_comparer(k1, k2) is True:
                    csv_file.writerow([' '.join(k1), ' '.join(k2), x[k1], y[k2]])
                else:
                    continue


title = WebScraper()
a = title.title_splitter(title.bbc[0], title.bbc[1], title.bbc[2], title.bbc[3])
b = title.title_splitter(title.abc[0], title.abc[1], title.abc[2], title.abc[3])
title.ltitle_comparer(a, b)

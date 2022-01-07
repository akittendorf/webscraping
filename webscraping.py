# OBJECTIVE: gather book titles, ratings, prices for books in stock at http://books.toscrape.com/ and save as csv
import requests
from bs4 import BeautifulSoup as bs

def getHTML(url): # takes a string url, returns HTML contents as text
    response = requests.get(url)
    html = response.text
    return html

def get_books(html): # takes html string, returns a list of lists
    books = []
    for i in range(1, 51):
        try:
            html = getHTML(f'http://books.toscrape.com/catalogue/page-{i}.html') 
            soup = bs(html, 'html.parser')
            #print(soup.prettify)
            titles = soup.find_all("li", {'class':"col-xs-6 col-sm-4 col-md-3 col-lg-3"})
            for title in titles:
                try:
                # set condition that title is in stock
                    if title.find('p', {'class': 'instock availability'}).text.strip() == 'In stock':
                        # get title, star-rating, and price
                        print(f"{title.h3.a['title']}, {title.p['class'][1]}, {title.find('div', {'class':'product_price'}).p.text[1:]}") 
                        books.append([title.h3.a['title'], title.p['class'][1], title.find('div', {'class':'product_price'}).p.text[1:]])
                except:
                    pass
        except:
            pass
    return books

def make_csv(books): # takes a list and writes to csv
__author__ = 'abhishekjaiswal'

import requests
import bs4
import psycopg2

url = 'http://mobiles.sulekha.com/nokia_mobiles.htm'


def crawl_url(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text)
    #grid-list-space  findAll('div', attrs={'class':'category5'}):

    for div in soup.findAll("div", {"class": "grid-list-space"}):

        #print div
        name = div.find("a", {"class": "text-black"})
        price = div.find(itemprop="price").get_text()
        print name.text.strip()
        print price

        print '-------------------------------------------------------------------------'

    #return [a.attrs.get('href') for a in soup.select('div.grid-list a[href^=/video]')]

crawl_url(url)

try:
    conn = psycopg2.connect("dbname='erpv8' user='openerp' host='localhost' password='mindfire'")
except:
    print "I am unable to connect to the database"

cur = conn.cursor()
#cur.execute("""SELECT datname from pg_database""")
cur.execute("""SELECT * from container_moves""")
rows = cur.fetchall()
print rows
from urllib2 import urlopen
from bs4 import BeautifulSoup as BS
from mechanize import Browser
import MySQLdb

url_input = raw_input("Enter search: ")

br = Browser()

br.set_handle_robots( False )
br.addheaders = [('User-agent', 'Firefox')]
print 'open url'
#open url
br.open("http://www.flipkart.com/")
br.select_form(nr=1)
br.form['q'] = url_input
response = br.submit()
print response,"======================="
print response.geturl()
bs = BS(response.read())
print 'start parsing'

mainlist = []
for i in bs.findAll("div", {"class": "gd-col gu3"}):
    templist = []
    temp_rating = " "
    temp_price = " "
    name = i.find("a", {"class": "fk-display-block"})
    price = i.find("span", {"class": "fk-font-17 fk-bold"})
    rating = i.find("div", {"class": "pu-rating"})
    templink = i.find("a",{"class": "fk-display-block"})
    link = "http://www.flipkart.com" + templink.get('href').strip()    
    img_url = i.find("a", {"class": "pu-image fk-product-thumb "})
    if img_url != None: 
	img_url = img_url.img.get('data-src')
    else:
	 img_url = "NULL"
    for j in str(price.text.strip()):
	if j == " " or j == "R" or j == "s" or j == "," or j == ".":
	    continue
	temp_price = temp_price + j

    if rating != None:
	for i in str(rating.text.strip()):
	    if i == " ":
		break
	    if i == "(":
		continue
	    temp_rating = temp_rating + i
    else:
	temp_rating = "0"

    templist.append(name.text.strip())
    templist.append(temp_price)
    templist.append(temp_rating)
    templist.append(link)
    templist.append(img_url)
    mainlist.append(templist)
    

print 'try'
a = 'NULL'


#sql = "INSERT INTO crawler_data VALUES ("+a+", '0','" + url_input + "', '" + mainlist[2][0] + "' , " + mainlist[2][1]  + ","+ mainlist[2][2] + ", '" + mainlist[2][3] + "' )"
#cursor.execute(sql)
#cursor.execute("INSERT INTO sites VALUES (a, 'stack01', '0')")
#sql = "INSERT INTO sites VALUES(" + a + ", 'stack011', '0')"

def additem(item):
    conn = MySQLdb.connect('localhost', 'root', 'mindfire', 'crawlerdb')
    cursor = conn.cursor()
    for k in item:
        print k
        cursor.execute("INSERT INTO crawler_data VALUES ("+a+", '0', '" + url_input + "', '" + k[0] + "' , " + k[1]  + ","+ k[2] + ", '" + k[3] + "', " + a + ", '" + k[4] + "' )")
    conn.close()

print 'hello'

additem(mainlist)

import requests
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import requests
import urllib,time
import sys
from bs4 import BeautifulSoup
import glob
s = requests.session()
s.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"})
URL = "https://images.search.yahoo.com/search/images;?p="
images = []
pathf= sys.argv[2]+"/"
pathh = pathf+sys.argv[3]+".yahoo."+sys.argv[1]+'*'
print pathh
if not os.path.exists(sys.argv[2]):
	try:
	    os.makedirs(sys.argv[2])
	except OSError as e:
	    pass
elif len(glob.glob(pathh))>0:
    print "Directory exists ... moving on!"
    quit()

def get_images(query, start):
    url=URL+str(sys.argv[1])+"&n=60&b="+str(start)+"60"
    request = s.get(url)
    bs = BeautifulSoup(request.text)
    for img in bs.findAll("li", {"class": "ld "}):
        ss=(img.find('img').attrs['data-src'])
        images.append(ss)

    


for x in range(1, 20):
	get_images(sys.argv[1], x)

print "yahoo: download of "+str(len(images))+" images has started"
for i,y in enumerate(images):
	try:
	    urllib.urlretrieve(y , str(sys.argv[2])+"/"+str(sys.argv[3])+'.yahoo.'+str(sys.argv[1])+'.'+str(i)+".jpg")
	except:
	    pass

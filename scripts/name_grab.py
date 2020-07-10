import requests
from bs4 import BeautifulSoup
from optparse import OptionParser as op
import sys

URL = str(input("Enter the github URL: "))

print("Scraping for file names in: {}".format(URL))

r = requests.get(URL)
soup = BeautifulSoup(r.text, 'html.parser')
container_ = soup.find('div',{'class':"js-details-container Details"})
name_ = container_.find_all('a',{'class':'js-navigation-open link-gray-dark'})
for i in name_:
    print(i.get('title'))

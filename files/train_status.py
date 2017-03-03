import urllib.request
from bs4 import BeautifulSoup 

url = 'http://indiarailinfo.com/train/reftrn?y=0&listID=-1&trainID=955'
#http://indiarailinfo.com/train/reftrn?y=0&trainID=955&trainNumber=12676&listID=-1&kkk=1488532602855

u = urllib.request.urlopen(url)
data = u.read()
soup = BeautifulSoup(data, "html5lib") 
for tag in soup.find_all('a', href=True):     
	print(tag.text)

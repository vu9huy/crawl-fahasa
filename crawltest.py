import requests;
from bs4 import BeautifulSoup;


baseUrl = 'https://www.fahasa.com/sach-trong-nuoc.html?order=num_orders&limit=48&p='

listUrl = []
for i in range(1, 600):
    url = baseUrl + str(i)
    listUrl.append(url)
print(listUrl)
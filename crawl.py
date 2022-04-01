import requests;
from bs4 import BeautifulSoup;
import pymongo;
from pymongo import MongoClient;

client = MongoClient('mongodb://localhost:27017/')
db = client['fahasa']
collection = db['book']

baseUrl = 'https://www.fahasa.com/sach-trong-nuoc.html?order=num_orders&limit=48&p='
# url = 'https://www.fahasa.com/sach-trong-nuoc.html?order=num_orders&limit=48&p=400'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def crawldata(link):
    # soup = BeautifulSoup("<p>Some<b>bad<i>HTML")
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text,'html.parser')
    item = soup.find_all("span", class_="product-image")

    srcImgTags = soup.find_all("img", class_="lazyload")
    nameProductTags = soup.find_all("h2", class_="product-name-no-ellipsis p-name-list")
    linkProductTags = soup.find_all("h2", class_="product-name-no-ellipsis p-name-list")
    priceTags = soup.find_all("p", class_="special-price")


    # START GET LIST srcImg
    srcImgList = []
    for srcImgTag in srcImgTags:
        srcImg = srcImgTag.get('data-src')
        srcImgObj = {'image-url': srcImg}
        srcImgList.append(srcImgObj)
    # END GET LIST srcImg


    # START GET LIST nameProduct
    nameProductList = []
    for nameProductTag in nameProductTags:
        nameProduct = nameProductTag.find("a", recursive=False).get('title')
        nameProductObj = {'name-product': nameProduct}
        nameProductList.append(nameProductObj)
    # END GET LIST nameProduct

    # START GET LIST linkProduct
    linkProductList = []
    for linkProductTag in linkProductTags:
        linkProduct = linkProductTag.find("a", recursive=False).get('href')
        linkProductObj = {'link-product': linkProduct}
        linkProductList.append(linkProductObj)
    # END GET LIST linkProduct

    # START GET LIST priceProduct
    priceList = []
    for priceTag in priceTags:
        price = priceTag.find("span", class_="price").getText()
        priceObj = {'price-product': price}
        priceList.append(priceObj)
    # END GET LIST priceProduct

    # START MERGE ALL LIST TO 1 LIST
    myData = []
    for i in range(len(linkProductList)):
        myObj  = {**srcImgList[i], **nameProductList[i],  **linkProductList[i], **priceList[i]}
        myData.append(myObj)
    print(myData)
    # END MERGE ALL LIST TO 1 LIST
    # START INSERT DATA TO MONGODB
    collection.insert_many(myData)
    # END INSERT DATA TO MONGODB


listUrl = []
for i in range(1, 600):
    url = baseUrl + str(i)
    crawldata(url)
print(listUrl)
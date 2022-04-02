import requests;
from bs4 import BeautifulSoup;
import pymongo;
from pymongo import MongoClient;

client = MongoClient('mongodb://localhost:27017/')
db = client['fahasa']
collection = db['book']



url = 'https://www.fahasa.com/chu-thuat-hoi-chien-tap-1-ban-thuong-tang-kem-obi-va-the-bo-goc-nhua-khong-kem-hop.html'
# url = 'https://www.fahasa.com/active-skills-for-reading-intro-student-book.html'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

def crawlDetailPage(link):
    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.text,'html.parser')

    if response.status_code == 200:
        # GET TAG 'tag'
        item1 = soup.find("li", class_="1")
        if item1:
            tag = item1.find("a" , recursive=False).getText()
        else: tag=''
        # print(tag)

        # GET AUTHOR 'tác giả'
        item2 = soup.find("div", class_="product-view-sa-author")
        authorList = item2.find_all("span" , recursive=False)
        if authorList:
            author = authorList[1].getText()
        else:
            author = ''
        # print(author)

        #  GET SUPLIER 'nhà cung cấp'
        item31 = soup.find_all("div", class_="product-view-sa_one")
        if item31:
            suplierList = item31[0].find("div", class_="product-view-sa-supplier").findChildren()
            suplier = suplierList[1].getText()
        else:
            suplier = ''
        # print(suplier)

        #  GET PUBLISHER 'nhà xuất bản'
        item32 = soup.find_all("div", class_="product-view-sa_two")
        if item32:
            publisherList=item32[0].find("div", class_="product-view-sa-supplier").findChildren()
            publisher = publisherList[1].getText()
        else:
            publisher = ''
        # print(publisher)

        # GET DESCRIPTION 'mô tả'
        item41 = soup.find("div", id="desc_content")
        descList = []
        if item41:
            item4 = item41.find_all("p" , recursive=False)
            for item4Detail in item4:
                if item4Detail:
                    descList.append(item4Detail.getText())
                else:
                    descList = ''
        else: 
            descList = []
            # print(descList)
                
        # GET MORE INFORMATION
        # 'dịch giả'
        item5 = soup.find("td", class_="data_translator")
        if item5:
            translator=item5.getText().strip()
        else:
            translator = ''
        # print(translator)
        # 'năm xuất bản'
        item6 = soup.find("td", class_="data_publish_year")
        if item6:
            publishYear=item6.getText().strip()
        else:
            publishYear = ''
        # print(publishYear)
        # 'trọng lượng'
        item7 = soup.find("td", class_="data_weight")
        if item7:
            weight=item7.getText().strip()
        else:
            weight = ''
        # print(weight)
        # 'kích thước'
        item8 = soup.find("td", class_="data_size")
        if item8:
            size=item8.getText().strip()
        else:
            size = ''
        # print(size)
        # 'số trang'
        item9 = soup.find("td", class_="data_qty_of_page")
        if item9:
            qtyOfPage=item9.getText().strip()
        else:
            qtyOfPage = ''
        # print(qtyOfPage)
        # 'hình thức'
        item10 = soup.find("td", class_="data_book_layout")
        if item10:
            bookLayout=item10.getText().strip()
        else:
            bookLayout = ''
        # print(bookLayout)

        # CREATE OBJECT SAVE DATA GET FROM FAHASA
        objectDB = {
                'tag': tag,
                'tác giả': author,
                'nhà cung cấp': suplier,
                'nhà xuất bản': publisher,
                'mô tả': descList,
                'dịch giả': translator,
                'năm xuất bản': publishYear,
                'trọng lượng': weight,
                'kích thước': size,
                'số trang': qtyOfPage,
                'hình thức': bookLayout
            }
        # print(objectDB)  


        # INSERT DATA TO MONGODB:
        # GET DOCUMENT FROM DATABASE
        collection.update_one({'link-product': link}, {'$set':objectDB})
       


# GET CURSOR FROM DATABASE
cur = collection.find()
# GET URL PRODUCT
for doc in cur:
    url=doc['link-product']
    print(url)
    crawlDetailPage(url)







# response = requests.get(url, headers=headers)
# soup = BeautifulSoup(response.text,'html.parser')

#  # GET TAG 'tag'
# item1 = soup.find("li", class_="1")
# tag = item1.find("a" , recursive=False).getText()
# print(tag)

#  # GET AUTHOR 'tác giả'
# item2 = soup.find("div", class_="product-view-sa-author")
# authorList = item2.find_all("span" , recursive=False)
# if authorList:
#     author = authorList[1].getText()
# else:
#     author = ''
# print(author)

# #  GET SUPLIER 'nhà cung cấp'
# item31 = soup.find_all("div", class_="product-view-sa_one")
# if item31:
#     suplierList = item31[0].find("div", class_="product-view-sa-supplier").findChildren()
#     suplier = suplierList[1].getText()
# else:
#     suplier = ''
# print(suplier)

# #  GET PUBLISHER 'nhà xuất bản'
# item32 = soup.find_all("div", class_="product-view-sa_two")
# if item32:
#     publisherList=item32[0].find("div", class_="product-view-sa-supplier").findChildren()
#     publisher = publisherList[1].getText()
# else:
#     publisher = ''
# print(publisher)

# # GET DESCRIPTION 'mô tả'
# item4 = soup.find("div", id="desc_content").find_all("p" , recursive=False)
# descList = []
# for item4Detail in item4:
#     if item4Detail:
#         descList.append(item4Detail.getText())
#     else:
#         descList = ''
# print(descList)
        
# # GET MORE INFORMATION
# # 'dịch giả'
# item5 = soup.find("td", class_="data_translator")
# if item5:
#     translator=item5.getText().strip()
# else:
#     translator = ''
# print(translator)
# # 'năm xuất bản'
# item6 = soup.find("td", class_="data_publish_year")
# if item6:
#     publishYear=item6.getText().strip()
# else:
#     publishYear = ''
# print(publishYear)
# # 'trọng lượng'
# item7 = soup.find("td", class_="data_weight")
# if item7:
#     weight=item7.getText().strip()
# else:
#     weight = ''
# print(weight)
# # 'kích thước'
# item8 = soup.find("td", class_="data_size")
# if item8:
#     size=item8.getText().strip()
# else:
#     size = ''
# print(size)
# # 'số trang'
# item9 = soup.find("td", class_="data_qty_of_page")
# if item9:
#     qtyOfPage=item9.getText().strip()
# else:
#     qtyOfPage = ''
# print(qtyOfPage)
# # 'hình thức'
# item10 = soup.find("td", class_="data_book_layout")
# if item10:
#     bookLayout=item10.getText().strip()
# else:
#     bookLayout = ''
# print(bookLayout)

# # CREATE OBJECT SAVE DATA GET FROM FAHASA
# objectDB = {
#         'tag': tag,
#         'tác giả': author,
#         'nhà cung cấp': suplier,
#         'nhà xuất bản': publisher,
#         'mô tả': descList,
#         'dịch giả': translator,
#         'năm xuất bản': publishYear,
#         'trọng lượng': weight,
#         'kích thước': size,
#         'số trang': qtyOfPage,
#         'hình thức': bookLayout
#     }
# print(objectDB)   
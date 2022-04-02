
# list1s = [1,2,3,4,5,6,7]
# list2s = ['a','b','c','d','e','f','g']

# myName = []
# myNum = []

# for list1 in list1s:
#     dict1 = {'num': list1}
#     myNum.append(dict1)

# for list2 in list2s:
#     dict2 = {'name': list2}
#     myName.append(dict2)

# myList = []
# for i in range(len(list1s)):
#     myObj  = {**myNum[i], **myName[i]}
#     myList.append(myObj)
# print(myList)
import requests;

url = 'https://www.fahasa.com/than-moc-cao-bat-tan-tap-1-ban-dac-biet-bia-cung.html'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

response = requests.get(url, headers=headers)
print(response.status_code)
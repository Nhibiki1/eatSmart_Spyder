import requests as R
import json

passwd = input("Input Your Password: ")

session = R.post("http://www.weimiaoqu.com/index.php?m=Users&a=checklogin", data={"username":"吃什么EatSmart","password":passwd}).headers["Set-Cookie"].split(";")[0].split("=")[1].strip()

raw_list = R.get("http://www.weimiaoqu.com/index.php?g=User&m=Store&a=orders&token=axdaze1485238944",cookies={"PHPSESSID":session})

text = R.get("http://www.weimiaoqu.com/index.php?g=User&m=Index&a=index",cookies={"PHPSESSID":session}).text
bomb = text.find("bomb_window")

bid = text[text.find("(",bomb):text.find(")",bomb)].split("'")[1]
token = text[text.find("(",bomb):text.find(")",bomb)].split("'")[3]

bombreq = R.get("http://www.weimiaoqu.com/index.php?g=User&m=Index&a=bomb_ajax&id="+bid+"&token="+token,cookies={"PHPSESSID":session})
bombreq = R.get("http://www.weimiaoqu.com/index.php?g=User&m=Function&a=show&id="+bid+"&token="+token,cookies={"PHPSESSID":session})
bombreq = R.get("http://www.weimiaoqu.com/index.php?g=User&m=Store&a=orders&token=axdaze1485238944",cookies={"PHPSESSID":session}).text

bill_list = []
next_item = 0

while (next_item != -1):
    next_item = bombreq.find('"showIntroDetail',next_item+1)
    if (next_item != -1):
        bill_list.append(bombreq[next_item+17:bombreq.find(')',next_item+1)])

items = []
for i in bill_list:
    item = R.get("http://www.weimiaoqu.com/index.php?g=User&m=Store&a=orderInfo&token=axdaze1485238944&dining=0&id=" + i,cookies={"PHPSESSID":session}).text
    it = {}
    for j in item.split("\r\n"):
        if (j[-4:] == "<br>" and "<span" not in j):
            it[j.split("：")[0].strip()] = j.split("：")[1].strip()[0:-4]
    if it != {}:
        items.append(it)

print(items)

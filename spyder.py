import requests as R
import json
import time
import datetime
import re



session = R.post("http://www.weimiaoqu.com/index.php?m=Users&a=checklogin", data={"username":"吃什么EatSmart","password":'weimiaoqu'}).headers["Set-Cookie"].split(";")[0].split("=")[1].strip()

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
dt = []
next_time = 0

while next_item != -1:
    next_item = bombreq.find('"showIntroDetail',next_item+1)
    if next_item != -1:
        bill_list.append(bombreq[next_item+17:bombreq.find(')',next_item+1)])
while next_time != -1:
    next_time = bombreq.find("<td>", next_time+1)
    if next_time != -1 and len(bombreq[next_time+4:bombreq.find('</td>', next_time+1)]) == 19:
        dt.append(bombreq[next_time+4:bombreq.find('</td>', next_time+1)])
items = []
count = 0
for i in bill_list:
    item = R.get("http://www.weimiaoqu.com/index.php?g=User&m=Store&a=orderInfo&token=axdaze1485238944&dining=0&id=" + i,cookies={"PHPSESSID":session}).text
    it = {}
    ip = []
    for j in item.split("\r\n"):

        if j[-5:] == '</td>' and '<br/>' not in j:
            name = j.find('<br>')
            ip.append(j[name+4:-5])
        if j[-4:] == "<br>" and "<span" not in j:
            it[j.split("：")[0].strip()] = j.split("：")[1].strip()[0:-4]
    if it != {}:
        it['valid'] = 1
        it['时间'] = dt[count]
        it['物品'] = ip
        count += 1
        items.append(it)

print(items)
for i in items:
    for k in i:
        print(k, ':', i[k])
    print('------------------------------')

A = '奢华'
B = '亲民'
C = '素食'

list_plan = [[], [], []]
list_dishes = [[], [], []]

for item in items:
        if A in item['物品'] and '-' not in item['物品']:
            list_plan[0].append(item)
        elif B in item['物品'] and '-' not in item['物品']:
            list_plan[1].append(item)
        elif C in item['物品'] and '-' not in item['物品']:
            list_plan[2].append(item)

        elif A in item['物品']:
            list_dishes[0].append(item)
        elif B in item['物品']:
            list_dishes[1].append(item)
        elif C in item['物品']:
            list_dishes[2].append(item)

DURATION = 7

def caltime(date1):
    date1 = time.strptime(date1,"%Y-%m-%d %H:%M:%S")
    date2 = datetime.datetime.now()
    date1 = datetime.datetime(date1[0],date1[1],date1[2],date1[3],date1[4],date1[5])
    return date2-date1


for plan in list_plan:
    for one in plan:
         if caltime(one['时间']).total_seconds() / 86400 > DURATION:
             one['valid'] = 0


invalid_request = []
valid_request = []

dish_base = [[], [], []]


for rank in range(len(list_plan)):
    for mem in list_plan[rank]:
        if len(mem['物品']) != int(mem['总数']):
            for dish in list_dishes:
                if dish['电话'] == mem['电话']:
                    invalid_request.append(dish)
                    break
        else:
            for dish in list_dishes:
                if dish['电话'] == mem['电话']:
                    if dish['物品'] in dish_base[rank]:
                        valid_request.append(dish)
                    else:
                        invalid_request.append(dish)



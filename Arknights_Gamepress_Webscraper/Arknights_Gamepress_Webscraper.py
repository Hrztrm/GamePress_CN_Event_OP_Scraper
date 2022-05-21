import requests
from bs4 import BeautifulSoup
from pathlib import Path

cur_dir = Path(__file__).parent
f = open("Arknights_Data.txt", 'w')
f.seek(0)
f.writelines("Arknights OP Event Data\n")
base_url = "https://gamepress.gg"
source_url = "https://gamepress.gg/arknights/other/cn-event-and-campaign-list"
list_url = []
OP_tq_new = 0
OP_tq_old = 0

def get_cn_event(soup2):
    s = soup2.find_all("tr")
    for line in s:
        if "Not Yet Global" in line.text:
            a = line.find("a")
            event_url = a.get('href')
            full_url = base_url + event_url
            list_url.append(full_url)
            
def Inside_event_pg(soup):
    #Getting the title of the event
    new_p = 0
    OP_quantity = 0
    global OP_tq_new
    global OP_tq_old
    s = soup.find('div', id= 'page-title')
    for line in s:
        if "Episode" in line.text:
            return 0
        if "CN" in line.text:
            f.writelines("\n" + line.text)
    try:
        #Gets the value of OP received from event
        event_div = soup.find_all('div', class_="event-total-summary")[0]
        new_player_content = event_div.find('td', class_="event-totals-text")
        #Check whether it is only for new players or not
        if "New Players" in new_player_content.text:
            new_p = 1
            f.writelines("\nNew Players only")

        #Gets the value of OP
        Object_quantity_w_tag = event_div.find("a")
        Object_href = Object_quantity_w_tag.get('href')
        if "originite-prime" in Object_href:
            OP_quantity_w_tag = event_div.find('div', class_="item-qty")
            OP_quantity = int(OP_quantity_w_tag.text)
            f.writelines("\nOriginal Prime from this event: " + str(OP_quantity) + "\n")
            OP_tq_new = OP_tq_new + OP_quantity
            if new_p != 1:
                OP_tq_old = OP_tq_old + OP_quantity
        else:
            f.writelines("\nEvent does not contain OP\n")
    except:
        f.writelines("\nEvent does not contain OP\n")
        
r = requests.get(source_url)
event_list_pg = BeautifulSoup(r.text, "html.parser")
get_cn_event(event_list_pg)
list_url = list_url[:-2]
for a in list_url:
    r = requests.get(a)
    soup = BeautifulSoup(r.text, "html.parser")
    Inside_event_pg(soup)
f.writelines("\nTotal OP Obtained (New Player): " + str(OP_tq_new))
f.writelines("\nTotal OP Obtained (Old Player): " + str(OP_tq_old))
f.close()
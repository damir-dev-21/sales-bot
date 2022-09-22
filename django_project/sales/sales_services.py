import base64
from unicodedata import name
import requests
from .models import Item

def get_reminds():
    userAndPass = base64.b64encode("Программист:1598753".encode()).decode()
    headers = {'Authorization':'Basic %s' % userAndPass}
    responce = requests.get("http://web.corp.siyob.uz:9696/sklad/hs/mobile/goods/",headers=headers
                               )
    if responce.status_code == 200:
        all_goods =  responce.json()['results']

        for i in all_goods:
            finded_item: Item = Item.objects.filter(uuid_id=i['GUID']).first()
            if finded_item:
                finded_item.name = " ".join(i['Товар'].split())
                finded_item.remind = i['Остаток']
                finded_item.price = i['Цена']
                finded_item.save()
            else:
                new_item: Item = Item(
                    name=i['Товар'],
                    uuid_id=i['GUID'],
                    remind=i['Остаток'],
                    group=i['ВидТовара'],
                    type=i['ТипТовара'],
                    price = i['Цена']
                ) 
                new_item.save()  

        return True         

    return False              


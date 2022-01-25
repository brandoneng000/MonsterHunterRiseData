from ast import Str
import re
from time import sleep
from tokenize import String
import requests
from bs4 import BeautifulSoup
import re

URL = "https://mhrise.kiranico.com/data/monsters/"
large_monsters = {}
monster_parts = []

class MonsterPart:
    def __init__(self, monster_name, part_name, state, sever, impact, ammo, fire, water, ice, thunder, dragon, stun) -> None:
        self.monster_name = monster_name
        self.part_name = part_name
        self.state = state
        self.sever = sever
        self.impact = impact
        self.ammo = ammo
        self.fire = fire
        self.water = water
        self.ice = ice
        self.thunder = thunder
        self.dragon = dragon
        self.stun = stun

    def __str__(self) -> str:
        return f"{self.monster_name},{self.part_name},{self.state},{self.sever},{self.impact},{self.ammo},{self.fire},"\
                 + f"{self.water},{self.ice},{self.thunder},{self.dragon},{self.stun}"
                
        
def main():
    get_kiranico_id()
    
    sleep(1)

    get_parts_data('Rathian')


def get_parts_data(monster_name):
    monster_kiranico_URL = URL + str(large_monsters[monster_name])
    page = requests.get(monster_kiranico_URL)

    soup = BeautifulSoup(page.text, "html.parser")
    data = soup.find_all("tr", class_="bg-white")

    average_HZV = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    number_parts = 0
    
    try:
        for mon in data:
            monster_part = str(mon)
            if 'BreakLevel' in monster_part:
                break

            part_name = re.search('([A-Z])\w+', monster_part)[0]
            HZV = re.findall('> (\d*)<', monster_part)
            print(HZV)
            number_parts += 1
            
            break
            
    except UnicodeEncodeError:
        pass

    

def get_kiranico_id():
    page = requests.get(URL)

    soup = BeautifulSoup(page.text, "html.parser")
    monster_URL_list = soup.find_all("img", class_="mx-auto h-20 w-20 rounded-sm lg:w-24 lg:h-24")

    monster_kiranico_data = [monster_URL.parent.parent for monster_URL in monster_URL_list]

    with open("Large Monster List.txt") as file:
        large_monster_names = file.readlines()
        for large_monster_name in large_monster_names:
            large_monster_name = large_monster_name.strip()
            for monster_URL in monster_kiranico_data:
                if bool(re.search('"' + large_monster_name + '"', str(monster_URL))):
                    kiranico_id = re.search('/(\d*)"', str(monster_URL))[1]
                    large_monsters[large_monster_name] = int(kiranico_id)

    # for mon in large_monsters.items():
    #     print(mon)

if __name__ == '__main__':
    main()
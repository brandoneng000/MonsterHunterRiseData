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

    with open("Large Monster List.txt") as file:
        for name in file:
            monster_name = name.rstrip("\n")
            print(f"Starting {monster_name}")
            get_parts_data(monster_name)
            print(f"Completed {monster_name}")
            sleep(1)

    with open("monster_hzv.csv", 'w') as file:
        for part in monster_parts:
            file.write(str(part) + '\n')


def get_parts_data(monster_name):
    monster_kiranico_URL = URL + str(large_monsters[monster_name])
    page = requests.get(monster_kiranico_URL)

    soup = BeautifulSoup(page.text, "html.parser")
    data = soup.find_all("tr", class_="bg-white")

    average_HZV = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    number_parts = 0
    part_name = ""
    
    try:
        for mon in data:
            monster_part_name = str(mon)
            if 'BreakLevel' in monster_part_name or 'PermitDamageAttr' in monster_part_name:
                break
            
            if 'Bishaten' in monster_name and 'Body' in part_name:
                part_name = 'Foreleg'
            elif 'Somnacanth' in monster_name and 'Leg' in part_name:
                part_name = re.search('([A-Z])\w+ \w+', monster_part_name)[0]
            elif 'Rakna-Kadaki' in monster_name and 'Claw' in part_name:
                part_name = '???'
            elif 'Goss Harag' in monster_name and (('Body' in part_name and int(hit_zone_value[0]) == 1) or '???' in part_name):
                part_name = '???'
            else:
                part_name = re.search('([A-Z])\w+', monster_part_name)[0]
            
            hit_zone_value = re.findall('> (\d*)<', monster_part_name)
            monster_parts.append(MonsterPart(monster_name, part_name, \
                int(hit_zone_value[0]), int(hit_zone_value[1]), int(hit_zone_value[2]), int(hit_zone_value[3]), int(hit_zone_value[4]), \
                int(hit_zone_value[5]), int(hit_zone_value[6]), int(hit_zone_value[7]), int(hit_zone_value[8]), int(hit_zone_value[9])))
            number_parts += 1
            for val in range(10):
                average_HZV[val] += int(hit_zone_value[val])

            if 'Arzuros' in monster_name and 'Abdomen' in part_name:
                break

            if 'Somnacanth' in monster_name and 'Head Fin' in part_name:
                break

            if 'Magnamalo' in monster_name and 'Tailblade' in part_name:
                monster_parts.append(MonsterPart(monster_name, "Wrist ghost", \
                    0, 48, 48, 45, 0, 10, 0, 15, 0, 0))
                monster_parts.append(MonsterPart(monster_name, "Gas pool", \
                    0, 63, 63, 50, 0, 5, 5, 10, 0, 0))
                monster_parts.append(MonsterPart(monster_name, "Face demon fire", \
                    0, 60, 60, 45, 0, 10, 5, 15, 0, 100))
                wrist_ghost = [0, 48, 48, 45, 0, 10, 0, 15, 0, 0]
                gas_pool = [0, 63, 63, 50, 0, 5, 5, 10, 0, 0]
                face_demon_fire = [0, 60, 60, 45, 0, 10, 5, 15, 0, 100]
                average_HZV = list(map(sum, zip(average_HZV, wrist_ghost, gas_pool, face_demon_fire)))
                number_parts += 3
                break

            
    except UnicodeEncodeError:
        pass
    
    
    monster_parts.append(MonsterPart(monster_name, 'Average', \
                int(average_HZV[0])//number_parts, int(average_HZV[1])//number_parts, int(average_HZV[2])//number_parts, int(average_HZV[3])//number_parts, int(average_HZV[4])//number_parts, \
                int(average_HZV[5])//number_parts, int(average_HZV[6])//number_parts, int(average_HZV[7])//number_parts, int(average_HZV[8])//number_parts, int(average_HZV[9])//number_parts))

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
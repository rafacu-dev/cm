import random
import datetime
import string
from os import path

base_url = "http://10.0.2.2:8000/"
#base_url = "https://revoli.herokuapp.com/"

def gson_to_string(string):
    try:
        if string[0] == '"' and string[-1] == '"':
            string = string[1:-1]

            return string
        else: return string

    except:
        return string

def fecha_actual():
    dt_tuple = datetime.datetime.now().timetuple()
    anno = str(dt_tuple.tm_year)
    dia = str(dt_tuple.tm_yday)
    hour = dt_tuple.tm_hour * 60 * 60
    min = dt_tuple.tm_min * 60
    seg = str(hour + min + dt_tuple.tm_sec)

    for _ in range(len(seg),5):
        seg = "0" + seg

    for _ in range(len(dia),3):
        dia = "0" + dia
    fecha_actual = int(anno + dia + seg)
    return fecha_actual

def formateDate(date):
    year = str(date.year)
    month = str(date.month)
    day = "005"#str(date.day)

    hour = date.hour * 60 * 60
    minute = date.minute * 60
    second = str(hour + minute + date.second)

    for _ in range(len(second),5):
        second = "0" + second

    for _ in range(len(day),3):
        day = "0" + day

    return int(year + day + second)

def generate_key(size=500):
    
    valores_admisibles = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','A','B','C',
                'D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','V','W','X','Y','Z',
                'q','r','s','t','u','v','w','x','y','z','1','2','3','4','5','6','7','8','9','0']
    
    key = ''
    
    while len(key) < size:
        letra = ''.join(random.choice(string.ascii_letters + string.digits))
        if letra in valores_admisibles: key += letra
    print(key)
    return key

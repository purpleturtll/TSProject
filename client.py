"""

Nagłówek:
Pole           -> |Pole Operacji|Pole Statusu|Pole Identyfikatora Sesji|  Timestamp  |Arg1 | Arg2 |
Klucz          -> |      OP     |     ST     |           ID            |      TS     | A1  |  A2  |


Operacje:
potęgowanie    -> OP=poteguj$
logarytmowanie -> OP=logarytmuj$
dodawanie      -> OP=dodaj$
odejmowanie    -> OP=odejmij$
mnożenie       -> OP=mnoz$
dzielenie      -> OP=dziel$
historia       -> OP=historia$

"""


import socket
import os
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("192.168.137.1", 8080))
# client.connect(("127.0.0.1", 8080))

client.setblocking(True)

def menu():
    print("OPERACJE:")
    print("1 - POTEGOWANIE")
    print("2 - LOGARYTMOWANIE")
    print("3 - DODAWANIE ")
    print("4 - ODEJMOWANIE")
    print("5 - MNOŻENIE")
    print("6 - DZIELENIE")
    print("7 - PEŁNA HISTORIA")
    print("8 - HISTORIA PO ID")
    print("9 - WYJDŹ")
    print()
    print("WYBIERZ NUMER OPERACJI:", end=" ")


def pods_wykl():
    print("PODAJ PODSTAWĘ:", end=" ")
    a = input()
    print("PODAJ WYKŁADNIK:", end=" ")
    b = input()
    return a, b


def dodaw_odejm():
    print("PODAJ PIERWSZĄ LICZBĘ:", end=" ")
    a = input()
    print("PODAJ DRUGĄ LICZBĘ:", end=" ")
    b = input()
    return a, b


def mnożenie():
    print("PODAJ PIERWSZY CZYNNIK:", end=" ")
    a = input()
    print("PODAJ DRUGI CZYNNIK:", end=" ")
    b = input()
    return a, b


def dzielenie():
    print("PODAJ DZIELNĄ:", end=" ")
    a = input()
    print("PODAJ DZIELNIK:", end=" ")

    while True:
        b = input()
        if(b == '0'):
            print("DZIELNIK NIE MOŻE BYĆ ZEREM")
            print("PODAJ POPRAWNY DZIELNIK:", end=" ")
        else:
            break
    return a, b


def całaHis():
    a, b ="", ""
    return a, b


def HistID():
    print("PODAJ ID: ", end=" ")
    a = input()
    b = ""
    return a, b    



def param(operacja):
  #  os.system('cls')

    if operacja == '1' or operacja == '2':
        return pods_wykl()

    if operacja == '3' or operacja == '4':
        return dodaw_odejm()

    if operacja == '5':
        return mnożenie()

    if operacja == '6':
        return dzielenie()

    if operacja == '7':
        return całaHis()

    if operacja == '8':
        return HistID()



def na_String(operacja):
    if operacja == '1':

        operacja = "poteguj"
    if operacja == '2':
        operacja = "logarytmuj"
    if operacja == '3':
        operacja = "dodaj"
    if operacja == '4':
        operacja = "odejmij"
    if operacja == '5':
        operacja = "mnoz"
    if operacja == '6':
        operacja = "dziel"
    if operacja == '7' or operacja == '8':
        operacja = "historia"

    return operacja


def dane(operacja, a1, a2):
    msg = "OP=" + operacja + "$"
    msg += "ST=" + str(0) + "$"
    msg += "ID=" + SESSION_ID + "$"
    msg += "TS=" + time.asctime(time.localtime(time.time())) + "$"
    msg += "A1=" + a1 + "$"
    msg += "A2=" + a2 + "$"
    return msg

def dzielOdp(res):
    wynik = res[-2][3:]
    return wynik

def historiaOgolna(res):
    data = res[6][3:].split(";")
    for i in range(len(data)):
        data[i] = data[i].split(" ")
    for i in range(len(data)):
        print(str(i+1) + "." + data[i][0])
        print("Argument nr 1: " + data[i][1])
        print("Argument nr 2: " + data[i][2])
        print("Wynik: " + data[i][3])


def historiaID(res):
    res = res.split(" ")
    print("OPERACJA: "+ res[0][3:])
    print("ARGUMENT NR 1: "+ res[1])
    print("ARGUMENT NR 2: "+ res[2])
    print("WYNIK: "+ res[3])


SESSION_ID = client.recv(1024).decode("utf-8")

while True:
    menu()
    operacja = '0'
    while int(operacja) > 9 or int(operacja) < 1:
        operacja = input()
        if int(operacja) > 9 or int(operacja) < 1: 
            print("NIEPOPRAWNY NUMER OPERACJI")
            input()
            os.system('cls')
            menu()
        else:
            break
    if operacja == '9':
        client.close()
        print()
        break
    os.system('cls')
    a, b = param(operacja)
    operacja = na_String(operacja)
    msg = dane(operacja, a, b)
    client.send(msg.encode("utf-8"))
    res = client.recv(1024)
    res = res.decode("utf-8")
    res = res.split("$")
    if res[0][3:] != "historia":
        wynik = dzielOdp(res)
        print("WYNIK = "+ wynik)
    else:
        if(res[4][3:] ==""):
            historiaOgolna(res)
        else:
            historiaID(res[6])
    input()
    os.system('cls')

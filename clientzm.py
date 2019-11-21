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

# client.connect(("192.168.137.1", 8080))
client.connect(("127.0.0.1", 8080))

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
    while True:
        try:
            print("PODAJ PODSTAWĘ:", end=" ")
            a = float(input())
        except ValueError:
            print("PODANA WARTOŚĆ MUSI BYĆ LICZBĄ ZMIENNOPRZECINKOWĄ")
            continue
        else:
            break

    while True:
        try:
            print("PODAJ WYKŁADNIK:", end=" ")
            b = float(input())
        except ValueError:
            print("PODANA WARTOŚĆ MUSI BYĆ LICZBĄ ZMIENNOPRZECINKOWĄ")
            continue
        else:
            break

    a = str(a)
    b = str(b)
    return a, b


def pods_wykl_log():
    while True:
        try:
            print("PODAJ PODSTAWĘ:", end=" ")
            a = float(input())
        except ValueError:
            print("PODANA WARTOŚĆ MUSI BYĆ LICZBĄ ZMIENNOPRZECINKOWĄ")
            continue
        else:
            a = str(a)
            if a == '0.0' or a == '-0.0':
                print("PODSTAWA NIE MOŻE BYĆ ZEREM")
            else:
                break

    while True:
        try:
            print("PODAJ WYKŁADNIK:", end=" ")
            b = float(input())
        except ValueError:
            print("PODANA WARTOŚĆ MUSI BYĆ LICZBĄ ZMIENNOPRZECINKOWĄ")
            continue
        else:
            b = str(b)
            if b == '0.0' or b == '1.0' or b == '-1.0' or b == '-0.0':
                print("WYKŁANDIK NIE MOŻE BYĆ ZEREM ANI JEDYNKĄ")
            else:
                break

    a = str(a)
    b = str(b)

    return a, b


def dodaw_odejm():
    while True:
        try:
            print("PODAJ PIERWSZĄ LICZBĘ:", end=" ")
            a = float(input())
        except ValueError:
            print("PODANA WARTOŚĆ MUSI BYĆ LICZBĄ ZMIENNOPRZECINKOWĄ")
            continue
        else:
            break

    while True:
        try:
            print("PODAJ DRUGĄ LICZBĘ:", end=" ")
            b = float(input())
        except ValueError:
            print("PODANA WARTOŚĆ MUSI BYĆ LICZBĄ ZMIENNOPRZECINKOWĄ")
            continue
        else:
            break

    a = str(a)
    b = str(b)
    return a, b


def mnożenie():
    while True:
        try:
            print("PODAJ PIERWSZY CZYNNIK:", end=" ")
            a = float(input())
        except ValueError:
            print("PODANA WARTOŚĆ MUSI BYĆ LICZBĄ ZMIENNOPRZECINKOWĄ")
            continue
        else:
            break
    while True:
        try:
            print("PODAJ DRUGI CZYNNIK:", end=" ")
            b = float(input())
        except ValueError:
            print("PODANA WARTOŚĆ MUSI BYĆ LICZBĄ ZMIENNOPRZECINKOWĄ")
            continue
        else:
            break

    a = str(a)
    b = str(b)
    return a, b


def dzielenie():
    while True:
        try:
            print("PODAJ DZIELNĄ:", end=" ")
            a = float(input())
        except ValueError:
            print("PODANA WARTOŚĆ MUSI BYĆ LICZBĄ ZMIENNOPRZECINKOWĄ")
            continue
        else:
            break
    while True:
        try:
            print("PODAJ DZIELNIK:", end=" ")
            b = float(input())
        except ValueError:
            print("PODANA WARTOŚĆ MUSI BYĆ LICZBĄ ZMIENNOPRZECINKOWĄ")
            continue
        else:
            b = str(b)
            if b == '0.0' or b == '-0.0':
                print("DZIELNIK NIE MOŻE BYĆ ZEREM")
            else:
                break

    a = str(a)
    b = str(b)
    return a, b


def całaHis():
    a, b = "", ""
    return a, b


def HistID():
    while True:
        try:
            print("PODAJ ID: ", end=" ")
            a = int(input())
        except ValueError:
            print("PODANA WARTOŚĆ TO NIE ID")
            continue
        else:
            break
    a = str(a)
    b = ""
    return a, b


def param(operacja):
    # os.system('cls')
    if operacja == '1':
        return pods_wykl()
    if operacja == '2':
        return pods_wykl_log()
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


def operWBezokoliczniku(res):
    oper = res
    if oper == "poteguj":
        oper = "POTĘGOWANIE"
    if oper == "logarytmuj":
        oper = "LOGARYTMOWANIE"
    if oper == "dodaj":
        oper = "DODAWANIE"
    if oper == "odejmij":
        oper = "ODEJMOWANIE"
    if oper == "mnoz":
        oper = "MNOŻENIE"
    if oper == "dziel":
        oper = "DZIELENIE"
    return oper


def historiaOgolna(res):
    data = res[6][3:].split(";")
    for i in range(len(data)):
        data[i] = data[i].split(" ")
    for i in range(len(data)):
        oper = operWBezokoliczniku(data[i][0])
        print("ID: " + str(i+1))
        print("OPERACJA: " + oper)
        print("ARGUMENT NR 1: " + data[i][1])
        print("ARGUMENT NR 2: " + data[i][2])
        print("WYNIK: " + data[i][3], end="\n\n")


def historiaID(res):
    res = res.split(" ")
    if len(res) > 1:
        oper = operWBezokoliczniku(res[0][3:])
        os.system("cls")
        print("OPERACJA: " + oper)
        print("ARGUMENT NR 1: " + res[1])
        print("ARGUMENT NR 2: " + res[2])
        print("WYNIK: " + res[3])


SESSION_ID = client.recv(1024).decode("utf-8")

while True:
    os.system("cls")
    print("TWOJE ID: ", SESSION_ID, end='\n\n')
    menu()
    operacja = '0'
    while int(operacja) > 9 or int(operacja) < 1:
        operacja = input()
        if operacja == '':
            operacja = '0'
            continue
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
        print("WYNIK = " + wynik)
    else:
        if(res[4][3:] == ""):
            historiaOgolna(res)
        else:
            historiaID(res[6])
    input()
    os.system('cls')

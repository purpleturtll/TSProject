"""

Nagłówek:
Pole           -> |Pole Operacji|Pole Identyfikatora Sesji|  Timestamp  |Arg1 | Arg2 |
Klucz          -> |      OP     |           ID            |      TS     | A1  |  A2  |


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
    print("0 - WYJDŹ")
    print()
    print("WYBIERZ NUMER OPERACJI:", end=" ")


def pods_wykl():
    while True:
        print("PODAJ PODSTAWĘ:", end=" ")
        a = input()
        if a == '':
            continue
        else:
            break
    while True:
        print("PODAJ WYKŁADNIK:", end=" ")
        b = input()
        if b == '':
            continue
        else:
            break
    return a, b


def pods_wykl_log():
    while True:
        print("PODAJ LICZBĘ:", end=" ")
        a = input()
        if a == '':
            continue
        else:
            break
    while True:
        print("PODAJ PODSTAWĘ:", end=" ")
        b = input()
        if b == '':
            continue
        else:
            break
    return a, b


def dodaw_odejm():
    while True:
        print("PODAJ PIERWSZĄ LICZBĘ:", end=" ")
        a = input()
        if a == '':
            continue
        else:
            break
    while True:
        print("PODAJ DRUGĄ LICZBĘ:", end=" ")
        b = input()
        if b == '':
            continue
        else:
            break
    return a, b


def mnożenie():
    while True:
        print("PODAJ PIERWSZY CZYNNIK:", end=" ")
        a = input()
        if a == '':
            continue
        else:
            break
    while True:
        print("PODAJ DRUGI CZYNNIK:", end=" ")
        b = input()
        if b == '':
            continue
        else:
            break
    return a, b


def dzielenie():
    while True:
        print("PODAJ DZIELNĄ:", end=" ")
        a = input()
        if a == '':
            continue
        else:
            break
    while True:
        print("PODAJ DZIELNIK:", end=" ")
        b = input()
        if b == '':
            continue
        else:
            break
    return a, b


def całaHis():
    a, b = "", ""
    return a, b


def HistID():
    while True:
        print("PODAJ ID: ", end=" ")
        a = input()
        if a == '':
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
    msg += "ID=" + SESSION_ID + "$"
    msg += "TS=" + str(time.time()) + "$"
    if a1 != "":
        msg += "A1=" + a1 + "$"
    if a2 != "":
        msg += "A2=" + a2 + "$"
    return msg


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


def historia(data):
    if data[1][3:] == "PUSTA":
        print("\nID: ")
        print("OPERACJA: ")
        print("ARGUMENT NR 1: ")
        print("ARGUMENT NR 2: ")
        print("STATUS: PUSTA")
        print("WYNIK: ")
    else:
        while data[1][3:] != "OK":
            oper = operWBezokoliczniku(data[0][3:])
            print("\nID: " + data[8][3:])
            print("OPERACJA: " + oper)
            print("ARGUMENT NR 1: " + data[4][3:])
            print("ARGUMENT NR 2: " + data[5][3:])
            print("STATUS: " + data[7][3:])
            print("WYNIK: " + data[6][3:], end="\n")
            client.send(("OP=ack$ID=" + SESSION_ID + "$TS=" +
                         str(time.time()) + "$").encode("utf-8"))
            data = client.recv(1024)
            data = data.decode("utf-8").split("$")
        oper = operWBezokoliczniku(data[0][3:])
        print("\nID: " + data[8][3:])
        print("OPERACJA: " + oper)
        print("ARGUMENT NR 1: " + data[4][3:])
        print("ARGUMENT NR 2: " + data[5][3:])
        print("STATUS: " + data[7][3:])
        print("WYNIK: " + data[6][3:], end="\n")


SESSION_ID = client.recv(1024).decode("utf-8").split("$")[2][3:]


def handleOpResult(data):
    print("WYNIK = " + data[3][3:])
    if data[0][3:] != "OK":
        print("STATUS: " + data[0][3:])


while True:
    os.system("cls")
    print("TWOJE ID: ", SESSION_ID, end='\n\n')
    menu()
    operacja = '-1'
    while int(operacja) > 8 or int(operacja) < 0:
        operacja = input()
        if operacja == '':
            operacja = '-1'
            continue
        if int(operacja) > 8 or int(operacja) < 0:
            print("NIEPOPRAWNY NUMER OPERACJI")
            input()
            os.system('cls')
            menu()
        else:
            break
    if operacja == '0':
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
    if len(res) == 5 and res[0][3:] != "historia":
        handleOpResult(res)
    else:
        historia(res)

    input()
    os.system('cls')

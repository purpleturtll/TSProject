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

status = "OK"


def menu():
    """ Funkcja wyświetlająca menu główne"""
    print("OPERACJE:")
    print("1 - POTĘGOWANIE")
    print("2 - LOGARYTMOWANIE")
    print("3 - DODAWANIE")
    print("4 - ODEJMOWANIE")
    print("5 - MNOŻENIE")
    print("6 - DZIELENIE")
    print("7 - PEŁNA HISTORIA")
    print("8 - HISTORIA PO ID")
    print("0 - WYJDŹ")
    print()
    print("WYBIERZ NUMER OPERACJI:", end=" ")


def pods_wykl():
    """ Funkcja przyjmująca od użytkownika dane do operacji potegowania"""
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
    """ Funkcja przyjmująca od użytkownika dane do operacji logarytmowania"""
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
    """ Funkcja przyjmująca od użytkownika dane do wybranej wcześniej operacji - dodawania lub odejmowania """
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
    """ Funkcja przyjmująca od użytkownika dane do operacji mnożenia"""
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
    """ Funkcja przyjmująca od użytkownika dane do operacji dzielenia"""
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
    """Funkcja obsługująca wyświetlanie pełnej historii operacji wykonanych przez danego użytkownika"""
    a, b = "", ""
    return a, b


def HistID():
    """Funkcja wczytująca od użytkownika numer ID operacji, którą chce wyświetlić z historii"""
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
    """ Funkcja wywołująca funkcję operacji, której odpowiada podana w argumencie cyfra """
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
    """ Zamiana danej lliczbowej podanej przez użytkownika na odpowiadającą jej wartość pola OP """
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
    """ Funkcja łącząca dane w gotową do wysłania przez klienta wiadomość """
    msg = "OP=" + operacja + "$"
    msg += "ST=" + status + "$"
    msg += "ID=" + SESSION_ID + "$"
    msg += "TS=" + str(time.time()) + "$"
    if a1 != "":
        msg += "A1=" + a1 + "$"
    if a2 != "":
        msg += "A2=" + a2 + "$"
    return msg


def operWBezokoliczniku(res):
    """ Funkcja zmieniająca dane w zmiennej oper na jej odpowiednik w bezokoliczniku,
    używana podczas wyświetlania historii przez użytkownika"""
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
    """Funkcja obsługująca wyświetlanie historii """
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
            client.send(("OP=history_ack$ST=OK$ID=" + SESSION_ID + "$TS=" +
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


# Odebranie komunikatu z ID sesji które przydzielił serwer
SESSION_ID = client.recv(1024).decode("utf-8").split("$")[2][3:]


def handleOpResult(data):
    """Funkcja wyświetlająca wynik operacji przesłany przez serwer oraz jej status"""
    print("WYNIK = " + data[4][3:])
    if data[1][3:] != "OK":
        print("STATUS: " + data[1][3:])


# Główna pętla do komunikacja z serwerem
while True:
    os.system("cls")
    print("TWOJE ID: ", SESSION_ID, end='\n\n')
    menu()
    operacja = '-1'
    # Pętla wyboru operacji przez klienta
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
        # Zamknięcie połączenia
        client.close()
        print()
        break
    os.system('cls')
    # Wczytanie parametrów dla wybranej operacji
    a, b = param(operacja)
    operacja = na_String(operacja)
    # Przygotowanie komuninkatu do wysłania
    msg = dane(operacja, a, b)
    # Zakodowanie znaków w formacie UTF-8 i przesłanie go do serwera
    client.send(msg.encode("utf-8"))
    # Odebranie komunikatu z serwera
    res = client.recv(1024)
    # Dekodowanie komunikatu
    res = res.decode("utf-8")
    # Podzielenie odebranego komunikatu na tablicę w której każdy element jest jednym polem
    res = res.split("$")
    if len(res) == 6 and res[0][3:] != "historia":
        # Wypisanie wyniku operacji
        handleOpResult(res)
    else:
        # Wypisanie historii jeśli operacją jest historia
        historia(res)

    input()
    os.system('cls')

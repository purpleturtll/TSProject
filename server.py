"""

Nagłówek:
Pole           -> |Pole Operacji|Pole Statusu|Pole Identyfikatora Sesji|  Timestamp  |Arg1 | Arg2 | Wynik |
Klucz          -> |      OP     |     ST     |           ID            |      TS     | A1  |  A2  |   WY  |


Operacje:
potęgowanie    -> OP=poteguj$
logarytmowanie -> OP=logarytmuj$
dodawanie      -> OP=dodaj$
odejmowanie    -> OP=odejmij$
mnożenie       -> OP=mnoz$
dzielenie      -> OP=dziel$
historia       -> OP=historia$

"""

import socketserver
import math
import time
import threading
import os
from decimal import Decimal

# HOST, PORT = "192.168.137.1", 8080
HOST, PORT = "127.0.0.1", 8080
SOCKETS = {}
OPERATIONS = {}
SESSION_ID = 1
OPERATION_ID = 1


def operWBezokoliczniku(res):
    """Funkcja zamieniająca operację na formę bezokolicznika.
    Używana przy wyświetlaniu."""
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


class Operation:
    """Klasa reprezentująca rekord w historii operacji"""

    def __init__(self, id, data, result, status):
        self.query = data
        self.result = result
        self.status = status
        self.id = id
        global OPERATION_ID
        self.server_id = OPERATION_ID
        OPERATION_ID += 1

    def pretty(self):
        """Funkcja która wypisuje informacje o zapisanej operacji"""
        print("ID_SERVER: " + str(self.server_id))
        print("ID_USER: " + str(self.id))
        print("OPERACJA: " + operWBezokoliczniku(str(self.query[0][3:])))
        print("STATUS: " + self.status)
        print("ARGUMENT NR 1: " + str(self.query[4][3:]))
        print("ARGUMENT NR 2: " + str(self.query[5][3:]))
        print("WYNIK: " + str(self.result), end="\n\n")

    def __str__(self):
        x = self.query[0][3:] + " " + self.query[4][3:] + \
            " " + self.query[5][3:] + " " + self.result + \
            " " + self.status + " " + str(self.id)
        return x


class Handler(socketserver.BaseRequestHandler):
    """Klasa do obsługi połączenia na gnieździe
    Tworzona jest jedna instancja dla każdego przychodzącego połączenia"""

    def __init__(self, request, client_address, server):
        self.request = request
        self.client_address = client_address
        self.server = server
        self.status = "OK"
        self.setup()
        try:
            self.handle()
        finally:
            self.finish()

    def potegowanie(self, x1, x2):
        """Funkcja obsługująca operację potęgowania"""
        try:
            x1 = float(x1)
            x2 = float(x2)
        except ValueError:
            self.status = "NIE_LICZBA"
            return "ERR"
        else:
            if x1 > 9223372036854775807 or x1 < -9223372036854775807:
                self.status = "ZAKRES"
                return "ERR"
            elif x2 > 10000 or x2 < -10000:
                self.status = "ZAKRES"
                return "ERR"
            else:
                return (Decimal(x1) ** Decimal(x2)).__str__()
        return

    def logarytmowanie(self, x1, x2):
        """Funkcja obsługująca operację logarytmowania"""
        try:
            x1 = float(x1)
            x2 = float(x2)
        except ValueError:
            self.status = "NIE_LICZBA"
            return "ERR"
        else:
            if x1 == 0 or x1 == -0:
                self.status = "LOG_0"
                return "ERR"
            elif x2 == 0 or x2 == -0 or x2 == 1 or x2 == -1:
                self.status = "LOG_PODSTAWA"
                return "ERR"
            else:
                return math.log(float(x1), float(x2))
        return

    def dodawanie(self, x1, x2):
        """Funkcja obsługująca operację dodawania"""
        try:
            x1 = float(x1)
            x2 = float(x2)
        except ValueError:
            self.status = "NIE_LICZBA"
            return "ERR"
        else:
            return x1 + x2
        return

    def odejmowanie(self, x1, x2):
        """Funkcja obsługująca operację odejmowania"""
        try:
            x1 = float(x1)
            x2 = float(x2)
        except ValueError:
            self.status = "NIE_LICZBA"
            return "ERR"
        else:
            return x1 - x2
        return

    def mnozenie(self, x1, x2):
        """Funkcja obsługująca operację mnożenia"""
        try:
            x1 = float(x1)
            x2 = float(x2)
        except ValueError:
            self.status = "NIE_LICZBA"
            return "ERR"
        else:
            return x1 * x2
        return

    def dzielenie(self, x1, x2):
        """Funkcja obsługująca operację dzielenia"""
        try:
            x1 = float(x1)
            x2 = float(x2)
        except ValueError:
            self.status = "NIE_LICZBA"
            return "ERR"
        else:
            if x2 == 0 or x2 == -0:
                self.status = "DZIEL_PRZEZ_0"
                return "ERR"
            else:
                return x1 / x2
        return

    def historia(self, data):
        """Funkcja obsługująca wysyłanie historii"""
        if len(data) == 5:
            # Historia po ID sesji
            if len(OPERATIONS[SOCKETS[self.request][0]]) == 0:
                # Jeśli historia jest pusta wyślij o tym informację do klienta
                self.request.send(("OP=historia$ST=PUSTA$ID=" + str(SOCKETS[self.request][0]) + "$TS=" +
                                   str(time.time()) + "$").encode("utf-8"))
            for i in range(len(OPERATIONS[SOCKETS[self.request][0]])):
                if i < len(OPERATIONS[SOCKETS[self.request][0]]) - 1:
                    # Wysyłaj kolejne rekordy historii ze statusem HIST
                    self.status = "HIST"
                    op = str(OPERATIONS[SOCKETS[self.request][0]].get(
                        i + 1)).split(" ")
                    self.request.send(
                        bytes(self.dane(op[0], op[1], op[2], op[3], op[4], op[5]), "utf-8"))
                    # Czekaj na potwierdzenie od klienta
                    self.request.recv(1024)
                else:
                    # Wyślij ostatni rekord historii ze statusem OK
                    # ,żeby klient wiedział kiedy zakończyć odbieranie rekordów
                    self.status = "OK"
                    op = str(OPERATIONS[SOCKETS[self.request][0]].get(
                        i + 1)).split(" ")
                    self.request.send(
                        bytes(self.dane(op[0], op[1], op[2], op[3], op[4], op[5]), "utf-8"))
        else:
            # Historia po ID operacji
            if int(data[4][3:]) in OPERATIONS[SOCKETS[self.request][0]].keys():
                # Jeśli ID operacji z zapytania klienta znajduje się w tablicy operacji na serwerze
                self.status = "OK"
                # Zamień instancje obiektu Operation na wartości oddzielone spacją
                op = str(OPERATIONS[SOCKETS[self.request][0]]
                         [int(data[4][3:])]).split(" ")
                # Prześlij odpowiednio przygotowany komunikat z rekordem historii
                self.request.send(
                    bytes(self.dane(op[0], op[1], op[2], op[3], op[4], op[5]), "utf-8"))
            else:
                # Wyślij informacje o braku rekordu o podanym ID w historii
                self.request.send(("OP=historia$ST=PUSTA$ID=" + str(SOCKETS[self.request][0]) + "$TS=" +
                                   str(time.time()) + "$").encode("utf-8"))

    def dane(self, operacja, a1, a2, result, status="", id=0):
        """Funkcja przygotowująca komunikat do wysłania"""
        msg = ""
        msg += "OP=" + operacja + "$"
        msg += "ST=" + self.status + "$"
        msg += "ID=" + str(SOCKETS[self.request][0]) + "$"
        msg += "TS=" + str(time.time()) + "$"
        if status != "":
            msg += "A1=" + a1 + "$"
            msg += "A2=" + a2 + "$"
        if result is not None:
            msg += "WY=" + result + "$"
        if status != "":
            msg += "OS=" + status + "$"
            msg += "OI=" + id + "$"
        return msg

    def handle(self):
        """Funkcja obsługująca połączenie"""
        global SOCKETS, SESSION_ID, OPERATIONS
        SOCKETS[self.request] = [SESSION_ID, 1]
        OPERATIONS[SOCKETS[self.request][0]] = {}
        SESSION_ID += 1

        # Wysłanie ID sesji do klienta
        self.request.send(("OP=id$ST=OK$ID=" + str(SOCKETS[self.request][0]) + "$TS=" +
                           str(time.time()) + "$").encode("utf-8"))

        # Główna pętla obsługi połączenia
        while(True):
            # Oczekiwanie na komunikat od klienta
            data = self.request.recv(1024)
            if not data:
                break

            # Dekodowanie i podzielenie komunikatu na pola
            data = data.decode("utf-8")
            data = data.split("$")

            # Sprawdzenie zgodności ID sesji z komunikatu z gniazdem
            if data[2][3:] != str(SOCKETS[self.request][0]):
                self.status = "ZLA_SESJA"
            else:
                self.status = "OK"

            # Wywołanie odpowiedniej funkcji na podstawie zawartości pola OP
            if data[0][3:] == "poteguj":
                result = str(self.potegowanie(data[4][3:], data[5][3:]))
            if data[0][3:] == "logarytmuj":
                result = str(self.logarytmowanie(data[4][3:], data[5][3:]))
            if data[0][3:] == "dodaj":
                result = str(self.dodawanie(data[4][3:], data[5][3:]))
            if data[0][3:] == "odejmij":
                result = str(self.odejmowanie(data[4][3:], data[5][3:]))
            if data[0][3:] == "mnoz":
                result = str(self.mnozenie(data[4][3:], data[5][3:]))
            if data[0][3:] == "dziel":
                result = str(self.dzielenie(data[4][3:], data[5][3:]))

            if data[0][3:] == "historia":
                # Odesłanie do klienta żądanej historii
                self.historia(data)
            else:
                # Dodanie operacji matematycznej do historii
                OPERATIONS[SOCKETS[self.request][0]][SOCKETS[self.request][1]] = Operation(SOCKETS[self.request][1],
                                                                                           data, result, self.status)
                SOCKETS[self.request][1] += 1
                # Odesłanie wyniku operacji matematycznej
                self.request.send(
                    bytes(self.dane(data[0][3:], data[4][3:], data[5][3:], result), "utf-8"))


class MyTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """Klasa pozwalająca na uruchomienie serwera na oddzielnym wątku"""
    pass


server = MyTCPServer((HOST, PORT), Handler)

with server:
    # Uruchomienie serwera
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    # Pętla dla interfejsu po stronie serwera
    while True:
        os.system("cls")
        print("0. WYJDŹ")
        print("1. PEŁNA HISTORIA")
        print("2. HISTORIA PO ID SESJI")
        print("3. HISTORIA PO ID OPERACJI")
        choice = input()
        os.system("cls")
        if choice == "0":
            break
        if choice == "1":
            # Wyświetlenie historii wszystkich operacji wykonanych na serwerze
            for id, operacje in OPERATIONS.items():
                for n, operacja in operacje.items():
                    operacja.pretty()
                    print()
        if choice == "2":
            # Wyświetlenie historii wszystkich operacji dla danego ID sesji
            print("PODAJ ID SESJI: ", end="")
            sess_id = input()
            try:
                sess_id = int(sess_id)
            except ValueError:
                continue

            for id, operacje in OPERATIONS.items():
                if id == sess_id:
                    for n, operacja in operacje.items():
                        operacja.pretty()
                        print()
        if choice == "3":
            # Wyświetlenie historii danej operacji
            print("PODAJ ID OPERACJI: ", end="")
            op_id = input()
            try:
                op_id = int(op_id)
            except ValueError:
                continue
            for i in range(len(OPERATIONS)):
                for n, operacja in OPERATIONS[i + 1].items():
                    if operacja.server_id == op_id:
                        operacja.pretty()
                        print()
        input()

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

SOCKETS = {}
OPERATIONS = {}
SESSION_ID = 1
OPERATION_ID = 1


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


class Operation:
    def __init__(self, id, data, result):
        self.query = data
        self.result = result
        self.id = id
        global OPERATION_ID
        self.server_id = OPERATION_ID
        OPERATION_ID += 1

    def pretty(self):
        print("ID_SERVER: " + str(self.server_id))
        print("ID_USER: " + str(self.id))
        print("OPERACJA: " + operWBezokoliczniku(str(self.query[0][3:])))
        print("ARGUMENT NR 1: " + str(self.query[4][3:]))
        print("ARGUMENT NR 2: " + str(self.query[5][3:]))
        print("WYNIK: " + str(self.result), end="\n\n")

    def __str__(self):
        return self.query[0][3:] + " " + self.query[4][3:] + " " + self.query[5][3:] + " " + self.result


class Handler(socketserver.BaseRequestHandler):

    def potegowanie(self, x1, x2):
        return pow(float(x1), float(x2))

    def logarytmowanie(self, x1, x2):
        return math.log(float(x1), float(x2))

    def dodawanie(self, x1, x2):
        return float(x1)+float(x2)

    def odejmowanie(self, x1, x2):
        return float(x1)-float(x2)

    def mnozenie(self, x1, x2):
        return float(x1)*float(x2)

    def dzielenie(self, x1, x2):
        return float(x1)/float(x2)

    def historia(self, x1):
        # print(OPERATIONS[SOCKETS[self.request][0]])
        if x1 != "":
            if int(x1) in OPERATIONS[SOCKETS[self.request][0]].keys():
                return str(OPERATIONS[SOCKETS[self.request][0]][int(x1)])
            else:
                return ""
        else:
            o = []
            for k, v in OPERATIONS[SOCKETS[self.request][0]].items():
                o.append(str(v))
            return str(";".join(o))

    def dane(self, operacja, a1, a2, result, status):
        msg = "OP=" + operacja + "$"
        msg += "ST=" + str(status) + "$"
        msg += "ID=" + str(SOCKETS[self.request][0]) + "$"
        msg += "TS=" + time.asctime(time.localtime(time.time())) + "$"
        msg += "A1=" + a1 + "$"
        msg += "A2=" + a2 + "$"
        msg += "WY=" + result + "$"
        return msg

    def handle(self):
        global SOCKETS, SESSION_ID, OPERATIONS
        SOCKETS[self.request] = [SESSION_ID, 1]
        OPERATIONS[SOCKETS[self.request][0]] = {}
        SESSION_ID += 1
        self.request.send(bytes(str(SOCKETS[self.request][0]), "utf-8"))
        while(True):
            data = self.request.recv(1024)
            if not data:
                break
            data = data.decode("utf-8")
            data = data.split("$")
            # print(data)

            if data[2][3:] != str(SOCKETS[self.request][0]):
                status = 1
            else:
                status = 0

            if status == 0:
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
                    result = str(self.historia(data[4][3:]))
                else:
                    OPERATIONS[SOCKETS[self.request][0]][SOCKETS[self.request][1]] = Operation(SOCKETS[self.request][1],
                                                                                               data, result)
                    SOCKETS[self.request][1] += 1
            else:
                result = ""
            self.request.send(
                bytes(self.dane(data[0][3:], data[4][3:], data[5][3:], result, status), "utf-8"))


class MyTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


# HOST, PORT = "192.168.137.1", 8080
HOST, PORT = "127.0.0.1", 8080

server = MyTCPServer((HOST, PORT), Handler)

# server.serve_forever()

with server:
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    while True:
        os.system("cls")
        print("0. WYJDZ")
        print("1. PEŁNA HISTORIA")
        print("2. HISTORIA PO ID SESJI")
        print("3. HISTORIA PO ID OPERACJI")
        choice = input()
        os.system("cls")
        if choice == "0":
            break
        if choice == "1":
            for id, operacje in OPERATIONS.items():
                for n, operacja in operacje.items():
                    operacja.pretty()
                    print()
        if choice == "2":
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

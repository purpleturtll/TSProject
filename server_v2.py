"""

Nagłówek:
Pole           -> |Pole Operacji|Pole Statusu|Pole Identyfikatora Sesji|  Timestamp  |Arg1 | Arg2 | 
Klucz          -> |      OP     |     ST     |           ID            |      TS     | A1  |  A2  |
Rozmiar(bajt)  -> |      14     |      4     |            4            |       8     |  4  |   4  |


Operacje:
potęgowanie    -> OP=poteguj$
logarytmowanie -> OP=logarytmuj$
dodawanie      -> OP=dodaj$
odejmowanie    -> OP=odejmij$
mnożenie       -> OP=mnoz$
dzielenie      -> OP=dziel$

"""

import socketserver
import math

SOCKETS = {}
OPERATIONS = {}
SESSION_ID = 1
OPERATION_ID = 1


class Operation:
    def __init__(self, data, result):
        global OPERATION_ID
        self.query = data
        self.resule = result
        self.operation_id = OPERATION_ID
        OPERATION_ID += 1

    def __str__(self):
        return self.query[0][3:] + " " + self.query[1][3:] + " " + self.query[2][3:]


class Handler(socketserver.StreamRequestHandler):

    def potegowanie(self, x1, x2):
        return pow(int(x1), int(x2))

    def logarytmowanie(self, x1, x2):
        return math.log(int(x2), int(x1))

    def dodawanie(self, x1, x2):
        return int(x1)+int(x2)

    def odejmowanie(self, x1, x2):
        return int(x1)-int(x2)

    def mnozenie(self, x1, x2):
        return int(x1)*int(x2)

    def dzielenie(self, x1, x2):
        return int(x1)/int(x2)

    def handle(self):
        global SOCKETS, SESSION_ID, OPERATIONS
        SOCKETS[self.request] = SESSION_ID
        OPERATIONS[SOCKETS[self.request]] = []
        SESSION_ID += 1
        while(True):
            data = self.request.recv(1024)
            if not data:
                break
            data = data.decode("utf-8")
            data = data.split("$")
            print(data)
            if data[0][3:] == "poteguj":
                result = str(self.potegowanie(data[1][3:], data[2][3:]))
                self.request.send(bytes(result, "utf-8"))
            if data[0][3:] == "logarytmuj":
                result = str(self.logarytmowanie(data[1][3:], data[2][3:]))
                self.request.send(bytes(result, "utf-8"))
            if data[0][3:] == "dodaj":
                result = str(self.dodawanie(data[1][3:], data[2][3:]))
                self.request.send(bytes(result, "utf-8"))
            if data[0][3:] == "odejmij":
                result = str(self.odejmowanie(data[1][3:], data[2][3:]))
                self.request.send(bytes(result, "utf-8"))
            if data[0][3:] == "mnoz":
                result = str(self.mnozenie(data[1][3:], data[2][3:]))
                self.request.send(bytes(result, "utf-8"))
            if data[0][3:] == "dziel":
                result = str(self.dzielenie(data[1][3:], data[2][3:]))
                self.request.send(bytes(result, "utf-8"))
            OPERATIONS[SOCKETS[self.request]] = Operation(data, result)
            print(OPERATIONS[SOCKETS[self.request]])


class MyTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


HOST, PORT = "192.168.137.1", 8080

server = MyTCPServer((HOST, PORT), Handler)

server.serve_forever()

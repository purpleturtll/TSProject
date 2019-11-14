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

SOCKETS = {}
OPERATIONS = {}
SESSION_ID = 1


class Operation:
    def __init__(self, id, data, result):
        self.query = data
        self.result = result
        self.id = id

    def __str__(self):
        return self.query[0][3:] + " " + self.query[4][3:] + " " + self.query[5][3:] + " " + self.result


class Handler(socketserver.BaseRequestHandler):

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

    def historia(self, x1):
        print(OPERATIONS[SOCKETS[self.request][0]])
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
            print(data)

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


#HOST, PORT = "192.168.137.1", 8080
HOST, PORT = "127.0.0.1", 8080

server = MyTCPServer((HOST, PORT), Handler)

# server.serve_forever()

with server:
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    time.sleep(math.pow(10, 6))

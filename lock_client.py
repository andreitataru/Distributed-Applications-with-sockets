#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 2 - lock_client.py
Grupo: 23
Números de aluno: 53746, 51153, 51220
"""
# Zona para fazer imports

import sys, socket as s
from lock_stub import lock_stub

# Programa principal

try:
    CLIENT_ID = int(sys.argv[1])
    HOST = sys.argv[2]
    PORT = int(sys.argv[3])
except:
    print("Insert command in format: ./lock_client.py CLIENT_ID HOST PORT")
    exit()

stub = lock_stub(HOST, PORT)
stub.connect()

while True:
    comando = str(input("Comando > "))
    cSplit = comando.split()
    if len(cSplit) == 0:
        print("INSERT A COMMAND")
    elif cSplit[0] == "EXIT":
        exit()
    elif cSplit[0] == "LOCK" or cSplit[0] == "RELEASE" or cSplit[0] == "STATUS" or cSplit[0] == "STATS" or cSplit[0] == "YSTATS" or cSplit[0] == "NSTATS":
        cSplit.append(CLIENT_ID)
        resp = stub.send_command(cSplit)
        print(resp)
    elif cSplit[0] == "HELP":
        print("COMMANDS ALLOWED: LOCK (TIME) (RESOURCE_ID) | RELEASE (RESOURCE_ID) | STATUS (RESOURCE_ID) | STATS (RESOURCE_ID) | YSTATS | NSTATS | EXIT")
    else:
        print("COMMAND NOT FOUND")
stub.close()

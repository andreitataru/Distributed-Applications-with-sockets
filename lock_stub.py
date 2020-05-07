#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 2 - lock_stub.py
Grupo: 23
Números de aluno: 53746, 51153, 51220
"""

# Zona para fazer importação

import sys, socket as s
import pickle, struct
from net_client import server

###############################################################################

class lock_stub:

    def __init__(self, address, port):
        self.server = server(address, port)

    def connect(self):
        self.server.connect()
    
    def send_command(self, com):
        comID = self.getCommandID(com[0])
        if comID == 10:
            msg = [comID, com[1], com[2], com[3]]
        elif comID == 20:
            msg = [comID, com[1], com[2]]
        elif comID == 30:
            msg = [comID, com[1]]
        elif comID == 40:
            msg = [comID, com[1]]
        elif comID == 50:
            msg = [comID]
        elif comID == 60:
            msg = [comID]
        return self.server.send_receive(msg)
        
    def getCommandID(self, command):
        if command == "LOCK":
            return 10
        elif command == "RELEASE":
            return 20
        elif command == "STATUS":
            return 30
        elif command == "STATS":
            return 40
        elif command == "YSTATS":
            return 50
        elif command == "NSTATS":
            return 60

    def close(self):
        self.server.close()

